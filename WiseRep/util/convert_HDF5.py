__author__ = 'Leon Liang'

import h5py, util.mkdir as mkdir

def write(data_category, data_name, data_type, spectrum):
	mkdir.data(data_category)
	data_file = h5py.File('supernova_data/' + data_category + '/data/' + data_type + '.hdf5', 'a')
	if data_name in data_file.keys():
		if data_file[data_name].shape != spectrum.shape:
			data_file.__delitem__(data_name)
			data_file[data_name] = spectrum
		else:
			data_file[data_name][...] = spectrum
	else:
		data_file.create_dataset(data_name, data = spectrum)
	data_file.close()
		
if __name__ == '__main__':
	convert_HDF5()