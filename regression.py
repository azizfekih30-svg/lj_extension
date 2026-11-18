from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn import linear_model
import numpy as np
import os
from os import walk
from sklearn.metrics import root_mean_squared_error
import lightgbm
from lightgbm import LGBMRegressor
import utils
import readers
from sklearnutils import GroupByTransformer,MassOewMtow,TargetIdentity,TargetStandardScaler,MassStandardScalerByAircraft,LearnMassStandardScalerByAircraft#,NoNormalizeMass
from add_localtime import add_localtime
from sklego.preprocessing import IdentityTransformer
import features
import argparse
import time
import itertools
import tqdm
from argparse import Namespace
import json

YVAR = "tow"

class Predictor:
    '''
    Embedds the regresion model, and the target normalization
    '''
    def __init__(self, norm_mass,model_params):
        self.norm_mass = norm_mass
        self.model_params=model_params
        self.log = {}
    def fit(self,feat):
        df = feat.data
        print(list(df))
        print(len(list(df)))
        categorical_features, numeric_features, preprocessor = preprocessor_flights(feat)
        model = LGBMRegressor(**self.model_params)
        clf = Pipeline([
            ("preprocessor",preprocessor),
            ("model",model)
        ])
        print(model.get_params())
        vx = categorical_features + numeric_features
        X = df[vx]
        self.norm_mass.fit(df)
        Y,w = self.norm_mass.transform(df)
        assert (len(Y.shape)==1)
        start_time = time.time()
        self.clf = clf.fit(X, Y,model__sample_weight=w,model__feature_name=vx,model__categorical_feature=categorical_features)
        self.log["elapsed_time"] = time.time() - start_time
        print(self.log["elapsed_time"])
        self.log["model_params"] = self.clf.named_steps["model"].get_params()
        return self

    def predict(self,df,**kwargs):
        rawypred = self.rawpredict(df,**kwargs)
        return self.norm_mass.inverse_transform(df, rawypred)
    def rawpredict(self,df,**kwargs):
        return self.clf.predict(df[self.clf.feature_names_in_],**kwargs)
    def valid_curve(self,dftest,step=2000):
        num_iterations = self.clf.named_steps["model"].n_estimators_
        rawypred = 0
        lloss = []
        for i in range(0,num_iterations,step):
            actual_step = min(step,num_iterations-i)
            rawypred += self.rawpredict(dftest,start_iteration=i,num_iteration=actual_step)
            lloss.append((i+actual_step, root_mean_squared_error(dftest[YVAR].values,self.norm_mass.inverse_transform(dftest,rawypred))))
        return lloss
    def feature_importances(self):
        return sorted(zip(self.clf.named_steps["model"].feature_importances_,self.clf.named_steps["model"].feature_name_), reverse=True)


def assemble_sub(dfsub,ysub):
    ''' used to generate the submission dataframe'''
    assert(not np.isnan(ysub).any())
    dfsub["tow"]=ysub
    return dfsub[["flight_id","tow"]]


def preprocessor_flights(feat):
    ''' Preprocessing of the features'''
    numeric_features = sorted(feat.numeric_features())
    numeric_features_not_scaled = sorted(feat.numeric_features_not_scaled())
    categorical_features = sorted(feat.categorical_features())
    categorical_transformer = Pipeline(
        steps=[
            ("encoder", OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1,encoded_missing_value=-1,dtype=np.int32)),
        ]
    )
    numeric_transformer = Pipeline(
        steps=[
            ("scaler", IdentityTransformer()),
        ]
    )
    # synonym={
    #     "B752":"B763",
    #     "B773":"B77W",
    #     "E290":"E195",
    #     "A310":"A319",
    #     }
    # scale_by_group = "aircraft_type"
    # numeric_transformer = Pipeline(
    #     steps=[
    #         ("scaler", GroupByTransformer(StandardScaler,synonym,by=scale_by_group)),#
    #     ]
    # )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, categorical_features),
            ("numeric", numeric_transformer, numeric_features),#+[scale_by_group])
            ("unscalednumeric", IdentityTransformer(), numeric_features_not_scaled),
        ],
        remainder = "drop",
    )
    return categorical_features, numeric_features+numeric_features_not_scaled, preprocessor


def train_valid(random_state):
    ''' returns a couple of training and validation set'''
    feat = features.read_features("challenge_set")
    dftrain, dftest = train_test_split(feat.data,test_size=0.2,random_state=random_state)
    feat.data = dftrain
    return feat, lambda : dftest

def train_test(random_state):
    ''' returns a couple of training and validation set'''
    feat = features.read_features("challenge_set")
    return feat, lambda : features.read_features("final_submission_set").data


def valid(predictor, dftest):
    ''' computes statistics using validation set'''
    test_rmse=predictor.valid_curve(dftest)
    best_test_rmse=min(test_rmse,key= lambda x:x[1])
    print(test_rmse)
    print(best_test_rmse)
    ypred = predictor.predict(dftest)
    loss = root_mean_squared_error(dftest[YVAR].values,ypred)
    for imp,v in predictor.feature_importances():
        print(f"{v:30} {imp:30}")
    predictor.log["test_error"]=loss
    print(f"test error {loss}")
    for ac in sorted(dftest.aircraft_type.unique()):
        mask = dftest.aircraft_type.values == ac
        loss = root_mean_squared_error(dftest[YVAR].values[mask],ypred[mask])
        print(f"test error |{ac:<10}|{mask.sum():>10}|{loss:>10.0f}|")
    for month in sorted(dftest.date.dt.month.unique()):
        mask = dftest.date.dt.month == month
        loss = root_mean_squared_error(dftest[YVAR].values[mask],ypred[mask])
        print(f"test error |{month:<10}|{mask.sum():>10}|{loss:>10.0f}|")

def submit(predictor, dftest, config):
    ''' builds the submission'''
    ysub = predictor.predict(dftest)
    dfsubpred = assemble_sub(dftest, ysub)
    utils.write_submission(config, dfsubpred)

EXT_MODES = ("val", "final")


def run_ext(args, model_params, config):
    '''
    Koopmann-Aziz extension modes (outputs only below EXT_FOLDER, named by variant/device/bins/seed):
      -what val   : train on challenge_set minus the held-out days of @split_file,
                    report the validation RMSE, write validation predictions
      -what final : train on the full challenge_set, predict final_submission_set
    The model, features and target scaling are exactly those of "-what submit".
    '''
    from koopmann_aziz import ext, split
    timer = ext.Timer()
    mon = ext.PeakRSS().start()
    folders = ext.ext_folders(config)
    val_days = split.load_val_days(args.split_file)
    days = None
    if args.smoke_days > 0:
        days = ext.smoke_days(val_days, args.smoke_days, ext.available_days(config))
    # smoke outputs get their own names so they can never be mistaken for real runs
    name = ext.run_name(args.what, ("SMOKE-" if days else "") + args.variant, model_params)
    info = {"name": name, "what": args.what, "variant": args.variant, "seed": model_params["random_state"],
            "device": model_params.get("device"), "max_bin": model_params.get("max_bin"),
            "n_estimators": model_params.get("n_estimators"), "model_params": model_params,
            "split_file": os.path.relpath(args.split_file), "smoke_days": days, **ext.git_info()}
    print("KA_START", info)
    feat = features.read_features("challenge_set", days=days)
    if args.what == "val":
        isval = split.offblock_day(feat.data).isin(val_days).values
        dfval = feat.data[isval]
        feat.data = feat.data[~isval]
        info.update(n_train=int((~isval).sum()), n_val=int(isval.sum()),
                    n_val_days=int(split.offblock_day(dfval).nunique()))
        print(f"KA_SPLIT train={info['n_train']} val={info['n_val']} val_days={info['n_val_days']}")
        if info["n_val"] == 0 or info["n_train"] == 0:
            raise SystemExit("empty training or validation part: check -split_file / -smoke_days")
    predictor = Predictor(MassOewMtow(YVAR,"aircraft_type"),model_params)
    predictor.fit(feat)
    info["fit_s"] = predictor.log["elapsed_time"]
    imp = pd.DataFrame(predictor.feature_importances(), columns=["gain", "feature"])
    imp.to_csv(ext.guard_output(os.path.join(folders["scores"], f"{name}__importance.csv"), config), index=False)
    if args.what == "val":
        ypred = predictor.predict(dfval)
        assert not np.isnan(ypred).any()
        y = dfval[YVAR].values
        info["val_rmse"] = float(root_mean_squared_error(y, ypred))
        bytype = []
        for ac in sorted(dfval.aircraft_type.unique()):
            m = dfval.aircraft_type.values == ac
            bytype.append((ac, int(m.sum()), float(root_mean_squared_error(y[m], ypred[m]))))
        info["val_rmse_by_type"] = bytype
        for ac, n, r in bytype:
            print(f"val error |{ac:<10}|{n:>10}|{r:>10.0f}|")
        out = pd.DataFrame({"flight_id": dfval.flight_id.values, "aircraft_type": dfval.aircraft_type.values,
                            "day": split.offblock_day(dfval).values, "tow": y, "tow_pred": ypred})
        fout = os.path.join(folders["preds"], f"{name}.csv")
    else:
        dftest = features.read_features("final_submission_set", days=days).data
        # leakage guard: the test set must not carry labels, and the model never sees the column
        if YVAR in dftest and dftest[YVAR].notna().any():
            raise RuntimeError("final_submission_set has non-missing tow values: refusing to continue")
        dftest = dftest.drop(columns=[YVAR], errors="ignore")
        ysub = predictor.predict(dftest)
        assert not np.isnan(ysub).any()
        out = pd.DataFrame({"flight_id": dftest.flight_id.values, "tow": ysub})
        fout = os.path.join(folders["submissions"], f"{name}.csv")
        info["n_pred"] = len(out)
    out.to_csv(ext.guard_output(fout, config), index=False)
    info["output"] = fout
    info["runtime_s"] = timer()
    info["peak_ram_gb"] = mon.stop()
    ext.write_json(info, os.path.join(folders["scores"], f"{name}.json"), config)
    print("KA_RESULT", json.dumps({k: info.get(k) for k in
          ["name", "val_rmse", "n_train", "n_val", "n_pred", "runtime_s", "fit_s", "peak_ram_gb", "output", "commit"]}))
    return info


def convert(v):
    try:
        return int(v)
    except:
        try:
            return float(v)
        except:
            return v

def main():
    parser = argparse.ArgumentParser(
                    prog='predictor',
                    description='',
    )
    parser.add_argument("-what",default="valid")
    parser.add_argument("-log",default="log_file")
    parser.add_argument("-random_state",default=0,type=int)
    # Koopmann-Aziz extension (only used by -what val / final)
    parser.add_argument("-variant",default="baseline")
    parser.add_argument("-split_file",default=os.path.join("koopmann_aziz","splits","val_days_seed0.txt"))
    parser.add_argument("-smoke_days",default=0,type=int)
    args, unknown = parser.parse_known_args()
    unknown = {k[1:]:convert(v) for k,v in zip(unknown[:-1:2],unknown[1::2])}
    print(unknown)
    log = {}
    log["args"]=args
    dsplitter = {
        "valid":train_valid,
        "submit":train_test,
    }
    config = utils.read_config()
    if args.what not in EXT_MODES:
        feat, fdftest = dsplitter[args.what](args.random_state)
    print(args)
    model_params = {'boosting_type': 'gbdt', 'class_weight': None, 'colsample_bytree': 0.7368753029236468, 'importance_type': 'gain', 'learning_rate': 0.04347089639866006, 'max_depth': -1, 'min_child_samples': 460, 'min_child_weight': 0.0, 'min_split_gain': 0.0, 'n_estimators': 50000, 'n_jobs': None, 'num_leaves': 14, 'objective': None, 'random_state': args.random_state, 'reg_alpha': 400, 'reg_lambda': 500, 'subsample': 0.879814641620981, 'subsample_for_bin': 400000, 'subsample_freq': 5, 'device': 'cpu', 'verbose': 1, 'max_bin': 511, 'cat_l2': 450, 'cat_smooth': 150,"deterministic":True,"force_col_wise":True}
#    model_params = {'boosting_type': 'gbdt', 'class_weight': None, 'colsample_bytree': 0.9983479969770903, 'importance_type': 'gain', 'learning_rate': 0.034044216343711194, 'max_depth': -1, 'min_child_samples': 360, 'min_child_weight': 0.0, 'min_split_gain': 0.0, 'n_estimators': 50000, 'n_jobs': None, 'num_leaves': 17, 'objective': None, 'random_state': 0, 'reg_alpha': 300, 'reg_lambda': 800, 'subsample': 0.9708398642260044, 'subsample_for_bin': 400000, 'subsample_freq': 100, 'device': 'cpu', 'verbose': 1, 'max_bin': 1023, 'cat_l2': 50, 'cat_smooth': 150}#, 'test_error': 1572.2932228357363}
    for k,v in unknown.items():
        if k in model_params:
            model_params[k]=v
        else:
            raise Exception(f"unknown args '-{k} {v}'")
    if args.what in EXT_MODES:
        return run_ext(args, model_params, config)
    predictor = Predictor(MassOewMtow(YVAR,"aircraft_type"),model_params)
    predictor.fit(feat)
    ypred = predictor.predict(feat.data)
    print("training error",root_mean_squared_error(feat.data[YVAR],ypred))
    if args.what == "valid":
        valid(predictor,fdftest())
        with open(args.log,"a") as f:
            loglog = {** log, **predictor.log}
            f.write(f"{loglog},")
    elif args.what == "submit":
        submit(predictor,fdftest(),config)
    print({**log, **predictor.log})

if __name__ == '__main__':
    main()

