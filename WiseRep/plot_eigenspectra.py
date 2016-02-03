__author__ = 'Leon Liang'

import numpy as np
import util.pca as pca
import matplotlib.pyplot as plt
import matplotlib.axis as ax

category = None
data_matrix = pca.form_matrix(category, data_type = 'log')
pca.normalize(data_matrix)
pca.compute_mean(data_matrix)
pca.demean(data_matrix)
pca.svd(data_matrix)
pca.compute_pca(data_matrix)
pca.reduce_pca(data_matrix, n = 6)


colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
for i in range(250):
	x = np.zeros([100])
	k = 0
	plt.figure()
	for data_category in data_matrix:
		coefficients_normal = data_matrix[data_category]['coefficients']['normal']
		[m,n] = coefficients_normal.shape
		plt.scatter(x[:n], coefficients_normal[i,:], color = colors[k%len(colors)], label = data_category)
		x += 1
		k += 1
	plt.scatter(x[0] + 2, np.array([0]), color = 'white')
	plt.legend()
	plt.title('Eigenspectra ' + str(i))
	name = 'supernova_data/all/plots/pca/coefficients/coefficient_' + str(i) + '.eps'
	plt.savefig(name, format='eps', dpi = 3500)
	plt.close()



