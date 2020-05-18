from pathlib import Path
import pandas as pd
from warnings import warn

root_path = Path("/Volumes/lhab_public/03_Data/03_data_tests_computer/01_WTS/01_rawdata/tp6")
out_path = Path("/Volumes/lhab_public/03_Data/03_data_tests_computer/01_WTS/aggregated_data/tp6")
out_path.mkdir(exist_ok=True, parents=True)

files = list(root_path.glob("*/*.csv"))
dfs = []
for f in files:
    df_ = pd.read_csv(f, sep=";", encoding="latin-1")
    df_["file"] = f
    dfs.append(df_)

df = pd.concat(dfs, sort=False)
df.reset_index(drop=True, inplace=True)
df.to_excel(out_path / "00_aggregated_WTS.xlsx", index=False)
