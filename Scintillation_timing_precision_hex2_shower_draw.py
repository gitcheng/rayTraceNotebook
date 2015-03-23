# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw timing precision comparison for hexagonal crystal bars</h1>
# 
# Data produced by <b>Scintillation_timing_precision_hex2_shower.ipynb</b>. Data include shower shape fluctuation.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import ScalarFormatter
import pickle

# <codecell>

tpres0 = pickle.load(open('../data/timing/tprecision_hex_preamp_geocolls2.p','rb'))
tpresh = pickle.load(open('../data/timing/tprecision_hex_preamp_shower_geocolls2.p','rb'))

# <codecell>

print tpres0.keys()
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

# <h2>Timing resolution without shower shape fluctuation</h2>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
colors=['b','r','g']
markers=['o','s','^']
for mat,cl in zip(['lyso','baf2','csi'],colors):
    for sd,apd,mk in zip(['9','9'],apdnames,markers):
        key= '%s%s%s:%s'%(mat,'po',sd, apd)
        plt.errorbar(tpres0['npelist'], tpres0[key]*1e3, tpres0[key+'_err']*1e3, 
                     fmt= '-', color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label=cnames[mat]+' '+apd, alpha=0.7)
        print key,
ax.set_title('Common shower shape')
plotmakeup(ax)
fig.savefig('../plots/shower/timing_dependence_on_pe_hexpol_xsh.pdf')

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
fig.savefig('../plots/shower/timing_dependence_on_pe_hexpol_fluc.pdf')

# <markdowncell>

# <h2>Compare with and without shower fluctuation</h2>
# 
# <h3>SL-APD</h3>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
colors=['b','r','g']
markers=['o','s','^']
lstyles=['--', '-']
for mat,cl in zip(['lyso','baf2','csi'],colors):
    for tpr, shlb, mk, ls in zip([tpres0, tpresh], ['common shower', 'fluctuate shower'], markers, lstyles):
        key= '%s%s:%s'%(mat,'po9', 'SL-APD9mm')
        print key,
        plt.errorbar(tpr['npelist'], tpr[key]*1e3, tpr[key+'_err']*1e3, 
                     fmt= ls, color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label=cnames[mat]+' '+shlb, alpha=0.7)
ax.set_title('SL-APD 9x9 mm$^2$')
plotmakeup(ax)
fig.savefig('../plots/shower/timing_dependence_on_pe_hexpol_SLAPD.pdf')

# <markdowncell>

# <h3>Std-APD</h3>

# <codecell>

fig= plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
colors=['b','r','g']
markers=['o','s','^']
lstyles=['--', '-']
for mat,cl in zip(['lyso','baf2','csi'],colors):
    for tpr, shlb, mk, ls in zip([tpres0, tpresh], ['common shower', 'fluctuate shower'], markers, lstyles):
        key= '%s%s:%s'%(mat,'po9', 'Std-APD9mm')
        print key,
        plt.errorbar(tpr['npelist'], tpr[key]*1e3, tpr[key+'_err']*1e3, 
                     fmt= ls, color=cl, mec='k', mew=1, ms=7, marker=mk, mfc=cl, label=cnames[mat]+' '+shlb, alpha=0.7)
ax.set_title('Standard APD 9x9 mm$^2$')
plotmakeup(ax)
fig.savefig('../plots/shower/timing_dependence_on_pe_hexpol_StdAPD.pdf')

# <codecell>


# <codecell>


