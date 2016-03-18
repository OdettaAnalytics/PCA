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

def init(category):
	'''
	category: a list of supernova category
	'''
	if type(category) == str:
		category = [category]
	for c in category:
		if not os.path.isdir('supernova_data/' + c):
			os.makedirs('supernova_data/' + c)
	data(category, kind = 'raw')

def data(category = None, kind = None):
	'''
	category: the supernova's category
	kind: the data type that is needed (trimmed, demeaned, etc.)
	'''
	if type(category) == str:
		category = [category]
	if category is not None:
		for c in category:
			if not os.path.isdir('supernova_data/' + c + "/data"):
				os.makedirs('supernova_data/' + c + '/data')
			if kind is not None:
				if not os.path.isdir('supernova_data/' + c + '/data/' + kind):
					os.makedirs('supernova_data/' + c + '/data/' + kind)
	else:
		categories = get.types()
		for category in categories:
			if not os.path.isdir('supernova_data/' + c + "/data"):
				os.makedirs('supernova_data/' + c + '/data/')
			if kind is not None:
				if not os.path.isdir('supernova_data/' + category + '/data/' + kind):
					os.makedirs('supernova_data/' + category + '/data/' + kind)

def plots(category = None, kind = None):
	'''
	category: the supernova's category
	kind: the data type that is needed (trimmed, demeaned, etc.)
	'''
	if type(category) == str:
		category = [category]
	if category is not None:
		for c in category:
			if not os.path.isdir('supernova_data/' + c + "/plots"):
				os.makedirs('supernova_data/' + c + '/plots')
			if kind is not None:
				if not os.path.isdir('supernova_data/' + c + '/plots/' + kind):
					os.makedirs('supernova_data/' + c + '/plots/' + kind)
	else:
		categories = get.types()
		for c in category:
			if not os.path.isdir('supernova_data/' + c + "/plots"):
				os.makedirs('supernova_data/' + c + '/plots')
			if kind is not None:
				if not os.path.isdir('supernova_data/' + category + '/plots/' + kind):
					os.makedirs('supernova_data/' + category + '/plots/' + kind)

# def remove(category=None, kind=None):


