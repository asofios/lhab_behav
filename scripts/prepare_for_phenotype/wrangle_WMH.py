import pandas as pd
from pathlib import Path


def wrangle_in_files(file, suffix, ubo_subject_ids=False):
    if file.suffix == ".xlsx":
        df = pd.read_excel(file)
    elif file.suffix == ".tsv":
        df = pd.read_csv(file, sep="\t")
    else:
        raise Exception

    if ubo_subject_ids:
        df.insert(0, "session_id", df.ID.str[9:])
        df.insert(0, "subject_id", df.ID.str[:9])
        df.drop(columns=["ID"], inplace=True)
    else:
        df.rename(columns={"subject": "subject_id", "session": "session_id"}, inplace=True)

    rep = {c: f"{c}{suffix}" for c in df.drop(columns=["subject_id", "session_id"]).columns}
    df.rename(columns=rep, inplace=True)

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
df, df_metadata = wrangle_in_files(file, suffix="_ubo2d_orig", ubo_subject_ids=True)
df.to_excel(out_dir / "lhab_wmh_ubo2d_orig_data.xlsx", index=False)
df_metadata.to_excel(out_dir / "lhab_wmh_ubo2d_orig_metadata.xlsx", index=False)

file = in_dir / "WMH_UBO_spreadsheet_3D_all_Tp5.xlsx"
df, df_metadata = wrangle_in_files(file, suffix="_ubo3d_orig", ubo_subject_ids=True)
df.to_excel(out_dir / "lhab_wmh_ubo3d_orig_data.xlsx", index=False)
df_metadata.to_excel(out_dir / "lhab_wmh_ubo3d_orig_metadata.xlsx", index=False)

atlases = ["JHUlabels", "JHUtracts", "hoCort", "hoSubcort", "oxThal"]
suffix_lut = {"lacunes": "_lacunes_parcMNI_{atlas}", "wmh": "_wmh_ubo2d_parcMNI_{atlas}"}

for domain in ["wmh", "lacunes"]:
    for atlas in atlases:
        file = in_dir / "MNI/stats" / domain / f"{domain}_{atlas}_volume.tsv"
        suffix = suffix_lut[domain].format(atlas=atlas)
        df, df_metadata = wrangle_in_files(file, suffix=suffix, ubo_subject_ids=False)
        df.to_excel(out_dir / f"lhab{suffix}_data.xlsx", index=False)
        df_metadata.to_excel(out_dir / f"lhab{suffix}_metadata.xlsx", index=False)
