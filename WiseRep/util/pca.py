__author__ = 'Leon liang'

import numpy as np 
import matplotlib.pyplot as plt
import os, os.path, glob, sys, optparse, h5py
import util.get_data as get_data
import util.mkdir as mkdir

def form_matrix(category, data_type):
	if data_type == 'linear':	
		data_path = get_data.linear(category)
	else:
		data_path = get_data.log(category)
	data_matrix = {}
	for data_file in data_path:
		data_mat = {}
		all_wavelength = np.array([], dtype = np.float64)
		all_flux = np.array([], dtype = np.float64)
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
		data_mat['keys'] = dataset.keys()
		data_matrix[data_category] = data_mat
	return data_matrix

def normalize(data_matrix):
	for data_category in data_matrix:
		flux = data_matrix[data_category]['flux']
		for i in range(len(flux)):
			if np.linalg.norm(flux[i,:]) > 0:
				flux[i,:] /= np.linalg.norm(flux[i,:])

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

def plot_components(data_matrix, category, pcomponents, save, xranges, yranges, legend):
	plots = []
	plot_names = []
	colors = ['blue', 'red', 'pink', 'orange', 'green', 'purple', 'black']
	k = 0
	if category:
		categories = category
	else:
		categories = data_matrix
	if len(pcomponents) == 0:
		for data_category in categories:
			coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
			c0 = coefficients_reduced[0,:]
			c1 = coefficients_reduced[1,:]
			plt.scatter(c0, c1, label = category)
			p = plt.scatter(c0, c1, color = colors[k], label = data_category)
			plots.append(p)
			plot_names.append(data_category)
			plt.xlabel('c0')
			plt.ylabel('c1')
			k += 1
			if save:
				if category:
					mkdir.plots(data_category, 'pca')
					name = 'supernova_data/' + data_category + '/plots/pca/' + data_category + '_pca_c0_vs_c1.eps'
				else:
					mkdir.plots('all', 'pca')
					name = 'supernova_data/all/plots/pca/all_pca_c0_vs_c1.eps'
				plt.savefig(name, format='eps', dpi = 3500)
		if legend:
			plt.legend(plot_names)
	else:
		# num_plots = 0
		for pcomponent in pcomponents:
			k = 0
			plots = []
			plot_names = []
			plt.figure()
			for data_category in categories:
				coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
				i = pcomponent[0]
				j = pcomponent[1]
				cx = coefficients_reduced[i,:]
				cy = coefficients_reduced[j,:]
				p = plt.scatter(cx, cy, color = colors[k], label = category)
				plots.append(p)
				plot_names.append(data_category)
				plt.xlabel('c' + str(i))
				plt.ylabel('c' + str(j))
				k += 1
			if legend:
				plt.legend(plot_names)
			if save:
				if category:
					mkdir.plots(data_category, 'pca')
					name = 'supernova_data/' + data_category + '/plots/pca/' + data_category + '_pca_c' + str(i) + '_vs_c' + str(j) + '.eps'
				else:
					mkdir.plots('all', 'pca')
					name = 'supernova_data/all/plots/pca/all_pca_c' + str(i) + '_vs_c' + str(j) + '.eps'
				plt.savefig(name, format='eps', dpi = 3500)
				# num_plots += 1
	if xranges:
		plt.xlim([xranges[0], xranges[1]])
	if yranges:
		plt.ylim([yranges[0], yranges[1]])
	plt.grid()
	plt.show()

def plot_raw_data(data_matrix, category, pcomponents, xranges, yranges):
	if category:
		categories = category
	else:
		categories = data_matrix
	match_raws = []
	if len(pcomponents) == 0:
		for data_category in categories:
			coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
			c0 = coefficients_reduced[0,:]
			c1 = coefficients_reduced[1,:]
			x = np.where(np.logical_and(c0 > xranges[0], c0 < xranges[1]))[0]
			y = np.where(np.logical_and(c1 > yranges[0], c1 < yranges[1]))[0]
			intersection = np.intersect1d(x,y)[0]
			match_raws.append(str(data_matrix[data_category]['keys'][intersection]))
	else:
		for pcomponent in pcomponents:
			for data_category in categories:
				coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
				i = pcomponent[0]
				j = pcomponent[1]
				cx = coefficients_reduced[i,:]
				cy = coefficients_reduced[j,:]
				x = np.where(np.logical_and(cx > xranges[0], cx < xranges[1]))[0]
				y = np.where(np.logical_and(cy > yranges[0], cy < yranges[1]))[0]
				intersection = np.intersect1d(x,y)[0]
				match_raws.append(str(data_matrix[data_category]['keys'][intersection]))

	plots = []
	for i in range(len(categories)):
		data_category = categories[i]
		dataset = match_raws[i]
		raw_data_path = get_data.raw([data_category], dataset)[0]
		spectrum = np.loadtxt(raw_data_path)
		wavelength = spectrum[:,0]
		flux = spectrum[:,1]
		p = plt.plot(wavelength, flux, label = dataset)
		plots.append(p)

	plt.legend(match_raws)
	plt.xlabel('wavelength')
	plt.ylabel('flux')
	plt.show()

def run(category = None, data_type = 'log', n = 6, pcomponents = [], save = False, plot_comps = True, plot_raw = False, xranges = None, yranges = None, legend = False):
	data_matrix = form_matrix(category, data_type)
	normalize(data_matrix)
	compute_mean(data_matrix)
	demean(data_matrix)
	svd(data_matrix)
	compute_pca(data_matrix)
	reduce_pca(data_matrix, n)
	# compute_K(data_matrix)
	if plot_comps:
		plot_components(data_matrix, category, pcomponents, save, xranges, yranges, legend)
	if plot_raw:
		plot_raw_data(data_matrix, category, pcomponents, xranges, yranges)

# data_matrix = form_matrix()
# normalize(data_matrix)
# compute_mean(data_matrix)
# demean(data_matrix)
# svd(data_matrix)
# compute_pca(data_matrix)
# reduce_pca(data_matrix)
# plot_components(data_matrix)
