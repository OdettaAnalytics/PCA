__author__ = 'Leon Liang'

'''
This Python file prcesses trimmed spectra and deredshift
spectra's wavelengths according to the correspond z value
for its supernova

Outputs deredshifted spectra into a hdf5 file
'''

import numpy as np, sys, h5py
import util.get_data as get_data
import util.mkdir as mkdir
import util.convert_HDF5 as convert_HDF5

def extract_z_values(object_z_file):
	object_zvalues = np.genfromtxt(object_z_file, dtype = 'str')
	[num_objects, columns] = object_zvalues.shape
	object_names = object_zvalues[1:, 0]
	z_values = np.zeros(num_objects-1)
	for i in range(num_objects - 1):
		z_values[i] = float(object_zvalues[i+1, 1])
	return object_names, z_values

def deredshift(category = None):
	data_path = get_data.trim(category)
	object_z_file = get_data.z_value()
	object_names, z_values = extract_z_values(object_z_file)
	num_objects = len(object_names)
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		data_category = data_file.split('/')[1]
		for data_name in dataset:
			name = str(data_name.split('.')[0])
			spectrum = dataset[data_name][:,:]
			wavelength = spectrum[:, 0]
			rest_of_spectrum = spectrum[:, 1:]
			z_value = None
			for j in range(num_objects):
				if (name.find(object_names[j]) != -1):
					z_value = z_values[j]
					break
			if z_value is None:
				print 'No such z value for ' + str(data_name)
				sys.exit()
			deredshift_wavelength = wavelength/(1 + z_value)
			deredshift_spectrum = deredshift_wavelength
			[rows, columns] = rest_of_spectrum.shape
			for i in range(columns):
				deredshift_spectrum = np.vstack([deredshift_spectrum, rest_of_spectrum[:,i]])
			deredshift_spectrum = deredshift_spectrum.T
			data_type = data_category + '_' + 'deredshift'
			convert_HDF5.write(data_category, str(data_name), data_type, deredshift_spectrum)

if __name__ == '__main__':
	deredshift()
