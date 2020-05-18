from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/06_DataConversion/00_Data_tp6/psychometric_data")
out_path = Path("/Volumes/lhab_public/03_Data/06_DataConversion/00_Data_tp6/aggregated_psychometric_data")
out_path.mkdir(exist_ok=True)

files = list(root_path.glob("lhab*.xlsx"))

df_pp_out = pd.DataFrame()
df_tap_out = pd.DataFrame()
df_wts_out = pd.DataFrame()


def format_test_sheet(df, fill_colls=['Domain', 'Test'], score_col="Score_Name",
                      var_cols=['Domain', 'Test', 'Score_Name']):
    df.dropna(axis="index", how="all", inplace=True)

    df[fill_colls] = df[fill_colls].fillna(method="ffill")
    df[score_col] = df[score_col].fillna("score")

    def j(l):
        return "_".join([str(i) for i in l])

    df["variable"] = df[var_cols].apply(j, axis=1)
    df.drop(columns=var_cols, inplace=True)
    df = df.melt(id_vars="variable", var_name="v")

    df["variable"] = df["variable"] + "_" + df["v"]
    df.drop(columns=['v'], inplace=True)
    df = df.sort_values(by="variable").dropna(axis="index", how="all", )
    df = df.set_index("variable").T
    return df


for f in files:
    # 1. General
    id = pd.read_excel(f, sheet_name="General", usecols="A:B", names=["variable", "value"], header=None)
    id = id.set_index("variable").T

    # 2. Paper pencil
    pp = pd.read_excel(f, sheet_name="PaperPencil")
    pp = format_test_sheet(pp)
    pp["file"] = f
    df_pp_ = pd.concat((id, pp), axis=1, sort=False)
    df_pp_out = df_pp_out.append(df_pp_, sort=False)

    # 3. TAP
    tap = pd.read_excel(f, sheet_name="TAP")
    tap = format_test_sheet(tap, fill_colls=['Test'], score_col="Score_Name", var_cols=['Test', 'Score_Name'])
    tap["file"] = f
    df_tap_ = pd.concat((id, tap), axis=1, sort=False)
    df_tap_out = df_tap_out.append(df_tap_, sort=False)

    # 4. WTS
    wts = pd.read_excel(f, sheet_name="WTS")
    wts = format_test_sheet(wts, fill_colls=['Test'], score_col="Score_Name", var_cols=['Test', 'Score_Name'])
    wts["file"] = f
    df_wts_ = pd.concat((id, wts), axis=1, sort=False)
    df_wts_out = df_wts_out.append(df_wts_, sort=False)

df_pp_out.reset_index(drop=True, inplace=True)
df_pp_out.to_excel(out_path / "00_aggregated_PP.xlsx", index=False)

df_tap_out.reset_index(drop=True, inplace=True)
df_tap_out.to_excel(out_path / "00_aggregated_TAP.xlsx", index=False)

df_wts_out.reset_index(drop=True, inplace=True)
df_wts_out.to_excel(out_path / "00_aggregated_WTS.xlsx", index=False)
