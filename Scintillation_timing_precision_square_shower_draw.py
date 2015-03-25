# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw timing precision comparison for square crystal bars</h1>
# 
# Data produced by <b>Scintillation_timing_precision_square_shower.ipynb</b>. Data include shower shape fluctuation.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import ScalarFormatter
import pickle

# <codecell>

tpresh = pickle.load(open('../data/timing/tprecision_square_preamp_shower_geocolls2.p','rb'))

# <codecell>

print tpresh.keys()

# <codecell>

cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
apdnames = ['SL-APD9mm', 'Std-APD9mm']

# <codecell>

def plotmakeup(ax):
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(5, 50000)
    plt.ylim(10, 10000)
    plt.legend()
    plt.grid(which='major')
    plt.grid(which='minor')
    plt.xlabel('Number of photoelectrons', fontsize='x-large')
    plt.ylabel('Precision (ps)', fontsize='x-large')
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.get_yaxis().set_major_formatter(ScalarFormatter())

# <markdowncell>

# <h2>Timing resolution with shower shape fluctuation</h2>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
colors=['b','r','g']
markers=['o','s','^']
for mat,cl in zip(['lyso','baf2','csi'],colors):
    for sd,apd,mk in zip(['9','9'],apdnames,markers):
        key= '%s%s%s:%s'%(mat,'po',sd, apd)
        print key,
        plt.errorbar(tpresh['npelist'], tpresh[key]*1e3, tpresh[key+'_err']*1e3, 
                     fmt= '-', color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label=cnames[mat]+' '+apd, alpha=0.7)
ax.set_title('Fluctuate shower shape')
plotmakeup(ax)
fig.savefig('../plots/shower/timing_dependence_on_pe_squarepol_fluc.pdf')

# <codecell>


# <codecell>


