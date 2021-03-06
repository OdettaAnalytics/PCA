__author__ = 'Leon Liang'

'''
This Python file takes trimmed and deredshifted spectra
and demean the flux values such that the mean for the 
flux values will be at zero

Outputs the demeaned spectra into a hdf5 file
'''

import numpy as np, h5py
import util.get as get
import util.convert_HDF5 as convert_HDF5

def demeaning(flux):
    mean = np.mean(flux)
    if (mean != 0):
        demeaned_flux = (flux/mean) - 1
        return demeaned_flux
    else:
        return flux

def demean_flux(category = None):
    data_path = get.data('trim', category)
    for data_file in data_path:
        dataset = h5py.File(data_file, 'r')
        data_category = data_file.split('/')[1]
        for data_name in dataset:
            name = str(data_name.split('.')[0])
            spectrum = dataset[data_name][:,:]
            wavelength = spectrum[:, 0]
            flux = spectrum[:, 1]
            demeaned_flux = demeaning(flux)
            demeaned_spectrum = np.vstack([wavelength, demeaned_flux])
            [nrows, ncolumns] = spectrum.shape
            rest_of_spectrum = None
            if ncolumns > 2:
                rest_of_spectrum = spectrum[:, 2:]
                [nrows, ncolumns] = rest_of_spectrum.shape
                for i in range(ncolumns):
                    demeaned_spectrum = np.vstack([demeaned_spectrum, rest_of_spectrum[:,i]])
            demeaned_spectrum = demeaned_spectrum.T
            data_filename = data_category + '_' + 'demean'
            convert_HDF5.write(data_category, str(data_name), data_filename, demeaned_spectrum)