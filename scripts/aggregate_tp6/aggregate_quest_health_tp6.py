from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/Data/tp6/04_complete")
files = list(root_path.glob("*quest*.xlsx"))
df_out = pd.DataFrame()


def read_sheet(filename, sheet_name, col_names=None, header=None):
    extra_args = {}
    if col_names:
        extra_args["names"] = col_names
    else:
        extra_args["header"] = header

    df_sheet = pd.read_excel(filename, sheet_name=sheet_name, **extra_args)
    df_sheet = df_sheet.loc[:, ~(df_sheet.columns == "_")]

    return df_sheet


def read_subect(filename):
    df_id = read_sheet(filename, "ID", header=0)
    subject = df_id.loc[df_id["Unnamed: 0"] == "VP-Nr."]["Unnamed: 1"][0]

    df = read_sheet(filename, "02_Gesundheitszustand", header=5)
    df_ = pd.DataFrame({"domain": ["info"], "variable": ["filename"], "value": [filename]}, index=[0])

    def app(df_, i):
        return df_.append(pd.DataFrame({"domain": i[0], "variable": i[1].values, "value": i[2].values},
                                       index=range(len(i[1]))))

    # Zeile 8 / Spalte A(Variable)/C(Wert)
    ind1 = 8 - 7
    ind2 = ind1 + 1
    df_ = app(df_, ("sf12", df.iloc[ind1:ind2]["Nr."], df.iloc[ind1:ind2]["Data"]))

    # Zeilen 13-20 / Spalten B(Variable)/C(Wert)
    ind1 = 13 - 7
    ind2 = ind1 + 20 - 13 + 1
    df_ = app(df_, ("sf12_tatigkeit", df.iloc[ind1:ind2]["Question"], df.iloc[ind1:ind2]["Data"]))

    # Zeilen 23-24 / Spalten B(Variable)/C(Wert)
    ind1 = 23 - 7
    ind2 = ind1 + 24 - 23 + 1
    df_ = app(df_, ("sf12_korperlich", df.iloc[ind1:ind2]["Question"], df.iloc[ind1:ind2]["Data"]))

    # Zeilen 27-28 / Spalten B(Variable)/C(Wert)
    ind1 = 27 - 7
    ind2 = ind1 + 24 - 23 + 1
    df_ = app(df_, ("sf12_emo", df.iloc[ind1:ind2]["Question"], df.iloc[ind1:ind2]["Data"]))

    # Zeile 30 / Spalte A(Variable)/C(Wert)
    ind1 = 30 - 7
    ind2 = ind1 + 1
    df_ = app(df_, ("sf12_schmerz", df.iloc[ind1:ind2]["Nr."], df.iloc[ind1:ind2]["Data"]))

    # Zeilen 33-35 / Spalten B(Variable)/C(Wert)
    ind1 = 33 - 7
    ind2 = ind1 + 35 - 33 + 1
    df_ = app(df_, ("sf12_ener", df.iloc[ind1:ind2]["Question"], df.iloc[ind1:ind2]["Data"]))

    # Zeile 37 / Spalte A(Variable)/C(Wert)
    ind1 = 37 - 7
    ind2 = ind1 + 1
    df_ = app(df_, ("sf12_kontakte", df.iloc[ind1:ind2]["Nr."], df.iloc[ind1:ind2]["Data"]))

    #
    # Unfall
    # Zeile 39 / Spalte A(Variable)/C(Wert)
    ind1 = 39 - 7
    ind2 = ind1 + 1
    df_ = app(df_, ("sf12_unfall", df.iloc[ind1:ind2]["Nr."], df.iloc[ind1:ind2]["Data"]))
    #
    # Symptome
    # Zeilen 54-76 / Spalten B(Variable)/C(Wert)
    ind1 = 54 - 7
    ind2 = ind1 + 76 - 54 + 1
    df_ = app(df_, ("sf12_sympt", df.iloc[ind1:ind2]["Question"], df.iloc[ind1:ind2]["Data"]))

    df_.insert(0, "subject", subject)
    df_.reset_index(drop=True, inplace=True)
    return df_


df = pd.DataFrame([])

for f in files:
    print(f)
    df_subject = read_subect(f)
    df = df.append(df_subject)

df.to_excel(root_path / "00_aggregated_health_long.xlsx")

df.set_index("subject", drop=True, inplace=True)
df["variable"] = df["domain"] + "_" + df["variable"]
df.drop(columns=["domain"], inplace=True)
df.pivot(columns="variable").to_excel(root_path / "00_aggregated_health_wide.xlsx")
