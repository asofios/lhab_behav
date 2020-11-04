from pathlib import Path
import pandas as pd
from warnings import warn

in_file = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data"
               "/00_aggregated_04_Medikationsanamnese.xlsx")
old_term_file = Path(
    "/Volumes/lhab_public/03_Data/04_data_questionnaires/02_datacleaning/01_clean_converted/03_medication/01_aggregateddata_medi/fl_tests/clusters_200_labled_MMu.xlsx")
out_path = Path("/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data/medi")
out_path.mkdir(exist_ok=True)

old_terms = pd.read_excel(old_term_file)
medis_tp6 = pd.read_excel(in_file)

reasons = pd.Series(medis_tp6.filter(like="Verwendungszweck").values.flatten()).dropna()

reasons = reasons.unique()

new_terms = set(reasons) - set(old_terms["problem"])

df = pd.DataFrame({"problem": list(new_terms)})
df.to_excel(out_path / "medis_new_problems_tp6.xlsx", index=False)
