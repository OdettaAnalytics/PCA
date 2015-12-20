__author__ = 'Leon liang'

'''
This Python file will make necessary directories
that will be used to store all data that other 
Python files are looking for
'''

import os, glob
import util.get_data as get_data

def init(categories):
	for category in categories:
		if not os.path.isdir('supernova_data/' + category):
			os.makekdirs('supernova_data/' + category + '/data/r')

def plots(category = None, kind = None):
	if category is not None:
		if kind is not None:
			if not os.path.isdir('supernova_data/' + category + '/plots/' + kind):
				os.makedirs('supernova_data/' + category + '/plots/' + kind)
		else:
			if not os.path.isdir('supernova_data/' + category + '/plots/'):
				os.makedirs('supernova_data/' + category + '/plots/')
	else:
		categoryDir = get_data.types()
		for categoryDir in categoryDirs:
			if kind is not None:
				if not os.path.isdir(categoryDir + '/plots/' + kind):
					os.makedirs(categoryDir + '/plots/' + kind)
			else:
				if not os.path.isdir(categoryDir + '/plots'):
					os.makedirs(categoryDir + '/plots')


def data(category = None, kind = None):
	if category is not None:
		if kind is not None:
			if not os.path.isdir('supernova_data/' + category + '/data/' + kind):
				os.makedirs('supernova_data/' + category + '/data/' + kind)
		else:
			if not os.path.isdir('supernova_data/' + category + '/data/'):
				os.makedirs('supernova_data/' + category + '/data/')
	else:
		categoryDir = get_data.types()
		for categoryDir in categoryDirs:
			if kind is not None:
				if not os.path.isdir(categoryDir + '/data/' + kind):
					os.makedirs(categoryDir + '/data/' + kind)
			else:
				if not os.path.isdir(categoryDir + '/data'):
					os.makedirs(categoryDir + '/data')

# def remove(category=None, kind=None):


