#!/usr/bin/python
import optparse
import sys
import numpy as np
import pylab as py
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

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
parser.add_option("--offset",dest="offset")
parser.add_option("--shift",dest="shift")
parser.add_option("--color",dest="color")

(opts, args) = parser.parse_args()
print args

n = len(args)

xcol = []
ycol = []
if (opts.cols):
   col_plot = opts.cols.split(',')
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



if (opts.linestyle): line = opts.linestyle.split(',')
else: line = ['']*n


for i in range(n):
    data = np.loadtxt(args[i])
    lin = line[i]
    x = data[:,xcol[i]]
    y = data[:,ycol[i]]
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
	py.scatter(x,y,c=colors)
    else:
        py.plot(x,y,lin)

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

if (opts.xtitle):  py.xlabel(opts.xtitle)
if (opts.ytitle):  py.ylabel(opts.ytitle)

if (opts.legend):
   if (opts.legend == '0'): 
	names = args
   else: 
	names = opts.legend.split(',')
   	if (opts.legendloc):
		loc = np.int(opts.legendloc)
	else:
		loc = 0
	py.legend(names,loc=loc)

if opts.ofile:
   plot_name = opts.ofile + '.eps' 
   plt.savefig(plot_name, format='eps', dpi = 3500)
else:
   py.show()

