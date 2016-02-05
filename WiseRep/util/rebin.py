__author__ = 'Leon Liang'

'''
This Python file takes processed spectra and interpolates
to desire number of points based on input, min_wave, and 
max_wave

Outputs the interpolated spectra into a hdf5 file
'''

import numpy as np
from scipy import interpolate
import h5py
import util.get as get
import util.convert_HDF5 as convert_HDF5

def interpolation(min_wave, max_wave, category = None):
	data_path = get.data('demean', category)
	f_x = {}
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			spectrum = dataset[data_name][:,:]
			wavelength = spectrum[:,0]
			flux = spectrum[:,1]
			nonzeros = np.where(flux)
			wavelength = wavelength[nonzeros]
			flux = flux[nonzeros]
			[num_waves,] = wavelength.shape
			f = interpolate.interp1d(wavelength, flux, bounds_error = False, fill_value = 0)
			f_x[data_name] = f
	return f_x

def run(min_wave = 4000, max_wave = 8000, resolution = 2000, category = None, rebin_type = 'log'):
	f_x = interpolation(min_wave, max_wave, category)
	data_path = get.data('demean', category)
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		data_category = data_file.split('/')[1]
		for data_name in dataset:
			if rebin_type == 'linear':
				new_wavelength = np.linspace(min_wave, max_wave, num = resolution, endpoint = False)
			else:
				new_wavelength = np.logspace(np.log10(min_wave), np.log10(max_wave), num = resolution, endpoint = False)
			f = f_x[str(data_name)]
			new_flux = f(new_wavelength)
			new_rebin_data = np.vstack([new_wavelength, new_flux]).T
			data_type = data_category + '_rebin_' + rebin_type
			convert_HDF5.write(data_category, str(data_name), data_type, new_rebin_data)

