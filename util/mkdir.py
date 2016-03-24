__author__ = 'Leon liang'

'''
This Python file will make necessary directories
that will be used to store all data that other 
Python files will be locating

init(): creates a initial directory "supernova_data" 
and a subdirectory for each of the category users want
analyze

data(): creates a directory inside [category]/data
to store all data generated from this data analysis

plots(): creates a directory that will be used to store
all plots related to the specific supernova
'''

import os, glob
import util.get as get

def init(category):
	'''
	init() creates an initial directory "supernova_data"
	and a subdirectory for each category users want to analyze

	Parameters
	----------
	category : a list of strings of categories
			   or a single string of category
	'''
	if type(category) == str:
		category = [category]
	for c in category:
		if not os.path.isdir('supernova_data/' + c):
			os.makedirs('supernova_data/' + c)
	data(category, data_type = 'raw')

def data(category = None, data_type = None):
	'''
	data() create a directory inside "supernova_data/[category]/data/"
	to store all data generated from this data analysis

	Parameters
	----------
	category : a list of strings of categories
			   or a single string of category

	data_type : a string indicating the data type (trimmed, demeaned, etc.)
	'''
	if type(category) == str:
		category = [category]
	if category is not None:
		for c in category:
			if not os.path.isdir('supernova_data/' + c + "/data"):
				os.makedirs('supernova_data/' + c + '/data')
			if data_type is not None:
				if not os.path.isdir('supernova_data/' + c + '/data/' + data_type):
					os.makedirs('supernova_data/' + c + '/data/' + data_type)
	else:
		categories = get.types()
		for category in categories:
			if not os.path.isdir('supernova_data/' + c + "/data"):
				os.makedirs('supernova_data/' + c + '/data/')
			if data_type is not None:
				if not os.path.isdir('supernova_data/' + category + '/data/' + data_type):
					os.makedirs('supernova_data/' + category + '/data/' + data_type)

def plots(category = None, data_type = None):
	'''
	plots() create a directory inside "supernova_data/[category]/plots/"
	to store all plots generated from this data analysisg

	Parameters
	----------
	category : a list of strings of categories
			   or a single string of category

	data_type : a string indicating the data type (trimmed, demeaned, etc.)
	'''
	if type(category) == str:
		category = [category]
	if category is not None:
		for c in category:
			if not os.path.isdir('supernova_data/' + c + "/plots"):
				os.makedirs('supernova_data/' + c + '/plots')
			if data_type is not None:
				if not os.path.isdir('supernova_data/' + c + '/plots/' + data_type):
					os.makedirs('supernova_data/' + c + '/plots/' + data_type)
	else:
		categories = get.types()
		for c in categories:
			if not os.path.isdir('supernova_data/' + c + "/plots"):
				os.makedirs('supernova_data/' + c + '/plots')
			if data_type is not None:
				if not os.path.isdir('supernova_data/' + c + '/plots/' + data_type):
					os.makedirs('supernova_data/' + c + '/plots/' + data_type)
