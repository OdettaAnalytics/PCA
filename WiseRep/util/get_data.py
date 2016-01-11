__author__ = 'Leon liang'

'''
This Python file gets all of data using glob
and returns the data as a list of strings
that other functions can then utilize
'''

import glob, sys

def raw(category = None):
	if category is not None:
		data_path = []
		for c in category:
			data_path += (glob.glob('supernova_data/' + c + '/data/raw_data/*'))
		return data_path
	else:
		return glob.glob('supernova_data/type*/data/raw_data/*')

def trim(category = None):
	if category is not None:
		data_path = []
		for c in category:
			data_path += (glob.glob('supernova_data/' + c + '/data/*trim*'))
		return data_path
	else:
		return glob.glob('supernova_data/type*/data/*trim*')

def deredshift(category = None):
	if category is not None:
		data_path = []
		for c in category:
			data_path += (glob.glob('supernova_data/' + c + '/data/*deredshift*'))
		return data_path
	else:
		return glob.glob('supernova_data/type*/data/*deredshift*')

def demean(category = None):
	if category is not None:
		data_path = []
		for c in category:
			data_path += (glob.glob('supernova_data/' + c + '/data/*demean*'))
		return data_path
	else:
		return glob.glob('supernova_data/type*/data/*demean*')

def linear(category = None):
	if category is not None:
		data_path = []
		for c in category:
			data_path += (glob.glob('supernova_data/' + c + '/data/*linear_rebin*'))
		return data_path
	else:
		return glob.glob('supernova_data/type*/data/*linear_rebin*')

def log(category = None):
	if category is not None:
		data_path = []
		for c in category:
			data_path += (glob.glob('supernova_data/' + c + '/data/*log_rebin*'))
		return data_path
	else:
		return glob.glob('supernova_data/type*/data/*log_rebin*')

# def hdf5(category = None, type_all = False):
# 	if category is not None:
# 		return glob.glob('supernova_data/' + category + '/data/hdf5_data/*')
# 	else:
# 		if type_all:
# 			return glob.glob('supernova_data/type*/data/hdf5_data/*')
# 		else:
# 			# types = glob.glob('supernova_data/type*/data/hdf5_data/*')
# 			# types.remove('supernova_data/type_all/data/hdf5_data/type_all.hdf5')
# 			# return types
# 			types = glob.glob('supernova_data/type*/hdf5_data/*')
# 			types.remove('supernova_data/type_all/hdf5_data/type_all.hdf5')
# 			return types

def z_value():
	z_value = glob.glob('objects_z_values*')
	if len(z_value) == 0:
		print 'Cannot find Z value file'
		sys.exit()
	else:
		return z_value[0]

# def all_hdf5(category = None):
# 	return glob.glob('supernova_data/type_all/hdf5_data/*')
# 	# for testing purposes:
# 	# return glob.glob('test.hdf5')

def types(category = None, data_type = None, type_all = False):
	types = glob.glob('supernova_data/type*')
	types.remove('supernova_data/type_all')
	return types
