from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/06_DataConversion/00_Data_tp6/psychometric_data")
out_path = Path("/Volumes/lhab_public/03_Data/06_DataConversion/00_Data_tp6/aggregated_psychometric_data")
out_path.mkdir(exist_ok=True)

files = list(root_path.glob("lhab*.xlsx"))
df_out = pd.DataFrame()
for f in files:
    df_ = pd.read_excel(f)
    subject = df_.columns[1]
    mmse = df_.iloc[5, 1]
    if mmse > 30:
        warn(f"{subject} {mmse}")
    if mmse < 10:
        warn(f"{subject} {mmse}")

    df_out_ = pd.DataFrame({"subject": subject,
                            "mmse": mmse,
                            "file": str(f)
                            }, index=[0]
                           )
    df_out = df_out.append(df_out_)
df_out.reset_index(drop=True, inplace=True)
df_out.to_excel(out_path / "00_aggregated_mmse.xlsx", index=False)
