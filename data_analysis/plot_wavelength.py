__author__ = 'Leon Liang'

'''
Taking the minimum wavelength value and the maximum
wavelength value divided by the redshift value (1+z)
to display a histogram of the maximum and minimum
wavelength observed in all of the types of supernovae
data downloaded

By default, a text file of all spectra's minimum and maximum 
wavelengths will be saved.
Addition option include:
	Plotting all types into one plot (--plot_all)
	Showing all plots (--show_plots)
	Saving all plots (--save_plots)
'''

import numpy as np
import matplotlib.pyplot as plt
import optparse
import sys

def extract_z_values(object_z_file):
	object_zvalues = np.genfromtxt(object_z_file, dtype='str')
	[num_objects, columns] = object_zvalues.shape
	object_names = object_zvalues[1:, 0]
	z_values = np.zeros(num_objects-1)

	for i in range(num_objects - 1):
		z_values[i] = float(object_zvalues[i+1, 1])

	return object_names, z_values

def find_min_max_wavelengths(data_list, objects, z_values):
	data_names = np.genfromtxt(data_list, dtype='str')
	[num_files, ] = data_names.shape
	max_wavelength = np.zeros(num_files)
	min_wavelength = np.zeros(num_files)

	for i in range(num_files):
		spectrum = np.loadtxt(data_names[i])
		wavelength = spectrum[:, 0]
		max_wavelength[i] = max(wavelength)
		min_wavelength[i] = min(wavelength)

	[num_objects, ] = objects.shape
	num_z_found = 0
	# objects_missed = ["" for x in range(300)]
	# num_z_missed = 0
	for i in range(num_files):
		for j in range(num_objects):
			if (data_names[i].find(objects[j]) != -1):
				max_wavelength[i] = max_wavelength[i]/(1+z_values[j])
				num_z_found = num_z_found + 1
				break
			# if (j == (num_objects - 1)):
			#     objects_missed[num_z_missed] = data_names[i]
			#     num_z_missed += 1

	return min_wavelength, max_wavelength

def filter_types(types):
	[num_files, ] = types.shape
	unique_types = np.unique(types)
	[num_types, ] = unique_types.shape
	change_point = np.zeros(num_types+1)
	types_seen = 1
	for i in range(1, num_files):
		if (types[i - 1] != types[i]):
			change_point[types_seen] = i
			types_seen += 1
	return unique_types, change_point

def gen_save_txt(data_list, min_wavelength, max_wavelength):
	data_file_names = np.genfromtxt(data_list, dtype='str', delimiter='/')
	[rows, dir_depth] = data_file_names.shape
	types = data_file_names[:, 0]
	# names = data_file_names[:, dir_depth -1 ]
	[unique_types, change_point] = filter_types(types)
	[num_types, ] = unique_types.shape
	for i in range(num_types):
		start = change_point[i]
		end = change_point[i + 1]
		if (end):
			gen_save_to_all_txt(data_file_names[start:end], min_wavelength[start:end], max_wavelength[start:end], func_call=True)
		else:
			gen_save_to_all_txt(data_file_names[start:], min_wavelength[start:], max_wavelength[start:], func_call=True)


def gen_save_to_all_txt(data_list, min_wavelength, max_wavelength, func_call=False):
	if (func_call):
		data_file_names = data_list
	else:
		data_file_names = np.genfromtxt(data_list, dtype='str', delimiter='/')

	[rows, dir_depth] = data_file_names.shape
	types = data_file_names[:, 0]
	names = data_file_names[:, dir_depth -1 ]
	wavelengths = np.vstack([types, names, min_wavelength, max_wavelength]).T

	labels = np.empty([1, 4], dtype='a16')
	labels[0, 0] = 'category'
	labels[0, 1] = 'dataset'
	labels[0, 2] = 'min_wavelength'
	labels[0, 3] = 'max_wavelength'

	if (func_call):
		wavelengths_txt = types[0] + '/plots/wavelength/min_max_wavelengths.txt'
		f = open(wavelengths_txt, 'w')
		np.savetxt(f, labels,  delimiter='\t', fmt="%s \t %s \t %s \t %s")
		np.savetxt(f, wavelengths, delimiter="\t", fmt="%s \t %s \t %s \t %s")
		f.close()
		print 'Saved minimum and maximum wavelength text file to ' + wavelengths_txt
	else:
		f = open('type_all/plots/wavelength/all_min_max_wavelengths.txt', 'w')
		np.savetxt(f, labels, delimiter='\t', fmt="%s \t %s \t %s \t %s"    )
		np.savetxt(f, wavelengths, fmt="%s \t %s \t %s \t %s")
		f.close()
		print 'Saved minimum and maximum wavelength text file to type_all/plots/wavelength/all_min_max_wavelengths.txt'

def plotting(data_list, min_wavelength, max_wavelength, plot_all, show_plots, save_plots):
	if (plot_all):
		print 'Plotting all supernovae types into one'
	else:
		print 'Plotting all supernovae types separately'

	if (show_plots):
		print 'Showing wavelength plots'

	if (plot_all):
		if (show_plots):
			plt.figure()
		max_plot = plt.subplot(211)
		plt.title("Min and Max Wavelengths of all Spectra")
		plt.hist(max_wavelength, label='Max')
		plt.xlabel("Wavelengths")
		plt.ylabel("Number of Spectra")
		plt.legend(['Max Wavelengths'])
		min_plot = plt.subplot(212)
		plt.hist(min_wavelength, label='Min')
		plt.legend(['Min Wavelengths'])
		plt.xlabel("Wavelengths")
		plt.ylabel("Number of Spectra")
		if (save_plots):
			plot_name = 'type_all/plots/wavelength/all_min_max_wavelengths.eps'
			plt.savefig(plot_name, format='eps', dpi=3500)
			print 'Saving plot as: type_all/plots/wavelength/all_min_max_wavelengths.eps'
		if (show_plots):
			plt.show()

	else:
		data_file_names = np.genfromtxt(data_list, dtype='str', delimiter='/')
		[rows, dir_depth] = data_file_names.shape
		types = data_file_names[:, 0]
		names = data_file_names[:, dir_depth -1 ]
		[unique_types, change_point] = filter_types(types)
		[num_types, ] = unique_types.shape
		for i in range(num_types):
			if (show_plots):
				plt.figure()
			start = int(change_point[i])
			end = int(change_point[i + 1])
			max_plot = plt.subplot(211)
			plt.title("Min and Max Wavelengths of all " + types[i] + " Spectra")
			if (end):
				plt.hist(max_wavelength[start:end], label='Max')
			else:
				plt.hist(max_wavelength[start:], label='Max')
			plt.xlabel("Wavelengths")
			plt.ylabel("Number of Spectra")
			plt.legend(['Max Wavelengths'])
			min_plot = plt.subplot(212)
			if (end):
				plt.hist(min_wavelength[start:end], label='Min')
			else:
				plt.hist(min_wavelength[start:], label='Min')
			plt.legend(['Min Wavelengths'])
			plt.xlabel("Wavelengths")
			plt.ylabel("Number of Spectra")
			if (save_plots):
				plot_name = types[start] + '/plots/wavelength/min_max_wavelengths.eps'
				plt.savefig(plot_name, format='eps', dpi=3500)
				print 'Saving plots as: ' + plot_name
			if (show_plots):
				plt.show()
			plt.clf()





parser = optparse.OptionParser()
parser.add_option("--plot_all",dest="plot_all")
parser.add_option("--show_plots",dest="show_plots")
parser.add_option("--save_plots",dest="save_plots")
(opts, args) = parser.parse_args()



if (opts.plot_all):
	if ((opts.plot_all.lower() == 'yes') | (opts.plot_all.lower() == 'y')):
		plot_all = True
	elif ((opts.plot_all.lower() == 'no') | (opts.plot_all.lower() == 'n')):
		plot_all = False
	else:
		print 'Please enter a valid option for plotting all: [y/n]'
		sys.exit()
else:
	plot_all = False

if (opts.show_plots):
	if ((opts.show_plots.lower() == 'yes') | (opts.show_plots.lower() == 'y')):
		show_plots = True
	elif ((opts.show_plots.lower() == 'no') | o(pts.show_plots.lower() == 'n')):
		show_plots = False
	else:
		print 'Please enter a valid option for showing plots: [y/n]'
		sys.exit()
else:
	show_plots = False

if (opts.save_plots):
	if ((opts.save_plots.lower() == 'yes') | (opts.save_plots.lower() == 'y')):
		save_plots = True
	elif ((opts.save_plots.lower() == 'no') | (opts.save_plots.lower() == 'n')):
		save_plots = False
	else:
		print 'Please enter a valid option for saving plots: [y/n]'
		sys.exit()
else:
	save_plots = False


num_args = len(args)

if (num_args != 2):
	print 'Please enter the valid file names: [data list] [object and z file]'
	sys.exit()
data_list = args[0]
object_z_file = args[1]





[objects, z_values] = extract_z_values(object_z_file)
[min_wavelength, max_wavelength] = find_min_max_wavelengths(data_list, objects, z_values)
if (plot_all):
	gen_save_to_all_txt(data_list, min_wavelength, max_wavelength)
else:
	gen_save_txt(data_list, min_wavelength, max_wavelength)

if (plot_all | show_plots | save_plots):
	plotting(data_list, min_wavelength, max_wavelength, plot_all, show_plots, save_plots)

print 'Finished calculating minimum and maximum wavelengths'