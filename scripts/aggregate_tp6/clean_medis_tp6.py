import pandas as pd

clusters_file = "/Volumes/lhab_public/03_Data/04_data_questionnaires/02_datacleaning/01_clean_converted/03_medication/01_aggregateddata_medi/fl_tests/clusters_200_labled_MMu_tp6added.xlsx"
label_meaning_lut = "/Volumes/lhab_public/03_Data/04_data_questionnaires/02_datacleaning/01_clean_converted/03_medication/01_aggregateddata_medi/fl_tests/cat_lut.xlsx"
medis_file = "/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data/00_aggregated_04_Medikationsanamnese.xlsx"
out_file = "/Volumes/lhab_public/03_Data/04_data_questionnaires/00_rawdata_tp6/aggregated_data" \
           "/00_aggregated_04_Medikationsanamnese_purpose_categories.xlsx"

df_orig = pd.read_excel(medis_file).rename(columns={"VP-Nr.": "vp_code"})
df_orig.vp_code = df_orig.vp_code.astype(str)

df = df_orig.melt(id_vars=["vp_code"])

lut = pd.read_excel(label_meaning_lut).set_index("N", drop=True).to_dict()["category"]

categories = pd.read_excel(clusters_file)[["problem", "label"]].dropna()
categories = categories.astype({"label": "int"})
categories = categories.replace({"label": lut}).set_index("problem")
use_cat_lut = categories.to_dict()["label"]

# # get use data
use = df[df.variable.str.contains("_purpose_")].copy()
use.dropna(subset=["value"], inplace=True)
use["value"] = use.value.map(use_cat_lut)
use = use.loc[use.value != 0]
use["tmp"] = 1

count = use.groupby(["vp_code", "value"]).tmp.sum().reset_index()
count_wide = count.pivot(index="vp_code", columns="value")
count_wide.columns = count_wide.columns.droplevel()

# reintroduce subjects that are available, but have none of the reasons focused on
count_wide = pd.merge(count_wide, df_orig[["vp_code"]], on="vp_code", how="outer")
count_wide.set_index("vp_code", drop=True, inplace=True)

count_wide.fillna(0, inplace=True)
count_wide[count_wide >= 1] = 1
count_wide = count_wide.astype(int)

# nan subjects in orig file without data
missing = df_orig.set_index("vp_code", drop=True).medi_01_name_tp6.isna()
count_wide[missing] = pd.np.nan

df_wide = count_wide
df_wide.columns = [f"{c}_tp6" for c in df_wide.columns]

df_wide.sort_values(by="vp_code", inplace=True)
df_wide.to_excel(out_file)
