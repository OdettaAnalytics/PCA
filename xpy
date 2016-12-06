#!/usr/bin/python
import optparse
import glob
import sys
import numpy as np
import pylab as py
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import rc
import matplotlib

rc('text', usetex=True)
matplotlib.rcParams.update({'figure.autolayout': True})

#matplotlib.rcParams['mathtext.fontset'] = 'stix'
#matplotlib.rcParams['font.family'] = 'STIXGeneral'

#Direct input 
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options
params = {'text.usetex' : True,
          'font.size' : 22,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          }
plt.rcParams.update(params) 

fig = plt.figure()
# Data manipulation:

def make_segments(x, y):
    '''
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    '''

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    return segments


# Interface to LineCollection:

def colorline(x, y, z=None, map=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0):
    '''
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    '''
    
    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))
           
    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])
        
    z = np.asarray(z)
    
    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)
    
    ax = plt.gca()
    ax.add_collection(lc)
    
    return lc
        
    
def clear_frame(ax=None): 
    # Taken from a post by Tony S Yu
    if ax is None: 
        ax = plt.gca() 
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False) 
    for spine in ax.spines.itervalues(): 
        spine.set_visible(False) 

#cm = py.get_cmap('rainbow')











# main XPY function


parser = optparse.OptionParser()
parser.add_option("-x",dest="cols")
parser.add_option("-s",dest="ofile")
parser.add_option("-l",dest="log")
parser.add_option("-n",action="store_true", dest="norm")
parser.add_option("-m",action="store_true", dest="max")
parser.add_option("--title",dest="titl")
parser.add_option("--xr",dest="xrange")
parser.add_option("--yr",dest="yrange")
parser.add_option("--yt",dest="ytitle")
parser.add_option("--xt",dest="xtitle")
parser.add_option("--math",dest="math")
parser.add_option("--line",dest="linestyle")
parser.add_option("--legend",dest="legend")
parser.add_option("--legendloc",dest="legendloc")
parser.add_option("--legendtextsize",dest="legend_text_size")
parser.add_option("--offset",dest="offset")
parser.add_option("--shift",dest="shift")
parser.add_option("--color",dest="color")
parser.add_option("--size",dest="markersize")
parser.add_option("--cumul",dest="cumul")
parser.add_option("--skip",dest="n_header", default=0, type=int)
parser.add_option("--filter",dest="file_name_filter")
parser.add_option("--add-zero",dest="add_zero", default=0, type=int)
parser.add_option("--sort-by-col",dest="i_sort", default=0, type=int)
parser.add_option("--vlines",dest="vline_x")



(opts, args) = parser.parse_args()
print args

files = []
for a in args:
    fnames = glob.glob(a)
    for f in fnames:
        if opts.file_name_filter:
            if opts.file_name_filter not in f:
                files.append(f)
        else:
            files.append(f)
args = files
print args
n = len(args)

xcol = []
ycol = []
names = None
if (opts.cols):
   col_plot = opts.cols.split(',')
   if len(col_plot) > 1 and n == 1:
      # plot multiple columns for a single file
      n = len(col_plot)
      args = args*n
      xcol = [int(z.split(":")[0])-1 for z in col_plot]
      ycol = [int(z.split(":")[1])-1 for z in col_plot]
      names = [ "Col %d" % d for d in range(1,n+1) ]
      loc = 0
   elif len(col_plot) == 1 and n == 1 and col_plot[0]=="all":
      data = np.loadtxt(args[0])
      if opts.cumul:
          n = len(data[0, :])-1
      else:
          n = len(data[0, :])-2
      args = args*n
      xcol = [0]*n
      ycol = range(1, n+1)
      names = [ "Col %d" % d for d in range(1,n+1) ]
      loc = 0
   else:
      for cp in col_plot:
         cols =  cp.split(':')
         if len(cols) != 2:
            print "must specify columns like so.. python xpy <filenames> -x 1:2,1:3"
            sys.exit() 

         if (n > 1) and (len(col_plot)==1):
            # assume the same columns for all files
            xcol = [int(cols[0]) - 1]*n
            ycol = [int(cols[1]) - 1]*n
         else:
            xcol.append(int(cols[0]) - 1)
            ycol.append(int(cols[1]) - 1)
else:
   xcol = [0]*n
   ycol = [1]*n

if (opts.markersize):
    markersize = int(opts.markersize)
else: 
    markersize = 4

if (opts.linestyle):
    line = opts.linestyle.split(',')
    if (n > 1 and len(line) == 1):
        line = line*n
elif opts.cumul:
    line = ['o']*(n-1)
    line.append('-')

else:
    line = ['']*n


for i in range(n):
    data = np.loadtxt(args[i], skiprows=opts.n_header)
    lin = line[i]
    try:
        x = data[:,xcol[i]]
        y = data[:,ycol[i]]
        if opts.i_sort > 0:
            ww = np.argsort(data[:, opts.i_sort - 1])
            x = x[ww]
            y = y[ww]
        if opts.add_zero > 0:
            x = np.append(x, x[-1])
            y = np.append(y, 1e-99)
    except IndexError:
        # if file does not have the desired column
        continue
    if opts.color:
        color=data[:,int(opts.color)-1]

#    bolsum = 0
#    for k in range(len(x)-1):
#          dx = x[k+1] - x[k]
#          bolsum += 0.5*(y[k+1] + y[k])*dx
#    print args[i] + ' bolometric = ' + str(bolsum)

    if (opts.math):
          val = float(opts.math[2:])
          if (opts.math[0] == 'y'):
             if (opts.math[1] == '*'): y = y*val
             if (opts.math[1] == '/'): y = y/val
             if (opts.math[1] == '+'): y = y+val
             if (opts.math[1] == '-'): y = y-val
          if (opts.math[0] == 'x'):
             if (opts.math[1] == '*'): x = x*val
             if (opts.math[1] == '/'): x = x/val
             if (opts.math[1] == '+'): x = x+val
             if (opts.math[1] == '-'): x = x-val
             

    if (opts.norm or opts.offset): y = y/np.mean(y)
    if (opts.max): y = y/np.max(y)
    if (opts.offset): y = y + i*float(opts.offset)
    if (opts.shift and i > 0): y=y*float(opts.shift)
    if (opts.titl): py.title(opts.titl)

    if opts.color:
        colors = [.5,.5,.5,1.0]#np.random.random(len(x))
	py.scatter(x,y,c=colors, markersize=markersize)
    else:
        py.plot(x,y,lin, markersize=markersize)

if (opts.log == 'y'): py.yscale('log')
if (opts.log == 'x'): py.xscale('log')
if (opts.log == 'xy' or opts.log == 'yx'): 
   py.yscale('log')
   py.xscale('log')


if (opts.xrange):
   xx = opts.xrange.split(',')
   x1 = float(xx[0])
   x2 = float(xx[1])
   py.xlim((x1,x2))

if (opts.yrange):
   xx = opts.yrange.split(',')
   x1 = float(xx[0])
   x2 = float(xx[1])
   py.ylim((x1,x2))

if (opts.xtitle):  py.xlabel(opts.xtitle.rstrip('\r\n'))
if (opts.ytitle):  py.ylabel(opts.ytitle.rstrip('\r\n'))

lsize = 20
if (opts.legend):
   if (opts.legend == '0'): 
	   names = args
   elif (opts.legend == 'topdirs'):
       names = []
       for a in args:
           if len(a.split("/")) > 1:
               names.append(a.split("/")[-2].replace("_","\_"))
           else:
               names.append(a.replace("_","\_"))
   elif (opts.legend == 'filenames'):
       names = []
       for a in args:
           if len(a.split("/")) > 1:
               names.append(a.split("/")[-1].split(".")[0].replace("_","\_"))
           else:
               names.append(a.split(".")[0].replace("_","\_"))
   else:
	   names = opts.legend.split(',')

   if (opts.legendloc):
	    loc = np.int(opts.legendloc)
   else:
	   loc = 0

   if (opts.legend_text_size):
       lsize = np.int(opts.legend_text_size)

if opts.vline_x:
    try:
        x_list = [np.float(v) for v in opts.vline_x.split(",")]
        for this_x in x_list:
            py.axvline(this_x, color="k", linestyle="dotted", label=str(x))
    except:
        print "error in vlines parameter"
        sys.exit()

if names and len(names) <= 10:
   py.legend(names,loc=loc, prop={'size':lsize})



if opts.ofile: 
   py.savefig(opts.ofile)
else:
   py.show()

