# This script takes tap raw files and cleans them up and tries to estimate the session label
# it's a first step to clean the tap data. output of this script has to be checked manually
# output: 1 file with all subjects where session label has been estimated
#        1 file with all subjects where this has not been possible

import pandas as pd
import numpy as np
import os
from glob import glob


def merge_dfs(search_str):
    df = pd.DataFrame([])
    g = glob(search_str)
    for file in g:
        # print(file)
        try:
            df_ = pd.read_csv(file, sep=";")
            df_["file"] = os.path.basename(file)
            df = pd.concat((df, df_))
        except pd.errors.EmptyDataError:
            print("Empty file:", file)
    return df


def convert_dates(df):
    # convert 'BIRTH' and all columns ending with '_DATE' to datetime
    date_cols = df.filter(like='_DATE').columns.tolist()
    date_cols.append("BIRTH")
    print(date_cols)

    for c in date_cols:
        df[c] = pd.to_datetime(df[c])

    return df


def tronic_id(df):
    # tronic subjects with 01_XX_2 id, where only 01_XX is important
    ind = df.SUBJECT.str.split("_").str.len() > 2
    df["tronic_session"] = False
    df.loc[ind, "tronic_session"] = True
    df.loc[ind, "SUBJECT"] = df[ind].SUBJECT.str.split("_").str[:2].str.join("_")

    #  rename tronic ids
    tr = pd.read_excel("/Users/franzliem/Desktop/lhab_tronic.xlsx")
    rename_dict = tr.set_index("tronic").to_dict()["lhab"]

    df.SUBJECT.replace(rename_dict, inplace=True)
    return df


def id_cleaning(df):
    #############
    # ID cleaning
    df = tronic_id(df)

    # hard coded typo fixes:
    df.replace({"SUBJECT": {
        "b3ncv": "b3nv"}}, inplace=True)

    # fixme
    # drop xfx1_t5
    ind = ~(df.SUBJECT == "xfx1_t5")
    df = df[ind]

    # remove test subjects
    ind = ~(df["SUBJECT"].str.lower().str.contains("test"))
    df = df[ind].copy()

    # remove time stubs of type abcd_t3
    ind = df.SUBJECT.str.lower().str.contains('\w{4}_t.', regex=True)
    df.loc[ind, "SUBJECT"] = df.loc[ind, "SUBJECT"].str.split("_").str[0]

    # remove time stubs of type abcd_2
    ind = df.SUBJECT.str.lower().str.contains('\w{4}_2', regex=True)
    df.loc[ind, "SUBJECT"] = df.loc[ind, "SUBJECT"].str.split("_").str[0]

    # drop 'neuer_Proband'
    ind = ~(df.SUBJECT == "neuer_Proband")
    df = df[ind]

    return df


# In[6]:


def date_correction(df):
    # correct time offset for dates < 2010
    date_col = df.filter(like="_DATE").columns.tolist()[0]
    ind = df[date_col] < pd.to_datetime("2010-01-01")
    time_offset = pd.Timedelta('4377 days')
    df["tap_orig_dat"] = df[date_col]
    df.loc[ind, date_col] = df.loc[ind, date_col] + time_offset

    # add cont session for merge
    df.sort_values(["SUBJECT", date_col], inplace=True)

    return df


def drop_dups(df):
    # if subject has been run twice at a date, keep last
    date_col = df.filter(like="_DATE").columns.tolist()[0]
    df.drop_duplicates(["SUBJECT", date_col], keep="last", inplace=True)
    return df


def get_session_labels(df):
    # prepare real session dates
    testdates = pd.read_excel(
        "/Volumes/lhab_public/03_Data/03_ComputerTests/02_TAP/10_TAP_export_Nov17/testdates_TAP.xlsx")
    valid_subjects = testdates.subject.values

    testdates = pd.wide_to_long(testdates, ["date_tp"], i="subject", j="session")
    testdates.reset_index(inplace=True)
    testdates["session"] = "tp" + testdates["session"]
    testdates.sort_values(["subject", "session"], inplace=True)
    testdates.rename({"subject": "SUBJECT"}, axis=1, inplace=True)

    #  prepare TAP dates
    date_col = df.filter(like="_DATE").columns.tolist()[0]
    df.sort_values(["SUBJECT", date_col], inplace=True)
    tap_dates = df[["SUBJECT", date_col]].copy()

    # get session mapping
    sessions = pd.merge(testdates, tap_dates, on="SUBJECT", how="outer")
    sessions["delta"] = (sessions[date_col] - sessions["date_tp"]).abs()
    sessions = sessions[sessions.delta < pd.Timedelta("5 days")]
    if len(sessions[sessions[["SUBJECT", "session"]].duplicated()]) != 0:
        raise Exception("sessions not unique")
    sessions.drop("delta", axis=1, inplace=True)

    # merge
    df = pd.merge(df, sessions, on=["SUBJECT", date_col], how="outer")

    # fill in tronic sessions as tp4
    df.loc[df.tronic_session, "session"] = "tp4"
    df.sort_values(["SUBJECT", "session"], inplace=True)

    # remove subjects not in testdates
    df = df[df.SUBJECT.isin(valid_subjects)]

    # hardcoded fix date
    ind = (df.SUBJECT == "xfx1") & (df["tap_orig_dat"] == "2004-08-08")
    df.loc[ind, "tap_orig_dat"] = pd.to_datetime("2004-08-07")

    # add hardcoded mapping for cases where automitic merge is not possible (bc. of random date offset)
    hardcoded = pd.read_excel(
        "/Volumes/lhab_public/03_Data/03_ComputerTests/02_TAP/10_TAP_export_Nov17/hard_coded_sessions.xlsx")
    hardcoded.sort_values(["subject", "tap_orig_dat"], inplace=True)
    hardcoded = hardcoded[["subject", "hard_coded_session", "tap_orig_dat"]]
    hardcoded.rename(columns={"subject": "SUBJECT"}, inplace=True)

    df = pd.merge(df, hardcoded, on=["SUBJECT", "tap_orig_dat"], how="left")
    ind = df.session.isnull()
    df.loc[ind, "session"] = df.loc[ind, "hard_coded_session"]
    return df


def format_output(df):
    df.rename(columns=str.lower, inplace=True)

    df.drop(["tronic_session", "age", "hard_coded_session"], axis=1, inplace=True)

    # sort columns
    date_col = df.filter(like="_date").columns.tolist()[0]
    date_col
    time_col = df.filter(like="_time").columns.tolist()[0]
    time_col
    front_cols = ["subject", "session", "date_tp", date_col, "tap_orig_dat", time_col, "birth"]
    all_cols = df.columns
    back_cols = [x for x in all_cols if x not in front_cols]
    c = front_cols + back_cols
    df = df[c]

    return df


def prepare_TAP_data(search_str):
    df = merge_dfs(search_str)
    df_orig = df.copy()

    df = convert_dates(df)

    df = id_cleaning(df)

    df = date_correction(df)

    df = drop_dups(df)

    # remove young subjects
    df["age"] = (pd.datetime.now() - df.BIRTH).dt.days / 365
    df = df[df.age > 60]

    df = get_session_labels(df)

    df = format_output(df)

    check_for_duplicates(df)

    return df, df_orig


def check_for_duplicates(df):
    ind = df.duplicated(["subject", "session"])
    if ind.sum() > 0:
        print(df[ind])
        raise Exception("Duplicates")


def strip_df(df):
    drop_cols = ['date_tp', 'tap_orig_dat', 'birth', 'examin', 'number', 'sex', 'school', 'file']
    all_cols = df.columns
    c = [x for x in all_cols if x not in drop_cols]
    df = df[c]

    # prepend "tap_"
    c = df.columns.tolist()
    c.remove("subject")
    c.remove("session")

    ren = {}
    for co in c:
        ren[co] = "tap_" + co
    df.rename(columns=ren, inplace=True)
    return df


# merge files
root_path = "/Volumes/lhab_public/03_Data/03_ComputerTests/02_TAP/10_TAP_export_Nov17/TAP_Export_Nov2017"
out_root_path = "/Volumes/lhab_public/03_Data/03_ComputerTests/02_TAP/10_TAP_export_Nov17/TAP_cleaned_DONTEDIT"
orig_dump_out_root_path = "/Volumes/lhab_public/03_Data/03_ComputerTests/02_TAP/10_TAP_export_Nov17/TAP_orig_dump"

test_names = ["al", "da", "gonogo", "wm3"]

if not os.path.isdir(out_root_path):
    os.makedirs(out_root_path)

if not os.path.isdir(orig_dump_out_root_path):
    os.makedirs(orig_dump_out_root_path)

d = {}
for test_name in test_names:
    f = "*/export_nov2017_{}_*_*.csv".format(test_name)
    search_str = os.path.join(root_path, f)

    df, df_orig = prepare_TAP_data(search_str)

    # output
    out_file = os.path.join(orig_dump_out_root_path, "TAP_{}_orig.tsv".format(test_name))
    df_orig.to_csv(out_file, sep="\t", index=False)

    out_file = os.path.join(out_root_path, "TAP_{}.tsv".format(test_name))
    df.to_csv(out_file, sep="\t", index=False)

    # prepare for wide df
    df = strip_df(df)
    d[test_name] = df.copy()

dd = pd.merge(d["al"], d["da"], on=["subject", "session"], how="outer")
dd = pd.merge(dd, d["gonogo"], on=["subject", "session"], how="outer")
dd = pd.merge(dd, d["wm3"], on=["subject", "session"], how="outer")
out_file = os.path.join(out_root_path, "00_TAP.tsv".format(test_name))
dd.to_csv(out_file, sep="\t", index=False)

# meta data
dd["n_subtests_avail"] = (~dd[["tap_al_date", "tap_da3_date", "tap_go1_date", "tap_wm3_date"]].isnull()).sum(1)
out_file = os.path.join(out_root_path, "00_TAP_subtest_count.tsv".format(test_name))
dd[["subject", "session", "n_subtests_avail"]].to_csv(out_file, sep="\t", index=False)

# session count
n = dd.groupby("subject").count()[["session"]]
n.rename(columns={"session": "n_sessions"}, inplace=True)
n.reset_index(inplace=True)
out_file = os.path.join(out_root_path, "00_TAP_session_count.tsv".format(test_name))
n.to_csv(out_file, sep="\t", index=False)
