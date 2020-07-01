#! /usr/bin/env python3

# std imports
import pathlib
import os

# CONSTANTS


# paths
PKG_DIR = pathlib.Path(__file__).parent
REPO_DIR = PKG_DIR / '..'
BIN_DIR = REPO_DIR / 'bin'
TEMP_DIR = REPO_DIR / 'temp'
RESOURCE_DIR = REPO_DIR / 'resource'


# settings
# There are also two ways to disable the CPU affinity-resetting behaviour of OpenBLAS itself.
#  At run-time you can use the environment variable OPENBLAS_MAIN_FREE (or GOTOBLAS_MAIN_FREE), for example
# https://stackoverflow.com/questions/15639779/why-does-multiprocessing-use-only-a-single-core-after-i-import-numpy
os.environ["OPENBLAS_MAIN_FREE"] = "1"
os.environ["GOTOBLAS_MAIN_FREE"] = "1"
