__author__ = 'Leon liang'

import glob, sys

def data(data_type, category = None, rebin_type = None, data_file = None):
	'''
	data() finds the necessary file paths and returns it as a list

	Parameters
	----------
	data_type : string indicating the data type wanted (raw, deredshift, trimmed, etc.)

	category : a list of strings of categories
			   or a single string of category

	rebin_type : string indicating the type of rebin wanted (log or linear)

	data_file : string of the specific raw data file wanted

	Returns
	-------
	data_path : list of strings of paths for the data wanted

	'''
	if type(category) == str:
		category = [category]
	if category is not None:
		data_path = []
		for c in category:
			if data_file is not None:
				data_path += (glob.glob('supernova_data/' + c + '/data/raw/' + data_file))
			elif data_type == 'raw':
				data_path += (glob.glob('supernova_data/' + c + '/data/raw/*'))
			elif rebin_type or data_type == 'rebin':
				if rebin_type == None:
					rebin_type = 'log'
				data_path += (glob.glob('supernova_data/' + c + '/data/*' + rebin_type + '*'))
			else:
				data_path += (glob.glob('supernova_data/' + c + '/data/*' + data_type + '*'))
		return data_path
	else:
		if data_type == 'raw':
			return glob.glob('supernova_data/type*/data/raw/*')
		elif data_type == 'rebin':
			if rebin_type == None:
				rebin_type = 'log'
			return glob.glob('supernova_data/type*/data/*' + rebin_type + '*')
		elif data_type == 'all':
			return glob.glob('supernova_data/all/data/all_pca.hdf5')
		else:
			return glob.glob('supernova_data/type*/data/*' + data_type + '*')

def z_value():
	'''
	z_value() returns the path of the z value file

	Returns
	-------
	z_value : string of the path of the z value file
	'''
	z_value = glob.glob('objects_z_values*')
	if len(z_value) == 0:
		print 'Cannot find Z value file'
		sys.exit()
	else:
		return z_value[0]

def types():
	'''
	types() returns the available category

	Returns
	-------
	types : list of strings of category
	'''
	path = glob.glob('supernova_data/type*')
	types = []
	for p in path:
		types.append(p.split('/')[1])
	return types
