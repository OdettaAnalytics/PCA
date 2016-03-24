__author__ = 'Leon Liang'

'''
This Python File serves as a command processing
file that takes all inputs from users and calls
corresponding functions from other files
'''

import optparse, sys
import util.trim as trim
import util.deredshift as deredshift
import util.demean as demean
import util.rebin as rebin
import util.pca as pca
import util.plot as plt
import util.mkdir as mkdir

parser = optparse.OptionParser()
parser.add_option("--trim", dest = "trim")
parser.add_option("--deredshift", dest = "deredshift")
parser.add_option("--demean", dest = "demean")
parser.add_option("--rebin", dest = "rebin")
parser.add_option("--rebin_type", dest = "rebin_type")
parser.add_option("--pca", dest = "pca")
parser.add_option("--category", dest = "category")
parser.add_option("--wave_range", dest = "wave_range")
parser.add_option("--min_wave", dest = "min_wave")
parser.add_option("--max_wave", dest = "max_wave")
parser.add_option("--components", dest = "components")
parser.add_option("--n_rebin", dest = "n_rebin")
parser.add_option("--legend", dest = "legend")
parser.add_option("--plot", dest = "plot")
parser.add_option("-n", dest = "n_comp")
parser.add_option("--n_coefs", dest = "n_coefs")
parser.add_option("-s", dest  = "save")
parser.add_option("--save", dest = "save")
parser.add_option("--show", dest  = "show")
parser.add_option("-f", dest = "file")
parser.add_option("--file", dest = "file")
parser.add_option("--init", dest = "init")

(opts, args) = parser.parse_args()

components = [[0,1]]
category = None
legend = True
n = 6
n_rebin = 2000
save = True
rebin_type = 'log'
show = False
compare = None
min_wave = 4000
max_wave = 8000
num_coefs = 80
data_file = None

if opts.init:
	if '[' in opts.init and ']' in opts.init and ',' in opts.init:
		category = opts.init.split('[')[1].split(']')[0].split(',')
	elif ',' in opts.init:
		category = opts.init.split(',')
	else:
		category = opts.init
	mkdir.init(category)
	sys.exit()

if opts.category:
	if '[' in opts.category and ']' in opts.category and ',' in opts.category:
		category = opts.category.split('[')[1].split(']')[0].split(',')
	elif ',' in opts.category:
		category = opts.category.split(',')
	else:
		category = opts.category
if opts.components:
	comps = opts.components.split('[')[1].split(']')[0].split(',')
	if len(comps) % 2 > 0:
		print 'Please enter an even number of principal components you want to analysis'
		sys.exit()
	else:
		components = []
		for i in range(0, len(comps) - 1, 2):
			cx = int(comps[i])
			cy = int(comps[i + 1])
			components.append([cx, cy])
if opts.rebin_type:
	if opts.rebin_type == 'linear':
		rebin_type = 'linear'
	else:
		rebin_type = 'log'
if opts.wave_range:
	min_wave = float(opts.wave_range[0])
	max_wave = float(opts.wave_range[1])
else:
	if opts.min_wave:
		min_wave = float(opts.min_wave)
	if opts.max_wave:
		max_wave = float(opts.max_wave)
if opts.n_comp:
	n = int(opts.n_comp)
if opts.n_rebin:
	n_rebin = int(opts.n_rebin)
if opts.save:
	if opts.save.lower() == 'false':
		save = False
if opts.legend:
	if opts.legend.lower() == 'false':
		legend = False
if opts.n_coefs:
	num_coefs = int(opts.n_coefs)
if opts.show:
	show = True
if opts.file:
	data_file = opts.file

if not (opts.trim or opts.deredshift or opts.demean or opts.rebin or opts.pca or opts.plot):
	trim.run(min_wave, max_wave, category)
	deredshift.run(category)
	demean.demean_flux(category)
	rebin.run(min_wave, max_wave, n_rebin, category, rebin_type)
	pca.run(category, rebin_type, n)
	plt.pcomponents(category, components, legend, save, show)
else:
	if opts.trim:
		trim.run(min_wave, max_wave, category)
	if opts.deredshift:
		deredshift.run(category)
	if opts.demean:
		demean.demean_flux(category)
	if opts.rebin:
		rebin.run(min_wave, max_wave, n_rebin, category, rebin_type)
	if opts.pca:
		pca.run(category, rebin_type, n)
	if opts.plot:
		if opts.plot.lower() == 'raw':
			plt.raw(category)
		elif opts.plot.lower() == 'deredshift':
			plt.deredshift(category)
		elif opts.plot.lower() == 'trim':
			plt.trim(category)
		elif opts.plot.lower() == 'rebin':
			plt.rebin(category, rebin_type)
		elif opts.plot.lower() == 'coefficients':
			plt.coefficients(category, rebin_type, num_coefs, legend, save, show)
		elif opts.plot.lower() == 'u':
			plt.U_matrix(category, legend, save, show)
		elif opts.plot.lower() == 'k_reduced':
			plt.K_reduced(category, data_file, legend, save, show)
		else:
			plt.pcomponents(category, components, legend, save, show)
				