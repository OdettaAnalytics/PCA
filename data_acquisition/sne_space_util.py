import simplejson
import os

data_path = os.getenv("ODETTA_DATA_PATH", "")
out_path = "supernova_data/type_%s"
types = ["IIn", "Ia", "Ib"]


def read_sn_file(name):
    fname = data_path + "sne_space/" + name
    return open(fname, 'r').read()


def read_sn_file_path(path):
    return open(path, 'r').read()


def get_redshift(json):
    # return redshift value from one SN
    name = json.keys()[0]

    try:
        z_dicts = json[name]["redshift"]
    except KeyError:
        # some SNe have no redshift data
        return

    if len(z_dicts) != 1:
        print "multiple redshifts available; using first entry with source \"%s\" and kind \"%s\"" % \
              (z_dicts[0]["source"], z_dicts[0]["kind"])
    return z_dicts[0]["value"]


def get_random_SNe(n):
    import glob
    import random as rd

    fnames = glob.glob(data_path + "sne_space/*.json")
    n_avail = len(fnames)

    return [fnames[rd.randint(0, n_avail)] for i in range(n)]



if __name__ == "__main__":
    all_text = read_sn_file("SN2011fe.json")

    j = simplejson.loads(all_text)
    for path in get_random_SNe(10):
        j = simplejson.loads(read_sn_file_path(path))
        print get_redshift(j)
