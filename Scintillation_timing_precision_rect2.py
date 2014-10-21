# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Scintillation timing precision for small rectangular prism crystals</h1>

# <markdowncell>

# * Use data produced by <b><code>scripts/time\_geom2\_rect\_*.py</code></b>
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
# Three crystals: BaF2, LYSO, and CsI rectangular prisms. 
# 
# Defined in geometry_collection_2.py
# 
# Three kinds of geometries. All have a cross section of 3mm X 3mm. The lengths are 10mm, 20mm, and 30mm.
# 
# Sensor: one 3 mm X 3 mm photosensor.

# <codecell>

fig= plt.figure(figsize=(10,7))
cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
i=0
for mat in ['lyso']:
    for lg in [1,2,3]:
        key = mat+'po'+str(lg)
        ax = fig.add_subplot(131+i, projection='3d')
        draw_one_crystal(ax, crects[key], xr=0.5, yr=0.5, zr= 3)
        i+= 1

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

# <markdowncell>

# <h2>APD pulse model</h2>

# <codecell>

slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')
# linear interpolation to fill in points in the model curve
apdmodel = fill_pmodel_gaps(slapd3mm, ndivs=5)
#apdmodel = slapd3mm

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
npe_baf2 = 200
npe_lyso = 4000
npe_csi = 200

# <codecell>

def draw_one_set(ax, dtpop, scinttau, npe0, pulsemodel, title):
    draw_pulse_samples(ax, dtpop, npe0= npe0, scinttau= scinttau, jittersigma= 0.1, noise= 0, pulsemodel= pulsemodel, n=20,
                       color='b', alpha=0.2)
    ax.set_title(title)

# <markdowncell>

# <h3>10 mm long polished crystals</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, rectdata['baf2po1'].t, tau_baf2, npe_baf2, apdmodel, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, rectdata['lysopo1'].t, tau_lyso, npe_lyso, apdmodel, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, rectdata['csipo1'].t, tau_csi, npe_csi, apdmodel, 'CsI')

# <markdowncell>

# <h3>10 mm long roughened crystals</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, rectdata['baf2ra1'].t, tau_baf2, npe_baf2, apdmodel, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, rectdata['lysora1'].t, tau_lyso, npe_lyso, apdmodel, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, rectdata['csira1'].t, tau_csi, npe_csi, apdmodel, 'CsI')

# <markdowncell>

# <h3>30 mm long polished crystals</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, rectdata['baf2po3'].t, tau_baf2, npe_baf2, apdmodel, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, rectdata['lysopo3'].t, tau_lyso, npe_lyso, apdmodel, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, rectdata['csipo3'].t, tau_csi, npe_csi, apdmodel, 'CsI')

# <markdowncell>

# <h3>30 mm long roughened crystals</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, rectdata['baf2ra3'].t, tau_baf2, npe_baf2, apdmodel, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, rectdata['lysora3'].t, tau_lyso, npe_lyso, apdmodel, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, rectdata['csira3'].t, tau_csi, npe_csi, apdmodel, 'CsI')

# <codecell>

print rectdata['baf2po3'].t.mean(), rectdata['baf2ra3'].t.mean()

# <markdowncell>

# <h2>Timing precision</h2>
# 
# Study the event timing precision for three crystals, three photodetector pulse models, and several different numbers of photoelectrons. For each event (accumulation of all photoelectrons), the timing is found by fitting a line around the point where the pulse height is closest to the threshold, and then solving the time at the threshold. The range of the linear fit is 10 points, which corresponds to 2.5 ns. 
# 
# The threshold is set at 20% of the maximum of each event.

# <codecell>

fthreshold = 0.1
pelist = [10, 30, 100, 300, 1000, 3000, 10000]
staudict = dict(baf2= tau_baf2, lyso= tau_lyso, csi= tau_csi)
apdname = 'SL-APD3mm'

# <codecell>

result= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for lg in [1,2,3]:
            key = mat+sur+str(lg)
            print key, apdname,
            tpres = []
            tpres_err = []
            dtpop = rectdata[key]
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

pickle.dump(result, open('../data/timing/tprecision_rect_geocolls2.p', 'wb'))

# <codecell>

result.keys()

# <codecell>

len(result)

# <headingcell level=2>

# =============================================================================

# <codecell>

bins= np.linspace(0,10,101)
plt.hist(rectdata['baf2po3'].t, bins=bins, histtype='step');
plt.hist(rectdata['baf2ra3'].t, bins=bins, histtype='step');

#plt.yscale('log')
plt.xlim(0,10)

# <codecell>

print rectdata['lysopo3'].t.mean()
print rectdata['lysora3'].t.mean()

# <codecell>

mat= 'baf2'
print staudict[mat]
print fthreshold
rand.seed(14)
tpolish3= timing_samples(rectdata['baf2po3'].t, 10000, staudict[mat], jittersigma= 0.1, pulsemodel= apdmodel,
                                    noise=0, fthreshold= fthreshold*1, n= 1000)
trough3= timing_samples(rectdata['baf2ra3'].t, 10000, staudict[mat], jittersigma= 0.1, pulsemodel= apdmodel,
                                    noise=0, fthreshold= fthreshold*1, n= 1000)

# <codecell>

print np.sqrt(tpolish3.var())
print np.sqrt(trough3.var())

# <codecell>

plt.figure(figsize=(12,4))
plt.subplot(121)
plt.hist(tpolish3, bins=100, histtype='step');
plt.subplot(122)
plt.hist(trough3, bins=100, histtype='step');

# <codecell>

plt.figure(figsize=(12,4))
plt.subplot(121)
plt.hist(tpolish1, bins=100, histtype='step');
plt.subplot(122)
plt.hist(trough1, bins=100, histtype='step');

# <codecell>

plt.hist(trough[trough1<0.04+13.84], bins=100, histtype='step');
plt.hist(trough[trough1>0.04+13.84], bins=100, histtype='step');

# <codecell>

plt.hist(tpolish, bins=100, histtype='step');

# <codecell>

plt.hist(trough, bins=100, histtype='step');

# <codecell>

apdmodel.t[3]-apdmodel.t[2]

# <codecell>

tevent= event_pulse(rectdata['baf2ra3'].t, npe0=10000, scinttau= 0.9, jittersigma= 0.1, noise= 0, pulsemodel= apdmodel)
print time_reach_threshold(tevent.t, tevent.p, fthreshold)

# <codecell>

plt.plot(tevent.t, tevent.p, 'bo-')
plt.xlim(12,18)

# <codecell>

from iminuit import Minuit
from probfit import Chi2Regression

# <codecell>

def logit(x, x0, norm, tau, y0):
    return norm/(1+np.exp(-(x-x0)/tau)) + y0

# <codecell>

x= np.arange(12, 18, 0.05)
sel= (tevent.t>12)&(tevent.t<18)&(tevent.p<0.5*np.max(tevent.p))&(tevent.p>0.01*np.max(tevent.p))
plt.plot(tevent.t[sel], tevent.p[sel], 'bo-')
plt.plot(x, logit(x, 14.9, 7000, 0.49, 0), 'g-')

# <codecell>

x2reg= Chi2Regression(logit, tevent.t[sel], tevent.p[sel])
m = Minuit(x2reg, print_level=0, x0= 14.0, norm=8000, tau= 0.5, pedantic=False)
m.migrad();
print m.values

# <codecell>

x2reg.draw();

# <codecell>

x2reg.draw_residual();

