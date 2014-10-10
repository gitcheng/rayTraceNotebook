# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw timing precision comparison for hexagonal-cross-section crystal bars</h1>
# 
# Data produced by <b>Scintillation_timing_precision_hex1.ipynb</b>.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import ScalarFormatter
import pickle

# <codecell>

result= pickle.load(open('../data/timing/tprecision_hex_1.p','rb'))

# <codecell>

crysnames = ['BaF2', 'LYSO', 'CsI']
apdnames = ['SL-APD9mm', 'SL-APD3mm', 'Std-APD9mm']

# <codecell>

print result.keys()

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

colors=['b','r','g']
markers=['o','s','^']
for cn,cl in zip(crysnames,colors):
    for apd,mk in zip(apdnames,markers):
        key= '%s:%s'%(cn, apd)
        plt.errorbar(result['npelist'], result[key]*1e3, result[key+'_err']*1e3, 
                     fmt= cl+mk+'-', label=key)
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

fig.savefig('../plots/timing_dependence_on_pe_hex1.pdf')

# <markdowncell>

# <h2>Fit a power law dependence</h2>
# 
# $p(N) = B \cdot N^a$

# <codecell>

from fit_utilities import *

# <codecell>

Bfactors= {}
apowers= {}

# <codecell>

# Do fits here
for cn in crysnames:
    for apd in apdnames:
        key= '%s:%s'%(cn, apd)
        values, errors = fit_power_law(result['npelist'][1:], result[key][1:]*1e3, result[key+'_err'][1:]/result[key][1:])
        Bfactors[key] = np.exp(values['b'])
        apowers[key] = values['a']

# <codecell>

def print_table(d, digits=0):
    print '%4s'%'',
    for apd in apdnames:
        print '%10s'%apd,
    print
    fmt = '%%10.%df'%digits
    for cn in crysnames:
        print '%4s'%cn,
        for apd in apdnames:
            key= '%s:%s'%(cn, apd)
            print fmt%d[key],
        print

# <markdowncell>

# The $B$ factor in $p(N) = B \cdot N^a$ 

# <codecell>

print_table(Bfactors)

# <markdowncell>

# The power $a$.

# <codecell>

print_table(apowers, digits=2)

# <codecell>


