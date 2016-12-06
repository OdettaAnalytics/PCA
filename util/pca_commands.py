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
coefficients_reduced = f1['coefficients_reduced'][:]
coefficients_normal = f1['coefficients_normal'][:]
U = f1['U'][:,:]
U_reduced = f1['U_reduced'][:,:]

data2 = get.data('pca', 'type_Ia')[0]
f2 = h5py.File(data2, 'r')
i = np.where(f2['keys'][:] == 'G15_0304_51609_436.dat')[0][0]
wavelength = f2['wavelength'][i,:]
flux2 = f2['flux'][i,:]

# data3 = get.data('pca', 'type_IIP')[0]
# f3 = h5py.File(data3, 'r')
# j = np.where(f3['keys'][:] == '2004dj_041115.ascii')[0][0]
# flux3 = f3['flux'][j,:]

# data4 = get.data('pca', 'type_Ib')[0]
# f4 = h5py.File(data4, 'r')
# k = np.where(f4['keys'][:] == 'iPTF13bvn_28junflxc.dat')[0][0]
# flux4 = f4['flux'][k,:]

# data5 = get.data('pca', 'type_IIb')[0]
# f5 = h5py.File(data5, 'r')
# m = np.where(f5['keys'][:] == 'SN1993J_19931217_photcal.dat')[0][0]
# flux5 = f5['flux'][m,:]

plt.plot(wavelength, flux2, label = 'type_Ia')
# plt.plot(wavelength, flux3, label = 'type_IIP')
# plt.plot(wavelength, flux4, label = 'type_Ib')
# plt.plot(wavelength, flux5, label = 'type_IIb')
for i in range(0, 1):
    plt.plot(wavelength, K_reduced[i,:], label = str(i))

plt.legend()
plt.show()

