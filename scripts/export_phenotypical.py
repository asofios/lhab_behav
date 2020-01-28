import os, re
from glob import glob
import pandas as pd
from lhab_behav.behav_utils import export_domain, create_session_count_file

s_id_lut = "/Volumes/lhab_raw/01_RAW/00_PRIVATE_sub_lists/new_sub_id_lut.tsv"

in_root_dir = "/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation"
out_root_dir = "/Volumes/lhab_public/03_Data/06_DataConversion/02_ConvertedData"


# get groups
os.chdir(in_root_dir)
groups = sorted(glob("*"))
groups = [d for d in groups if os.path.isdir(d)]
if "00_Misc" in groups:
    groups.remove("00_Misc")

for group in groups:
    group_out_dir = os.path.join(out_root_dir, group)
    group_in_dir = os.path.join(in_root_dir, group, "05_ready_2_convert")
    os.chdir(group_in_dir)

    domains = sorted(glob("*"))
    domains = [d for d in domains if os.path.isdir(d)]
    print(group, domains)

    if domains:
        os.makedirs(group_out_dir, exist_ok=True)


    for domain in domains:
        export_domain(group_in_dir, group_out_dir, s_id_lut, domain)


    if domains:
        # create a file with counts per testscore/session for checking
        group_report_dir = os.path.join(group_out_dir, "report")
        create_session_count_file(os.path.join(group_out_dir, "data"), group_report_dir, group)