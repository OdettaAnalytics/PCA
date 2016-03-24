__author__ = 'Leon Liang'

import h5py
import util.mkdir as mkdir

def write(data_category, data_name, data_filename, spectrum):
	'''
	write() takes in a numpy array and outputs to a HDF5 file

	Parameters
	----------
	data_category : a string of the supernova's category

	data_name : a string of the name of the raw data

	data_filename : a string of the output filename

	spectrum : numpy array of the data that is going to be output
	'''
	if data_category != 'all':	
		mkdir.init(data_category)
	mkdir.data(data_category)
	data_file = h5py.File('supernova_data/' + data_category + '/data/' + data_filename + '.hdf5', 'a')
	if data_name in data_file.keys():
		if data_file[data_name].shape != spectrum.shape:
			data_file.__delitem__(data_name)
			data_file[data_name] = spectrum
		else:
			data_file[data_name][...] = spectrum
	else:
		data_file.create_dataset(data_name, data = spectrum)
	data_file.close()