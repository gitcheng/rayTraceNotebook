# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw timing precision comparison for small rectangular prism for PET</h1>
# 
# Data produced by <b>Scintillation_timing_precision_rect2.ipynb</b>.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import ScalarFormatter
import pickle

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

result= pickle.load(open('../data/timing/tprecision_rect_preamp_geocolls2.p'))

# <codecell>

print result.keys()

# <codecell>

cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
apdname= 'SL-APD3mm'

# <codecell>

def figform(ax):
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(5, 50000)
    plt.ylim(3, 30000)
    plt.legend()
    plt.grid(which='major')
    plt.grid(which='minor')
    plt.xlabel('Number of photoelectrons', fontsize='x-large')
    plt.ylabel('Precision (ps)', fontsize='x-large')
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.get_yaxis().set_major_formatter(ScalarFormatter())

# <markdowncell>

# <h2>Polished crystals</h2>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

colors=['b','r','g']
markers=['o','s','^']

dkeys=[]
for mat,cl in zip(['lyso','baf2','csi'],colors):
    for lg,mk in zip([1,2,3],markers):
        key= '%s%s%d:%s'%(mat,'po',lg, apdname)
        dkeys.append(key)
        plt.errorbar(result['npelist'], result[key]*1e3, result[key+'_err']*1e3, 
                     fmt= '-', color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label='%s:%d cm'%(cnames[mat],lg), alpha=0.7)
print dkeys
figform(ax)

# <codecell>

fig.savefig('../plots/timing_dependence_on_pe_rectcolls2_pol.pdf')

# <markdowncell>

# <h2>Roughened crystals</h2>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

colors=['b','r','g']
markers=['o','s','^']

for mat,cl in zip(['lyso','baf2','csi'],colors):
    for lg,mk in zip([1,2,3],markers):
        key= '%s%s%d:%s'%(mat,'ra',lg, apdname)
        dkeys.append(key)
        plt.errorbar(result['npelist'], result[key]*1e3, result[key+'_err']*1e3, 
                     fmt= '-', color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label='%s:%d cm'%(cnames[mat],lg), alpha=0.7)
figform(ax)

# <codecell>

fig.savefig('../plots/timing_dependence_on_pe_rectcolls2_ruf.pdf')

# <markdowncell>

# <h2>Fit a power law dependence</h2>
# 
# $p(N) = B \cdot (N/100)^a$

# <codecell>

from fit_utilities import *

# <codecell>

Bfactors= {}
apowers= {}
Bferrors= {}
aperrors= {}

# <codecell>

# Do fits here
for key in dkeys:
    # Ignore the first two points
    npe100= np.array(result['npelist'][2:])/100.0  # number of photoelectrons in multiple of 100
    rmsps= result[key][2:]*1e3   # precision in picoseconds
    error= result[key+'_err'][2:]*1e3 # error in picoseconds  ##/result[key][2:]
    values, errors = fit_power_lawab(npe100, rmsps, error)
    Bfactors[key] = values['b']
    Bferrors[key] = errors['b']
    apowers[key] = values['a']
    aperrors[key] = errors['a']

# <codecell>

print cnames

# <codecell>

def print_table(d, e, digits=0):
    print '%4s'%'',
    print '%10s%10s%10s'%('1 cm','2 cm', '3 cm'),
    print
    fmt = ' & $%%.%df\\pm%%.%df$'%(digits,digits)
    for mat in ['baf2','lyso','csi']:
        print '%4s'%cnames[mat],
        for tag in ['po1','po2','po3']:
            key= '%s%s:%s'%(mat,tag, apdname)
            print fmt%(d[key],e[key]),
        print

# <markdowncell>

# The $B$ factor in $p(N) = B \cdot (N/100)^a$ 

# <codecell>

print_table(Bfactors, Bferrors, digits=1)

# <markdowncell>

# The power $a$.

# <codecell>

print_table(apowers, aperrors, digits=3)

# <codecell>

np.power(2,3)

# <codecell>


