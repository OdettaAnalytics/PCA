# @author Leon Liang
#
# Takes in a text file that consists of all
# [filenames] and generate a .mspec with
# all data in one big file

import numpy as np
import sys


def combine_mspec(filename):

	[x,] = filename.shape # x to determine the number of file

	# an *.mspec file is [2499,3] size matrix

	spectrum = np.loadtxt(filename[0]) #, usecols=(0,1,4)) <-- no need for this anymore since all are 0,1,4 colums
									   # create the first matrix using the first file

	for i in range(1,x): # starting with 2nd element sinze the first was already created
		data = np.loadtxt(filename[i]) #, usecols=(0,1,4)) <-- no need for this anymore
		spectrum = np.hstack([spectrum, data])

	return spectrum


# first input is text file with all data file names
# secont input is a name for the output file
filenames = sys.argv[1]
filenames = np.genfromtxt(filenames, dtype='str')
spectrum = combine_mspec(filenames)
name = sys.argv[2]
np.savetxt(name, spectrum)

