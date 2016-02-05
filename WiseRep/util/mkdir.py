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
import util.get as get

def init(categories):
	'''
	categories: a list of supernova categories
	'''
	for category in categories:
		if not os.path.isdir('supernova_data/' + category):
			os.makekdirs('supernova_data/' + category)

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
		categories = get.types()
		for category in categories:
			if kind is not None:
				if not os.path.isdir('supernova_data/' + category + '/data/' + kind):
					os.makedirs('supernova_data/' + category + '/data/' + kind)
			else:
				if not os.path.isdir('supernova_data/' + category + '/data/'):
					os.makedirs('supernova_data/' + category + '/data/')

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
		categories = get.types()
		for category in categories:
			if kind is not None:
				if not os.path.isdir('supernova_data/' + category + '/plots/' + kind):
					os.makedirs('supernova_data/' + category + '/plots/' + kind)
			else:
				if not os.path.isdir('supernova_data/' + category + '/plots/'):
					os.makedirs('supernova_data/' + category + '/plots/')

# def remove(category=None, kind=None):


