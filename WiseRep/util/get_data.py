__author__ = 'Leon liang'

'''
This Python file gets all of data using glob
and returns the data as a list of strings
that other functions can then utilize
'''

import glob, sys

def raw(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/raw_data/*')
	else:
		return glob.glob('supernova_data/type*/data/raw_data/*')

def trimmed(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/*trim*')
	else:
		return glob.glob('supernova_data/type*/data/*trimmed*')

def deredshift(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/*deredshift*')
	else:
		return glob.glob('supernova_data/type*/data/*deredshift*')

def demeaned(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/*demean*')
	else:
		return glob.glob('supernova_data/type*/data/*demeaned')

def linear(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/*linear_rebin*')
	else:
		return glob.glob('supernova_data/type*/data/*linear_rebin*')

def log(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/*log_rebin*')
	else:
		return glob.glob('supernova_data/type*/data/*log_rebin*')

def hdf5(category = None, type_all = False):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/data/hdf5_data/*')
	else:
		if type_all:
			return glob.glob('supernova_data/type*/data/hdf5_data/*')
		else:
			# types = glob.glob('supernova_data/type*/data/hdf5_data/*')
			# types.remove('supernova_data/type_all/data/hdf5_data/type_all.hdf5')
			# return types
			types = glob.glob('supernova_data/type*/hdf5_data/*')
			types.remove('supernova_data/type_all/hdf5_data/type_all.hdf5')
			return types

def z_value():
	z_value = glob.glob('objects_z_values*')
	if len(z_value) == 0:
		print 'Cannot find Z value file'
		sys.exit()
	else:
		return z_value[0]

def all_hdf5(category = None):
	return glob.glob('supernova_data/type_all/hdf5_data/*')
	# for testing purposes:
	# return glob.glob('test.hdf5')

def types(category = None, data_type = None, type_all = False):
	if category is not None:
		if data_type is not None:
			if data_type == 'trimmed':
				return trimmed(category)
			if data_type == 'demeaned':
				return demeand(category)
			if data_type == 'deredshift':
				return deredshift(category)
			if data_type == 'raw':
				return raw_data(category)
			if data_type == 'linear':
				return linear(category)
			if data_type == 'log':
				return log(category)
			if data_type == 'hdf5':
				return hdf5(category)
	if type_all:
		return glob.glob('supernova_data/type*')
	else:
		types = glob.glob('supernova_data/type*')
		types.remove('supernova_data/type_all')
		return types
