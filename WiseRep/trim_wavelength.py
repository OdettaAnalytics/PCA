import numpy as np, os, os.path, sys
import get_data


def trim_wavelength(min_wave, max_wave):
	dataset = get_data.deredshift()
	for data in dataset:
		spectrum = np.loadtxt(data)
		wavelength = spectrum[:,0]
		if (min(wavelength) > min_wave):
			continue
		if (max(wavelength) < max_wave):
			continue
		[num_wave,] = wavelength.shape
		for i in range(num_wave):
			if wavelength[i] >= 4000:
				min_range_start = i
				break
		for j in xrange(num_wave-1, min_range_start, -1):
			if wavelength[j] <= 8000:
				max_range_start = j
				break
		trimmed_spectrum = spectrum[min_range_start:max_range_start+1,:]
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[3]
		if not (os.path.isdir('supernova_data/' + data_type + '/trimmed_data/')):
			os.mkdir('supernova_data/' + data_type + '/trimmed_data/')
		trimmed_wave = 'supernova_data/' + data_type + '/trimmed_data/' + data_name
		np.savetxt(trimmed_wave, trimmed_spectrum)

# need to store the indices of where wavelength is out of range
# and then use the same indices to keep the flux that's in the range 

if __name__ == '__main__':
	min_wave = 4000
	max_wave = 8000
	trim_wavelength(min_wave, max_wave)