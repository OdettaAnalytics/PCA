__author__ = 'Leon Liang'

import numpy as np
import util.pca as pca
import matplotlib.pyplot as plt
import util.get_data as get_data
import util.mkdir as mkdir
import h5py
import optparse, sys

def raw(category = None):
	data_path = get_data.raw(category)
	mkdir.plots(category = None, kind = 'raw')
	for data_name in data_path:
		spectrum = np.loadtxt(data_name)
		wavelength = spectrum[:,0]
		flux = spectrum[:,1]
		plt.figure()
		plt.plot(wavelength, flux)
		plt.title(data_name)
		data_category = data_name.split('/')[1]
		name = data_name.split('/')[4]
		filename = 'supernova_data/' + data_category + '/plots/raw/' + name + '.eps'
		plt.savefig(filename, format='eps', dpi = 3500)
		plt.close()

def interpolate(category = None, data_type = 'log'):
	if data_type == 'linear':	
		data_path = get_data.linear(category)
	else:
		data_path = get_data.log(category)
	mkdir.plots(category = None, kind = data_type)
	for data_file in data_path:
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			plt.figure()
			plt.plot(wavelength, flux)
			plot_name = data_name
			plt.title(plot_name)
			filename = 'supernova_data/' + data_category + '/plots/' + data_type + '/' + data_name + '.eps'
			plt.savefig(filename, format='eps', dpi = 3500)
			plt.close()
		dataset.close()

def eigenspectra(category = None, data_type = 'log'):
	data_matrix = pca.form_matrix(category, data_type)
	pca.normalize(data_matrix)
	pca.compute_mean(data_matrix)
	pca.demean(data_matrix)
	pca.svd(data_matrix)
	pca.compute_pca(data_matrix)
	pca.reduce_pca(data_matrix, n = 6)
	colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
	mkdir.plots(category = ['all'], kind = 'pca/coefficients')
	for i in range(250):
		x = np.zeros([100])
		k = 0
		plt.figure()
		for data_category in data_matrix:
			coefficients_normal = data_matrix[data_category]['coefficients']['normal']
			[m,n] = coefficients_normal.shape
			plt.scatter(x[:n], coefficients_normal[i,:], color = colors[k%len(colors)], label = data_category)
			x += 1
			k += 1

		plt.scatter(x[0] + 2, np.array([0]), color = 'white')
		plt.legend()
		plt.title('Eigenspectra ' + str(i))
		name = 'supernova_data/all/plots/pca/coefficients/coefficient_' + str(i) + '.eps'
		plt.savefig(name, format='eps', dpi = 3500)
		plt.close()

parser = optparse.OptionParser()
parser.add_option("--rebin", dest = "rebin")
parser.add_option("--category", dest = "category")
(opts, args) = parser.parse_args()

if len(args) == 0:
	print "Please enter the what you want to plot: [raw, interpolate, eigenspectra]."
	sys.exit()

rebin = 'log'
if opts.rebin:
	if opts.rebin == 'linear':
		rebin = 'linear'

category = None
if opts.category:
	category = opts.category.split('[')[1].split(']')[0].split(',')

if args[0] == 'raw':
	raw(category)
elif args[0] == 'interpolate':
	interpolate(category, rebin)
elif args[0] == 'eigenspectra':
	eigenspectra(category, rebin)
else:
	print 'Incorrect plot type entered.'
	sys.exit()






