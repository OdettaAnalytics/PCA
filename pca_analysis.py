# @author Leon Liang
#
# Takes in [filename] that consists of all data points
# of a supernova and do principal component analysis
# with [n] components

# importing necessary packages to do PCA analysis
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import sys

def data_T(data): # function used for transposing input data
	from numpy import array
	data_T = array(data).T # transposing input data
	return data_T

def normalize(data_T): 												# function used for normalizing tranposed data
	from numpy import array, shape, linalg, zeros
	[a,b] = data_T.shape 											# determining the dimnension of the input (transposed) data
	magnitude = zeros(a) 											# allocating memory for calculaing normalized data
	normalized_data_T = zeros([a,b]) 								# allocating memory for calculaing normalized data
	for i in range(a): 												# looping through each row to calculate the norm of data
		magnitude[i] = array(linalg.norm(data_T[i,:])) 				# using linalg.norm function to calculate the norm of data
	for j in range(a): 												# looping through matrix to divid components by the norm to normalize
		normalized_data_T[j,:] = data_T[j,:]/magnitude[j]
	return normalized_data_T

def calculate_mean(normal_data_T): 									# function to calculating the mean values of the normalized data
	from numpy import mean, array, hstack
	row1mean = array([0]) 											# first row does not need to be demeaned
	mean_list = array([mean(row) for row in normal_data_T[1:,:]]) 	# computing mean for each row
	mu = hstack([row1mean, mean_list]) 								# combining all means into matrix mu
	return mu

def demeaning(normal_data_T, mu): 									# function to demeaning the normalized, transposed data
	from numpy import array, zeros
	[a,b] = normal_data_T.shape 									# determing the dimensions of the normalized data
	demean_data_T = zeros([a,b]) 									# allocating memory for calculaing normalized data
	for i in range(a): 												# looping through the normal data and subtracting it from mean to demean
		demean_data_T[i,:] = normal_data_T[i,:] - mu[i]
	demean_data = demean_data_T.T 									# tranposing the demeaned data back to original shape
	return demean_data

def svd(demean_data_T): 											# function to calcuate the singular value decomposition (eigenvalues and eigenvectors)
																	# U is eigenvector, S is eigenvalue of U
	from numpy import linalg, diag, zeros
	[U, s, V_T] = linalg.svd(demean_data_T) 						# calculaing the singular value decomposition
	[a,b] = demean_data_T.shape 									# determing the shape of the demean_data matrix
	S = zeros([a,b]) 												# allocating memory for calculaing normalized data
	if (a < b):
		for i in range(a):
			S[i,i] = s[i] 											# making the values in s as a diagonal of matrix S
	else:
		S[:b,:b] = diag(s)
	return U, S, V_T, s

def dot_product(U, S, V_T): 										# function to calculate the dot product
	from numpy import dot
	X_pca = U.dot(S).dot(V_T) 										# dotting all three matrix to get PCA
	return X_pca

def compute_PCA(U, S, V_T, data): 									# function to compute the PCA
	V = V_T.T 														# tranposing V_T to V
	pca_matrix = (V.dot(S.T)).T
	coefficients = (U.T).dot(data)
	return pca_matrix, coefficients

def reducing_PCA(n, U, data): 										# function to reduce the PCA to only contain the important data
	from numpy import zeros
	U_reduced = zeros(U.shape) 										# allocating memory for calculaing normalized data
	for i in range(n): 												# looping through to keep only the 1st n components
		U_reduced[:,i] = U[:,i]
	coeffs_reduced = (U_reduced.T).dot(data)
	return U_reduced, coeffs_reduced

def plotting(U_reduced, coeffs_reduced, mu):
	from numpy import dot
	model = U_reduced.dot(coeffs_reduced) + mu 						# added the mean back to the data
	return model

# def eigens(pca_matrix):
# 	from numpy import dot, linalg
# 	W = pca_matrix.dot(pca_matrix.T)
# 	eigenvalues, eigenvectors = linalg.eig(W)

# first input is filename
# second input is the number of components want for PCA
# third input is a name for the PCA output file
# fourth input is the option to view a the data at a specific time
filename = sys.argv[1]
n = int(sys.argv[2])
pcomp_name = sys.argv[3]
time = int(sys.argv[4])
picture_name = sys.argv[5]

# np.set_printoptions(threshold=np.inf) used to display all elements in matrix


rebinned_data = np.loadtxt(filename)

data_T = data_T(rebinned_data)
normalized_data_T = normalize(data_T)
mu = calculate_mean(normalized_data_T)
demean_data_T = demeaning(normalized_data_T, mu)
[U, S, V_T, s] = svd(demean_data_T)
X_pca = dot_product(U, S, V_T)
pca_matrix, coefficients = compute_PCA(U, S, V_T, rebinned_data) # pca_matrix is eigenvectors
U_reduced, coeffs_reduced = reducing_PCA(n, U, rebinned_data)
model = plotting(U_reduced, coeffs_reduced, mu)

datapoints = coefficients[:2, :].T
f = open(pcomp_name, 'w')
np.savetxt(f, datapoints)
f.close()
# PCA coefficients
# need to plot these to see coeff components
c1 = datapoints[:,0]
c2 = datapoints[:,1]
# plt.scatter(c1, c2)
plt.xlabel('c1')
plt.ylabel('c2')

# generate a plot of data at [time]
plt.plot(model[:,time])

plt.savefig(picture_name, format='eps', dpi = 3500)
plt.show()


