# @author Leon Liang
#
# Takes in a text file that consists of all
# [filenames] and generate a .mspec with
# all data in one big file

import numpy as np
import glob
import sys


def combine_mspec(list_of_data):

	[num_files,] = list_of_data.shape # num_files to determine the number of file

	# a *.mspec file we're using is [2499,3] size matrix

	spectrum = np.loadtxt(list_of_data[0]) #, usecols=(0,1,4)) <-- no need for this anymore since all are 0,1,4 colums
									   # create the first matrix using the first file
	if (num_files > 1):							   
		for i in range(1, num_files): # starting with 2nd element since the first was already created
			data = np.loadtxt(list_of_data[i]) #, usecols=(0,1,4)) <-- no need for this anymore
			spectrum = np.hstack([spectrum, data])

	return spectrum

def check_data_exists(list_of_data):

# first input is text file with all data file names
# secont input is a name for the output file

if (len(sys.argv) >= 2):
	list_of_data = sys.argv[1]
	file_exists = check_data_exists(list_of_data)
	if (!file_exists):
		print 'File does not exist. Please input a valid data'

		print 'Did not enter a name for output file. Using defaul name: all.mspec'


	if (len(sys.argv) > 2):
		combined_data_name = sys.argv[2]
		print 'Saving output files to ' + combined_data_name



list_of_data = np.genfromtxt(list_of_data, dtype='str')
spectrum = combine_mspec(list_of_data)

combined_data_name = sys.argv[2]
np.savetxt(combined_data_name, spectrum)

# save_to_hdf5() to output these to binary