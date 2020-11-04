from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/04_complete")
out_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data")
out_path.mkdir(exist_ok=True)

files = list(root_path.glob("*quest*.xlsx"))
df_out = pd.DataFrame()


def excel_letter_to_num(l):
    from string import ascii_lowercase
    letter_lut = {letter: index for index, letter in enumerate(ascii_lowercase, start=0)}
    return letter_lut[l.lower()]


def extract_data_via_mapping(file, lut_newfile, lut_oldfile, sheet, row_offset=-2):
    df_out = pd.DataFrame()
    df_in = pd.read_excel(file, sheet_name=sheet)

    if "oldfile" in str(file):
        lut = lut_oldfile.dropna(axis="index", how="all")
    else:
        lut = lut_newfile.dropna(axis="index", how="all")

    for _, row in lut.iterrows():
        name, col_idx, row_idx = row["variable_short_engl"], excel_letter_to_num(row["value_col"]), \
                                 int(row["value_row"]) + row_offset
        df_out = df_out.append(pd.DataFrame({"variable": name, "value": df_in.iloc[row_idx, col_idx]}, index=[0]))
    df_out = df_out.set_index("variable").T

    return df_out


sheet = "04_Medikationsanamnese"

lut_file_new = Path(
    f"/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/mapping/mapping_{sheet}.xlsx")
lut_newfile = pd.read_excel(lut_file_new)
lut_file_old = Path(
    f"/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/mapping/mapping_{sheet}_oldfile.xlsx")
lut_oldfile = pd.read_excel(lut_file_old)

dfs = []
for f in files:
    print(f)
    id = pd.read_excel(f, sheet_name="ID", usecols="A:B", names=["variable", "value"], header=None)
    id.dropna(axis="index", how="all", inplace=True)
    id = id.set_index("variable").T
    id["file"] = f

    df1 = extract_data_via_mapping(f, lut_newfile, lut_oldfile, sheet=sheet)
    df = pd.concat((id, df1), axis=1)
    dfs.append(df)

df_out = pd.concat(dfs, axis=0, sort=False)
df_out.to_excel(out_path / f"00_aggregated_{sheet}.xlsx", index=False)
