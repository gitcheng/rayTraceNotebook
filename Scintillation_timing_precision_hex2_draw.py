# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw timing precision comparison for hexagonal-cross-section crystal bars</h1>
# 
# Data produced by <b>Scintillation_timing_precision_hex2.ipynb</b>.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import ScalarFormatter
import pickle

# <codecell>

result= pickle.load(open('../data/timing/tprecision_hex_geocolls2.p','rb'))

# <codecell>

print result.keys()

# <codecell>

cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
apdnames = ['SL-APD9mm', 'SL-APD3mm', 'Std-APD9mm']

# <markdowncell>

# <h2>Polished crystals</h2>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

colors=['b','r','g']
markers=['o','s','^']

dkeys=[]
for mat,cl in zip(['lyso','baf2','csi'],colors):
    for sd,apd,mk in zip(['9','3','9'],apdnames,markers):
        key= '%s%s%s:%s'%(mat,'po',sd, apd)
        dkeys.append(key)
        plt.errorbar(result['npelist'], result[key]*1e3, result[key+'_err']*1e3, 
                     fmt= '-', color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label=cnames[mat]+' '+apd, alpha=0.7)
print dkeys
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

# <codecell>

fig.savefig('../plots/timing_dependence_on_pe_hexcolls2_pol.pdf')

# <markdowncell>

# <h2>Compare polished and roughened</h2>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

colors=['b','r','g']
markers=['o','s','^']

apd= 'SL-APD9mm'
sd= '9'

for mat,cl in zip(['lyso','baf2','csi'],colors):
    for sur,slb,mk in zip(['po','ra'],['Polished','Roughened'],['s','*']):
        key= '%s%s%s:%s'%(mat,sur,sd, apd)
        plt.errorbar(result['npelist'], result[key]*1e3, result[key+'_err']*1e3, 
                     fmt= '-', color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label=cnames[mat]+' '+slb, alpha=0.7)
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

# <codecell>

fig.savefig('../plots/timing_dependence_on_pe_hexcolls2_sl9mm_polvrough.pdf')

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

# Do fits here
#for key in dkeys:
#    values, errors = fit_power_law(result['npelist'][2:], result[key][2:]*1e3, result[key+'_err'][2:]/result[key][2:])
#    Bfactors[key] = np.exp(values['b'])
#    apowers[key] = values['a']

# <codecell>

print apdnames
print cnames

# <codecell>

def print_table(d, e, digits=0):
    print '%4s'%'',
    for apd in apdnames:
        print '%10s'%apd,
    print
    fmt = '$%%.%df\\pm%%.%df$'%(digits,digits)
    for mat in ['baf2','lyso','csi']:
        print '%4s'%cnames[mat],
        for tag,apd in zip(['po9','po3','po9'], apdnames):
            key= '%s%s:%s'%(mat,tag, apd)
            print fmt%(d[key],e[key]),
        print

# <markdowncell>

# The $B$ factor in $p(N) = B \cdot (N/100)^a$ 

# <codecell>

print_table(Bfactors, Bferrors)

# <markdowncell>

# The power $a$.

# <codecell>

print_table(apowers, aperrors, digits=3)

# <codecell>


