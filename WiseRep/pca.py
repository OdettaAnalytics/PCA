__author__ = 'Leon liang'

import numpy as np 
import matplotlib.pyplot as plt
import os, os.path, glob, sys, optparse, h5py
import util.get_data as get_data

def form_matrix(category = None, data_type = 'log'):
	if data_type == 'linear':	
		data_path = get_data.linear(category)
	else:
		data_path = get_data.log(category)
	data_matrix = {}
	for data_file in data_path:
		data_mat = {}
		all_wavelength = np.array([])
		all_flux = np.array([])
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			if len(all_wavelength) == 0:
				all_wavelength = wavelength
				all_flux = flux
			else:
				all_wavelength = np.vstack([all_wavelength, wavelength])
				all_flux = np.vstack([all_flux, flux])
		data_mat['wavelength'] = all_wavelength
		data_mat['flux'] = all_flux
		data_matrix[data_category] = data_mat
	return data_matrix

def normalize(data_matrix):
	for data_category in data_matrix:
		flux = data_matrix[data_category]['flux']
		for i in range(len(flux)):
			if np.linalg.norm(flux[i,:]) > 0:
				flux /= np.linalg.norm(flux[i,:])

def compute_mean(data_matrix):
	for data_category in data_matrix:
		mu_matrix = {}
		flux = data_matrix[data_category]['flux']
		flux_mu = np.zeros(flux.shape)
		for i in range(len(flux)):
			flux_mu[i] = np.mean(flux[i,:])
		mu_matrix['flux'] = flux_mu
		data_matrix[data_category]['mu'] = mu_matrix


def demean(data_matrix):
	compute_mean(data_matrix)
	for data_category in data_matrix:
		flux = data_matrix[data_category]['flux']
		mu_matrix = data_matrix[data_category]['mu']
		for i in range(len(flux)):
			flux[i,:] -= mu_matrix['flux'][i]

def svd(data_matrix):
	for data_category in data_matrix:
		svd_mat = {}
		flux = data_matrix[data_category]['flux'].T
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
		data_matrix[data_category]['svd'] = svd_mat

def dot_product(data_matrix):
	from numpy import dot
	for data_category in data_matrix:
		U = data_matrix[data_category]['svd']['U']
		S = data_matrix[data_category]['svd']['S']
		V = data_matrix[data_category]['svd']['V']
		X_pca = U.dot(S).dot(V.T)
		data_matrix[data_category]['x_pca'] = X_pca

def compute_pca(data_matrix):
	from numpy import dot
	for data_category in data_matrix:
		data_matrix[data_category]['coefficients'] = {}
		U = data_matrix[data_category]['svd']['U']
		S = data_matrix[data_category]['svd']['S']
		V = data_matrix[data_category]['svd']['V']

		flux = data_matrix[data_category]['flux']
		pca_matrix = (V.dot(S.T)).T
		coefficients = (U.T).dot(flux.T)
		data_matrix[data_category]['pca'] = pca_matrix
		data_matrix[data_category]['coefficients']['normal'] = coefficients

def reduce_pca(data_matrix, n):
	for data_category in data_matrix:
		flux = data_matrix[data_category]['flux']
		U = data_matrix[data_category]['svd']['U']
		U_reduced = np.zeros(U.shape)
		for i in range(n):
			U_reduced[:,i] = U[:,i]
		coefficients_reduced = (U_reduced.T).dot(flux.T)
		data_matrix[data_category]['svd']['U_reduced'] = U_reduced
		data_matrix[data_category]['coefficients']['reduced'] = coefficients_reduced

def compute_K(data_matrix):
	for data_category in data_matrix:
		K_mat = {}
		coefficients = data_matrix[data_category]['coefficients']['normal']
		coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
		U = data_matrix[data_category]['svd']['U']
		S = data_matrix[data_category]['svd']['S']
		V = data_matrix[data_category]['svd']['V']
		U_reduced = data_matrix[data_category]['svd']['U_reduced']
		K = (U.dot(coefficients)).T
		K_reduced = (U_reduced.dot(coefficients_reduced)).T
		K_mat['normal'] = K
		K_mat['reduced'] = K_reduced
		data_matrix[data_category]['K'] = K_mat

def plotting(data_matrix, components = None, category = None):
	if category is not None:
		coefficients_reduced = data_matrix[category]['coefficients']['reduced']
		if components is None:
			c1 = coefficients_reduced[0,:]
			c2 = coefficients_reduced[1,:]
			plt.scatter(c1, c2, label = category)
			plt.xlabel('c0')
			plt.ylabel('c1')
		else:
			for component in components:
				i = component[0]
				j = component[1]
				cx = coefficients_reduced[i,:]
				cy = coefficients_reduced[j,:]
				plt.scatter(cx, cy, label = category)
				plt.xlabel('c' + str(i))
				plt.ylabel('c' + str(j))
		plt.show()
	else:
		plots = []
		plot_names = []
		colors = ['blue', 'red', 'pink', 'orange', 'green', 'purple', 'black']
		i = 0
		for data_category in data_matrix:
			coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
			if components is None:
				c1 = coefficients_reduced[0,:]
				c2 = coefficients_reduced[1,:]
				plt.scatter(c1, c2, label = category)
				p = plt.scatter(c1, c2, color = colors[i], label = data_category)
				plots.append(p)
				plot_names.append(data_category)
				plt.xlabel('c0')
				plt.ylabel('c1')
			else:
				for component in components:
					i = component[0]
					j = component[1]
					cx = coefficients_reduced[i,:]
					cy = coefficients_reduced[j,:]
					p = plt.scatter(cx, cy, color = colors[i], label = category)
					plots.append(p)
					plot_names.append(data_category)
					plt.xlabel('c' + str(i))
					plt.ylabel('c' + str(j))
			i += 1
		plt.legend(plots, plot_names)
		plt.show()
