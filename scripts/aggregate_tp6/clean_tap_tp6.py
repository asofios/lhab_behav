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

sel_cols = ['SUBJECT', 'AL_COR0', 'AL_OMI0', 'AL_LAP0', 'AL_ANT0', 'AL_MEA0',
            'AL_MDN0', 'AL_STD0', 'AL_COR1', 'AL_OMI1', 'AL_LAP1', 'AL_ANT1',
            'AL_MEA1', 'AL_MDN1', 'AL_STD1', 'AL_COR2', 'AL_OMI2', 'AL_LAP2',
            'AL_ANT2', 'AL_MEA2', 'AL_MDN2', 'AL_STD2', 'AL_COR3', 'AL_OMI3',
            'AL_LAP3', 'AL_ANT3', 'AL_MEA3', 'AL_MDN3', 'AL_STD3', 'AL_COR4',
            'AL_OMI4', 'AL_LAP4', 'AL_ANT4', 'AL_MEA4', 'AL_MDN4', 'AL_STD4',
            'AL_COR5', 'AL_OMI5', 'AL_LAP5', 'AL_ANT5', 'AL_MEA5', 'AL_MDN5',
            'AL_STD5', 'WM3_COR0', 'WM3_ERR0', 'WM3_OMI0', 'WM3_LAP0', 'WM3_MEA0',
            'WM3_MDN0', 'WM3_STD0', 'DA3_COR0', 'DA3_ERR0', 'DA3_OMI0', 'DA3_LAP0',
            'DA3_MEA0', 'DA3_MDN0', 'DA3_STD0', 'DA3_COR1', 'DA3_OMI1', 'DA3_LAP1',
            'DA3_MEA1', 'DA3_MDN1', 'DA3_STD1', 'DA3_ERR2', 'DA3_OMI2', 'GO1_COR0',
            'GO1_ERR0', 'GO1_OMI0', 'GO1_LAP0', 'GO1_MEA0', 'GO1_MDN0', 'GO1_STD0',
            'file']
df = pd.read_excel(in_file)[sel_cols]

df.rename(columns={"SUBJECT": "vp_code"}, inplace=True)

df.vp_code = df.vp_code.str.lower()
df.vp_code = df.vp_code.str.replace("_tp6", "")

error_index = (df.vp_code.str.len() != 4)
print(df.loc[error_index])

df.to_excel(out_file, index=False)
