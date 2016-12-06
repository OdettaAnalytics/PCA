import simplejson
import os

data_path = os.getenv("ODETTA_DATA_PATH", "")
out_path = "supernova_data/type_%s"
types = ["IIn", "Ia", "Ib"]

def open_sn_file(name):
    fname = data_path + name
    return open(fname, 'r').read()




if __name__ == "__main__":
    print open_sn_file("ptf2011fe.json")