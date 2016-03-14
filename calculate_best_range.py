__author__ = 'Leon Liang'

import numpy as np
import matplotlib.pyplot as plt
import sys

def calculate_best_range(wavelengths_list):
	wavelengths = np.genfromtxt(wavelengths_list, dtype='str')
	[num_wavelengths, columns] = wavelengths.shape
	min_wavelength = np.zeros(num_wavelengths)
	max_wavelength = np.zeros(num_wavelengths)
	for i in range(1, num_wavelengths):
		min_wavelength[i - 1] = float(wavelengths[i, 2])
		max_wavelength[i - 1] = float(wavelengths[i, 3])

	delta = np.linspace(1000, 10000, 10)
	min_waves = np.linspace(2000, 7000, 8)
	mat = np.zeros([len(min_waves), len(delta)])

	for i in range(len(min_waves)):
		for j in range(len(delta)):
			for k in range(num_wavelengths - 1):
				if ((min_wavelength[k] <= min_waves[i]) & (max_wavelength[k] >= min_wavelength[k] + delta[j])):
						mat[i,j] += 1

	plt.contourf(min_waves, delta, mat.T)
	plt.colorbar()
	plt.xlabel('Minimum wavelength')
	plt.ylabel('Delta')
	plt.title('Best Wavenlength Range')
	plot_name = 'type_all/plots/wavelength/best_range.eps'
	plt.savefig(plot_name, format='eps', dpi=3500)
	plt.show()


wavelengths_list = 'type_all/plots/wavelength/all_min_max_wavelengths.txt'
calculate_best_range(wavelengths_list)
