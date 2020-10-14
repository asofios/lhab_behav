from pathlib import Path
import pandas as pd
from warnings import warn

"""
renames "SUBJECT": "vp_code"
makes vp_codes lower case
removes "_tp6" from vp_codes
"""
in_file = "/Volumes/lhab_public/03_Data/03_data_tests_computer/02_TAP/aggregated_data/tp6/00_aggregated_TAP_orig.xlsx"
out_file = "/Volumes/lhab_public/03_Data/03_data_tests_computer/02_TAP/aggregated_data/tp6/00_aggregated_TAP_clean" \
           ".xlsx"

df = pd.read_excel(in_file)

df.rename(columns={"SUBJECT": "vp_code"}, inplace=True)

df.vp_code = df.vp_code.str.lower()
df.vp_code = df.vp_code.str.replace("_tp6", "")

error_index = (df.vp_code.str.len() != 4)
if error_index.any():
    raise Exception(f"Some vp codes are not of len 4 {df.loc[error_index]}")

# fixme
# df.replace({"?":pd.np.nan}, inplace=True)
df.to_excel(out_file, index=False)
