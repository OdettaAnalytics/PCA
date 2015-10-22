import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import os, os.path
import glob
import sys
import optparse

def interpolation(min_wave, max_wave):
	data_dir = get_data_dir()
	f_x = []
	num_points = []
	for data in data_dir:
		spectrum = np.loadtxt(data)
		wavelength = spectrum[:,0]
		flux = spectrum[:,1]
		[num_waves,] = wavelength.shape
		f = interpolate.interp1d(wavelength, flux, bounds_error=False, fill_value=0)
		f_x.append(f)
		num_points.append(num_waves)
	return f_x, num_points

def get_data_dir():
	return glob.glob('supernova_data/type*/demeaned_data/*')

def log_rebinning(min_wave, max_wave):
	f_x, num_points = interpolation(min_wave, max_wave)
	data_dir = get_data_dir()
	index = 0
	for data in data_dir:
		num_waves = num_points[index]
		new_wavelength = np.logspace(np.log10(min_wave), np.log10(max_wave), num=num_waves, endpoint=False)
		f = f_x[index]
		new_flux = f(new_wavelength)
		new_rebin_data = np.vstack([new_wavelength, new_flux]).T
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[3]
		if not (os.path.isdir('supernova_data/' + data_type + '/log_rebin_data/')):
			os.mkdir('supernova_data/' + data_type + '/log_rebin_data/')
		rebin_new_wavelength_dir = 'supernova_data/' + data_type + '/log_rebin_data/' + data_name
		np.savetxt(rebin_new_wavelength_dir, new_rebin_data, delimiter='\t')
		print 'Rebinned data saved to ' + rebin_new_wavelength_dir
		index += 1
	return None

def linear_rebinning(min_wave, max_wave):
	f_x, num_points = interpolation(min_wave, max_wave)
	data_dir = get_data_dir()
	index = 0
	for data in data_dir:
		num_waves = num_points[index]
		new_wavelength = np.linspace(min_wave, max_wave, num=num_waves, endpoint=False)
		f = f_x[index]
		new_flux = f(new_wavelength)
		new_rebin_data = np.vstack([new_wavelength, new_flux]).T
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[3]
		if not (os.path.isdir('supernova_data/' + data_type + '/linear_rebin_data/')):
			os.mkdir('supernova_data/' + data_type + '/linear_rebin_data/')
		rebin_new_wavelength_dir = 'supernova_data/' + data_type + '/linear_rebin_data/' + data_name
		np.savetxt(rebin_new_wavelength_dir, new_rebin_data, delimiter='\t')
		print 'Rebinned data saved to ' + rebin_new_wavelength_dir
		index += 1
	return None

# if __name__ == '__main__':
# 	min_wave = 4000
# 	max_wave = 8000
# 	interpolation(min_wave, max_wave)
# 	rebinning(min_wave, max_wave)

parser = optparse.OptionParser()
parser.add_option("--rebin",dest="rebin")
(opts, args) = parser.parse_args()

if (opts.rebin):
	log = False
	linear = False
	if (opts.rebin.lower() == 'log'):
		log = True
	elif (opts.rebin.lower() == 'linear'):
		linear = True
	else:
		print 'Please enter a valid rebin option: [log / linear]'
		sys.exit()
else:
	log = True
	linear = False

if (log):
	print 'Logrithmic rebinning data...'

if (linear):
	print 'Linearly rebinning data...'

min_wave = 4000
max_wave = 8000
# interpolation(min_wave, max_wave)
if (log):
	log_rebinning(min_wave, max_wave)
if (linear):
	linear_rebinning(min_wave, max_wave)



