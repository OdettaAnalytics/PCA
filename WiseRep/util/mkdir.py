__author__ = 'Leon liang'

'''
This Python file will make necessary directories
that will be used to store all data that other 
Python files will be locating

init(): creates a initial directory "supernova_data" 
that will later contain all of the different categories
of supernovae and its data, plots, etc.

data(): creates a directory that will house different
categories of supernovae

plots(): creates a directory that will be used to store
all plots related to the specific supernova
'''

import os, glob
import util.get_data as get_data

def init(categories):
	'''
	categories: a list of supernova categories
	'''
	for category in categories:
		if not os.path.isdir('supernova_data/' + category):
			os.makekdirs('supernova_data/' + category + '/data/r')

def data(category = None, kind = None):
	'''
	category: the supernova's category
	kind: the data type that is needed (trimmed, demeaned, etc.)
	'''
	if category is not None:
		if kind is not None:
			if not os.path.isdir('supernova_data/' + category + '/data/' + kind):
				os.makedirs('supernova_data/' + category + '/data/' + kind)
		else:
			if not os.path.isdir('supernova_data/' + category + '/data/'):
				os.makedirs('supernova_data/' + category + '/data/')
	else:
		category_dirs = get_data.types()
		for category_dir in category_dirs:
			if kind is not None:
				if not os.path.isdir(category_dir + '/data/' + kind):
					os.makedirs(category_dir + '/data/' + kind)
			else:
				if not os.path.isdir(category_dir + '/data/'):
					os.makedirs(category_dir + '/data/')

def plots(category = None, kind = None):
	'''
	category: the supernova's category
	kind: the data type that is needed (trimmed, demeaned, etc.)
	'''
	if category is not None:
		for c in category:
			if kind is not None:
				if not os.path.isdir('supernova_data/' + c + '/plots/' + kind):
					os.makedirs('supernova_data/' + c + '/plots/' + kind)
			else:
				if not os.path.isdir('supernova_data/' + c + '/plots/'):
					os.makedirs('supernova_data/' + c + '/plots/')
	else:
		category_dirs = get_data.types()
		for category_dir in category_dirs:
			if kind is not None:
				if not os.path.isdir(category_dir + '/plots/' + kind):
					os.makedirs(category_dir + '/plots/' + kind)
			else:
				if not os.path.isdir(category_dir + '/plots/'):
					os.makedirs(category_dir + '/plots/')

# def remove(category=None, kind=None):


