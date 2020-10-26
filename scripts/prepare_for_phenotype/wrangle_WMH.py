import pandas as pd
from pathlib import Path


def wrangle_ubo(file, suffix):
    df = pd.read_excel(file)
    rep = {c: f"{c}{suffix}" for c in df.drop(columns=["ID"]).columns}
    df.rename(columns=rep, inplace=True)
    df.insert(0, "session_id", df.ID.str[9:])
    df.insert(0, "subject_id", df.ID.str[:9])
    df.drop(columns=["ID"], inplace=True)

    df_metadata = pd.DataFrame([], columns=["subject_id", "session_id", "missing", "missing_text"])
    df_metadata["subject_id"] = df["subject_id"]
    df_metadata["session_id"] = df["session_id"]
    df_metadata["missing"] = 0

    return df, df_metadata


in_dir = Path("/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation/10_Neuroimaging/01_wrangling/01_wmh")
out_dir = Path(
    "/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation/10_Neuroimaging/05_ready_2_convert/01_wmh")
out_dir.mkdir(exist_ok=True, parents=True)

file = in_dir / "WMH_UBO_spreadsheet_2D_fulldata_Tp6.xlsx"
df, df_metadata = wrangle_ubo(file, "_2D")
df.to_excel(out_dir / "lhab_wmh_ubo_2D_data.xlsx", index=False)
df_metadata.to_excel(out_dir / "lhab_wmh_ubo_2D_metadata.xlsx", index=False)

file = in_dir / "WMH_UBO_spreadsheet_3D_all_Tp5.xlsx"
df, df_metadata = wrangle_ubo(file, "_3D")
df.to_excel(out_dir / "lhab_wmh_ubo_3D_data.xlsx", index=False)
df_metadata.to_excel(out_dir / "lhab_wmh_ubo_3D_metadata.xlsx", index=False)
