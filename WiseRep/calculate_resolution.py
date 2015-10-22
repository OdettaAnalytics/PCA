__author__ = 'Leon Liang'

# The resolutions of the spectrum determines how
# accurate the data can be. To calculate the
# resolutions of the spectrum, take the difference
# between each data point and find the average
# difference between each data point to calculate
# the resolutions of the spectrum

import numpy as np
import matplotlib.pyplot as plt
import sys

def calculate_resolutions(data_lists):
    data_names = np.genfromtxt(data_lists, dtype='str')
    [num_files, ] = data_names.shape
    resolutions = np.zeros([num_files])
    number_of_points = np.zeros([num_files])
    for i in range(num_files):
        data = np.loadtxt(data_names[i])
        [num_points, columns] = data.shape
        difference = np.zeros([num_points - 1, 1])
        for j in range(1, num_points):
            difference[j-1] = abs(data[j-1, 0] - data[j, 0])

        resolutions[i] = np.sum(difference)/num_points
        number_of_points[i] = num_points

    return resolutions, number_of_points


data_list = sys.argv[1]
supernova_type = sys.argv[2]
dir_path = sys.argv[3]

[resolutions, number_of_points] = calculate_resolutions(data_list)

data_names = np.genfromtxt(data_list, dtype='str', delimiter='/')
[rows, dir_depth] = data_names.shape
type_and_names = np.vstack([data_names[:, 0],data_names[:, dir_depth-1]]).T
save_file = np.vstack([type_and_names[:, 0], type_and_names[:, 1], number_of_points, resolutions]).T
labels = np.empty([1, 4], dtype='a16')
labels[0, 0] = 'category'
labels[0, 1] = 'dataset'
labels[0, 2] = 'resolutions'
labels[0, 3] = 'number_of_points'
resolutions_txt = dir_path + supernova_type + '_resolutions.txt'
f = open(resolutions_txt, 'w')
np.savetxt(f, labels, delimiter="\t", fmt="%s")
np.savetxt(f, save_file, delimiter="\t", fmt="%s")
f.close()


res = plt.scatter(number_of_points, resolutions)
plt.xlabel('Number of Points per Spectrum')
plt.ylabel('resolutions')
title = 'resolutions of ' + supernova_type + ' Spectrum'
plt.title(title)
plot_name = dir_path + supernova_type + '_resolutions.eps'
plt.savefig(plot_name, format='eps', dpi=3500)
# plt.show()

