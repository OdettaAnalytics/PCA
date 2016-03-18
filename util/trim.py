__author__ = 'Leon Liang'

'''
This Python file processes raw spectra
and trim it so that the remaining wavelengths will be within
the min_wave and max_wave inputs

Outputs trimmed spectra into a hdf5 file
'''

import numpy as np, h5py
import util.get as get
import util.convert_HDF5 as convert_HDF5

def run(min_wave = 4000, max_wave = 8000, category = None):
	data_path = get.data('deredshift', category)
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		data_category = data_file.split('/')[1]
		data_type = data_category + '_' + 'trim'
		for data_name in dataset:
			spectrum = dataset[data_name][:]
			wavelength = spectrum[:,0]
			if (min(wavelength) > min_wave) and (max(wavelength) < max_wave):
				convert_HDF5.write(data_category, str(data_name), data_type, spectrum)
				continue
			[num_wave,] = wavelength.shape
			for i in range(num_wave):
				if wavelength[i] >= min_wave:
					min_range_start = i
					break
			for j in xrange(num_wave-1, min_range_start, -1):
				if wavelength[j] <= max_wave:
					max_range_start = j
					break
			trimmed_spectrum = spectrum[min_range_start:max_range_start+1,:]
			convert_HDF5.write(data_category, str(data_name), data_type, trimmed_spectrum)