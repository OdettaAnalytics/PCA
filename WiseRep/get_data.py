import glob

def trimmed():
	return glob.glob('supernova_data/type*/trimmed_data/*')

def demeaned():
	return glob.glob('supernova_data/type*/demeaned_data/*')

def deredshift():
	return glob.glob('supernova_data/type*/deredshift_data/*')

def raw():
	return glob.glob('supernova_data/type*/raw_data/*')

def linear():
	return glob.glob('supernova_data/type*/linear_rebin_data/*')

def log():
	return glob.glob('supernova_data/type*/linear_rebin_data/*')

def hdf5():
	return glob.glob('supernova_data/type*/hdf5_data/*')

def all_hdf5():
	return glob.glob('supernova_data/type_all/hdf5_data/*')