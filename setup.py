#! /usr/bin/env python


descr = """lhab_behov"""

import os
from setuptools import setup, find_packages

DISTNAME = "lhab_behav"
DESCRIPTION = descr
MAINTAINER = 'Franz Liem'
MAINTAINER_EMAIL = 'franziskus.liem@uzh.ch'
LICENSE = 'Apache2.0'
DOWNLOAD_URL = 'xxx'
VERSION = "dev"

PACKAGES = find_packages()

if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          version=VERSION,
          url=DOWNLOAD_URL,
          download_url=DOWNLOAD_URL,
          packages=PACKAGES,
          )
