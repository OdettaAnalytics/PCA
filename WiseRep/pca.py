__author__ = Leon liang

import numpy as np 
import numpy as np
import matplotlib.pyplot as plt
import os, os.path, glob, sys, optparse, h5py
import get_data

def form_Matrix():
	dataset = get_data.all_hdf5()
	data_matrix = {}
	for data in dataset:
		all_wavelength = np.array([])
		all_flux = np.array([])
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[3]
		data_file = h5py.File(data, 'r')
		for name in data_file:
			wavelength = data_file[name][:, 0]
			flux = data_file[name][:, 1]
			if len(all_wavelength) == 0:
				all_wavelength = wavelength
				all_flux = flux
			else:
				all_wavelength = np.vstack([all_wavelength, wavelength])
				all_flux = np.vstack([all_flux, flux])
		data_matrix[data_type] = (all_wavelength, all_flux)
	return data_matrix

def normalize(data_matrix):
	norm_data_matrix = {}
	for data_type in data_matrix:
		norm_wavelength = data_matrix[data_type][0]
		flux = data_matrix[data_type][1]
		for i in range(len(norm_wavelength)):
			norm_wavelength /= np.linalg.norm(norm_wavelength[i,:])
		norm_data_matrix[data_type] = (norm_wavelength, flux)
	return norm_data_matrix

def svd(norm_data_matrix):






def normalize(dataset):

