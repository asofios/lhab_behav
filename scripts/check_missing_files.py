import os, re
from glob import glob
import pandas as pd
from lhab_behav.behav_utils import export_domain, create_session_count_file
from pathlib import Path
from warnings import warn
import re

in_root_dir = Path("/Volumes/lhab_public/03_Data/06_DataConversion/01_DataPreparation")

# get groups
os.chdir(in_root_dir)
groups = sorted(glob("*"))
groups = [d for d in groups if os.path.isdir(d)]
if "00_Misc" in groups:
    groups.remove("00_Misc")

for group in groups:
    group_in_dir = in_root_dir / group / "05_ready_2_convert"
    os.chdir(group_in_dir)

    domains = sorted(glob("*"))
    domains = [d for d in domains if os.path.isdir(d)]
    print(group, domains)

    for domain in domains:
        os.chdir(group_in_dir / domain)
        data_files = sorted(Path.cwd().glob("*_data.xlsx"))
        metadata_files = sorted(Path.cwd().glob("*_metadata.xlsx"))
        data_files = [x for x in data_files if not str(x.name).startswith("~$")]
        metadata_files = [x for x in metadata_files if not str(x.name).startswith("~$")]

        if (len(data_files) == 0) or (len(metadata_files) == 0):
            warn(f"Domain empty {domain} {len(data_files)}/{len(metadata_files)}")
        else:
            print(f"{domain} {len(data_files)}/{len(metadata_files)}")

        if len(data_files) != len(metadata_files):
            warn("somethings off")

        # check that for each data_file there is a metadata file
        for data_file in data_files:
            p = re.compile(r"(lhab_)(\w*?)(_data)")
            test_name = p.findall(os.path.basename(data_file))[0][1]

            metadata_str = "lhab_{}_metadata.xlsx".format(test_name)
            g = glob(metadata_str)
            if len(g) > 1:
                raise Exception("More than one meta data file found: {}".format(g))
            elif len(g) == 0:
                raise Exception("No meta data file found: {}".format(metadata_str))

        for metadata_file in metadata_files:
            p = re.compile(r"(lhab_)(\w*?)(_metadata)")
            test_name = p.findall(os.path.basename(metadata_file))[0][1]

            data_str = "lhab_{}_metadata.xlsx".format(test_name)
            g = glob(data_str)
            if len(g) > 1:
                raise Exception("More than one data file found: {}".format(g))
            elif len(g) == 0:
                raise Exception("No data file found: {}".format(data_str))
            a = 1
