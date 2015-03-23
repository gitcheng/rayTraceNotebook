# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Scintillation timing precision for hexagonal crystal bars with shower fluctuation</h1>

# <markdowncell>

# * Use data produced by <b><code>scripts2/time\_shower\_hex\_*.py</code></b>
# * Geometry defined in <b><code>geometry_collection_2</code></b>
# * A similar version in <b><code>Scintillation_timing_precision_hex2</code></b> uses simple parametrized shower profile for every event. So there was no shower shape fluctuation there.

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
# 2. Random sample $\Npe$ arrival times from ray-tracing simulation with shower samples
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
# Sensors: two 9 mm X 9 mm photosensors.

# <markdowncell>

# <h2>APD pulse model</h2>

# <markdowncell>

# <h3>From fast laser measurement</h3>

# <codecell>

slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')
# Fill in points using linear interpolation
slapd9mm = fill_pmodel_gaps(slapd9mm, ndivs=5)
stdapd9mm = fill_pmodel_gaps(stdapd9mm, ndivs=5)
slapd3mm = fill_pmodel_gaps(slapd3mm, ndivs=5)
# t>=0
slapd9mm = slapd9mm[slapd9mm.t>0]
slapd3mm = slapd3mm[slapd3mm.t>0]
stdapd9mm = stdapd9mm[stdapd9mm.t>0]

# <codecell>

plt.plot(slapd9mm.t, slapd9mm.p, label='SL-APD 9mm');
plt.plot(slapd9mm.t, stdapd9mm.p, label='STD-APD 9mm');
plt.plot(slapd9mm.t, slapd3mm.p, label='SL-APD 3mm');
plt.xlim(0,200)
plt.ylim(-0.2,1.1)
plt.plot([0,200],[0,0], 'k-')
plt.legend()
plt.xlabel('ns');
plt.title('APD response time');

# <markdowncell>

# <h3>Convolve with simple preamp model <h3>

# <codecell>

def pulse_shape_simple(x, tauR, tauD, A):
    return A* (np.exp(-x/tauD)-np.exp(-x/tauR))

# <codecell>

t= slapd9mm.t
ps= pulse_shape_simple(t, 6.0, 15.0, 1.0)
pream= np.array(zip(t,ps), dtype=slapd9mm.dtype).view(np.recarray)
plt.plot(pream.t, pream.p)
plt.title('Preamp model');
plt.xlabel('ns');

# <codecell>

pmslapd9mm= convolve_two_pulse_model(slapd9mm, pream)
pmslapd3mm= convolve_two_pulse_model(slapd3mm, pream)
pmstdapd9mm= convolve_two_pulse_model(stdapd9mm, pream)

# <codecell>

plt.plot(pmslapd9mm.t, pmslapd9mm.p/pmslapd9mm.p.max(), label='SL-APD 9mm');
plt.plot(pmslapd9mm.t, pmstdapd9mm.p/pmstdapd9mm.p.max(), label='STD-APD 9mm');
plt.plot(pmslapd9mm.t, pmslapd3mm.p/pmslapd3mm.p.max(), label='SL-APD 3mm');
plt.xlim(0,200)
plt.ylim(-0.2,1.1)
plt.plot([0,200],[0,0], 'k-')
plt.legend()
plt.xlabel('ns');
plt.title('APD+Preamp response time');

# <markdowncell>

# <h2>Photon arrival time using shower shape from GEANT4</h2>

# <codecell>

d1 = np.load('../data/timing/time_geom2_shower_hex_baf2po9_01.npy')
d2 = np.load('../data/timing/time_geom2_shower_hex_baf2po9_02.npy')

# <codecell>

dd = np.concatenate((d1,d2)).view(np.recarray)

# <codecell>

print dd.dtype
print len(dd)
print dd.shape
print dd.shape[0]
print np.ndim(dd)
print np.ndim(dd.t)
print np.ndim(dd[0].t)
print np.ndim(dd.t[0])
print dd.t[0].shape

# <codecell>

# The timing population to sample from
hexdata= {}
for mat in ['lyso','baf2','csi']:
    key = mat+'po9'
    data= None
    for i in xrange(1,6):
        filename= '../data/timing/time_geom2_shower_hex_%s_%02d.npy'%(key, i)
        if data is None:
            data = np.load(filename)
        else:
            data = np.concatenate((data, np.load(filename)))
    print '%s population : %d'%(key,len(data))
    hexdata[key] = data.view(np.recarray)

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
draw_one_set(ax, hexdata['baf2po9'].t, tau_baf2, npe_baf2, pmslapd9mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo9'].t, tau_lyso, npe_lyso, pmslapd9mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo9'].t, tau_csi, npe_csi, pmslapd9mm, 'CsI')

# <markdowncell>

# <h3>Standard APD 9mm pulse mode </h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, hexdata['baf2po9'].t, tau_baf2, npe_baf2, pmstdapd9mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo9'].t, tau_lyso, npe_lyso, pmstdapd9mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo9'].t, tau_csi, npe_csi, pmstdapd9mm, 'CsI')

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
apdlist = [pmslapd9mm, pmstdapd9mm]
apdnames = ['SL-APD9mm', 'Std-APD9mm']

# <codecell>

result= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po']:
        for sd, apdname, apdmodel in zip(['9','9'],apdnames,apdlist):
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

pickle.dump(result, open('../data/timing/tprecision_hex_preamp_shower_geocolls2.p', 'wb'))

# <codecell>

result.keys()

# <codecell>

result['baf2po9:SL-APD9mm']

# <codecell>

result['baf2po9:Std-APD9mm']

# <codecell>

pelist

# <codecell>


