import readers
import pandas as pd
from functools import wraps
import utils
import os
from pitot import geodesy
import numpy as np
from add_localtime import add_localtime

FID = "flight_id"

def read_parquet_days(fname, days=None):
    '''
    Koopmann-Aziz: pd.read_parquet(fname), optionally restricted to the day files
    <fname>/<day>.parquet of the list @days (smoke runs). days=None: original behaviour.
    '''
    if days is None or not os.path.isdir(fname):
        return pd.read_parquet(fname)
    files = [os.path.join(fname, f"{d}.parquet") for d in days]
    files = [f for f in files if os.path.exists(f)]
    if not files:
        raise FileNotFoundError(f"none of the days {days} in {fname}")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def sortedout(method):
    ''' decorator to sort features'''
    @wraps(method)
    def _sortedout(self):
        # res = method(self)
        # print(res)
        return sorted(method(self))
    return _sortedout


class AllNumeric:
    '''
    From a dataframe file @fname use all its column, except flight_id, as numerical feature
    The distinction between Scaled/not_scaled feature is not actually used.
    It was tested but it was not conclusive.
    Nonetheless, the idea is interesting, so the code is left as is for future tests.
    '''
    def __init__(self, fname, days=None):
        super().__init__()
        self.fname = fname
        self.data = read_parquet_days(fname, days)
    @sortedout
    def categorical_features(self):
        return []
    @sortedout
    def numeric_features_not_scaled(self):
        return []
    @sortedout
    def numeric_features(self):
        return sorted([x for x in self.data if x!=FID])


class AllNumericNotScaled:
    '''
    From a dataframe file @fname use all its column, except flight_id, as numerical feature
    '''
    def __init__(self, fname, days=None):
        super().__init__()
        self.fname = fname
        self.data = read_parquet_days(fname, days)
    @sortedout
    def categorical_features(self):
        return []
    @sortedout
    def numeric_features_not_scaled(self):
        return sorted([x for x in self.data if x!=FID])
    @sortedout
    def numeric_features(self):
        return []

class AllCategorical:
    '''
    From a dataframe file @fname use all its column, except flight_id, as categorical feature
    '''
    def __init__(self, fname, days=None):
        super().__init__()
        self.fname = fname
        self.data = read_parquet_days(fname, days)
    @sortedout
    def categorical_features(self):
        return sorted([x for x in self.data if x!=FID])
    @sortedout
    def numeric_features_not_scaled(self):
        return []
    @sortedout
    def numeric_features(self):
        return []

def round_to_hour(time):
    ''' from the datetime, computes the time in minutes of the day'''
#    return (2*(time.dt.hour+time.dt.minute/60)).round().astype(np.int32)
    return 60 * time.dt.hour + time.dt.minute#)).round().astype(np.int32)

class Flights:
    '''
    Class used to model the features extracted from the flights files
    '''
    def __init__(self, config, what):
        fname = os.path.join(config.flights,f"{what}.parquet")
        self.fname = fname
        df = readers.read_flights(fname)#.query("date.dt.month<=1").query("date.dt.day<=1")
        print(f"{df.shape=}")
        airports = pd.read_parquet(os.path.join(config.FOLDER_DATA,"airports_tz.parquet"))
        df=add_localtime(airports,df,"actual_offblock_time","arrival_time")
        df["local_hour_adep"]=round_to_hour(df["local_actual_offblock_time"])
        df["local_hour_ades"]=round_to_hour(df["local_arrival_time"])
        # print(df["local_hour_adep"].describe())
        # raise Exception
        weather = pd.read_parquet(os.path.join(config.FOLDER_DATA,"weather",f"{what}.parquet"))
        df = df.join(weather.set_index("flight_id"),on="flight_id",how="left")
        print(f"{df.shape=}")
        for airport in ["adep","ades"]:
            df= pd.merge(df,airports[["icao_code","latitude_deg","longitude_deg","elevation_ft"]],how="left",left_on=airport,right_on="icao_code",suffixes=('_adep','_ades'))
        print(f"{df.shape=}")
        df["bird_distance"]=geodesy.distance(
            df.latitude_deg_adep.values,df.longitude_deg_adep.values,
            df.latitude_deg_ades.values,df.longitude_deg_ades.values,
        )/utils.NM2METER
        self.data=df

    @sortedout
    def categorical_features(self):
        return ["adep","ades","airline","aircraft_type","wtc","country_code_ades","country_code_adep","dayofweek"]#,#"callsign",
    @sortedout
    def numeric_features_not_scaled(self):
        aptvar = [f"{v}_{apt}" for apt in ["ades","adep"] for v in ["drct","tmpf","sknt","elevation_ft","vsby","latitude_deg","longitude_deg"]]#"alti","drct","sknt","tmpf"]]
        return ["local_hour_ades","local_hour_adep","weekofyear"]+aptvar
    @sortedout
    def numeric_features(self):
        #return ["arrival_minutes","actual_offblock_minutes"]#"flight_duration","taxiout_time","flown_distance","arrival_minutes","actual_offblock_minutes"]
        return ["flight_duration","taxiout_time","flown_distance","bird_distance"]


class Cruise(AllNumeric):
    '''
    Class used to model the features related to the cruise files
    '''
    def __init__(self,fname,days=None):
        super().__init__(fname,days)
        prefix = "CruiseDeltaAlt_"
        nb = max(int(x[len(prefix):])  for x in list(self.data) if x.startswith(prefix))+1
        print(nb)
        for i in range(nb):
            isclimb =  self.data[f"CruiseDeltaAlt_{i}"] > 200
            isdescent = self.data[f"CruiseDeltaAlt_{i}"] < -200
            iscount = self.data[f"Cruisemachcount_{i}"] < 100
            #iscount = self.data[f"Cruisemachcount_{i}"]/self.data["f_duration"]*nb<0.2
            self.data[f"CruiseMedianAlt_{i}"]= ((self.data[f"CruiseMedianAlt_{i}"]/1000).round())*1000
            for v in [f"CruiseMedianAlt_{i}",f"Cruisemach_{i}"]:
                self.data.loc[isclimb,v]= -10000
                self.data.loc[isdescent,v]= -20000
                self.data.loc[iscount,v]= np.nan
            print(self.data[f"CruiseMedianAlt_{i}"].unique())

class Mass(AllNumeric):
    '''
    Class used to model the features related to the climbing files
    '''
    def __init__(self,norange,scale,fname,days=None):
        super().__init__(fname,days)
        if "index" in list(self.data):
            self.data=self.data.drop(columns="index")
        if scale:
            for v in list(self.data):
                if "mass_" in v and v not in ["mass_min","mass_max"]:
                    print(f"scaling {v}")
                    self.data[v]=(self.data[v]-self.data["mass_min"])/(self.data["mass_max"]-self.data["mass_min"])
        if norange:
            self.data = self.data.drop(columns=["mass_min","mass_max"])


class Union:
    '''
    Class used to unify alll the features objects defined with above classes
    '''
    def __init__(self,flights,lfeatures):
        self.data = flights.data#.copy()
        for i,features in enumerate(lfeatures):
            print(features.fname)
            self.data = self.data.join(features.data.set_index("flight_id"),on="flight_id",how="left")
        self.lfeatures = lfeatures
        self.flights = flights
        self.fname = (flights.fname,)+tuple(x.fname for x in lfeatures)
    @sortedout
    def categorical_features(self):
        return [y for x in self.lfeatures for y in x.categorical_features()] +  self.flights.categorical_features()
    @sortedout
    def numeric_features_not_scaled(self):
        return [y for x in self.lfeatures for y in x.numeric_features_not_scaled()] + self.flights.numeric_features_not_scaled()
    @sortedout
    def numeric_features(self):
        return [y for x in self.lfeatures for y in  x.numeric_features()] + self.flights.numeric_features()

def read_features(what, days=None):
    '''
    Return a Union object used to assemble all the features
    It contains a dataframe of the features
    And the names of the categorical/numerical features
    Koopmann-Aziz: @days (list of 'YYYY-MM-DD') restricts to those day files and to
    flights with that 'date' (smoke runs only); days=None is the original behaviour.
    '''
    config = utils.read_config()
    lfeatures = [
        Mass(norange=True,scale=True,fname=os.path.join(config.FOLDER_DATA,f"classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses/{what}"),days=days),
        AllNumericNotScaled(os.path.join(config.FOLDER_DATA,f"thunder/{what}.parquet"),days=days),
        AllNumericNotScaled(os.path.join(config.FOLDER_DATA,f"classic__1e-2_wind/{what}"),days=days),
        Cruise(os.path.join(config.FOLDER_DATA,f"classic__1e-2__20_cruise/{what}"),days=days),
    ]
    flights = Flights(config, what)
    feat = Union(flights, lfeatures)
    if days is not None:
        feat.data = feat.data[feat.data["date"].dt.strftime("%Y-%m-%d").isin(days)]
    print(f"{feat.data.shape=}")
    feat.data=feat.data.query("aircraft_type!='C56X'").query("aircraft_type!='A310'")#.reset_index()
    print(f"{feat.data.shape=}")
    return feat
