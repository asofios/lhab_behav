"""
The following subtests have a complex structure that cannot be dealt with automaitcally, hence a mapping file is
required for
1	Studienteilnahme - Allgemein
3	Kognitives Training
4	Berufliche Tätigkeiten
5	Reisen
"""
from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/04_complete")
out_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data")
lut_file = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/change_mapping_sb.xlsx")
out_path.mkdir(exist_ok=True)

files = list(root_path.glob("*quest*.xlsx"))
df_out = pd.DataFrame()


def j(l):
    return "_".join([str(i) for i in l])


def format_change(file, sheet, usecols=["Nr.", "Question", "Data", "Missing", "Change_Log"],
                  var_cols=["domain", "Nr.", "Question"]):
    info = {
        "02_PrivatesUmfeld": (24, 31),
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


def excel_letter_to_num(l):
    from string import ascii_lowercase
    letter_lut = {letter: index for index, letter in enumerate(ascii_lowercase, start=0)}
    return letter_lut[l.lower()]


def lookup_change(file, lut, sheet="01_Veränderungsfragebogen", row_offset=-2):
    df_out = pd.DataFrame()
    lut = lut.dropna(axis="index", how="all")
    df_in = pd.read_excel(file, sheet_name=sheet)

    for _, row in lut.iterrows():
        name, col_idx, row_idx = row["variable_short_engl"], excel_letter_to_num(row["value_col"]), \
                                 int(row["value_row"]) + row_offset
        df_out = df_out.append(pd.DataFrame({"variable": name, "value": df_in.iloc[row_idx, col_idx]}, index=[0]))
    df_out = df_out.set_index("variable").T

    return df_out


dfs = []
lut = pd.read_excel(lut_file)
sheet = "01_Veränderungsfragebogen"
for f in files:
    id = pd.read_excel(f, sheet_name="ID", usecols="A:B", names=["variable", "value"], header=None)
    id.dropna(axis="index", how="all", inplace=True)
    id = id.set_index("variable").T
    id["file"] = f

    df1 = lookup_change(f, lut)
    df2 = format_change(f, sheet)
    df = pd.concat((id, df1, df2), axis=1)
    dfs.append(df)

    df_out = pd.concat(dfs, axis=0, sort=False)
    df_out.to_excel(out_path / f"00_aggregated_{sheet}.xlsx", index=False)
