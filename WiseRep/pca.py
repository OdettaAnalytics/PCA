__author__ = 'Leon liang'

import numpy as np 
import numpy as np
import matplotlib.pyplot as plt
import os, os.path, glob, sys, optparse, h5py
import get_data

def form_matrix(category = None):
	if category is not None:
		dataset = get_data.hdf5(category)
	else:
		dataset = get_data.hdf5()
	data_matrix = {}
	for data in dataset:
		data_mat = {}
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
		data_mat['wavelength'] = all_wavelength
		data_mat['flux'] = all_flux
		data_matrix[data_type] = data_mat
	return data_matrix

def normalize(data_matrix):
	for data_type in data_matrix:
		# wavelength = data_matrix[data_type]['wavelength']
		flux = data_matrix[data_type]['flux']
		for i in range(len(flux)):
			# wavelength /= np.linalg.norm(wavelength[i,:])
			flux /= np.linalg.norm(flux[i,:])

def compute_mean(data_matrix):
	for data_type in data_matrix:
		mu_matrix = {}
		# wavelength = data_matrix[data_type]['wavelength']
		flux = data_matrix[data_type]['flux']
		# wavelength_mu = np.zeros(wavelength.shape)
		flux_mu = np.zeros(flux.shape)
		for i in range(len(flux)):
			# wavelength_mu[i] = np.mean(wavelength[i,:])
			flux_mu[i] = np.mean(flux[i,:])
		# mu_matrix['wavelength'] = wavelength_mu
		mu_matrix['flux'] = flux_mu
		data_matrix[data_type]['mu'] = mu_matrix


def demean(data_matrix):
	compute_mean(data_matrix)
	for data_type in data_matrix:
		# wavelength = data_matrix[data_type]['wavelength']
		flux = data_matrix[data_type]['flux']
		mu_matrix = data_matrix[data_type]['mu']
		for i in range(len(flux)):
			# wavelength[i,:] -= mu_matrix['wavelength'][i]
			flux[i,:] -= mu_matrix['flux'][i]

def svd(data_matrix):
	for data_type in data_matrix:
		svd_mat = {}
		# wavelength = data_matrix[data_type]['wavelength']
		flux = data_matrix[data_type]['flux'].T
		[U, s, V_T] = np.linalg.svd(flux)
		[m, n] = flux.shape
		S = np.zeros([m, n])
		if (m < n):
			for i in range(m):
				S[i,i] = s[i] 											
		else:
			S[:n,:n] = np.diag(s)
		svd_mat['U'] = U
		svd_mat['S'] = S
		svd_mat['V'] = V_T.T
		data_matrix[data_type]['svd'] = svd_mat

def dot_product(data_matrix):
	from numpy import dot
	for data_type in data_matrix:
		U = data_matrix[data_type]['svd']['U']
		S = data_matrix[data_type]['svd']['S']
		V = data_matrix[data_type]['svd']['V']
		X_pca = U.dot(S).dot(V.T)
		data_matrix[data_type]['x_pca'] = X_pca
	# return X_pca

def compute_pca(data_matrix):
	from numpy import dot
	for data_type in data_matrix:
		data_matrix[data_type]['coefficients'] = {}
		U = data_matrix[data_type]['svd']['U']
		S = data_matrix[data_type]['svd']['S']
		V = data_matrix[data_type]['svd']['V']

		flux = data_matrix[data_type]['flux']
		pca_matrix = (V.dot(S.T)).T
		coefficients = (U.T).dot(flux.T)
		data_matrix[data_type]['pca'] = pca_matrix
		data_matrix[data_type]['coefficients']['normal'] = coefficients

def reduce_pca(data_matrix, n):
	for data_type in data_matrix:
		flux = data_matrix[data_type]['flux']
		U = data_matrix[data_type]['svd']['U']
		U_reduced = np.zeros(U.shape)
		for i in range(n):
			U_reduced[:,i] = U[:,i]
		coefficients_reduced = (U_reduced.T).dot(flux.T)
		data_matrix[data_type]['svd']['U_reduced'] = U_reduced
		data_matrix[data_type]['coefficients']['reduced'] = coefficients_reduced

	