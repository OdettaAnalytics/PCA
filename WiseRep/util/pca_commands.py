# For testing purposes

category = None
data_matrix = pca.form_matrix(category, 'log')
pca.normalize(data_matrix)
pca.compute_mean(data_matrix)
pca.demean(data_matrix)
pca.svd(data_matrix)
pca.compute_pca(data_matrix)
pca.reduce_pca(data_matrix)

# For testing solutions
data_category = category[0]
coefficients_all = data_matrix[data_category]['coefficients']
coefficients_normal = coefficients_all['normal']
coefficients_reduced = coefficients_all['reduced']
U = data_matrix[data_category]['svd']['U']
S = data_matrix[data_category]['svd']['S']
V = data_matrix[data_category]['svd']['V']
wavelength = data_matrix[data_category]['wavelength']
flux = data_matrix[data_category]['flux']
U_reduced = data_matrix[data_category]['svd']['U_reduced']

K = (U.dot(coefficients_normal)).T
K_reduce = (U_reduced.dot(coefficients_reduced)).T

data_category = trim.keys()

# max vs min c0
plt.plot(trim[data_category[63]][:][:,0], trim[data_category[63]][:][:,1], label='min c0')
plt.plot(trim[data_category[47]][:][:,0], trim[data_category[47]][:][:,1], label='max c0')
plt.xlabel('trimmed wavelength')
plt.ylabel('flux')
plt.legend(['min c0', 'max c0'])
plt.show()

# max vs min c1
plt.plot(trim[data_category[19]][:][:,0], trim[data_category[19]][:][:,1], label='min c0')
plt.plot(trim[data_category[21]][:][:,0], trim[data_category[21]][:][:,1], label='max c0')
plt.xlabel('trimmed wavelength')
plt.ylabel('flux')
plt.legend(['min c1', 'near 0 c1'])
plt.show()

# plotting K_reduces

data1 = get.data('pca', 'all')[0]
f1 = h5py.File(data1, 'r')
K_normal = f1['K_normal'][:,:]
K_reduced = f1['K_reduced'][:,:]

data2 = get.data('rebin', rebin_type = 'log')[0] # for type_Ia
f2 = h5py.File(data2, 'r')
rebin = f['GM13_0480_51989_024.dat'][:,:]

wavelength = np.linspace(4000, 8000, 2000)

