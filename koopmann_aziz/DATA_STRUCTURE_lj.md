# likable_jelly data structure on pc182

Generated 2026-11-18T11:38:56 by dump_lj_structure.py (pandas 2.2.3, Python 3.12.15). Read-only; no test labels included.

## Top-level files of the data folder

### `E:/Koopmann-Aziz/data/prc2024/lj\METARs.parquet`
- size: 2.38 GB
- read: metadata + first 2000 rows only
- rows: 42,613,794; columns: 33

| column | dtype | missing share |
| --- | --- | --- |
| `station` | string | n/a (sample only) |
| `valid` | datetime64[ns, UTC] | n/a (sample only) |
| `lon` | float64 | n/a (sample only) |
| `lat` | float64 | n/a (sample only) |
| `elevation` | float64 | n/a (sample only) |
| `tmpf` | float64 | n/a (sample only) |
| `dwpf` | float64 | n/a (sample only) |
| `relh` | float64 | n/a (sample only) |
| `drct` | float64 | n/a (sample only) |
| `sknt` | float64 | n/a (sample only) |
| `p01i` | float64 | n/a (sample only) |
| `alti` | float64 | n/a (sample only) |
| `mslp` | float64 | n/a (sample only) |
| `vsby` | float64 | n/a (sample only) |
| `gust` | float64 | n/a (sample only) |
| `skyc1` | string | n/a (sample only) |
| `skyc2` | string | n/a (sample only) |
| `skyc3` | string | n/a (sample only) |
| `skyc4` | string | n/a (sample only) |
| `skyl1` | float64 | n/a (sample only) |
| `skyl2` | float64 | n/a (sample only) |
| `skyl3` | float64 | n/a (sample only) |
| `skyl4` | float64 | n/a (sample only) |
| `wxcodes` | string | n/a (sample only) |
| `ice_accretion_1hr` | float64 | n/a (sample only) |
| `ice_accretion_3hr` | float64 | n/a (sample only) |
| `ice_accretion_6hr` | float64 | n/a (sample only) |
| `peak_wind_gust` | float64 | n/a (sample only) |
| `peak_wind_drct` | float64 | n/a (sample only) |
| `peak_wind_time` | object | n/a (sample only) |
| `feel` | float64 | n/a (sample only) |
| `metar` | string | n/a (sample only) |
| `snowdepth` | float64 | n/a (sample only) |

Example rows (first 25 of 33 columns):

| station | valid | lon | lat | elevation | tmpf | dwpf | relh | drct | sknt | p01i | alti | mslp | vsby | gust | skyc1 | skyc2 | skyc3 | skyc4 | skyl1 | skyl2 | skyl3 | skyl4 | wxcodes | ice_accretion_1hr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WMKM | 2021-12-31 00:00:00+00:00 | 102.2515 | 2.2634 | 9.0 | 75.2 | 73.4 | 94.14 | 80.0 | 7.0 | 0.0 | 29.88 | nan | 6.21 | nan | FEW | SCT | <NA> | <NA> | 1200.0 | 2600.0 | nan | nan | -RA | nan |
| EPLB | 2021-12-31 00:00:00+00:00 | 17.77 | 54.42 | 151.24 | 41.0 | 41.0 | 100.0 | 250.0 | 8.0 | 0.0 | 29.91 | nan | 2.8 | nan | BKN | OVC | <NA> | <NA> | 600.0 | 800.0 | nan | nan | BR | nan |
| LFRV | 2021-12-31 00:00:00+00:00 | -2.7186 | 47.7233 | 133.45 | 50.0 | 50.0 | 100.0 | 170.0 | 6.0 | 0.0 | 30.09 | nan | 0.81 | nan | VV  | <NA> | <NA> | <NA> | nan | nan | nan | nan | BR | nan |

### `E:/Koopmann-Aziz/data/prc2024/lj\airports_tz.parquet`
- size: 0.1 MB
- rows: 502; columns: 19

| column | dtype | missing share |
| --- | --- | --- |
| `id` | int64 | 0.000 |
| `type` | string | 0.000 |
| `name` | string | 0.000 |
| `latitude_deg` | float64 | 0.000 |
| `longitude_deg` | float64 | 0.000 |
| `elevation_ft` | float64 | 0.000 |
| `continent` | string | 0.090 |
| `iso_country` | string | 0.000 |
| `iso_region` | string | 0.000 |
| `municipality` | string | 0.002 |
| `scheduled_service` | string | 0.000 |
| `gps_code` | string | 0.002 |
| `iata_code` | string | 0.010 |
| `local_code` | string | 0.890 |
| `home_link` | string | 0.281 |
| `wikipedia_link` | string | 0.000 |
| `keywords` | string | 0.488 |
| `icao_code` | string | 0.000 |
| `time_zone` | string | 0.000 |

Example rows:

| id | type | name | latitude_deg | longitude_deg | elevation_ft | continent | iso_country | iso_region | municipality | scheduled_service | gps_code | iata_code | local_code | home_link | wikipedia_link | keywords | icao_code | time_zone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 123 | large_airport | Keflavik International Airport | 63.985001 | -22.6056 | 171.0 | EU | IS | IS-2 | Reykjavík | yes | BIKF | KEF | <NA> | https://www.isavia.is/en/keflavik-airpor | https://en.wikipedia.org/wiki/Keflav%C3% | Keflavik Naval Air Station,REK | BIKF | Atlantic/Reykjavik |
| 4614 | medium_airport | Priština Adem Jashari International Airp | 42.5728 | 21.035801 | 1789.0 | EU | XK | XK-01 | Prishtina | yes | BKPR | PRN | <NA> | http://www.airportpristina.com/ | https://en.wikipedia.org/wiki/Pristina_I | LYPR, Pristina, Slatina Air Base | BKPR | Europe/Belgrade |
| 1729 | medium_airport | Iqaluit Airport | 63.756402 | -68.555801 | 110.0 | <NA> | CA | CA-NU | Iqaluit | yes | CYFB | YFB | <NA> | <NA> | https://en.wikipedia.org/wiki/Iqaluit_Ai | Frobisher Bay Air Base | CYFB | America/Iqaluit |

### `E:/Koopmann-Aziz/data/prc2024/lj\download.log`
- size: 0.0 MB
- (not described)

### `E:/Koopmann-Aziz/data/prc2024/lj\ram_monitor.log`
- size: 2.0 MB
- (not described)

### `E:/Koopmann-Aziz/data/prc2024/lj\run_lj.log`
- size: 0.6 MB
- (not described)

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2__20_cruise`
- total: 0.33 GB in 730 files; subfolders: challenge_set, final_submission_set

#### Subfolder `challenge_set`: 0.22 GB in 365 files; first `2022-01-01.parquet`, last `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2__20_cruise\challenge_set\2022-01-01.parquet`
- size: 0.3 MB
- rows: 531; columns: 82
- 82 columns, grouped by name pattern (`_<i>` = slice index):

| pattern | count | dtype | missing share (min-max) |
| --- | --- | --- | --- |
| `flight_id` | 1 | int64 | 0.000-0.000 |
| `f_duration` | 1 | float64 | 0.000-0.000 |
| `Cruisemach_<i>` | 20 | float64 | 0.032-0.458 |
| `Cruisemachcount_<i>` | 20 | float64 | 0.004-0.379 |
| `CruiseDeltaAlt_<i>` | 20 | float64 | 0.021-0.412 |
| `CruiseMedianAlt_<i>` | 20 | float64 | 0.021-0.412 |

Example rows (first 25 of 82 columns):

| flight_id | f_duration | Cruisemach_0 | Cruisemachcount_0 | CruiseDeltaAlt_0 | CruiseMedianAlt_0 | Cruisemach_1 | Cruisemachcount_1 | CruiseDeltaAlt_1 | CruiseMedianAlt_1 | Cruisemach_2 | Cruisemachcount_2 | CruiseDeltaAlt_2 | CruiseMedianAlt_2 | Cruisemach_3 | Cruisemachcount_3 | CruiseDeltaAlt_3 | CruiseMedianAlt_3 | Cruisemach_4 | Cruisemachcount_4 | CruiseDeltaAlt_4 | CruiseMedianAlt_4 | Cruisemach_5 | Cruisemachcount_5 | CruiseDeltaAlt_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248750643 | 11984.437223003 | nan | nan | nan | nan | 0.5838493865411525 | 470.0 | 22121.78462688106 | 13739.093310442271 | 0.7787735969916509 | 599.0 | 10282.634917135838 | 31588.130863714418 | 0.7865003253861966 | 472.0 | -16.951776107052865 | 34000.0 | 0.786864509628854 | 570.0 | 964.4356501432412 | 34000.000000000015 | 0.8071663266751812 | 599.0 | 1035.5009711375023 |
| 248750693 | 4190.301274782 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | 0.28719290437160916 | 48.0 | 2240.3062162080187 | 1880.9303919603 | 0.47983260003619777 | 117.0 | 9594.861407315993 | 10718.19154596398 | 0.594593837264966 | 161.0 | 9061.914284576422 |
| 248750694 | 12154.423219106 | 0.6035046146395863 | 279.0 | 21602.741484260634 | 18327.713877128426 | 0.7455464707410819 | 608.0 | 10780.754230600385 | 30156.857160789517 | 0.7599088475341219 | 555.0 | 1999.9999999961074 | 35999.99999999148 | 0.767542676989001 | 586.0 | 0.0 | 36000.0 | 0.7717690047873411 | 582.0 | 4.254705709172413e-05 | 36000.0 | 0.7579169918557055 | 581.0 | 50.16046273239044 |

#### Subfolder `final_submission_set`: 0.11 GB in 365 files; first `2022-01-01.parquet`, last `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2__20_cruise\final_submission_set\2022-01-01.parquet`
- size: 0.2 MB
- rows: 250; columns: 82
- 82 columns, grouped by name pattern (`_<i>` = slice index):

| pattern | count | dtype | missing share (min-max) |
| --- | --- | --- | --- |
| `flight_id` | 1 | int64 | 0.000-0.000 |
| `f_duration` | 1 | float64 | 0.000-0.000 |
| `Cruisemach_<i>` | 20 | float64 | 0.020-0.516 |
| `Cruisemachcount_<i>` | 20 | float64 | 0.012-0.400 |
| `CruiseDeltaAlt_<i>` | 20 | float64 | 0.020-0.468 |
| `CruiseMedianAlt_<i>` | 20 | float64 | 0.020-0.468 |

Example rows (first 25 of 82 columns):

| flight_id | f_duration | Cruisemach_0 | Cruisemachcount_0 | CruiseDeltaAlt_0 | CruiseMedianAlt_0 | Cruisemach_1 | Cruisemachcount_1 | CruiseDeltaAlt_1 | CruiseMedianAlt_1 | Cruisemach_2 | Cruisemachcount_2 | CruiseDeltaAlt_2 | CruiseMedianAlt_2 | Cruisemach_3 | Cruisemachcount_3 | CruiseDeltaAlt_3 | CruiseMedianAlt_3 | Cruisemach_4 | Cruisemachcount_4 | CruiseDeltaAlt_4 | CruiseMedianAlt_4 | Cruisemach_5 | Cruisemachcount_5 | CruiseDeltaAlt_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248750690 | 13267.195653611 | 0.440291326209226 | 159.0 | 8803.740720296179 | 8216.789203556185 | 0.6647896923059595 | 664.0 | 16036.524120001457 | 20069.101362213685 | 0.7660570172440181 | 645.0 | 7399.9792352975055 | 31394.407776498214 | 0.7711983248534813 | 500.0 | 23.6532648808643 | 34000.681433464706 | 0.7769575620304686 | 638.0 | 26.88683566970576 | 34000.00135639927 | 0.7616357434433136 | 607.0 | -18.982432252247236 |
| 248750710 | 7999.578914456 | 0.34377116317606987 | 130.0 | 10993.400457125375 | 2739.221127271854 | 0.6456706724118264 | 314.0 | 15808.846257563098 | 22462.59294813332 | 0.7719689162989294 | 400.0 | 9329.370172907205 | 32433.886991194537 | 0.7879187708151575 | 400.0 | 244.82776498565363 | 38000.00001714118 | 0.7667871688706637 | 376.0 | -29.160486533372023 | 38000.00002468727 | 0.771205616391049 | 400.0 | 3.162686794916226 |
| 248750808 | 4875.756752728 | nan | nan | nan | nan | 0.25667854373965093 | 88.0 | 3360.792335814 | 1913.0137183792635 | 0.46540969360747686 | 244.0 | 13034.986043501527 | 10493.671966797843 | 0.6341353834691844 | 244.0 | 9538.256359686191 | 21661.6161390591 | 0.7395881887059854 | 243.0 | 6789.466518583595 | 29201.81273986432 | 0.7587918992242599 | 244.0 | 3393.5305854564212 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses`
- total: 1.94 GB in 730 files; subfolders: challenge_set, final_submission_set

#### Subfolder `challenge_set`: 1.31 GB in 365 files; first `2022-01-01.parquet`, last `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses\challenge_set\2022-01-01.parquet`
- size: 2.1 MB
- rows: 529; columns: 542
- 542 columns, grouped by name pattern (`_<i>` = slice index):

| pattern | count | dtype | missing share (min-max) |
| --- | --- | --- | --- |
| `flight_id` | 1 | int64 | 0.000-0.000 |
| `mass_max` | 1 | float64 | 0.000-0.000 |
| `mass_min` | 1 | float64 | 0.000-0.000 |
| `climbmass_<i>` | 48 | float64 | 0.059-1.000 |
| `climbmasscount_<i>` | 48 | float64 | 0.034-1.000 |
| `climbmassadepdate_<i>` | 48 | float64 | 0.034-1.000 |
| `climbmassadesdate_<i>` | 48 | float64 | 0.034-1.000 |
| `climbDeltaROCD_<i>` | 48 | float64 | 0.049-1.000 |
| `climbROCD_<i>` | 48 | float64 | 0.049-1.000 |
| `climbe_rate_median_<i>` | 48 | float64 | 0.059-1.000 |
| `climbtas_median_<i>` | 48 | float64 | 0.053-1.000 |
| `climbDeltaT_median_<i>` | 48 | float64 | 0.047-1.000 |
| `climbe_rate_max_<i>` | 48 | float64 | 0.059-1.000 |
| `climbe_rate_min_<i>` | 48 | float64 | 0.059-1.000 |
| `takeoffmass_<i>` | 1 | float64 | 0.992-0.992 |
| `takeoffmasscount_<i>` | 1 | float64 | 0.921-0.921 |
| `takeoffmassadepdate_<i>` | 1 | float64 | 0.921-0.921 |
| `takeoffmassadesdate_<i>` | 1 | float64 | 0.921-0.921 |
| `takeoffDeltaROCD_<i>` | 1 | float64 | 0.981-0.981 |
| `takeoffROCD_<i>` | 1 | float64 | 0.981-0.981 |
| `takeoffe_rate_median_<i>` | 1 | float64 | 0.992-0.992 |
| `takeofftas_median_<i>` | 1 | float64 | 0.987-0.987 |
| `takeoffDeltaT_median_<i>` | 1 | float64 | 0.921-0.921 |
| `takeoffe_rate_max_<i>` | 1 | float64 | 0.992-0.992 |
| `takeoffe_rate_min_<i>` | 1 | float64 | 0.992-0.992 |

Example rows (first 25 of 542 columns):

| flight_id | mass_max | mass_min | climbmass_0 | climbmasscount_0 | climbmassadepdate_0 | climbmassadesdate_0 | climbDeltaROCD_0 | climbROCD_0 | climbe_rate_median_0 | climbtas_median_0 | climbDeltaT_median_0 | climbe_rate_max_0 | climbe_rate_min_0 | climbmass_1 | climbmasscount_1 | climbmassadepdate_1 | climbmassadesdate_1 | climbDeltaROCD_1 | climbROCD_1 | climbe_rate_median_1 | climbtas_median_1 | climbDeltaT_median_1 | climbe_rate_max_1 | climbe_rate_min_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248750643 | 242000.0 | 122780.0 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| 248750693 | 79000.0 | 41400.0 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | 0.0 | 768.319109072 | 3418.98216571 | 0.20901408218345185 | 6.442132570466594 | nan | 79.62201326916535 | -4.288379689586691 | nan | nan |
| 248750694 | 93500.0 | 48500.0 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |

#### Subfolder `final_submission_set`: 0.64 GB in 365 files; first `2022-01-01.parquet`, last `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses\final_submission_set\2022-01-01.parquet`
- size: 1.2 MB
- rows: 249; columns: 542
- 542 columns, grouped by name pattern (`_<i>` = slice index):

| pattern | count | dtype | missing share (min-max) |
| --- | --- | --- | --- |
| `flight_id` | 1 | int64 | 0.000-0.000 |
| `mass_max` | 1 | float64 | 0.000-0.000 |
| `mass_min` | 1 | float64 | 0.000-0.000 |
| `climbmass_<i>` | 48 | float64 | 0.052-1.000 |
| `climbmasscount_<i>` | 48 | float64 | 0.040-1.000 |
| `climbmassadepdate_<i>` | 48 | float64 | 0.040-1.000 |
| `climbmassadesdate_<i>` | 48 | float64 | 0.040-1.000 |
| `climbDeltaROCD_<i>` | 48 | float64 | 0.044-1.000 |
| `climbROCD_<i>` | 48 | float64 | 0.044-1.000 |
| `climbe_rate_median_<i>` | 48 | float64 | 0.052-1.000 |
| `climbtas_median_<i>` | 48 | float64 | 0.048-1.000 |
| `climbDeltaT_median_<i>` | 48 | float64 | 0.044-1.000 |
| `climbe_rate_max_<i>` | 48 | float64 | 0.052-1.000 |
| `climbe_rate_min_<i>` | 48 | float64 | 0.052-1.000 |
| `takeoffmass_<i>` | 1 | float64 | 0.984-0.984 |
| `takeoffmasscount_<i>` | 1 | float64 | 0.892-0.892 |
| `takeoffmassadepdate_<i>` | 1 | float64 | 0.892-0.892 |
| `takeoffmassadesdate_<i>` | 1 | float64 | 0.892-0.892 |
| `takeoffDeltaROCD_<i>` | 1 | float64 | 0.968-0.968 |
| `takeoffROCD_<i>` | 1 | float64 | 0.968-0.968 |
| `takeoffe_rate_median_<i>` | 1 | float64 | 0.984-0.984 |
| `takeofftas_median_<i>` | 1 | float64 | 0.968-0.968 |
| `takeoffDeltaT_median_<i>` | 1 | float64 | 0.892-0.892 |
| `takeoffe_rate_max_<i>` | 1 | float64 | 0.984-0.984 |
| `takeoffe_rate_min_<i>` | 1 | float64 | 0.984-0.984 |

Example rows (first 25 of 542 columns):

| flight_id | mass_max | mass_min | climbmass_0 | climbmasscount_0 | climbmassadepdate_0 | climbmassadesdate_0 | climbDeltaROCD_0 | climbROCD_0 | climbe_rate_median_0 | climbtas_median_0 | climbDeltaT_median_0 | climbe_rate_max_0 | climbe_rate_min_0 | climbmass_1 | climbmasscount_1 | climbmassadepdate_1 | climbmassadesdate_1 | climbDeltaROCD_1 | climbROCD_1 | climbe_rate_median_1 | climbtas_median_1 | climbDeltaT_median_1 | climbe_rate_max_1 | climbe_rate_min_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248750690 | 93500.0 | 48500.0 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| 248750710 | 85100.0 | 44600.0 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| 248750808 | 78000.0 | 42600.0 | 62329.557045174406 | 8.0 | 395.965399569 | 4463.791353159 | 10.688313416130146 | 13.421807166971721 | 109.73744288255257 | 82.62042547675395 | -3.380919718944199 | 123.30465970660195 | 95.27772182242973 | 48816.305227152036 | 17.0 | 412.965399569 | 4446.791353159 | 3.0553718164083623 | 17.27499229759076 | 151.26392116670945 | 79.08920825930191 | -1.1996809162224054 | 161.12668352038048 | 127.16681080823415 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2_interpolated_trajectories`
- total: 0.0 MB in 0 files; subfolders: none

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2_wind`
- total: 9.5 MB in 730 files; subfolders: challenge_set, final_submission_set

#### Subfolder `challenge_set`: 6.3 MB in 365 files; first `2022-01-01.parquet`, last `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2_wind\challenge_set\2022-01-01.parquet`
- size: 0.0 MB
- rows: 531; columns: 2

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `wind_effect` | float64 | 0.000 |

Example rows:

| flight_id | wind_effect |
| --- | --- |
| 248750643 | -14.749631586534866 |
| 248750693 | -8.481066303809893 |
| 248750694 | -29.069137611687072 |

#### Subfolder `final_submission_set`: 3.2 MB in 365 files; first `2022-01-01.parquet`, last `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\classic__1e-2_wind\final_submission_set\2022-01-01.parquet`
- size: 0.0 MB
- rows: 250; columns: 2

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `wind_effect` | float64 | 0.000 |

Example rows:

| flight_id | wind_effect |
| --- | --- |
| 248750690 | -36.95203420508345 |
| 248750710 | -11.669310238771107 |
| 248750808 | -20.945753261424276 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\classic_filtered_trajectories`
- total: 0.0 MB in 0 files; subfolders: none

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\flights`
- total: 0.12 GB in 4 files; subfolders: none
- files here: 4; first: `challenge_set.csv`, last: `final_submission_set.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\flights\challenge_set.csv`
- size: 70.8 MB
- rows: 369,013; columns: 18
- `tow` (training label): non-missing = 369013

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | object | 0.000 |
| `callsign` | object | 0.000 |
| `adep` | object | 0.000 |
| `name_adep` | object | 0.000 |
| `country_code_adep` | object | 0.000 |
| `ades` | object | 0.000 |
| `name_ades` | object | 0.000 |
| `country_code_ades` | object | 0.000 |
| `actual_offblock_time` | object | 0.000 |
| `arrival_time` | object | 0.000 |
| `aircraft_type` | object | 0.000 |
| `wtc` | object | 0.000 |
| `airline` | object | 0.000 |
| `flight_duration` | int64 | 0.000 |
| `taxiout_time` | int64 | 0.000 |
| `flown_distance` | int64 | 0.000 |
| `tow` | float64 | 0.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance | tow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248763780 | 2022-01-01 | 3840d84f25d3f5fcc0a1be3076bb4039 | EGLL | London Heathrow | GB | EICK | Cork | IE | 2022-01-01T13:46:00Z | 2022-01-01T15:04:56Z | A320 | M | a73f82288988b79be490c6322f4c32ed | 61 | 18 | 321 | 54748.0 |
| 248760618 | 2022-01-01 | f6f610e73002b8892a239a81321f7f1d | LEBL | Barcelona | ES | KMIA | Miami | US | 2022-01-01T09:55:00Z | 2022-01-01T19:37:56Z | B772 | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 570 | 13 | 4193 | 185441.0 |
| 248753824 | 2022-01-01 | 139670936660762c230ca92556ba842b | ESSA | Stockholm Arlanda | SE | KORD | Chicago O'Hare | US | 2022-01-01T09:39:00Z | 2022-01-01T19:08:13Z | A333 | H | 8be5c854fd664bcb97fb543339f74770 | 554 | 15 | 3770 | 230396.0 |

### `E:/Koopmann-Aziz/data/prc2024/lj\flights\challenge_set.parquet`
- size: 13.0 MB
- rows: 369,013; columns: 18
- `tow` (training label): non-missing = 369013

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | datetime64[ns, UTC] | 0.000 |
| `callsign` | string | 0.000 |
| `adep` | string | 0.000 |
| `name_adep` | string | 0.000 |
| `country_code_adep` | string | 0.000 |
| `ades` | string | 0.000 |
| `name_ades` | string | 0.000 |
| `country_code_ades` | string | 0.000 |
| `actual_offblock_time` | datetime64[ns, UTC] | 0.000 |
| `arrival_time` | datetime64[ns, UTC] | 0.000 |
| `aircraft_type` | string | 0.000 |
| `wtc` | string | 0.000 |
| `airline` | string | 0.000 |
| `flight_duration` | float64 | 0.000 |
| `taxiout_time` | float64 | 0.000 |
| `flown_distance` | float64 | 0.000 |
| `tow` | float64 | 0.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance | tow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248763780 | 2022-01-01 00:00:00+00:00 | 3840d84f25d3f5fcc0a1be3076bb4039 | EGLL | London Heathrow | GB | EICK | Cork | IE | 2022-01-01 13:46:00+00:00 | 2022-01-01 15:04:56+00:00 | A320 | M | a73f82288988b79be490c6322f4c32ed | 61.0 | 18.0 | 321.0 | 54748.0 |
| 248760618 | 2022-01-01 00:00:00+00:00 | f6f610e73002b8892a239a81321f7f1d | LEBL | Barcelona | ES | KMIA | Miami | US | 2022-01-01 09:55:00+00:00 | 2022-01-01 19:37:56+00:00 | B772 | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 570.0 | 13.0 | 4193.0 | 185441.0 |
| 248753824 | 2022-01-01 00:00:00+00:00 | 139670936660762c230ca92556ba842b | ESSA | Stockholm Arlanda | SE | KORD | Chicago O'Hare | US | 2022-01-01 09:39:00+00:00 | 2022-01-01 19:08:13+00:00 | A333 | H | 8be5c854fd664bcb97fb543339f74770 | 554.0 | 15.0 | 3770.0 | 230396.0 |

### `E:/Koopmann-Aziz/data/prc2024/lj\flights\final_submission_set.csv`
- size: 29.3 MB
- rows: 158,149; columns: 18
- `tow` present in a TEST file: non-missing values = 0  <- should be 0

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | object | 0.000 |
| `callsign` | object | 0.000 |
| `adep` | object | 0.000 |
| `name_adep` | object | 0.000 |
| `country_code_adep` | object | 0.000 |
| `ades` | object | 0.000 |
| `name_ades` | object | 0.000 |
| `country_code_ades` | object | 0.000 |
| `actual_offblock_time` | object | 0.000 |
| `arrival_time` | object | 0.000 |
| `aircraft_type` | object | 0.000 |
| `wtc` | object | 0.000 |
| `airline` | object | 0.000 |
| `flight_duration` | int64 | 0.000 |
| `taxiout_time` | int64 | 0.000 |
| `flown_distance` | int64 | 0.000 |
| `tow` | float64 | 1.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248753821 | 2022-01-01 | 3b3de0f3ad0ee192513995c02f7bf7cf | LTFJ | Istanbul Sabiha Gokcen | TR | LFLL | Lyon | FR | 2022-01-01T09:44:00Z | 2022-01-01T12:48:33Z | B738 | M | 6351ec1b849adacc0cbb3b1313d8d39b | 170 | 15 | 1122 |
| 248753822 | 2022-01-01 | e06dd03d4a879ca37d9e18c1bd7cad16 | EBBR | Brussels | BE | KJFK | New York JFK | US | 2022-01-01T09:45:00Z | 2022-01-01T17:49:51Z | A333 | H | bdeeef3a675587d530de70a25d7118d2 | 470 | 15 | 3205 |
| 248754498 | 2022-01-01 | 2d3b1c962c78c4ebeef11bcd51b9e94c | KMIA | Miami | US | EGLL | London Heathrow | GB | 2022-01-01T01:52:00Z | 2022-01-01T09:55:16Z | B77W | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 473 | 10 | 3965 |

### `E:/Koopmann-Aziz/data/prc2024/lj\flights\final_submission_set.parquet`
- size: 6.1 MB
- rows: 158,149; columns: 18
- `tow` present in a TEST file: non-missing values = 0  <- should be 0

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | datetime64[ns, UTC] | 0.000 |
| `callsign` | string | 0.000 |
| `adep` | string | 0.000 |
| `name_adep` | string | 0.000 |
| `country_code_adep` | string | 0.000 |
| `ades` | string | 0.000 |
| `name_ades` | string | 0.000 |
| `country_code_ades` | string | 0.000 |
| `actual_offblock_time` | datetime64[ns, UTC] | 0.000 |
| `arrival_time` | datetime64[ns, UTC] | 0.000 |
| `aircraft_type` | string | 0.000 |
| `wtc` | string | 0.000 |
| `airline` | string | 0.000 |
| `flight_duration` | float64 | 0.000 |
| `taxiout_time` | float64 | 0.000 |
| `flown_distance` | float64 | 0.000 |
| `tow` | float64 | 1.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248753821 | 2022-01-01 00:00:00+00:00 | 3b3de0f3ad0ee192513995c02f7bf7cf | LTFJ | Istanbul Sabiha Gokcen | TR | LFLL | Lyon | FR | 2022-01-01 09:44:00+00:00 | 2022-01-01 12:48:33+00:00 | B738 | M | 6351ec1b849adacc0cbb3b1313d8d39b | 170.0 | 15.0 | 1122.0 |
| 248753822 | 2022-01-01 00:00:00+00:00 | e06dd03d4a879ca37d9e18c1bd7cad16 | EBBR | Brussels | BE | KJFK | New York JFK | US | 2022-01-01 09:45:00+00:00 | 2022-01-01 17:49:51+00:00 | A333 | H | bdeeef3a675587d530de70a25d7118d2 | 470.0 | 15.0 | 3205.0 |
| 248754498 | 2022-01-01 00:00:00+00:00 | 2d3b1c962c78c4ebeef11bcd51b9e94c | KMIA | Miami | US | EGLL | London Heathrow | GB | 2022-01-01 01:52:00+00:00 | 2022-01-01 09:55:16+00:00 | B77W | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 473.0 | 10.0 | 3965.0 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\rawtrajectories`
- total: 306.37 GB in 365 files; subfolders: none
- files here: 365; first: `2022-01-01.parquet`, last: `2022-12-31.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\rawtrajectories\2022-01-01.parquet`
- size: 0.57 GB
- read: metadata + first 2000 rows only
- rows: 11,862,463; columns: 13

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | n/a (sample only) |
| `timestamp` | datetime64[ns, UTC] | n/a (sample only) |
| `latitude` | float64 | n/a (sample only) |
| `longitude` | float64 | n/a (sample only) |
| `altitude` | float64 | n/a (sample only) |
| `groundspeed` | float64 | n/a (sample only) |
| `track` | float64 | n/a (sample only) |
| `vertical_rate` | float64 | n/a (sample only) |
| `icao24` | int64 | n/a (sample only) |
| `u_component_of_wind` | float64 | n/a (sample only) |
| `v_component_of_wind` | float64 | n/a (sample only) |
| `temperature` | float64 | n/a (sample only) |
| `specific_humidity` | float64 | n/a (sample only) |

Example rows:

| flight_id | timestamp | latitude | longitude | altitude | groundspeed | track | vertical_rate | icao24 | u_component_of_wind | v_component_of_wind | temperature | specific_humidity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248763775 | 2022-01-01 18:14:38+00:00 | 30.898406982421875 | 31.240270278033087 | 38000.0 | 429.0 | 350.888642955216 | -64.0 | 248763775 | 8.754635828971816 | -13.070077743165415 | 221.81961838926793 | 7.579897014706791e-06 |
| 248763775 | 2022-01-01 18:14:39+00:00 | 30.909615209547137 | 31.238250732421875 | 38000.0 | 429.0 | 351.02043432984954 | 128.0 | 248763775 | 8.69674926772829 | -13.106523802414069 | 221.79478176758906 | 7.605728996807239e-06 |
| 248763775 | 2022-01-01 18:14:40+00:00 | 30.909615209547137 | 31.238250732421875 | 38000.0 | 429.0 | 351.02043432984954 | 128.0 | 248763775 | 8.697086859321246 | -13.10718419939935 | 221.7946999439807 | 7.606141694465598e-06 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\submissions`
- total: 96.9 MB in 21 files; subfolders: none
- files here: 21; first: `___v0_.csv`, last: `averaged_10.csv`

### `E:/Koopmann-Aziz/data/prc2024/lj\submissions\___v0_.csv`
- size: 4.6 MB
- rows: 158,149; columns: 2
- `tow` (training label): non-missing = 158149

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `tow` | float64 | 0.000 |

Example rows:

| flight_id | tow |
| --- | --- |
| 248753821 | 71055.56209916864 |
| 248753822 | 215627.65631826088 |
| 248754498 | 223216.68940528823 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\submissions_subset5`
- total: 4.6 MB in 1 files; subfolders: none
- files here: 1; first: `___v0_.csv`, last: `___v0_.csv`

### `E:/Koopmann-Aziz/data/prc2024/lj\submissions_subset5\___v0_.csv`
- size: 4.6 MB
- rows: 158,149; columns: 2
- `tow` (training label): non-missing = 158149

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `tow` | float64 | 0.000 |

Example rows:

| flight_id | tow |
| --- | --- |
| 248753821 | 68699.23436868846 |
| 248753822 | 215783.7895199556 |
| 248754498 | 217263.73238159585 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\thunder`
- total: 3.9 MB in 2 files; subfolders: none
- files here: 2; first: `challenge_set.parquet`, last: `final_submission_set.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\thunder\challenge_set.parquet`
- size: 2.6 MB
- rows: 369,013; columns: 31

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `thunder_max_TS_1_ades` | float64 | 0.000 |
| `thunder_max_pTS_1_ades` | float64 | 0.000 |
| `thunder_max_VCTS_1_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_1_ades` | float64 | 0.000 |
| `thunder_max_FG_1_ades` | float64 | 0.000 |
| `thunder_max_TS_2_ades` | float64 | 0.000 |
| `thunder_max_pTS_2_ades` | float64 | 0.000 |
| `thunder_max_VCTS_2_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_2_ades` | float64 | 0.000 |
| `thunder_max_FG_2_ades` | float64 | 0.000 |
| `thunder_max_TS_3_ades` | float64 | 0.000 |
| `thunder_max_pTS_3_ades` | float64 | 0.000 |
| `thunder_max_VCTS_3_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_3_ades` | float64 | 0.000 |
| `thunder_max_FG_3_ades` | float64 | 0.000 |
| `thunder_max_TS_4_ades` | float64 | 0.000 |
| `thunder_max_pTS_4_ades` | float64 | 0.000 |
| `thunder_max_VCTS_4_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_4_ades` | float64 | 0.000 |
| `thunder_max_FG_4_ades` | float64 | 0.000 |
| `thunder_max_TS_5_ades` | float64 | 0.000 |
| `thunder_max_pTS_5_ades` | float64 | 0.000 |
| `thunder_max_VCTS_5_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_5_ades` | float64 | 0.000 |
| `thunder_max_FG_5_ades` | float64 | 0.000 |
| `thunder_max_TS_6_ades` | float64 | 0.000 |
| `thunder_max_pTS_6_ades` | float64 | 0.000 |
| `thunder_max_VCTS_6_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_6_ades` | float64 | 0.000 |
| `thunder_max_FG_6_ades` | float64 | 0.000 |

Example rows (first 25 of 31 columns):

| flight_id | thunder_max_TS_1_ades | thunder_max_pTS_1_ades | thunder_max_VCTS_1_ades | thunder_max_pVCTS_1_ades | thunder_max_FG_1_ades | thunder_max_TS_2_ades | thunder_max_pTS_2_ades | thunder_max_VCTS_2_ades | thunder_max_pVCTS_2_ades | thunder_max_FG_2_ades | thunder_max_TS_3_ades | thunder_max_pTS_3_ades | thunder_max_VCTS_3_ades | thunder_max_pVCTS_3_ades | thunder_max_FG_3_ades | thunder_max_TS_4_ades | thunder_max_pTS_4_ades | thunder_max_VCTS_4_ades | thunder_max_pVCTS_4_ades | thunder_max_FG_4_ades | thunder_max_TS_5_ades | thunder_max_pTS_5_ades | thunder_max_VCTS_5_ades | thunder_max_pVCTS_5_ades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248763780 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 248760618 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 248753824 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### `E:/Koopmann-Aziz/data/prc2024/lj\thunder\final_submission_set.parquet`
- size: 1.3 MB
- rows: 158,149; columns: 31

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `thunder_max_TS_1_ades` | float64 | 0.000 |
| `thunder_max_pTS_1_ades` | float64 | 0.000 |
| `thunder_max_VCTS_1_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_1_ades` | float64 | 0.000 |
| `thunder_max_FG_1_ades` | float64 | 0.000 |
| `thunder_max_TS_2_ades` | float64 | 0.000 |
| `thunder_max_pTS_2_ades` | float64 | 0.000 |
| `thunder_max_VCTS_2_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_2_ades` | float64 | 0.000 |
| `thunder_max_FG_2_ades` | float64 | 0.000 |
| `thunder_max_TS_3_ades` | float64 | 0.000 |
| `thunder_max_pTS_3_ades` | float64 | 0.000 |
| `thunder_max_VCTS_3_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_3_ades` | float64 | 0.000 |
| `thunder_max_FG_3_ades` | float64 | 0.000 |
| `thunder_max_TS_4_ades` | float64 | 0.000 |
| `thunder_max_pTS_4_ades` | float64 | 0.000 |
| `thunder_max_VCTS_4_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_4_ades` | float64 | 0.000 |
| `thunder_max_FG_4_ades` | float64 | 0.000 |
| `thunder_max_TS_5_ades` | float64 | 0.000 |
| `thunder_max_pTS_5_ades` | float64 | 0.000 |
| `thunder_max_VCTS_5_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_5_ades` | float64 | 0.000 |
| `thunder_max_FG_5_ades` | float64 | 0.000 |
| `thunder_max_TS_6_ades` | float64 | 0.000 |
| `thunder_max_pTS_6_ades` | float64 | 0.000 |
| `thunder_max_VCTS_6_ades` | float64 | 0.000 |
| `thunder_max_pVCTS_6_ades` | float64 | 0.000 |
| `thunder_max_FG_6_ades` | float64 | 0.000 |

Example rows (first 25 of 31 columns):

| flight_id | thunder_max_TS_1_ades | thunder_max_pTS_1_ades | thunder_max_VCTS_1_ades | thunder_max_pVCTS_1_ades | thunder_max_FG_1_ades | thunder_max_TS_2_ades | thunder_max_pTS_2_ades | thunder_max_VCTS_2_ades | thunder_max_pVCTS_2_ades | thunder_max_FG_2_ades | thunder_max_TS_3_ades | thunder_max_pTS_3_ades | thunder_max_VCTS_3_ades | thunder_max_pVCTS_3_ades | thunder_max_FG_3_ades | thunder_max_TS_4_ades | thunder_max_pTS_4_ades | thunder_max_VCTS_4_ades | thunder_max_pVCTS_4_ades | thunder_max_FG_4_ades | thunder_max_TS_5_ades | thunder_max_pTS_5_ades | thunder_max_VCTS_5_ades | thunder_max_pVCTS_5_ades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248753821 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 248753822 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| 248754498 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Folder `E:/Koopmann-Aziz/data/prc2024/lj\weather`
- total: 11.6 MB in 2 files; subfolders: none
- files here: 2; first: `challenge_set.parquet`, last: `final_submission_set.parquet`

### `E:/Koopmann-Aziz/data/prc2024/lj\weather\challenge_set.parquet`
- size: 8.0 MB
- rows: 369,013; columns: 35

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `mslp_adep` | float64 | 0.949 |
| `tmpf_adep` | float64 | 0.001 |
| `drct_adep` | float64 | 0.088 |
| `sknt_adep` | float64 | 0.002 |
| `gust_adep` | float64 | 0.969 |
| `wxcodes_adep` | string | 0.863 |
| `vsby_adep` | float64 | 0.001 |
| `skyl1_adep` | float64 | 0.387 |
| `skyl2_adep` | float64 | 0.707 |
| `skyl3_adep` | float64 | 0.919 |
| `skyl4_adep` | float64 | 0.995 |
| `skyc1_adep` | string | 0.315 |
| `skyc2_adep` | string | 0.705 |
| `skyc3_adep` | string | 0.917 |
| `skyc4_adep` | string | 0.994 |
| `alti_adep` | float64 | 0.003 |
| `relh_adep` | float64 | 0.001 |
| `mslp_ades` | float64 | 0.950 |
| `tmpf_ades` | float64 | 0.001 |
| `drct_ades` | float64 | 0.089 |
| `sknt_ades` | float64 | 0.001 |
| `gust_ades` | float64 | 0.965 |
| `wxcodes_ades` | string | 0.868 |
| `vsby_ades` | float64 | 0.001 |
| `skyl1_ades` | float64 | 0.393 |
| `skyl2_ades` | float64 | 0.711 |
| `skyl3_ades` | float64 | 0.920 |
| `skyl4_ades` | float64 | 0.995 |
| `skyc1_ades` | string | 0.323 |
| `skyc2_ades` | string | 0.708 |
| `skyc3_ades` | string | 0.918 |
| `skyc4_ades` | string | 0.993 |
| `alti_ades` | float64 | 0.004 |
| `relh_ades` | float64 | 0.001 |

Example rows (first 25 of 35 columns):

| flight_id | mslp_adep | tmpf_adep | drct_adep | sknt_adep | gust_adep | wxcodes_adep | vsby_adep | skyl1_adep | skyl2_adep | skyl3_adep | skyl4_adep | skyc1_adep | skyc2_adep | skyc3_adep | skyc4_adep | alti_adep | relh_adep | mslp_ades | tmpf_ades | drct_ades | sknt_ades | gust_ades | wxcodes_ades | vsby_ades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248763780 | nan | 57.2 | 190.0 | 9.0 | nan | <NA> | 6.21 | 2800.0 | nan | nan | nan | FEW | <NA> | <NA> | <NA> | 30.0 | 76.82 | nan | 51.8 | 210.0 | 21.0 | nan | <NA> | 6.21 |
| 248760618 | nan | 53.6 | 240.0 | 7.0 | nan | BCFG | 4.35 | 300.0 | nan | nan | nan | SCT | <NA> | <NA> | <NA> | 30.33 | 93.6 | 1017.4 | 80.0 | 150.0 | 11.0 | 18.0 | <NA> | 10.0 |
| 248753824 | nan | 26.6 | 340.0 | 10.0 | nan | <NA> | 6.21 | 1600.0 | nan | nan | nan | OVC | <NA> | <NA> | <NA> | 30.06 | 86.07 | 1009.5 | 33.0 | 40.0 | 18.0 | 26.0 | -SN | 2.0 |

### `E:/Koopmann-Aziz/data/prc2024/lj\weather\final_submission_set.parquet`
- size: 3.6 MB
- rows: 158,149; columns: 35

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `mslp_adep` | float64 | 0.949 |
| `tmpf_adep` | float64 | 0.001 |
| `drct_adep` | float64 | 0.090 |
| `sknt_adep` | float64 | 0.001 |
| `gust_adep` | float64 | 0.969 |
| `wxcodes_adep` | string | 0.863 |
| `vsby_adep` | float64 | 0.001 |
| `skyl1_adep` | float64 | 0.389 |
| `skyl2_adep` | float64 | 0.707 |
| `skyl3_adep` | float64 | 0.920 |
| `skyl4_adep` | float64 | 0.995 |
| `skyc1_adep` | string | 0.316 |
| `skyc2_adep` | string | 0.705 |
| `skyc3_adep` | string | 0.918 |
| `skyc4_adep` | string | 0.994 |
| `alti_adep` | float64 | 0.003 |
| `relh_adep` | float64 | 0.001 |
| `mslp_ades` | float64 | 0.950 |
| `tmpf_ades` | float64 | 0.001 |
| `drct_ades` | float64 | 0.090 |
| `sknt_ades` | float64 | 0.002 |
| `gust_ades` | float64 | 0.966 |
| `wxcodes_ades` | string | 0.867 |
| `vsby_ades` | float64 | 0.001 |
| `skyl1_ades` | float64 | 0.394 |
| `skyl2_ades` | float64 | 0.712 |
| `skyl3_ades` | float64 | 0.921 |
| `skyl4_ades` | float64 | 0.995 |
| `skyc1_ades` | string | 0.324 |
| `skyc2_ades` | string | 0.709 |
| `skyc3_ades` | string | 0.919 |
| `skyc4_ades` | string | 0.993 |
| `alti_ades` | float64 | 0.004 |
| `relh_ades` | float64 | 0.001 |

Example rows (first 25 of 35 columns):

| flight_id | mslp_adep | tmpf_adep | drct_adep | sknt_adep | gust_adep | wxcodes_adep | vsby_adep | skyl1_adep | skyl2_adep | skyl3_adep | skyl4_adep | skyc1_adep | skyc2_adep | skyc3_adep | skyc4_adep | alti_adep | relh_adep | mslp_ades | tmpf_ades | drct_ades | sknt_ades | gust_ades | wxcodes_ades | vsby_ades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248753821 | nan | 50.0 | 250.0 | 13.0 | nan | <NA> | 6.21 | 1500.0 | 3500.0 | 10000.0 | nan | FEW | SCT | BKN | <NA> | 30.06 | 87.37 | nan | 46.4 | nan | 3.0 | nan | <NA> | 6.21 |
| 248753822 | nan | 51.8 | 170.0 | 5.0 | nan | <NA> | 6.21 | nan | nan | nan | nan | <NA> | <NA> | <NA> | <NA> | 30.24 | 87.47 | 1007.9 | 51.0 | 200.0 | 5.0 | nan | -RA BR | 0.25 |
| 248754498 | 1019.5 | 75.0 | 100.0 | 6.0 | nan | <NA> | 10.0 | 2000.0 | nan | nan | nan | FEW | <NA> | <NA> | <NA> | 30.11 | 81.9 | nan | 55.4 | 190.0 | 11.0 | nan | <NA> | 6.21 |

## Folder `E:/Koopmann-Aziz/data/prc2024/raw` (challenge files and truth)

### `E:/Koopmann-Aziz/data/prc2024/raw\flight_list.csv`
- size: 0.10 GB
- contains the TRUE tow of all flights, test flights included: columns only, no values

| column | dtype (first 1000 rows) |
| --- | --- |
| `flight_id` | int64 |
| `date` | object |
| `callsign` | object |
| `adep` | object |
| `name_adep` | object |
| `country_code_adep` | object |
| `ades` | object |
| `name_ades` | object |
| `country_code_ades` | object |
| `actual_offblock_time` | object |
| `arrival_time` | object |
| `aircraft_type` | object |
| `wtc` | object |
| `airline` | object |
| `flight_duration` | int64 |
| `taxiout_time` | int64 |
| `flown_distance` | int64 |
| `tow` | float64 |
- rows: 527,162

### `E:/Koopmann-Aziz/data/prc2024/raw\partC_ids.csv`
- size: 0.6 MB
- rows: 52,190; columns: 1

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |

Example rows:

| flight_id |
| --- |
| 248763650 |
| 248763651 |
| 248754231 |

### `E:/Koopmann-Aziz/data/prc2024/raw\test.csv`
- size: 19.6 MB
- rows: 105,959; columns: 18
- `tow` present in a TEST file: non-missing values = 0  <- should be 0

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | object | 0.000 |
| `callsign` | object | 0.000 |
| `adep` | object | 0.000 |
| `name_adep` | object | 0.000 |
| `country_code_adep` | object | 0.000 |
| `ades` | object | 0.000 |
| `name_ades` | object | 0.000 |
| `country_code_ades` | object | 0.000 |
| `actual_offblock_time` | object | 0.000 |
| `arrival_time` | object | 0.000 |
| `aircraft_type` | object | 0.000 |
| `wtc` | object | 0.000 |
| `airline` | object | 0.000 |
| `flight_duration` | int64 | 0.000 |
| `taxiout_time` | int64 | 0.000 |
| `flown_distance` | int64 | 0.000 |
| `tow` | float64 | 1.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248753821 | 2022-01-01 | 3b3de0f3ad0ee192513995c02f7bf7cf | LTFJ | Istanbul Sabiha Gokcen | TR | LFLL | Lyon | FR | 2022-01-01T09:44:00Z | 2022-01-01T12:48:33Z | B738 | M | 6351ec1b849adacc0cbb3b1313d8d39b | 170 | 15 | 1122 |
| 248753822 | 2022-01-01 | e06dd03d4a879ca37d9e18c1bd7cad16 | EBBR | Brussels | BE | KJFK | New York JFK | US | 2022-01-01T09:45:00Z | 2022-01-01T17:49:51Z | A333 | H | bdeeef3a675587d530de70a25d7118d2 | 470 | 15 | 3205 |
| 248754498 | 2022-01-01 | 2d3b1c962c78c4ebeef11bcd51b9e94c | KMIA | Miami | US | EGLL | London Heathrow | GB | 2022-01-01T01:52:00Z | 2022-01-01T09:55:16Z | B77W | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 473 | 10 | 3965 |

### `E:/Koopmann-Aziz/data/prc2024/raw\test_final.csv`
- size: 29.3 MB
- rows: 158,149; columns: 18
- `tow` present in a TEST file: non-missing values = 0  <- should be 0

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | object | 0.000 |
| `callsign` | object | 0.000 |
| `adep` | object | 0.000 |
| `name_adep` | object | 0.000 |
| `country_code_adep` | object | 0.000 |
| `ades` | object | 0.000 |
| `name_ades` | object | 0.000 |
| `country_code_ades` | object | 0.000 |
| `actual_offblock_time` | object | 0.000 |
| `arrival_time` | object | 0.000 |
| `aircraft_type` | object | 0.000 |
| `wtc` | object | 0.000 |
| `airline` | object | 0.000 |
| `flight_duration` | int64 | 0.000 |
| `taxiout_time` | int64 | 0.000 |
| `flown_distance` | int64 | 0.000 |
| `tow` | float64 | 1.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248753821 | 2022-01-01 | 3b3de0f3ad0ee192513995c02f7bf7cf | LTFJ | Istanbul Sabiha Gokcen | TR | LFLL | Lyon | FR | 2022-01-01T09:44:00Z | 2022-01-01T12:48:33Z | B738 | M | 6351ec1b849adacc0cbb3b1313d8d39b | 170 | 15 | 1122 |
| 248753822 | 2022-01-01 | e06dd03d4a879ca37d9e18c1bd7cad16 | EBBR | Brussels | BE | KJFK | New York JFK | US | 2022-01-01T09:45:00Z | 2022-01-01T17:49:51Z | A333 | H | bdeeef3a675587d530de70a25d7118d2 | 470 | 15 | 3205 |
| 248754498 | 2022-01-01 | 2d3b1c962c78c4ebeef11bcd51b9e94c | KMIA | Miami | US | EGLL | London Heathrow | GB | 2022-01-01T01:52:00Z | 2022-01-01T09:55:16Z | B77W | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 473 | 10 | 3965 |

### `E:/Koopmann-Aziz/data/prc2024/raw\train.csv`
- size: 70.8 MB
- rows: 369,013; columns: 18
- `tow` (training label): non-missing = 369013

| column | dtype | missing share |
| --- | --- | --- |
| `flight_id` | int64 | 0.000 |
| `date` | object | 0.000 |
| `callsign` | object | 0.000 |
| `adep` | object | 0.000 |
| `name_adep` | object | 0.000 |
| `country_code_adep` | object | 0.000 |
| `ades` | object | 0.000 |
| `name_ades` | object | 0.000 |
| `country_code_ades` | object | 0.000 |
| `actual_offblock_time` | object | 0.000 |
| `arrival_time` | object | 0.000 |
| `aircraft_type` | object | 0.000 |
| `wtc` | object | 0.000 |
| `airline` | object | 0.000 |
| `flight_duration` | int64 | 0.000 |
| `taxiout_time` | int64 | 0.000 |
| `flown_distance` | int64 | 0.000 |
| `tow` | float64 | 0.000 |

Example rows:

| flight_id | date | callsign | adep | name_adep | country_code_adep | ades | name_ades | country_code_ades | actual_offblock_time | arrival_time | aircraft_type | wtc | airline | flight_duration | taxiout_time | flown_distance | tow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 248763780 | 2022-01-01 | 3840d84f25d3f5fcc0a1be3076bb4039 | EGLL | London Heathrow | GB | EICK | Cork | IE | 2022-01-01T13:46:00Z | 2022-01-01T15:04:56Z | A320 | M | a73f82288988b79be490c6322f4c32ed | 61 | 18 | 321 | 54748.0 |
| 248760618 | 2022-01-01 | f6f610e73002b8892a239a81321f7f1d | LEBL | Barcelona | ES | KMIA | Miami | US | 2022-01-01T09:55:00Z | 2022-01-01T19:37:56Z | B772 | H | 5543e4dc327359ffaf5b9c0e6faaf0e1 | 570 | 13 | 4193 | 185441.0 |
| 248753824 | 2022-01-01 | 139670936660762c230ca92556ba842b | ESSA | Stockholm Arlanda | SE | KORD | Chicago O'Hare | US | 2022-01-01T09:39:00Z | 2022-01-01T19:08:13Z | A333 | H | 8be5c854fd664bcb97fb543339f74770 | 554 | 15 | 3770 | 230396.0 |

