#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


clusters_file = "/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation/09_Questionnaires/03_medication/clusters_200_labled_MMu.xlsx"
label_meaning_lut = "/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation/09_Questionnaires/03_medication/cat_lut.xlsx"
medis_file = "/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation/09_Questionnaires/03_medication/lhab_medi_data.xlsx"
out_file = "/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation/09_Questionnaires/03_medication/lhab_medi_data_clean.xlsx"
df = pd.read_excel(medis_file).melt(id_vars=["vp_code"])


# # prepare lut

# In[3]:


lut = pd.read_excel(label_meaning_lut).set_index("N", drop=True).to_dict()["category"]
lut


# In[4]:


categories = pd.read_excel(clusters_file)[["problem", "label"]].dropna()
categories = categories.astype({"label": "int"})
categories = categories.replace({"label": lut}).set_index("problem")
use_cat_lut = categories.to_dict()["label"]


# # get use data

# In[5]:


use = df[df.variable.str.contains("medi_use_")].copy()
use.dropna(subset=["value"], inplace=True)
use = use.replace(use_cat_lut)
use.variable = use.variable.str.replace("medi_use", "medi_use_cat")


# In[6]:


ind = df.variable.str.contains("medi_name_") | df.variable.str.contains("medi_use_")
df_clean = df[ind].copy()
df_clean = pd.concat((df_clean, use))


# # format

# In[7]:


df_clean["sort1"] = df_clean.variable.str.split("_").str[-1]
df_clean["sort2"] = df_clean.variable.str.split("_").str[-2]
df_clean = df_clean.astype({"sort2": "int"})
df_clean["sort3"] = df_clean.variable.str.split("_").str[:-2].str.join("_")
df_clean = df_clean.sort_values(by="vp_code sort1 sort2 sort3".split(" "))


# In[8]:


cols = df_clean.variable.unique()
df_wide = df_clean[["vp_code", "variable", "value"]].set_index("vp_code").pivot(columns="variable", values=["value"])
df_wide.columns = df_wide.columns.droplevel()
df_wide = df_wide[cols]


# In[9]:


df_wide.to_excel(out_file)

