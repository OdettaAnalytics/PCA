category = 'type_all'
data_matrix = pca.form_matrix(category)
pca.normalize(data_matrix)
pca.demean(data_matrix)
pca.svd(data_matrix)
pca.dot_product(data_matrix)
pca.compute_pca(data_matrix)
pca.reduce_pca(data_matrix, 6)

# For testing solutions
data_type = category
coefficients = data_matrix[data_type]['coefficients']['normal']
coefficients_reduced = data_matrix[data_type]['coefficients']['reduced']
U = data_matrix[data_type]['svd']['U']
S = data_matrix[data_type]['svd']['S']
V = data_matrix[data_type]['svd']['V']
wavelength = data_matrix[data_type]['wavelength']
flux = data_matrix[data_type]['flux']
U_reduced = data_matrix[data_type]['svd']['U_reduced']

K = (U.dot(coefficients)).T
K_reduce = (U_reduced.dot(coefficients_reduced)).T

q = 6

plt.plot(wavelength[q,:], flux[q,:])
plt.plot(wavelength[q,:], K[q,:])
plt.plot(wavelength[q,:], K_reduce[q,:])
plt.show()


# c1 = coefficients[0,:]
# c2 = coefficients[1,:]
# c3 = coefficients[2,:]
# c4 = coefficients_reduced[3,:]
# c5 = coefficients_reduced[4,:]

# # reduced coefficients
c1 = coefficients_reduced[0,:]
c2 = coefficients_reduced[1,:]
c3 = coefficients_reduced[2,:]
# c4 = coefficients_reduced[3,:]
# c5 = coefficients_reduced[4,:]

plt.scatter(c1, c2, color='blue')
plt.scatter(c1, c3, color='red')
# plt.scatter(c1, c4, color='green')
plt.scatter(c2, c3, color='black')
# plt.scatter(c2, c4, color='pink')
# plt.scatter(c3, c4, color='purple')

plt.show()


# For testing solutions with all data_type
n = 3
data_matrix = pca.form_matrix()
pca.normalize(data_matrix)
pca.demean(data_matrix)
pca.svd(data_matrix)
pca.dot_product(data_matrix)
pca.compute_pca(data_matrix)
pca.reduce_pca(data_matrix, n)

colors = ['blue', 'red', 'pink', 'orange', 'green', 'purple', 'black']
plots = []
plotNames = []
i = 0
for data_type in data_matrix:
	if data_type != 'type_test':
		print 'plotting ' + str(data_type)
		coefficients = data_matrix[data_type]['coefficients']['normal']
		coefficients_reduced = data_matrix[data_type]['coefficients']['reduced']
		U = data_matrix[data_type]['svd']['U']
		S = data_matrix[data_type]['svd']['S']
		V = data_matrix[data_type]['svd']['V']
		wavelength = data_matrix[data_type]['wavelength']
		flux = data_matrix[data_type]['flux']
		U_reduced = data_matrix[data_type]['svd']['U_reduced']

		K = (U.dot(coefficients)).T
		K_reduce = (U_reduced.dot(coefficients_reduced)).T
		c1 = coefficients_reduced[0,:]
		c2 = coefficients_reduced[1,:]
		p = plt.scatter(c1, c2, color=colors[i], label=data_type)
		plots.append(p)
		plotNames.append(data_type)
		plt.xlabel('c1')
		plt.ylabel('c2')
		i += 1


plt.legend(plots, plotNames)
plt.show()

# For testing solution on plotting components in a straight line for spectrum from t = 1, ... , n
n = 6
category = 'type_test'
data_matrix = pca.form_matrix(category)
pca.normalize(data_matrix)
pca.demean(data_matrix)
pca.svd(data_matrix)
pca.dot_product(data_matrix)
pca.compute_pca(data_matrix)
pca.reduce_pca(data_matrix, n)

data_type = category
coefficients = data_matrix[data_type]['coefficients']['normal']
coefficients_reduced = data_matrix[data_type]['coefficients']['reduced']
U = data_matrix[data_type]['svd']['U']
S = data_matrix[data_type]['svd']['S']
V = data_matrix[data_type]['svd']['V']
wavelength = data_matrix[data_type]['wavelength']
flux = data_matrix[data_type]['flux']
U_reduced = data_matrix[data_type]['svd']['U_reduced']

K = (U.dot(coefficients)).T
K_reduce = (U_reduced.dot(coefficients_reduced)).T

c1 = coefficients_reduced[0,:]
c2 = coefficients_reduced[1,:]
c3 = coefficients_reduced[2,:]

l = ['c1c2', 'c1c3', 'c2c3']
p1 = plt.plot(c1, c2, color='blue')
p2 = plt.plot(c1, c3, color='green')
p3 = plt.plot(c2, c3, color='black')
plt.show()

