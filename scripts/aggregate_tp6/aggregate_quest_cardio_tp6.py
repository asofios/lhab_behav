from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/04_complete")
out_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data")
out_path.mkdir(exist_ok=True)

files = sorted(root_path.glob("*quest*.xlsx"))
df_out = pd.DataFrame()


def excel_letter_to_num(l):
    from string import ascii_lowercase
    letter_lut = {letter: index for index, letter in enumerate(ascii_lowercase, start=0)}
    return letter_lut[l.lower()]


def extract_data_via_mapping(file, lut27, lut29, sheet="01_Veränderungsfragebogen", row_offset=-2):
    df_out = pd.DataFrame()

    # encoding breaks load code
    sheet_ = 4 if sheet == "03_Kardivaskulär" else sheet

    df_in = pd.read_excel(file, sheet_name=sheet_)

    # cardio comes in different formats 29 and 27 lines
    # (this is because some files dont have the Keine der genannten Behandlungen cells

    if len(df_in) == 29:
        lut = lut29.dropna(axis="index", how="all")
    elif len(df_in) == 27:
        lut = lut27.dropna(axis="index", how="all")
    else:
        raise Exception(file, len(df_in))

    for _, row in lut.iterrows():
        name, col_idx, row_idx = row["variable_short_engl"], excel_letter_to_num(row["value_col"]), \
                                 int(row["value_row"]) + row_offset
        df_out = df_out.append(pd.DataFrame({"variable": name, "value": df_in.iloc[row_idx, col_idx]}, index=[0]))
    df_out = df_out.set_index("variable").T

    return df_out


sheet = "03_Kardivaskulär"

lut_file = Path(
    f"/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/mapping/mapping_{sheet}_27.xlsx")
lut_27 = pd.read_excel(lut_file)
lut_file = Path(
    f"/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/mapping/mapping_{sheet}_29.xlsx")
lut_29 = pd.read_excel(lut_file)

dfs = []
for f in files:
    id = pd.read_excel(f, sheet_name="ID", usecols="A:B", names=["variable", "value"], header=None)
    id.dropna(axis="index", how="all", inplace=True)
    id = id.set_index("variable").T
    id["file"] = f

    df1 = extract_data_via_mapping(f, lut_27, lut_29, sheet=sheet)
    df = pd.concat((id, df1), axis=1)
    dfs.append(df)

df_out = pd.concat(dfs, axis=0, sort=False)
df_out.to_excel(out_path / f"00_aggregated_{sheet}.xlsx", index=False)
