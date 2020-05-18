from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/Data/tp6/04_complete")
out_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/Data/tp6//aggregated_data")
out_path.mkdir(exist_ok=True)

sheets = ["05_Lebenszufriedenheit", "06_HADS", "07_PANAS", "08_PRMQ", "09_TICS", "11_Epworth_Sleepiness_Scale"]
files = list(root_path.glob("*quest*.xlsx"))
df_out = pd.DataFrame()


def j(l):
    return "_".join([str(i) for i in l])


def format_hads_style(file, sheet, usecols=["Nr.", "Question", "Data", "Missing", "Change_Log"],
                      var_cols=["Nr.", "Question"]):
    """
    HADS style sheets
    header in line 2 (1-based)
    """
    df = pd.read_excel(file, sheet_name=sheet, header=1, usecols=usecols)
    df.dropna(axis="index", how="all", inplace=True)

    df["variable"] = df[var_cols].apply(j, axis=1)
    df.drop(columns=var_cols, inplace=True)
    df = df.melt(id_vars="variable", var_name="v")

    df["variable"] = df["variable"] + "_" + df["v"]
    df.drop(columns=['v'], inplace=True)
    df = df.sort_values(by="variable").dropna(axis="index", how="all", )
    df = df.set_index("variable").T
    return df


dfs = {}
for sheet in sheets:
    dfs[sheet] = []

for f in files:
    id = pd.read_excel(f, sheet_name="ID", usecols="A:B", names=["variable", "value"], header=None)
    id.dropna(axis="index", how="all", inplace=True)
    id = id.set_index("variable").T
    id["file"] = f

    for sheet in sheets:
        df = pd.concat((id, format_hads_style(f, sheet)), axis=1, sort=False)
        dfs[sheet].append(df)

for sheet in sheets:
    df_out = pd.concat(dfs[sheet], axis=0, sort=False)
    df_out.to_excel(out_path / f"00_aggregated_{sheet}.xlsx", index=False)
