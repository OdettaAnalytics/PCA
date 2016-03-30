__author__ = 'Leon Liang'

import numpy as np
from scipy import interpolate
import h5py
import util.get as get
import util.convert_HDF5 as convert_HDF5

def interpolation(min_wave, max_wave, category = None):
	'''
	generates the interpolation function

	Parameters
	----------
	min_wave : int indicating the minimum wavelength range

	max_wave : int indicating the maximum wavelength range

	category : list of strings of category for rebinning

	Returns
	-------
	f_x : list of interpolation functions for eahc of the dataset
	'''
	data_path = get.data('demean', category)
	f_x = {}
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			spectrum = dataset[data_name][:,:]
			wavelength = spectrum[:,0]
			flux = spectrum[:,1]
			nonzeros = np.where(wavelength)
			wavelength = wavelength[nonzeros]
			flux = flux[nonzeros]
			[num_waves,] = wavelength.shape
			f = interpolate.interp1d(wavelength, flux, bounds_error = False, fill_value = 0)
			f_x[data_name] = f
	return f_x

def run(min_wave = 4000, max_wave = 8000, n_rebin = 2000, category = None, rebin_type = 'log'):
	'''
	rebin each of the trimmed data in the category to desired number of points

	Parameters
	----------
	min_wave : int indicating the minimum wavelength range

	max_wave : int indicating the maximum wavelength range

	n_rebin : int indicatinng the number of points wanted for rebin

	category : list of strings of category for rebinning

	rebin_type : string indicating the type of rebin wanted (log or linear)
	'''
	f_x = interpolation(min_wave, max_wave, category)
	data_path = get.data('demean', category)
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		data_category = data_file.split('/')[1]
		for data_name in dataset:
			if rebin_type == 'linear':
				new_wavelength = np.linspace(min_wave, max_wave, num = n_rebin, endpoint = False)
			else:
				new_wavelength = np.logspace(np.log10(min_wave), np.log10(max_wave), num = n_rebin, endpoint = False)
			f = f_x[str(data_name)]
			new_flux = f(new_wavelength)
			new_rebin_data = np.vstack([new_wavelength, new_flux]).T
			data_filename = data_category + '_rebin_' + rebin_type
			convert_HDF5.write(data_category, str(data_name), data_filename, new_rebin_data)

