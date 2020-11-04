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
select_cols = ['V1 - Probandenname',
               'V6 CORSI/S1 RW-UBS - Rohwert Unmittelbare Blockspanne',
               'V7 CORSI/S1 RW-UBSR - Rohwert Richtige (UBS)',
               'V8 CORSI/S1 RW-UBSF - Rohwert Falsche (UBS)',
               'V9 CORSI/S1 RW-UBSA - Rohwert Ausgelassene (UBS)',
               'V10 CORSI/S1 RW-UBSP - Rohwert Sequenzierungsfehler (UBS)',
               'V11 CORSI/S1 RW-BT - Rohwert Bearbeitungszeit',
               'V13 MLS/S2 RW-AIMRF - Rohwert Aiming Fehlerzahl Rechte Hand',
               'V14 MLS/S2 RW-AIMLF - Rohwert Aiming Fehlerzahl Linke Hand',
               'V15 MLS/S2 RW-AIMRTR - Rohwert Aiming Trefferzahl Rechte Hand',
               'V16 MLS/S2 RW-AIMLTR - Rohwert Aiming Trefferzahl Linke Hand',
               'V17 MLS/S2 RW-AIMRFD - Rohwert Aiming Fehlerdauer (in Sekunden) Rechte Hand',
               'V18 MLS/S2 RW-AIMLFD - Rohwert Aiming Fehlerdauer (in Sekunden) Linke Hand',
               'V19 MLS/S2 RW-AIMRGD - Rohwert Aiming Gesamtdauer (in Sekunden) Rechte Hand',
               'V20 MLS/S2 RW-AIMLGD - Rohwert Aiming Gesamtdauer (in Sekunden) Linke Hand',
               'V21 MLS/S2 RW-STERF - Rohwert Steadiness Fehlerzahl Rechte Hand',
               'V22 MLS/S2 RW-STELF - Rohwert Steadiness Fehlerzahl Linke Hand',
               'V23 MLS/S2 RW-STERFD - Rohwert Steadiness Fehlerdauer (in Sekunden) Rechte Hand',
               'V24 MLS/S2 RW-STELFD - Rohwert Steadiness Fehlerdauer (in Sekunden) Linke Hand',
               'V25 MLS/S2 RW-LINRF - Rohwert Liniennachfahren Fehlerzahl Rechte Hand',
               'V26 MLS/S2 RW-LINLF - Rohwert Liniennachfahren Fehlerzahl Linke Hand',
               'V27 MLS/S2 RW-LINRFD - Rohwert Liniennachfahren Fehlerdauer (in Sekunden) Rechte Hand',
               'V28 MLS/S2 RW-LINLFD - Rohwert Liniennachfahren Fehlerdauer (in Sekunden) Linke Hand',
               'V29 MLS/S2 RW-LINRGD - Rohwert Liniennachfahren Gesamtdauer (in Sekunden) Rechte Hand',
               'V30 MLS/S2 RW-LINLGD - Rohwert Liniennachfahren Gesamtdauer (in Sekunden) Linke Hand',
               'V31 MLS/S2 RW-TAPRTR - Rohwert Tapping Trefferzahl Rechte Hand',
               'V32 MLS/S2 RW-TAPLTR - Rohwert Tapping Trefferzahl Linke Hand',
               'V38 STROOP/S8 RW-MDRTF5K - Lesen kongruent (sec.)',
               'V39 STROOP/S8 RW-MDRTF5I - Lesen inkongruent (sec.)',
               'V40 STROOP/S8 RW-MDRTF6K - Benennen kongruent (sec.)',
               'V41 STROOP/S8 RW-MDRTF6I - Benennen inkongruent (sec.)',
               'V42 STROOP/S8 RW-FKF5 - Lesen kongruent',
               'V43 STROOP/S8 RW-FIF5 - Lesen inkongruent',
               'V44 STROOP/S8 RW-FKF6 - Benennen kongruent',
               'V45 STROOP/S8 RW-FIF6 - Benennen inkongruent',
               'V46 STROOP/S8 RW-DRTKIF5 - Rohwert Lese-Interferenzneigung (sec.)',
               'V47 STROOP/S8 RW-DRTKIF6 - Rohwert Benenn-Interferenzneigung (sec.)',
               'file']

df = pd.read_excel(in_file)

# fix columns with special characters
remove_chars = ["'", "{", "}"]
ren = {}
for c in df.columns:
    new_col = c
    for r in remove_chars:
        new_col = new_col.replace(r, "")
    ren[c] = new_col

df.rename(columns=ren, inplace=True)

df = df[select_cols]

df.rename(columns={"V1 - Probandenname": "vp_code"}, inplace=True)

df.vp_code = df.vp_code.str.lower()
df.vp_code = df.vp_code.str.replace("_tp6", "")

if not (df.vp_code.str.len() == 4).all():
    raise Exception("Some vp codes are not of len 4")

df.to_excel(out_file, index=False)
