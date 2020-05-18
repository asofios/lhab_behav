from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/Data/tp6/04_complete")
out_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/Data/tp6//aggregated_data")
out_path.mkdir(exist_ok=True)

files = list(root_path.glob("*quest*.xlsx"))
df_out = pd.DataFrame()


def j(l):
    return "_".join([str(i) for i in l])


def format_change(file, sheet, usecols=["Nr.", "Question", "Data", "Missing", "Change_Log"],
                  var_cols=["domain", "Nr.", "Question"]):
    info = {
        "02_PrivatesUmfeld": (24, 31),
        # "03_KognitivesTraining": (34, 43),
        "06_Freizeitbeschäftigungen_01_Sport": (66, 75),
        "06_Freizeitbeschäftigungen_02_HandwerklicheAktivitäten": (78, 84),
        "06_Freizeitbeschäftigungen_03_Spiele": (87, 94),
        "06_Freizeitbeschäftigungen_05_TV": (97, 103),
        "06_Freizeitbeschäftigungen_06_KulturelleAktivitäten": (106, 122),
        "06_Freizeitbeschäftigungen_07_SozialeAktivitäten": (125, 138),
        "06_Freizeitbeschäftigungen_08_Wissenserwerb	": (141, 151),
        "06_Freizeitbeschäftigungen_09_Diverses": (154, 160),
    }
    df = pd.DataFrame()

    offset = 5
    df_in = pd.read_excel(file, sheet_name=sheet, header=offset, usecols=usecols)

    for domain, (start, stop) in info.items():
        start -= (offset + 2)
        stop -= (offset + 1)
        df_selected = df_in.iloc[start:stop].copy()
        df_selected["domain"] = domain
        df = df.append(df_selected)

    df["variable"] = df[var_cols].apply(j, axis=1)
    df.drop(columns=var_cols, inplace=True)
    df = df.melt(id_vars="variable", var_name="v")

    df["variable"] = df["variable"] + "_" + df["v"]
    df.drop(columns=['v'], inplace=True)
    df = df.sort_values(by="variable").dropna(axis="index", how="all", )
    df = df.set_index("variable").T
    return df


dfs = []
sheet = "01_Veränderungsfragebogen"
for f in files:
    id = pd.read_excel(f, sheet_name="ID", usecols="A:B", names=["variable", "value"], header=None)
    id.dropna(axis="index", how="all", inplace=True)
    id = id.set_index("variable").T
    id["file"] = f

    df = pd.concat((id, format_change(f, sheet)), axis=1, sort=False)
    dfs.append(df)

    df_out = pd.concat(dfs, axis=0, sort=False)
    df_out.to_excel(out_path / f"00_aggregated_{sheet}.xlsx", index=False)
