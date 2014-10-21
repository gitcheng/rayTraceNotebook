# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Scintillation timing precision for hexagonal-cross-section crystal bars</h1>

# <markdowncell>

# * Use data produced by <b><code>scripts/time\_geom2\_hex\_*.py</code></b>
# * Geometry defined in <b><code>geometry_collection_2</code></b>

# <markdowncell>

# Major contributions to scintillation detector timing precision are [Phys. Med. Biol. 59 (2014) 3261]:
# 
# 1. Depth of interaction (DOI): incident particle speed is different from optical photon speed in the scintillator
# 2. Scintillator rise time
# 3. Scintillator decay tie
# 4. Optical photon time dispersion due to variation in path length
# 5. Number of photoelectrons detected
# 6. Photodetector time jitter (time diffrence between the creation of the p.e. and the signal pulse)
# 7. Electronic noise
# 8. Trigger threshold model
# 
# The simulation of ray-tracing with a shower profile includes effects (1. DOI) and (4. time dispersion). The Poisson statistics (5.) can be easily achieved by random sampling. Scintillator rise/decay time (2., 3.) can be modeled with exponentials. Photodetector time jitter (6.) can be model with a Gaussian.

# <markdowncell>

# $\newcommand{\Npe}{N_{\rm p.e.}}
# \newcommand{\Npehat}{\hat{N}_{\rm p.e.}}
# $

# <markdowncell>

# <h2>Event timing precision</h2>
# 
# <h3>Simulate one event of incident particle</h3>
# 
# 1. Given $\Npehat$ the expected number of detected p.e. (energy times p.e./MeV), $\Npe = {\rm Poisson}(\Npe)$.
# 2. Random sample $\Npe$ arrival times from ray-tracing simulation
# 3. Convolve with the scintillator decay time $e^{-t/\tau_d}$ (ignoring the scintilattor rise time, which is much smaller than the decay time).
# 4. Convolve with the photodetector time jitter, modeled by a Gaussian.
# 5. Convolve with the photodetector pulse shape model.
# 6. Electronic noise (how?)
# 
# <h3>Event timing</h3>
# 
# Set a threshold. Find the point at which the pulse height is the closest the threshold. Use 10 points around that point to fit a linear function and solve for the time at the threshold
# 
# <h3>Precision</h3>
# 
# Repeat above steps. Study event timing distribution.

# <markdowncell>

# <h2> Sample </h2>

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt

# <codecell>

import numpy as np
rand = np.random
from timing_utilities import *
from geometry_collection_2 import *
from gen_utilities import *
import pickle

# <codecell>

%load_ext autoreload
%autoreload 2

# <markdowncell>

# <h2>Geometry</h2>
# 
# Three crystals: BaF2, LYSO, and CsI bars with a hexagonal cross section. The length is approximately proportional to the radiation length. The cross sections are the same for all three crystals.
# 
# Defined in geometry_collection_2.py
# 
# Length: BaF2 20 cm; LYSO 11 cm;  CsI 19 cm.<br>
# Width of the hexagon (distance between opposite parallel edges)= 3.3 cm.
# 
# Sensors: two 9 mm X 9 mm, or two 3 mm X 3 mm photosensors.

# <codecell>

fig= plt.figure(figsize=(18,10))
cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
i=0
for mat in ['lyso','baf2','csi']:
    for sd in ['9','3']:
        key = mat+'po'+sd
        ax = fig.add_subplot(161+i, projection='3d')
        ax.set_title(cnames[mat])
        draw_one_crystal(ax, chexes[key])
        i+= 1

# <codecell>

# The timing population to sample from
hexdata= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd in ['3','9']:
            key= mat+sur+sd
            filename= '../data/timing/time_geom2_hex_%s.npy'%(key)
            data = np.load(filename).view(np.recarray)
            hexdata[key]= data
            print '%s population : %d'%(key,len(data))

# <markdowncell>

# <h2>APD pulse model</h2>

# <codecell>

slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')
# Fill in points using linear interpolation
slapd9mm = fill_pmodel_gaps(slapd9mm, ndivs=5)
stdapd9mm = fill_pmodel_gaps(stdapd9mm, ndivs=5)
slapd3mm = fill_pmodel_gaps(slapd3mm, ndivs=5)

# <codecell>

plt.plot(slapd9mm.t, slapd9mm.p, label='SL-APD 9mm');
plt.plot(slapd9mm.t, stdapd9mm.p, label='STD-APD 9mm');
plt.plot(slapd9mm.t, slapd3mm.p, label='SL-APD 3mm');
plt.xlim(0,200)
plt.ylim(-0.2,1.1)
plt.plot([0,200],[0,0], 'k-')
plt.legend()
plt.xlabel('ns')
plt.title('APD response time')

# <markdowncell>

# <h2>Event pulse samples</h2>
# 
# Draw a pulse shapes for a few events. We assume the photoelectron ratio is BaF2:LYSO:CsI = 1: 20: 1.

# <codecell>

## Scintillator decay time
tau_baf2 = 0.9
tau_lyso = 40
tau_csi = 30
## photoelectrons for these samples
npe_baf2 = 1000
npe_lyso = 20000
npe_csi = 1000

# <codecell>

def draw_one_set(ax, dtpop, scinttau, npe0, pulsemodel, title):
    draw_pulse_samples(ax, dtpop, npe0= npe0, scinttau= scinttau, jittersigma= 0.1, noise= 0, pulsemodel= pulsemodel, n=20,
                       color='b', alpha=0.2)
    ax.set_title(title)

# <markdowncell>

# <h3>SL APD 9mm pulse model</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, hexdata['baf2po9'].t, tau_baf2, npe_baf2, slapd9mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo9'].t, tau_lyso, npe_lyso, slapd9mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo9'].t, tau_csi, npe_csi, slapd9mm, 'CsI')

# <markdowncell>

# <h3>SL APD 3mm pulse model</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, hexdata['baf2po3'].t, tau_baf2, npe_baf2, slapd3mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo3'].t, tau_lyso, npe_lyso, slapd3mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo3'].t, tau_csi, npe_csi, slapd3mm, 'CsI')

# <markdowncell>

# <h3>Standard APD 9mm pulse mode </h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, hexdata['baf2po9'].t, tau_baf2, npe_baf2, stdapd9mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo9'].t, tau_lyso, npe_lyso, stdapd9mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo9'].t, tau_csi, npe_csi, stdapd9mm, 'CsI')

# <markdowncell>

# <h2>Timing precision</h2>
# 
# Study the event timing precision for three crystals, three photodetector pulse models, and several different numbers of photoelectrons. For each event (accumulation of all photoelectrons), the timing is found by fitting a line around the point where the pulse height is closest to the threshold, and then solving the time at the threshold. The range of the linear fit is 10 points, which corresponds to 2.5 ns. 
# 
# The threshold is set at 10% of the maximum of each event.

# <codecell>

fthreshold = 0.1

# <codecell>

pelist = [10, 30, 100, 300, 1000, 3000, 10000, 30000]
staudict = dict(baf2= tau_baf2, lyso= tau_lyso, csi= tau_csi)
apdlist = [slapd9mm, slapd3mm, stdapd9mm]
apdnames = ['SL-APD9mm', 'SL-APD3mm', 'Std-APD9mm']

# <codecell>

result= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd, apdname, apdmodel in zip(['9','3','9'],apdnames,apdlist):
            key = mat+sur+sd
            print key, apdname,
            tpres = []
            tpres_err = []
            dtpop = hexdata[key]
            for npe in pelist:
                print npe,
                rand.seed(0)
                tot= timing_samples(dtpop.t, npe, staudict[mat], jittersigma= 0.1, pulsemodel= apdmodel,
                                    noise=0, fthreshold= fthreshold, n= 1000)
                rms= np.sqrt(tot.var())
                tpres.append(rms)
                tpres_err.append(rms/np.sqrt(2*len(tot)))
            print
            rkey= key+':'+apdname
            result[rkey]= np.array(tpres)
            result[rkey+'_err']= np.array(tpres_err)

# <codecell>

result['npelist'] = pelist

# <codecell>

pickle.dump(result, open('../data/timing/tprecision_hex_geocolls2.p', 'wb'))

# <codecell>

result.keys()

# <codecell>


