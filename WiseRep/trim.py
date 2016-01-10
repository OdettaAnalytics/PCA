__author__ = 'Leon Liang'

'''
This Python file processes raw spectra
and trim it so that the remaining wavelengths will be within
the min_wave and max_wave inputs

Outputs trimmed spectra into a hdf5 file
'''

import numpy as np
import util.get_data as get_data
import util.convert_HDF5 as convert_HDF5

def trim(min_wave, max_wave, category = None):
	data_path = get_data.raw(category)
	for data in data_path:
		spectrum = np.loadtxt(data)
		wavelength = spectrum[:,0]
		if (min(wavelength) > min_wave) and (max(wavelength) < max_wave):
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
		data_str = data.split('/')
		data_category = data_str[1]
		data_name = data_str[4]
		data_type = data_category + '_' + 'trim'
		convert_HDF5.write(data_category, data_name, data_type, trimmed_spectrum)

if __name__ == '__main__':
	min_wave = 4000
	max_wave = 8000
	trim(min_wave, max_wave)