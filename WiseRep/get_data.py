import glob

def trimmed(category = None):
	if category is not None:
		return glob.glob(category + '/trimmed_data/*')
	else:
		return glob.glob('supernova_data/type*/trimmed_data/*')

def demeaned(category = None):
	if category is not None:
		return glob.glob(category + '/demeaned_data/*')
	else:
		return glob.glob('supernova_data/type*/demeaned_data/*')

def deredshift(category = None):
	if category is not None:
		return glob.glob(category + '/deredshift_data/*')
	else:
		return glob.glob('supernova_data/type*/deredshift_data/*')

def raw(category = None):
	if category is not None:
		return glob.glob(category + '/raw_data/*')
	else:
		return glob.glob('supernova_data/type*/raw_data/*')

def linear(category = None):
	if category is not None:
		return glob.glob(category + '/linear_rebin_data/*')
	else:
		return glob.glob('supernova_data/type*/linear_rebin_data/*')

def log(category = None):
	if category is not None:
		return glob.glob(category + '/log_rebin_data/*')
	else:
		return glob.glob('supernova_data/type*/log_rebin_data/*')

def hdf5(category = None):
	if category is not None:
		return glob.glob(category + '/hdf5_data/*')
	else:
		return glob.glob('supernova_data/type*/hdf5_data/*')


def all_hdf5(category = None):
	return glob.glob('supernova_data/type_all/hdf5_data/*')
	# return glob.glob('test.hdf5')

def types(category = None, data_type = None, type_all=False):
	if category is not None:
		if data_type is not None:
			if data_type == 'trimmed':
				return trimmed(category)
			if data_type == 'demeaned':
				return demeand(category)
			if data_type == 'deredshift':
				return deredshift(category)
			if data_type == 'raw':
				return raw_data(category)
			if data_type == 'linear':
				return linear(category)
			if data_type == 'log':
				return log(category)
			if data_type == 'hdf5':
				return hdf5(category)
	if type_all:
		return glob.glob('supernova_data/type*')
	else:
		types = glob.glob('supernova_data/type*')
		types.remove('supernova_data/type_all')
		return types
