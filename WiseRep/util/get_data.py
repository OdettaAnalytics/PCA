__author__ = 'Leon liang'

'''
This Python file gets all of data using glob
and returns the data as a list of strings
that other functions can then utilize
'''

import glob, sys

def raw(category = None, dataset = None):
	if category is not None:
		data_path = []
		for c in category:
			if dataset:
				data_path += (glob.glob('supernova_data/' + c + '/data/raw_data/' + dataset))
			else:
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

def z_value():
	z_value = glob.glob('objects_z_values*')
	if len(z_value) == 0:
		print 'Cannot find Z value file'
		sys.exit()
	else:
		return z_value[0]

def types(category = None, data_type = None, type_all = False):
	types = glob.glob('supernova_data/type*')
	return types
