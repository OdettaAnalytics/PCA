import numpy as np, os, os.path, sys, glob
import util.get_data as get_data
import util.mkdir as mkdir

def extract_z_values(object_z_file):
	object_zvalues = np.genfromtxt(object_z_file, dtype='str')
	[num_objects, columns] = object_zvalues.shape
	object_names = object_zvalues[1:, 0]
	z_values = np.zeros(num_objects-1)

	for i in range(num_objects - 1):
		z_values[i] = float(object_zvalues[i+1, 1])

	return object_names, z_values

def deredshift(category = None):
	dataset = get_data.raw(category)
	object_z_file = get_data.z_value()
	object_names, z_values = extract_z_values(object_z_file)
	for data in dataset:
		spectrum = np.loadtxt(data)
		wavelength = spectrum[:, 0]
		rest_of_spectrum = spectrum[:, 1:]
		num_objects = len(object_names)
		z_value = None
		for j in range(num_objects):
			if (data.find(object_names[j]) != -1):
				z_value = z_values[j]
				break
		if (z_value == None):
			print 'No such z value for ' + data
			sys.exit()
		deredshift_wavelength = wavelength/(1 + z_value)
		deredshift_spectrum = deredshift_wavelength
		[rows, columns] = rest_of_spectrum.shape
		for i in range(columns):
			deredshift_spectrum = np.vstack([deredshift_spectrum, rest_of_spectrum[:,i]])
		deredshift_spectrum = deredshift_spectrum.T
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[4]
		mkdir.data(category=data_type, kind='deredshift_data')
		# if not (os.path.isdir('supernova_data/' + data_type + '/deredshift_data/')):
		# 	os.mkdir('supernova_data/' + data_type + '/deredshift_data/')
		deredshift_data = 'supernova_data/' + data_type + '/data/deredshift_data/' + data_name
		np.savetxt(deredshift_data, deredshift_spectrum)

if __name__ == '__main__':
	deredshift()
