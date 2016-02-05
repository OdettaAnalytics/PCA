__author__ = 'Leon Liang'

import numpy as np
import util.pca as pca
import matplotlib.pyplot as plt
import util.get as get
import util.mkdir as mkdir
import h5py
import optparse, sys

WARNING = "Please enter the what you want to plot: python ploy.py [raw, interpolates, coefficients]."
COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'purple', 'black']

def raw(category = None):
	data_path = get.data('raw', category)
	mkdir.plots(category = None, kind = 'raw')
	for data_name in data_path:
		spectrum = np.loadtxt(data_name)
		wavelength = spectrum[:,0]
		flux = spectrum[:,1]
		plt.figure()
		plt.plot(wavelength, flux)
		name = data_name.split('/')[4]
		plt.title(name)
		plt.xlabel('wavelength')
		plt.ylabel('flux')
		data_category = data_name.split('/')[1]
		filename = 'supernova_data/' + data_category + '/plots/raw/' + name + '.eps'
		plt.savefig(filename, format='eps', dpi = 3500)
		plt.close()

def deredshift(category = None):
	data_path = get.data('deredshift', category)
	mkdir.plots(category = None, kind = 'deredshift')
	for data_file in data_path:
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			plt.figure()
			plt.plot(wavelength, flux)
			plt.xlabel('wavelength')
			plt.ylabel('flux')
			plt.title(data_name)
			filename = 'supernova_data/' + data_category + '/plots/deredshift/' + data_name + '.eps'
			plt.savefig(filename, format='eps', dpi = 3500)
			plt.close()
		dataset.close()

def rebin(category = None, rebin_type = 'log', save = True):
	data_path = get.data('rebin', category)
	mkdir.plots(category = None, kind = 'rebin_' + rebin_type)
	for data_file in data_path:
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			plt.figure()
			plt.plot(wavelength, flux)
			plt.xlabel('wavelength')
			plt.ylabel('flux')
			plt.title(data_name)
			filename = 'supernova_data/' + data_category + '/plots/rebin_' + rebin_type + '/' + data_name + '.eps'
			plt.savefig(filename, format='eps', dpi = 3500)
			plt.close()
		dataset.close()

def coefficients(category = None, rebin_type = 'log', legend = True, save = True, show = False):
	data_path = get.data('pca', category)
	mkdir.plots(category = 'all', kind = 'pca/coefficients')
	for i in range(81):
		x = np.zeros([100])
		k = 0
		plt.figure()
		for data_file in data_path:
			data_category = data_file.split('/')[1]
			dataset = h5py.File(data_file, 'r')	
			coefficients_normal = dataset['coefficients_normal']
			[m,n] = coefficients_normal.shape
			plt.scatter(x[:n], coefficients_normal[i,:], color = COLORS[k%len(COLORS)], label = data_category)
			x += 1
			k += 1
			dataset.close()

		plt.scatter(x[0] + 2, np.array([0]), color = 'white')
		plt.title('coefficient ' + str(i))
		if legend:
			plt.legend()
		if save:
			name = 'supernova_data/all/plots/pca/coefficients/coefficient_' + str(i) + '.eps'
			plt.savefig(name, format='eps', dpi = 3500)
		if show:
			plt.show()
		plt.close()

def pcomponents(category = None, components = [[0,1]], legend = True, save = True, show = False):
	data_path = get.data('pca', category)
	mkdir.plots(category = 'all', kind = 'pca/pcomponents')
	for component in components:
		k = 0
		plots = []
		plot_names = []
		plt.figure()
		i = pcomponent[0]
		j = pcomponent[1]
		for data_file in data_path:
			data_category = data_file.split('/')[1]
			dataset = h5py.File(data_file, 'r')	
			coefficients_reduced = dataset['coefficients_reduced']
			cx = coefficients_reduced[i,:]
			cy = coefficients_reduced[j,:]
			p = plt.scatter(cx, cy, color = COLORS[k%len(COLORS)], label = category)
			plots.append(p)
			plot_names.append(data_category)
			k += 1
		if legend:
			plt.legend(plot_names, loc='right', bbox_to_anchor = (1.1, 0.2), fancybox = True)
		plt.grid()
		plt.xlabel('c' + str(i))
		plt.ylabel('c' + str(j))
		plt.title('c' + str(i) + ' vs ' + 'c' + str(j))
		name = 'supernova_data/all/plots/pca/pcomponents/' + 'c' + str(i) + '_vs_' + 'c' + str(j) + '.eps'
		plt.savefig(name, format='eps', dpi = 3500)
		if show:
			plt.show()


parser = optparse.OptionParser()
parser.add_option("--rebin_type", dest = "rebin_type")
parser.add_option("--category", dest = "category")
parser.add_option("--components", dest = "components")
parser.add_option("--legend", dest = "legend")
parser.add_option("--show", dest = "show")
parser.add_option("-s", dest = "save")

(opts, args) = parser.parse_args()

if len(args) == 0:
	print WARNING
	sys.exit()

rebin_type = 'log'
if opts.rebin_type:
	if opts.rebin_type == 'linear':
		rebin_type = 'linear'


category = None
if opts.category:
	category = opts.category.split('[')[1].split(']')[0].split(',')

components = [[0,1]]
if opts.components:
	pcomps = opts.components.split('[')[1].split(']')[0].split(',')
	if len(pcomps)%2 != 0:
		print 'Please enter an even number of principal components you want to analysis'
		sys.exit()
	else:
		components = []
		for i in range(0, len(pcomps) - 1, 2):
			cx = int(pcomps[i])
			cy = int(pcomps[i + 1])
			components.append([cx, cy])

show = False
if opts.show:
	show = True

legend = True
if opts.legend:
	if opts.legend == 'False':
		legend = False

save = True
if opts.save:
	if opts.save == 'False':
		save = False


if args[0] == 'raw':
	raw(category)
elif args[0] == 'deredshift':
	deredshift(category)
elif args[0] == 'rebin':
	rebin(category, rebin_type)
elif args[0] == 'coefficients':
	coefficients(category, rebin)
elif args[0] == 'pcomponents':
	pcomponents(category, components, legend, save, show)
else:
	print 'Incorrect plot type entered. ' + WARNING
	sys.exit()






