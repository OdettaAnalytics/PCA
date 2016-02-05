__author__ = 'Leon liang'

'''
This Python file gets all of data using glob
and returns the data as a list of strings
that other functions can then utilize
'''

import glob, sys

def data(data_type, category = None, data_file = None):
	if type(category) == str:
		category = [category]

	if category is not None:
		data_path = []
		for c in category:
			if data_file is not None:
				data_path += (glob.glob('supernova_data/' + c + '/data/raw_data/' + data_file))
			elif data_type == 'raw':
				data_path += (glob.glob('supernova_data/' + c + '/data/raw_data/*'))
			else:
				data_path += (glob.glob('supernova_data/' + c + '/data/*' + data_type + '*'))
		return data_path
	else:
		if data_type == 'raw':
			return glob.glob('supernova_data/type*/data/raw_data/*')
		else:
			return glob.glob('supernova_data/type*/data/*' + data_type + '*')

def z_value():
	z_value = glob.glob('objects_z_values*')
	if len(z_value) == 0:
		print 'Cannot find Z value file'
		sys.exit()
	else:
		return z_value[0]

def types(category = None):
	path = glob.glob('supernova_data/type*')
	types = []
	for p in path:
		types.append(p.split('/')[1])
	return types
