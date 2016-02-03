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
import util.interpolate as interpolate
import util.pca as pca

parser = optparse.OptionParser()
parser.add_option("--trim", dest = "trim")
parser.add_option("--deredshift", dest = "deredshift")
parser.add_option("--demean", dest = "demean")
parser.add_option("--interpolate", dest = "interpolate")
parser.add_option("--rebin", dest = "rebin")
parser.add_option("--pca", dest = "pca")
parser.add_option("--category", dest = "category")
parser.add_option("--wave_range", dest = "wave_range")
parser.add_option("--min_wave", dest = "min_wave")
parser.add_option("--max_wave", dest = "max_wave")
parser.add_option("--pcomponents", dest = "pcomponents")
parser.add_option("--resolution", dest = "resolution")
parser.add_option("--legend", dest = "legend")
parser.add_option("--xranges", dest = "xranges")
parser.add_option("--yranges", dest = "yranges")
parser.add_option("--plot", dest = "plot")
parser.add_option("--compare", dest = "compare")
parser.add_option("-n", dest = "n_comp")
parser.add_option("-s", dest  = "save")


(opts, args) = parser.parse_args()

pcomponents = [[0,1]]
category = None
legend = False
n = 6
resolution = 2000
save = False
rebin = 'log'
xranges = None
yranges = None
plot_comps = True
plot_raw = False
show = True
compare = None
min_wave = 4000
max_wave = 8000

if opts.category:
	category = opts.category.split('[')[1].split(']')[0].split(',')
if opts.pcomponents:
	pcomps = opts.pcomponents.split('[')[1].split(']')[0].split(',')
	if len(pcomps) % 2 > 0:
		print 'Please enter an even number of principal components you want to analysis'
		sys.exit()
	else:
		pcomponents = []
		for i in range(0, len(pcomps) - 1, 2):
			cx = int(pcomps[i])
			cy = int(pcomps[i + 1])
			pcomponents.append([cx, cy])
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
if opts.resolution:
	resolution = int(opts.resolution)
if opts.save:
	save = True
if opts.xranges:
	xranges = opts.xranges.split('[')[1].split(']')[0].split(',')
	xranges[0] = float(xranges[0])
	xranges[1] = float(xranges[1])
if opts.yranges:
	yranges = opts.yranges.split('[')[1].split(']')[0].split(',')
	yranges[0] = float(yranges[0])
	yranges[1] = float(yranges[1])
if opts.legend:
	legend = True
if opts.plot:
	if opts.plot.lower() == 'raw':
		plot_raw = True
		plot_comps = False
	if opts.plot.lower() == 'false':
		show = False
	if opts.compare:
		compare = str(opts.compare)


if not (opts.trim or opts.deredshift or opts.demean or opts.interpolate or opts.pca):
	trim.trim(min_wave, max_wave, category)
	
	deredshift.deredshift(category)

	demean.demean_flux(category)

	if opts.rebin:
		if opts.rebin == 'linear':
			rebin = 'linear'
			interpolate.linear_rebinning(min_wave, max_wave, resolution, category)
		else:
			interpolate.log_rebinning(min_wave, max_wave, resolution, category)

	else:
		interpolate.log_rebinning(min_wave, max_wave, resolution, category)

	pca.run(category, rebin, n, pcomponents, save, plot_comps, plot_raw, xranges, yranges, legend, compare, show)

else:
	if opts.trim:
		trim.trim(min_wave, max_wave, category)
	if opts.deredshift:
		deredshift.deredshift(category)
	if opts.demean:
		demean.demean_flux(category)
	if opts.interpolate:
		if opts.rebin:
			if opts.rebin == 'linear':
				rebin = 'linear'
				interpolate.linear_rebinning(min_wave, max_wave, resolution, category)
			else:
				interpolate.log_rebinning(min_wave, max_wave, resolution, category)

		else:
			interpolate.log_rebinning(min_wave, max_wave, resolution, category)

	if opts.pca:
		pca.run(category, rebin, n, pcomponents, save, plot_comps, plot_raw, xranges, yranges, legend, compare, show)