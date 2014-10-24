# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Photon arrival time</h1>
# 
# * Use data produced by <b><code>scripts/time\_geom2\_hex\_*.py</code></b> and <b><code>scripts/time\_geom2\_rect\_*.py</code></b>
# * Geometry defined in <b><code>geometry_collection_2</code></b>

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pickle

# <codecell>

hexdata= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd in ['3','9']:
            key= mat+sur+sd
            filename= '../data/timing/time_geom2_hex_%s.npy'%(key)
            data = np.load(filename).view(np.recarray)
            hexdata[key]= data
            print '%s population : %d'%(key,len(data))

# <codecell>

rectdata= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for lg in [1,2,3]:
            key= mat+sur+str(lg)
            filename= '../data/timing/time_geom2_rect_%s.npy'%(key)
            data = np.load(filename).view(np.recarray)
            rectdata[key]= data
            print '%s population : %d'%(key,len(data))

# <codecell>

cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
snames=dict(ra9='Roughened', po9='Polished')

# <codecell>

attris= dict(bins=np.linspace(0,40,81), histtype='step')
fig= plt.figure(figsize=(12,4))
for i,mat in enumerate(['baf2','lyso','csi']):
    ax = fig.add_subplot(131+i)
    for sur in ['po9','ra9']:
        at= hexdata[mat+sur]
        plt.hist(at.t, label=snames[sur], lw=2, **attris)
    ax.set_yscale('log')
    ax.legend()
    ax.set_title(cnames[mat])
    ax.set_xlabel('ns')
fig.savefig('../plots/arrtimes_hex_colls2.pdf')

# <codecell>

attris= dict(bins=np.linspace(0,15,61), histtype='step')
labels= dict(po1='Polished 10 mm',po3='Polished 30 mm',ra1='Roughened 10 mm',ra3='Roughened 30 mm')
colors= dict(po1='b',po3='g',ra1='r',ra3='c')
fig= plt.figure(figsize=(12,4))
for i,mat in enumerate(['baf2','lyso','csi']):
    ax = fig.add_subplot(131+i)
    for sur in ['po','ra']:
        for lg in [1,3]:
            at= rectdata[mat+sur+str(lg)]
            key= sur+str(lg)
            plt.hist(at.t, label=labels[key], color=colors[key], lw=2, **attris)
    ax.set_yscale('log')
    ax.legend()
    ax.set_title(cnames[mat])
    ax.set_xlabel('ns')
    ax.set_xlim(0,15)
fig.savefig('../plots/arrtimes_rect_colls2.pdf')

# <codecell>


# <codecell>

rand = np.random
from timing_utilities import *
from geometry_collection_2 import *
from gen_utilities import *

# <codecell>

def draw_one_set(ax, dtpop, scinttau, npe0, pulsemodel, title):
    draw_pulse_samples(ax, dtpop, npe0= npe0, scinttau= scinttau, jittersigma= 0.1, noise= 0, pulsemodel= pulsemodel, n=20,
                       color='b', alpha=0.2)
    ax.set_title(title)

# <codecell>

## Scintillator decay time
tau_baf2 = 0.9
tau_lyso = 40
tau_csi = 30
## photoelectrons for these samples
npe_baf2 = 200
npe_lyso = 4000
npe_csi = 200

# <codecell>

slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')
# Fill in points using linear interpolation
slapd9mm = fill_pmodel_gaps(slapd9mm, ndivs=5)
stdapd9mm = fill_pmodel_gaps(stdapd9mm, ndivs=5)
slapd3mm = fill_pmodel_gaps(slapd3mm, ndivs=5)

# <codecell>

apdmodel= slapd3mm
fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, rectdata['baf2po3'].t, tau_baf2, npe_baf2, apdmodel, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, rectdata['lysopo3'].t, tau_lyso, npe_lyso, apdmodel, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, rectdata['csipo3'].t, tau_csi, npe_csi, apdmodel, 'CsI')
fig.savefig('../plots/event_pulses_rect_geocolls2.pdf')

# <codecell>

## photoelectrons for these samples
npe_baf2 = 1000
npe_lyso = 20000
npe_csi = 1000

apdmodel= slapd9mm
fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, hexdata['baf2po9'].t, tau_baf2, npe_baf2, apdmodel, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo9'].t, tau_lyso, npe_lyso, apdmodel, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo9'].t, tau_csi, npe_csi, apdmodel, 'CsI')
fig.savefig('../plots/event_pulses_hex_geocolls2.pdf')

# <codecell>


