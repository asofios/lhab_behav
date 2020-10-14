from pathlib import Path
import pandas as pd
from warnings import warn

"""
renames "V1 - Probandenname": "vp_code"
makes vp_codes lower case
removes "_tp6" from vp_codes
"""
in_file = "/Volumes/lhab_public/03_Data/03_data_tests_computer/01_WTS/aggregated_data/tp6/00_aggregated_WTS_orig.xlsx"
out_file = "/Volumes/lhab_public/03_Data/03_data_tests_computer/01_WTS/aggregated_data/tp6/00_aggregated_WTS_clean.xlsx"

df = pd.read_excel(in_file)

df.rename(columns={"V1 - Probandenname": "vp_code"}, inplace=True)

df.vp_code = df.vp_code.str.lower()
df.vp_code = df.vp_code.str.replace("_tp6", "")

if not (df.vp_code.str.len() == 4).all():
    raise Exception("Some vp codes are not of len 4")

# fixme
# df.replace({"?":pd.np.nan}, inplace=True)
df.to_excel(out_file, index=False)
