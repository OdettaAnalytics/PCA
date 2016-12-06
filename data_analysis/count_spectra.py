__author__ = 'Leon Liang'

# Script to output the category, object, number of spectra, and z values
# into a text file 

import numpy as np 
import os, os.path
import glob
import sys


def extract_z_values(object_z_file):
    object_zvalues = np.genfromtxt(object_z_file, dtype='str')
    [num_objects, columns] = object_zvalues.shape
    object_names = object_zvalues[1:, 0]
    z_values = np.zeros(num_objects-1)

    for i in range(num_objects - 1):
        z_values[i] = object_zvalues[i+1, 1]

    return object_names, z_values

# def combine_all_info(objects, z_values, )

object_z_file = sys.argv[1]
dir_path = sys.argv[2]
[objects, z_values] = extract_z_values(object_z_file)
[num_objects] = objects.shape
category = np.empty(num_objects, dtype='a10')
num_spectra = np.zeros(num_objects, dtype='int')
supernova_types = np.array(glob.glob('type*'))
# num_datasets = np.zeros(len(supernova_types))

# i = 0 # counter

for type_dir in supernova_types:
    if (os.path.isdir(type_dir)):
        for dataset in glob.glob('supernova_data/' + type_dir + '/raw_data/*'):
            for i in range(num_objects):
                if (dataset.find(objects[i]) != -1):
                    category[i] = type_dir
                    num_spectra[i] += 1

# finished counting the number of spectra per object

labels = np.empty([1, 4], dtype='a16')
labels[0, 0] = 'category'
labels[0, 1] = 'objects'
labels[0, 2] = 'num_spectra'
labels[0, 3] = 'z_values'
supernovae_info = np.vstack([category, objects, num_spectra, z_values]).T

supernovae_info_txt = dir_path + 'supernovae_info.txt'
f = open(supernovae_info_txt, 'w')
np.savetxt(f, labels, delimiter='\t', fmt="%s")
np.savetxt(f, supernovae_info, fmt="%s \t %s \t %s \t %s")
f.close()

# format float %6.4


