import optparse

# parser = optparse.OptionParser()
# parser.add_option("--log",dest="log")
# parser.add_option("--linear",dest="linear")
# (opts, args) = parser.parse_args()

# if (opts.log):
# 	print "log rebin"

# if opts.linear:
# 	print "linear rebin"

import get_data_dir

print get_data_dir.get_data_dir()