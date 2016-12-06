__author__ = 'Leon liang'

import numpy as np 
import matplotlib.pyplot as plt
import os, os.path, glob, sys, optparse, h5py
import util.get as get
import util.mkdir as mkdir
import util.convert_HDF5 as convert_HDF5

def form_matrix(category = None, rebin_type = 'log'):
    data_path = get.data('rebin', category, rebin_type)
    data_matrix = {}
    all_wavelength = np.array([], dtype = np.float64)
    all_flux = np.array([], dtype = np.float64)
    all_keys = []
    for data_file in data_path:
        data_mat = {}
        category_wavelength = np.array([], dtype = np.float64)
        category_flux = np.array([], dtype = np.float64)
        data_category = data_file.split('/')[1]
        dataset = h5py.File(data_file, 'r')
        for data_name in dataset:
            wavelength = dataset[data_name][:, 0]
            flux = dataset[data_name][:, 1]
            if len(category_wavelength) == 0:
                category_wavelength = wavelength
                category_flux = flux
            else:
                category_wavelength = np.vstack([category_wavelength, wavelength])
                category_flux = np.vstack([category_flux, flux])
            if len(all_wavelength) == 0:
                all_wavelength = wavelength
                all_flux = flux
            else:
                all_wavelength = np.vstack([all_wavelength, wavelength])
                all_flux = np.vstack([all_flux, flux])
        all_keys += dataset.keys()
        data_mat['wavelength'] = category_wavelength
        data_mat['flux'] = category_flux
        data_mat['keys'] = np.array(dataset.keys(), dtype = str)
        data_matrix[data_category] = data_mat
        dataset.close()
    data_mat = {}
    data_mat['wavelength'] = all_wavelength
    data_mat['flux'] = all_flux
    data_mat['keys'] = np.array(all_keys, dtype = str)
    data_matrix['all'] = data_mat
    return data_matrix

def normalize(data_matrix):
    for data_category in data_matrix:
        flux = data_matrix[data_category]['flux']
        for i in range(len(flux)):
            if np.linalg.norm(flux[i,:]) > 0:
                flux[i,:] /= np.linalg.norm(flux[i,:])

def compute_mean(data_matrix):
    data_category = 'all'
    mu_matrix = {}
    flux = data_matrix[data_category]['flux']
    flux_mu = np.zeros(flux.shape)
    for i in range(len(flux)):
        flux_mu[i] = np.mean(flux[i,:])
    mu_matrix['flux'] = flux_mu
    data_matrix[data_category]['mu'] = mu_matrix


def demean(data_matrix):
    compute_mean(data_matrix)
    data_category = 'all'
    flux = data_matrix[data_category]['flux']
    mu_matrix = data_matrix[data_category]['mu']
    for i in range(len(flux)):
        flux[i,:] -= mu_matrix['flux'][i]

def svd(data_matrix):
    data_category = 'all'
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
    data_category = 'all'
    U = data_matrix[data_category]['svd']['U']
    for data_category in data_matrix:
        data_matrix[data_category]['coefficients'] = {}
        flux = data_matrix[data_category]['flux']
        coefficients = (flux.dot(U)).T
        data_matrix[data_category]['coefficients']['normal'] = coefficients

def reduce_pca(data_matrix, n = 10):
    data_category = 'all'
    U = data_matrix[data_category]['svd']['U']
    U_reduced = np.zeros(U.shape)
    for i in range(n):
        U_reduced[:,i] = U[:,i]
    data_matrix[data_category]['svd']['U_reduced'] = U_reduced
    for data_category in data_matrix:
        flux = data_matrix[data_category]['flux']
        coefficients_reduced = (flux.dot(U_reduced)).T #(U_reduced.T).dot(flux.T)
        data_matrix[data_category]['coefficients']['reduced'] = coefficients_reduced

def compute_K(data_matrix):
    data_category = 'all'
    U = data_matrix[data_category]['svd']['U']
    U_reduced = data_matrix[data_category]['svd']['U_reduced']
    for data_category in data_matrix:
        K_mat = {}
        coefficients = data_matrix[data_category]['coefficients']['normal']
        coefficients_reduced = data_matrix[data_category]['coefficients']['reduced']
        K = (U.dot(coefficients)).T
        K_reduced = (U_reduced.dot(coefficients_reduced)).T
        K_mat['normal'] = K
        K_mat['reduced'] = K_reduced
        data_matrix[data_category]['K'] = K_mat

def save_pca(data_matrix):
    for data_category in data_matrix:
        data_filename = data_category + "_pca"
        if data_category == 'all':
            convert_HDF5.write(data_category, 'U', data_filename, data_matrix[data_category]['svd']['U'])
            convert_HDF5.write(data_category, 'U_reduced', data_filename, data_matrix[data_category]['svd']['U_reduced'])
            convert_HDF5.write(data_category, 'S', data_filename, data_matrix[data_category]['svd']['S'])
            convert_HDF5.write(data_category, 'V', data_filename, data_matrix[data_category]['svd']['V'])
        convert_HDF5.write(data_category, 'wavelength', data_filename, data_matrix[data_category]['wavelength'])
        convert_HDF5.write(data_category, 'flux', data_filename, data_matrix[data_category]['flux'])
        convert_HDF5.write(data_category, 'keys', data_filename, data_matrix[data_category]['keys'])
        convert_HDF5.write(data_category, 'coefficients_normal', data_filename, data_matrix[data_category]['coefficients']['normal'])
        convert_HDF5.write(data_category, 'coefficients_reduced', data_filename, data_matrix[data_category]['coefficients']['reduced'])
        convert_HDF5.write(data_category, 'K_normal', data_filename, data_matrix[data_category]['K']['normal'])
        convert_HDF5.write(data_category, 'K_reduced', data_filename, data_matrix[data_category]['K']['reduced'])


def run(category = None, rebin_type = 'log', n = 10):
    data_matrix = form_matrix(category, rebin_type)
    normalize(data_matrix)
    compute_mean(data_matrix)
    demean(data_matrix)
    svd(data_matrix)
    compute_pca(data_matrix)
    reduce_pca(data_matrix, n)
    compute_K(data_matrix)
    save_pca(data_matrix)

