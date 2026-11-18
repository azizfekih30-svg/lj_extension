"""Synthetic likable_jelly data folder for laptop tests (Koopmann-Aziz).

Builds a small data folder with the layout, column names and dtypes documented
in koopmann_aziz/DATA_STRUCTURE_lj.md (pc182, 2026-11-18): flights, weather,
thunder, airports_tz, a tiny METARs file, the per-day climb / cruise / wind
feature folders, and a separate "raw" folder with train.csv, test_final.csv and
flight_list.csv (the truth file; the tests check that no training code reads it).

The target is made learnable: the load fraction (tow-oew)/(mtow-oew) depends on
distance plus noise, and the climb "equivalent mass" columns are noisy copies
of the true mass, so a model trained on these features beats a constant.

Usage:
    python -m koopmann_aziz.synth --out koopmann_aziz/_synth --write-config
"""
import argparse
import hashlib
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

FIRST_DAY = "2022-01-01"
N_CLIMB_SLICES = 48
N_CRUISE_SLICES = 20
CLIMB_VARS = ["mass", "masscount", "massadepdate", "massadesdate", "DeltaROCD", "ROCD",
              "e_rate_median", "tas_median", "DeltaT_median", "e_rate_max", "e_rate_min"]
CRUISE_VARS = ["Cruisemach", "Cruisemachcount", "CruiseDeltaAlt", "CruiseMedianAlt"]
THUNDER_VARS = ["TS", "pTS", "VCTS", "pVCTS", "FG"]
SETS = ["challenge_set", "final_submission_set"]

# (icao, iata, name, municipality, lat, lon, elev_ft, country, continent, tz)
AIRPORTS = [
    ("EGLL", "LHR", "London Heathrow", "London", 51.4706, -0.461941, 83.0, "GB", "EU", "Europe/London"),
    ("EICK", "ORK", "Cork", "Cork", 51.8413, -8.49111, 502.0, "IE", "EU", "Europe/Dublin"),
    ("LEBL", "BCN", "Barcelona", "Barcelona", 41.2971, 2.07846, 12.0, "ES", "EU", "Europe/Madrid"),
    ("KMIA", "MIA", "Miami", "Miami", 25.7932, -80.2906, 8.0, "US", None, "America/New_York"),
    ("ESSA", "ARN", "Stockholm Arlanda", "Stockholm", 59.6519, 17.9186, 137.0, "SE", "EU", "Europe/Stockholm"),
    ("KORD", "ORD", "Chicago O'Hare", "Chicago", 41.9786, -87.9048, 680.0, "US", None, "America/Chicago"),
    ("LTFJ", "SAW", "Istanbul Sabiha Gokcen", "Istanbul", 40.8986, 29.3092, 312.0, "TR", "AS", "Europe/Istanbul"),
    ("LFLL", "LYS", "Lyon", "Lyon", 45.7256, 5.08111, 821.0, "FR", "EU", "Europe/Paris"),
    ("EBBR", "BRU", "Brussels", "Brussels", 50.9014, 4.48444, 184.0, "BE", "EU", "Europe/Brussels"),
    ("KJFK", "JFK", "New York JFK", "New York", 40.6398, -73.7789, 13.0, "US", None, "America/New_York"),
    ("EDDF", "FRA", "Frankfurt", "Frankfurt", 50.0333, 8.57056, 364.0, "DE", "EU", "Europe/Berlin"),
    ("LFPG", "CDG", "Paris Charles de Gaulle", "Paris", 49.0128, 2.55, 392.0, "FR", "EU", "Europe/Paris"),
    ("EHAM", "AMS", "Amsterdam Schiphol", "Amsterdam", 52.3086, 4.76389, -11.0, "NL", "EU", "Europe/Amsterdam"),
    ("LIRF", "FCO", "Rome Fiumicino", "Rome", 41.8003, 12.2389, 13.0, "IT", "EU", "Europe/Rome"),
]

# missing shares of the weather columns (DATA_STRUCTURE_lj.md, challenge_set)
WEATHER_COLS = [  # (name, kind, missing share)
    ("mslp", "f", 0.95), ("tmpf", "f", 0.001), ("drct", "f", 0.09), ("sknt", "f", 0.002),
    ("gust", "f", 0.97), ("wxcodes", "s", 0.865), ("vsby", "f", 0.001), ("skyl1", "f", 0.39),
    ("skyl2", "f", 0.71), ("skyl3", "f", 0.92), ("skyl4", "f", 0.995), ("skyc1", "s", 0.32),
    ("skyc2", "s", 0.71), ("skyc3", "s", 0.92), ("skyc4", "s", 0.994), ("alti", "f", 0.003),
    ("relh", "f", 0.001),
]

METAR_COLS = [  # (name, kind) in file order
    ("station", "s"), ("valid", "t"), ("lon", "f"), ("lat", "f"), ("elevation", "f"), ("tmpf", "f"),
    ("dwpf", "f"), ("relh", "f"), ("drct", "f"), ("sknt", "f"), ("p01i", "f"), ("alti", "f"),
    ("mslp", "f"), ("vsby", "f"), ("gust", "f"), ("skyc1", "s"), ("skyc2", "s"), ("skyc3", "s"),
    ("skyc4", "s"), ("skyl1", "f"), ("skyl2", "f"), ("skyl3", "f"), ("skyl4", "f"), ("wxcodes", "s"),
    ("ice_accretion_1hr", "f"), ("ice_accretion_3hr", "f"), ("ice_accretion_6hr", "f"),
    ("peak_wind_gust", "f"), ("peak_wind_drct", "f"), ("peak_wind_time", "o"), ("feel", "f"),
    ("metar", "s"), ("snowdepth", "f"),
]


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def haversine_nm(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(lon2 - lon1)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * 6371000.0 * np.arcsin(np.sqrt(a)) / 1852.0


def _with_missing(rng, values, share):
    values = pd.Series(values)
    if share > 0:
        values = values.mask(rng.random(len(values)) < share)
    return values


def make_flights(rng, days, n_per_day):
    masses = pd.read_csv(os.path.join(REPO, "aircraft_type_masses.csv"))
    types = masses.aircraft_type.tolist()
    # common types much more frequent; keep C56X and A310 (excluded by the team) rare
    w = np.array([0.2 if t in ("C56X", "A310") else (8.0 if t in ("A320", "B738", "A319", "A321") else 1.0)
                  for t in types])
    w = w / w.sum()
    apt = pd.DataFrame(AIRPORTS, columns=["icao", "iata", "name", "muni", "lat", "lon", "elev", "cc", "cont", "tz"])
    # a fixed pool of "routes" (airline, callsign, adep, ades, type) so callsigns repeat across days
    n_routes = max(40, n_per_day // 2)
    routes = []
    for r in range(n_routes):
        i, j = rng.choice(len(apt), size=2, replace=False)
        routes.append(dict(
            airline=md5(f"airline{rng.integers(0, 8)}"),
            callsign=md5(f"callsign{r}"),
            adep=i, ades=j,
            aircraft_type=rng.choice(types, p=w),
            load_bias=rng.normal(0, 0.08),
        ))
    rows = []
    fid = 248750000
    for day in days:
        d0 = pd.Timestamp(day, tz="UTC")
        for _ in range(n_per_day):
            fid += int(rng.integers(1, 20))
            r = routes[rng.integers(0, n_routes)]
            a, b = apt.iloc[r["adep"]], apt.iloc[r["ades"]]
            gc = haversine_nm(a.lat, a.lon, b.lat, b.lon)
            flown = int(round(gc * rng.uniform(1.02, 1.12) + 20))
            duration = int(round(flown / 7.5 + 25 + rng.normal(0, 5)))
            taxi = int(rng.integers(5, 30))
            # ~2% of flights leave the evening before their "date" (tests day-of-offblock grouping)
            if rng.random() < 0.02:
                offblock = d0 - pd.Timedelta(minutes=int(rng.integers(10, 120)))
            else:
                offblock = d0 + pd.Timedelta(minutes=int(rng.integers(0, 24 * 60 - 1)))
            arrival = offblock + pd.Timedelta(minutes=taxi + duration) + pd.Timedelta(seconds=int(rng.integers(0, 60)))
            ac = r["aircraft_type"]
            m = masses.set_index("aircraft_type").loc[ac]
            frac = np.clip(0.45 + 0.35 * min(gc / 5000, 1) + r["load_bias"] + rng.normal(0, 0.06), 0.05, 0.99)
            tow = float(round(m.oew + frac * (m.mtow - m.oew)))
            rows.append(dict(
                flight_id=fid, date=d0, callsign=r["callsign"],
                adep=a.icao, name_adep=a["name"], country_code_adep=a.cc,
                ades=b.icao, name_ades=b["name"], country_code_ades=b.cc,
                actual_offblock_time=offblock, arrival_time=arrival,
                aircraft_type=ac, wtc=("L" if m.mtow < 15000 else ("H" if m.mtow > 136000 else "M")),
                airline=r["airline"], flight_duration=duration, taxiout_time=taxi,
                flown_distance=flown, tow=tow,
                _frac=frac, _mtow=float(m.mtow), _oew=float(m.oew), _gc=gc,
            ))
    df = pd.DataFrame(rows)
    return df, apt


FLIGHT_COLS = ["flight_id", "date", "callsign", "adep", "name_adep", "country_code_adep", "ades",
               "name_ades", "country_code_ades", "actual_offblock_time", "arrival_time",
               "aircraft_type", "wtc", "airline", "flight_duration", "taxiout_time",
               "flown_distance", "tow"]
STR_COLS = ["callsign", "adep", "name_adep", "country_code_adep", "ades", "name_ades",
            "country_code_ades", "aircraft_type", "wtc", "airline"]


def flights_parquet_frame(df):
    out = df[FLIGHT_COLS].copy()
    for c in STR_COLS:
        out[c] = out[c].astype("string")
    for c in ["flight_duration", "taxiout_time", "flown_distance", "tow"]:
        out[c] = out[c].astype("float64")
    for c in ["date", "actual_offblock_time", "arrival_time"]:
        out[c] = pd.to_datetime(out[c], utc=True).astype("datetime64[ns, UTC]")
    out["flight_id"] = out["flight_id"].astype("int64")
    return out


def flights_csv_frame(df):
    out = df[FLIGHT_COLS].copy()
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    for c in ["actual_offblock_time", "arrival_time"]:
        out[c] = out[c].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    for c in ["flight_duration", "taxiout_time", "flown_distance"]:
        out[c] = out[c].astype("int64")
    return out


def make_airports(apt):
    n = len(apt)
    df = pd.DataFrame({
        "id": np.arange(100, 100 + n, dtype="int64"),
        "type": pd.Series(["large_airport"] * n, dtype="string"),
        "name": apt["name"].astype("string"),
        "latitude_deg": apt.lat.astype("float64"),
        "longitude_deg": apt.lon.astype("float64"),
        "elevation_ft": apt.elev.astype("float64"),
        "continent": apt.cont.astype("string"),
        "iso_country": apt.cc.astype("string"),
        "iso_region": (apt.cc + "-1").astype("string"),
        "municipality": apt.muni.astype("string"),
        "scheduled_service": pd.Series(["yes"] * n, dtype="string"),
        "gps_code": apt.icao.astype("string"),
        "iata_code": apt.iata.astype("string"),
        "local_code": pd.Series([pd.NA] * n, dtype="string"),
        "home_link": pd.Series([pd.NA] * n, dtype="string"),
        "wikipedia_link": ("https://en.wikipedia.org/wiki/" + apt.iata).astype("string"),
        "keywords": pd.Series([pd.NA] * n, dtype="string"),
        "icao_code": apt.icao.astype("string"),
        "time_zone": apt.tz.astype("string"),
    })
    return df


def make_weather(rng, df):
    out = {"flight_id": df.flight_id.values.astype("int64")}
    n = len(df)
    for side in ["adep", "ades"]:
        for name, kind, share in WEATHER_COLS:
            if kind == "s":
                choices = {"wxcodes": ["-RA", "BR", "-SN", "BCFG", "-RA BR", "TSRA"]}.get(
                    name, ["FEW", "SCT", "BKN", "OVC"])
                v = pd.Series(rng.choice(choices, n)).astype("string")
                v = v.mask(rng.random(n) < share)
                out[f"{name}_{side}"] = v.astype("string")
            else:
                base = {"mslp": (1013, 8), "tmpf": (50, 15), "drct": (180, 100), "sknt": (9, 5),
                        "gust": (25, 5), "vsby": (6, 2), "skyl1": (2000, 1500), "skyl2": (5000, 3000),
                        "skyl3": (10000, 4000), "skyl4": (20000, 5000), "alti": (30.0, 0.3),
                        "relh": (75, 15)}[name]
                v = rng.normal(base[0], base[1], n)
                out[f"{name}_{side}"] = _with_missing(rng, v, share).astype("float64")
    return pd.DataFrame(out)


def make_thunder(rng, df):
    out = {"flight_id": df.flight_id.values.astype("int64")}
    for k in range(1, 7):
        for v in THUNDER_VARS:
            out[f"thunder_max_{v}_{k}_ades"] = (rng.random(len(df)) < 0.05).astype("float64")
    return pd.DataFrame(out)


def climb_frame(rng, df):
    """one row per flight; columns in the order of feature_climbing.py"""
    n = len(df)
    true_mass = df._oew.values + df._frac.values * (df._mtow.values - df._oew.values)
    cols = {"flight_id": df.flight_id.values.astype("int64"),
            "mass_max": df._mtow.values.astype("float64"),
            "mass_min": df._oew.values.astype("float64")}
    # slice i observed with probability decreasing with altitude (high slices ~always missing)
    p_obs = np.clip(0.94 - np.arange(N_CLIMB_SLICES) * 0.025, 0.0, 0.94)
    p_obs[40:] = 0.0
    for prefix, nslices, pobs in [("climb", N_CLIMB_SLICES, p_obs), ("takeoff", 1, np.array([0.08]))]:
        for i in range(nslices):
            obs = rng.random(n) < pobs[i]
            mass_obs = obs & (rng.random(n) < 0.98)
            def put(var, values, mask):
                cols[f"{prefix}{var}_{i}"] = np.where(mask, values, np.nan).astype("float64")
            put("mass", true_mass * rng.normal(1, 0.06, n), mass_obs)
            put("masscount", rng.integers(0, 40, n).astype(float), obs)
            put("massadepdate", 300 + 60 * i + rng.normal(0, 30, n), obs)
            put("massadesdate", df.flight_duration.values * 60 - 60 * i + rng.normal(0, 30, n), obs)
            put("DeltaROCD", np.abs(rng.normal(5, 3, n)), obs)
            put("ROCD", rng.normal(12, 4, n), obs)
            put("e_rate_median", rng.normal(120, 30, n), mass_obs)
            put("tas_median", 80 + 4 * i + rng.normal(0, 5, n), obs)
            put("DeltaT_median", rng.normal(0, 4, n), obs)
            put("e_rate_max", rng.normal(150, 30, n), mass_obs)
            put("e_rate_min", rng.normal(90, 30, n), mass_obs)
    return pd.DataFrame(cols)


def cruise_frame(rng, df):
    n = len(df)
    cols = {"flight_id": df.flight_id.values.astype("int64"),
            "f_duration": (df.flight_duration.values * 60 + rng.normal(0, 60, n)).astype("float64")}
    for i in range(N_CRUISE_SLICES):
        miss = rng.random(n) < (0.03 + 0.4 * abs(i - 9.5) / 9.5)
        cols[f"Cruisemach_{i}"] = np.where(miss, np.nan, rng.uniform(0.3, 0.85, n))
        cols[f"Cruisemachcount_{i}"] = np.where(miss, np.nan, rng.integers(10, 700, n).astype(float))
        cols[f"CruiseDeltaAlt_{i}"] = np.where(miss, np.nan, rng.normal(0, 3000, n))
        cols[f"CruiseMedianAlt_{i}"] = np.where(miss, np.nan, rng.uniform(2000, 39000, n))
    return pd.DataFrame(cols)


def raw_trajectories(rng, df, n_flights=4, step_s=4):
    """columns/dtypes of rawtrajectories/<day>.parquet; simple climb-cruise-descent profiles"""
    out = []
    apt = {a[0]: a for a in AIRPORTS}
    for _, f in df.head(n_flights).iterrows():
        dur = max(int(f.flight_duration) * 60, 1200)
        t = np.arange(0, dur, step_s)
        a, b = apt[f.adep], apt[f.ades]
        frac = t / dur
        lat = a[4] + (b[4] - a[4]) * frac
        lon = a[5] + (b[5] - a[5]) * frac
        cruise = 35000.0
        alt = np.minimum.reduce([np.full_like(frac, cruise), t * 2500 / 60, (dur - t) * 2000 / 60])
        vr = np.gradient(alt, t) * 60
        gs = np.clip(150 + alt / cruise * 300, 140, 480) + rng.normal(0, 3, len(t))
        start = f.actual_offblock_time + pd.Timedelta(minutes=int(f.taxiout_time))
        out.append(pd.DataFrame({
            "flight_id": np.int64(f.flight_id),
            "timestamp": (start + pd.to_timedelta(t, unit="s")).astype("datetime64[ns, UTC]"),
            "latitude": lat, "longitude": lon, "altitude": np.round(alt / 25) * 25,
            "groundspeed": np.round(gs), "track": np.full(len(t), 90.0) + rng.normal(0, 1, len(t)),
            "vertical_rate": np.round(vr / 64) * 64, "icao24": np.int64(f.flight_id),
            "u_component_of_wind": rng.normal(5, 3, len(t)), "v_component_of_wind": rng.normal(-5, 3, len(t)),
            "temperature": 288.15 - 0.0019812 * np.minimum(alt, 36089) + rng.normal(0, 1, len(t)),
            "specific_humidity": np.abs(rng.normal(1e-4, 5e-5, len(t))),
        }))
    res = pd.concat(out, ignore_index=True)
    res["flight_id"] = res["flight_id"].astype("int64")
    res["icao24"] = res["icao24"].astype("int64")
    return res


def make_metars(rng, apt, days):
    rows = 200
    out = {}
    for name, kind in METAR_COLS:
        if name == "station":
            out[name] = pd.Series(rng.choice(apt.icao.values, rows), dtype="string")
        elif name == "valid":
            out[name] = (pd.Timestamp(days[0], tz="UTC") +
                         pd.to_timedelta(rng.integers(0, 24 * 60 * len(days), rows), unit="min")
                         ).astype("datetime64[ns, UTC]")
        elif kind == "s":
            out[name] = pd.Series(rng.choice(["FEW", "SCT", "BKN"], rows), dtype="string")
        elif kind == "o":
            out[name] = pd.Series([None] * rows, dtype="object")
        else:
            out[name] = rng.normal(0, 1, rows).astype("float64")
    return pd.DataFrame(out)


def generate(out, n_days=4, n_challenge_per_day=130, n_final_per_day=60, seed=0):
    """Write the synthetic folders under @out: <out>/lj (FOLDER_DATA), <out>/raw, <out>/ext."""
    rng = np.random.default_rng(seed)
    days = [str(d.date()) for d in pd.date_range(FIRST_DAY, periods=n_days, freq="D")]
    lj = os.path.join(out, "lj")
    raw = os.path.join(out, "raw")
    for d in [lj, raw, os.path.join(out, "ext"), os.path.join(out, "tmp")]:
        os.makedirs(d, exist_ok=True)
    allf, apt = make_flights(rng, days, n_challenge_per_day + n_final_per_day)
    is_final = np.zeros(len(allf), dtype=bool)
    for day in days:
        idx = np.flatnonzero(allf.date.dt.strftime("%Y-%m-%d").values == day)
        is_final[rng.choice(idx, n_final_per_day, replace=False)] = True
    sets = {"challenge_set": allf[~is_final].reset_index(drop=True),
            "final_submission_set": allf[is_final].reset_index(drop=True)}

    os.makedirs(os.path.join(lj, "flights"), exist_ok=True)
    for name, df in sets.items():
        fp = flights_parquet_frame(df)
        fc = flights_csv_frame(df)
        if name == "final_submission_set":
            fp["tow"] = np.nan
            fc["tow"] = np.nan
        fp.to_parquet(os.path.join(lj, "flights", f"{name}.parquet"), index=False)
        fc.to_csv(os.path.join(lj, "flights", f"{name}.csv"), index=False)
    make_airports(apt).to_parquet(os.path.join(lj, "airports_tz.parquet"), index=False)
    make_metars(rng, apt, days).to_parquet(os.path.join(lj, "METARs.parquet"), index=False)
    for sub, maker in [("weather", make_weather), ("thunder", make_thunder)]:
        os.makedirs(os.path.join(lj, sub), exist_ok=True)
        for name, df in sets.items():
            maker(rng, df).to_parquet(os.path.join(lj, sub, f"{name}.parquet"), index=False)
    folders = {
        "classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses": (climb_frame, 0.004),
        "classic__1e-2__20_cruise": (cruise_frame, 0.0),
        "classic__1e-2_wind": (lambda r, d: pd.DataFrame({"flight_id": d.flight_id.values.astype("int64"),
                                                         "wind_effect": r.normal(-10, 15, len(d))}), 0.0),
    }
    for folder, (maker, drop) in folders.items():
        for name, df in sets.items():
            os.makedirs(os.path.join(lj, folder, name), exist_ok=True)
            for day in days:
                d = df[df.date.dt.strftime("%Y-%m-%d") == day]
                d = d[rng.random(len(d)) >= drop]
                maker(rng, d).to_parquet(os.path.join(lj, folder, name, f"{day}.parquet"), index=False)
    for empty in ["classic__1e-2_interpolated_trajectories", "classic_filtered_trajectories"]:
        os.makedirs(os.path.join(lj, empty), exist_ok=True)
    os.makedirs(os.path.join(lj, "rawtrajectories"), exist_ok=True)
    for day in days:  # a few flights per day (both sets), enough for trajectory-code tests later
        d = allf[allf.date.dt.strftime("%Y-%m-%d") == day]
        raw_trajectories(rng, d).to_parquet(os.path.join(lj, "rawtrajectories", f"{day}.parquet"), index=False)

    # raw challenge files; flight_list.csv holds the truth of ALL flights
    flights_csv_frame(sets["challenge_set"]).to_csv(os.path.join(raw, "train.csv"), index=False)
    tf = flights_csv_frame(sets["final_submission_set"])
    tf["tow"] = np.nan
    tf.to_csv(os.path.join(raw, "test_final.csv"), index=False)
    tf.to_csv(os.path.join(raw, "test.csv"), index=False)
    pd.DataFrame({"flight_id": tf.flight_id.values[: len(tf) // 3]}).to_csv(os.path.join(raw, "partC_ids.csv"), index=False)
    truth = flights_csv_frame(allf.sort_values("flight_id"))
    truth.to_csv(os.path.join(raw, "flight_list.csv"), index=False)
    return dict(lj=lj, raw=raw, ext=os.path.join(out, "ext"), tmp=os.path.join(out, "tmp"), days=days)


def write_config(paths, fname):
    p = {k: os.path.abspath(v).replace("\\", "/") for k, v in paths.items() if k != "days"}
    with open(fname, "w") as f:
        f.write("# generated by koopmann_aziz/synth.py -- synthetic data, laptop only\n")
        f.write(f"FOLDER_DATA = {p['lj']}\n")
        f.write(f"SUBMISSIONS_FOLDER = {p['ext']}/submissions_team_format\n")
        f.write(f"JSON = {p['ext']}/no_team_json.json\n")
        f.write(f"EXT_FOLDER = {p['ext']}\n")
        f.write(f"TEMP_FOLDER = {p['tmp']}\n")
        f.write(f"# for tests only (never read by training code): {p['raw']}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(HERE, "_synth"))
    ap.add_argument("--days", type=int, default=4)
    ap.add_argument("--challenge-per-day", type=int, default=130)
    ap.add_argument("--final-per-day", type=int, default=60)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--write-config", action="store_true",
                    help="write koopmann_aziz/config/CONFIG.laptop pointing at --out")
    a = ap.parse_args()
    paths = generate(a.out, a.days, a.challenge_per_day, a.final_per_day, a.seed)
    print("synthetic data written to", os.path.abspath(a.out))
    if a.write_config:
        cfg = os.path.join(HERE, "config", "CONFIG.laptop")
        write_config(paths, cfg)
        print("config written to", cfg)


if __name__ == "__main__":
    main()
