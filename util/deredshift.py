__author__ = 'Leon Liang'

import numpy as np, sys
import util.get as get
import util.mkdir as mkdir
import util.convert_HDF5 as convert_HDF5

def extract_z_values(object_z_file):
    '''
    extracts z value from the text file

    Parameter
    ---------
    object_z_file : string of the path to the z value text file

    Returns
    -------
    object_names : numpy array of strings of each of the object name

    z_values : numpy array of the z values corresponding to each object name
    '''
    object_zvalues = np.genfromtxt(object_z_file, dtype = 'str')
    [num_objects, columns] = object_zvalues.shape
    object_names = object_zvalues[1:, 0]
    z_values = np.zeros(num_objects-1)
    for i in range(num_objects - 1):
        z_values[i] = float(object_zvalues[i+1, 1])
    return object_names, z_values

def run(category = None):
    '''
    run() deredshifts all raw data from each category based on
    z value found and outputs to HDF5 File

    Parameter
    ---------
    category : list of category to deredshift
    '''
    data_path = get.data('raw', category)
    object_z_file = get.z_value()
    object_names, z_values = extract_z_values(object_z_file)
    for data_file in data_path:
        filename = data_file.split('/')
        data_category = filename[1]
        data_name = filename[len(filename)-1]
        name = data_name.split('.')[0]
        spectrum = np.loadtxt(data_file)
        wavelength = spectrum[:, 0]
        rest_of_spectrum = spectrum[:, 1:]
        z_value = None
        for j in range(len(object_names)):
            if (name.find(object_names[j]) != -1):
                z_value = z_values[j]
                break
        if z_value != None:
            deredshift_wavelength = wavelength/(1 + z_value)
            deredshift_spectrum = deredshift_wavelength
            [rows, columns] = rest_of_spectrum.shape
            for i in range(columns):
                deredshift_spectrum = np.vstack([deredshift_spectrum, rest_of_spectrum[:,i]])
            deredshift_spectrum = deredshift_spectrum.T
            data_filename = data_category + '_' + 'deredshift'
            convert_HDF5.write(data_category, str(data_name), data_filename, deredshift_spectrum)
        else:
            print 'Cannot find z value for ' + str(data_name)
