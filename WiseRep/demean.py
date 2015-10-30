import numpy as np, os, os.path
import get_data


def demeaning(flux):
	mean = np.mean(flux)
	demeaned_flux = (flux/mean) - 1
	return demeaned_flux

def demean_flux():
	dataset = get_data.trimmed()
	for data in dataset:
		spectrum = np.loadtxt(data)
		wavelength = spectrum[:, 0]
		flux = spectrum[:, 1]
		# rest_of_spectrum = None
		[rows, columns] = spectrum.shape
		more_data = False
		if columns > 2:
			more_data = True
			rest_of_spectrum = spectrum[:, 2:]
		demeaned_flux = demeaning(flux)
		demean_spectrum = np.vstack([wavelength, demeaned_flux])
		if (more_data):
			[rows, columns] = rest_of_spectrum.shape
			for i in range(columns):
				demeaned_dat = np.vstack([demean_spectrum, rest_of_spectrum[:,i]])
		demean_spectrum = demean_spectrum.T 
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[3]
		if not (os.path.isdir('supernova_data/' + data_type + '/demeaned_data/')):
			os.mkdir('supernova_data/' + data_type + '/demeaned_data/')
		demeaned_data = 'supernova_data/' + data_type + '/demeaned_data/' + data_name
		np.savetxt(demeaned_data, demean_spectrum)


if __name__ == '__main__':
	demean_flux()




