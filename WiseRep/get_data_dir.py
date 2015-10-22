import numpy as np
import os, os.path
import glob
import sys

def get_data_dir():
	return glob.glob('supernova_data/type*/trimmed_data/*')