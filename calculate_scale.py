__author__ = 'Leon Liang'

# Python code to calculate the scale of the 
# flux values of supernova

import numpy as np 
import matplotlib.pyplot as plt
import sys

def calculate_scale(data_list):
	data_names = np.genfromtxt(data_list, dtype='str')
	[num_files, ] = data_names.shape
	num_flux_vals = np.zeros([num_files])
	scale = np.zeros([num_files])
	average_flux = np.zeros([num_files])

	for i in range(num_files):
		data = np.loadtxt(data_names[i])
		[num_points, columns] = data.shape
		average_flux[i] = np.nanmean(data[:,1])
		num_flux_vals[i] = num_points
		if (average_flux[i] > 0):
			scale[i] = np.log10(average_flux[i])

	return num_flux_vals, average_flux, scale

def gen_save_info(data_list, num_flux_vals, scale):
	data_info = np.genfromtxt(data_list, dtype='str', delimiter='/')
	labels = np.empty([1, 4], dtype='a16')
	labels[0, 0] = 'types'
	labels[0, 1] = 'dataset'
	labels[0, 2] = 'num_flux_vals'
	labels[0, 3] = 'scale'
	types = data_info[:, 0]
	dataset_names = data_info[:, 2]
	[unique_types, change_point] = filter_types(types)
	[num_types, ] = unique_types.shape
	for i in range(num_types):
		start = change_point[i]
		end = change_point[i + 1]
		if (end):
			save_file_info = np.vstack([types[start:end], dataset_names[start:end], num_flux_vals[start:end], scale[start:end]]).T
		else:
			save_file_info = np.vstack([types[start:], dataset_names[start:], num_flux_vals[start:], scale[start:]]).T

		scale_txt = types[start] + '/plots/scale/' + types[start] + '_scale.txt'
		f = open(scale_txt, 'w')
		np.savetxt(f, labels, delimiter="\t", fmt="%s")
		np.savetxt(f, save_file_info, delimiter="\t", fmt="%s")
		f.close()
	return types, dataset_names

def plot_scale(types, dataset_names, scale, num_flux_vals):
	[unique_types, change_point] = filter_types(types)
	[num_types, ] = unique_types.shape
	for i in range(num_types):
		start = int(change_point[i])
		end = int(change_point[i + 1])
		if (end):
			scale_plot = plt.scatter(num_flux_vals[start:end], scale[start:end])
		else:
			scale_plot = plt.scatter(num_flux_vals[start:], scale[start:])
		plt.xlabel('Number of Flux Values per Spectrum')
		plt.ylabel('Scale (log10)')
		title = 'Scale of ' + unique_types[i]
		plt.title(title)
		plot_name = types[start] + '/plots/scale/' + types[start] + '_scale.eps'
		plt.savefig(plot_name, format='eps', dpi=3500)
		plt.clf()
	# scale_plot = plt.scatter(num_flux_vals[change_point[num_types - 1]:], scale[change_point[num_types - 1]:])
	# plt.xlabel('Number of Flux Values per Spectrum')
	# plt.ylabel('Scale (log10)')
	# title = 'Scale of ' + unique_types[num_types - 1]
	# plt.title(title)
	# plot_name = types[change_point[num_types - 1]] + '/plots/scale/' + types[change_point[num_types - 1]] + '_scale.eps'
	# plt.savefig(plot_name, format='eps', dpi=3500)
	# plt.clf()

def filter_types(types):
	[num_files, ] = types.shape
	unique_types = np.unique(types)
	[num_types, ] = unique_types.shape
	change_point = np.zeros(num_types + 1)
	types_seen = 1
	for i in range(1, num_files):
		if (types[i - 1] != types[i]):
			change_point[types_seen] = i
			types_seen += 1
	return unique_types, change_point


data_list = sys.argv[1]
# supernova_type = sys.argv[2]
# dir_path = sys.argv[3]

[num_flux_vals, average_flux, scale] = calculate_scale(data_list)
[types, dataset_names] = gen_save_info(data_list, num_flux_vals, scale)
plot_scale(types, dataset_names, scale, num_flux_vals)



