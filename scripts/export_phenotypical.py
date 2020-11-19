import os
from glob import glob
from pathlib import Path
from lhab_behav.behav_utils import export_domain, create_session_count_file

lut_root = Path("/Volumes/lhab_raw")
s_id_lut = lut_root / "01_RAW/00_PRIVATE_sub_lists/new_sub_id_lut.tsv"

data_root = Path("/Volumes/lhab_public")
in_root_dir = data_root / "03_Data/06_DataConversion/01_DataPreparation"

out_root_dir = data_root / "03_Data/06_DataConversion/02_ConvertedData"

files_already_have_new_id = ['lhab_lacunes_parcMNI_JHUlabels_data.xlsx',
                             'lhab_lacunes_parcMNI_JHUtracts_data.xlsx',
                             'lhab_lacunes_parcMNI_hoCort_data.xlsx',
                             'lhab_lacunes_parcMNI_hoSubcort_data.xlsx',
                             'lhab_lacunes_parcMNI_oxThal_data.xlsx',
                             'lhab_wmh_ubo2d_orig_data.xlsx',
                             'lhab_wmh_ubo2d_parcMNI_JHUlabels_data.xlsx',
                             'lhab_wmh_ubo2d_parcMNI_JHUtracts_data.xlsx',
                             'lhab_wmh_ubo2d_parcMNI_hoCort_data.xlsx',
                             'lhab_wmh_ubo2d_parcMNI_hoSubcort_data.xlsx',
                             'lhab_wmh_ubo2d_parcMNI_oxThal_data.xlsx',
                             'lhab_wmh_ubo3d_orig_data.xlsx']

# check folders are available
if not lut_root.is_dir():
    raise NotADirectoryError(f"lut_root {lut_root} not found. Connect to server? Stopping.")
if not data_root.is_dir():
    raise NotADirectoryError(f"data_root {data_root} not found. Connect to server? Stopping.")

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
        export_domain(group_in_dir, group_out_dir, s_id_lut, domain, files_already_have_new_id)

    if domains:
        # create a file with counts per testscore/session for checking
        group_report_dir = os.path.join(group_out_dir, "report")
        create_session_count_file(os.path.join(group_out_dir, "data"), group_report_dir, group)
