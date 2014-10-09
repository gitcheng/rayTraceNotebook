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

