# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Scintillation timing precision for small crystals</h1>
# 
# See the introduction in <b>Scintillation_timinig_precision_hex1.ipynb</b>.

# <markdowncell>

# $\newcommand{\Npe}{N_{\rm p.e.}}
# \newcommand{\Npehat}{\hat{N}_{\rm p.e.}}
# $

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
rand = np.random
from timing_utilities import *
from geometry_collection_1 import *
from gen_utilities import *
import pickle

# <codecell>

%load_ext autoreload
%autoreload 2

# <markdowncell>

# <h2>Geometry</h2>
# 
# Three crystals: BaF2, LYSO, and CsI of the exactly the same geometry: 1cm x 1cm x 2cm
# 
# Defined in geometry_collection_1.py
# 
# Sensors: one 5mm x 5mm photosensor.

# <codecell>

fig= plt.figure(figsize=(10,4))
titles= ['LYSO', 'BaF2', 'CsI']
for i, crys in enumerate([cpet_lyso, cpet_baf2, cpet_csi]):
    ax = fig.add_subplot(131+i, projection='3d')
    ax.set_title(titles[i])
    draw_one_crystal(ax, crys, xr=1.0, yr=1.0, zr=2.5, nbins=3, elev=10)

# <codecell>

# The timing population to sample from
baf2pop = np.load('../data/timing/ts_baf2_pet_1_1_2_n100k_0001.npy')
lysopop = np.load('../data/timing/ts_lyso_pet_1_1_2_n500k_0001.npy')
csipop = np.load('../data/timing/ts_csi_pet_1_1_2_n100k_0001.npy')
print 'Population BaF2: ' , len(baf2pop)
print 'Population LYSO: ' , len(lysopop)
print 'Population CsI:  ' , len(csipop)

# <markdowncell>

# <h2>APD pulse model</h2>

# <codecell>

slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')

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
draw_one_set(ax, baf2pop, tau_baf2, npe_baf2, slapd9mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, lysopop, tau_lyso, npe_lyso, slapd9mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, csipop, tau_csi, npe_csi, slapd9mm, 'CsI')

# <markdowncell>

# <h3>SL APD 3mm pulse model</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, baf2pop, tau_baf2, npe_baf2, slapd3mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, lysopop, tau_lyso, npe_lyso, slapd3mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, csipop, tau_csi, npe_csi, slapd3mm, 'CsI')

# <markdowncell>

# <h3>Standard APD 9mm pulse mode </h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, baf2pop, tau_baf2, npe_baf2, stdapd9mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, lysopop, tau_lyso, npe_lyso, stdapd9mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, csipop, tau_csi, npe_csi, stdapd9mm, 'CsI')

# <markdowncell>

# <h2>Timing precision</h2>
# 
# Study the event timing precision for three crystals, three photodetector pulse models, and several different numbers of photoelectrons. For each event (accumulation of all photoelectrons), the timing is found by fitting a line around the point where the pulse height is closest to the threshold, and then solving the time at the threshold. The range of the linear fit is 10 points, which corresponds to 2.5 ns. 
# 
# The threshold is set at 10% of the maximum of each event.

# <codecell>

fthreshold = 0.1

# <codecell>

rand.seed(0)
pelist = [10, 30, 100, 300, 1000, 3000, 10000, 30000]
dtpoplist = [baf2pop, lysopop, csipop]
apdlist = [slapd9mm, slapd3mm, stdapd9mm]
crysnames = ['BaF2', 'LYSO', 'CsI']
staulist = [tau_baf2, tau_lyso, tau_csi]
apdnames = ['SL-APD9mm', 'SL-APD3mm', 'Std-APD9mm']

# <codecell>

result= {}
for i in xrange(len(dtpoplist)):
    for j in xrange(len(apdlist)):
        key = '%s:%s'%(crysnames[i],apdnames[j])
        print key, 
        tpres = []
        tpres_err = []
        for npe in pelist:
            print npe,
            tot= timing_samples(dtpoplist[i], npe, staulist[i], jittersigma= 0.2, pulsemodel= apdlist[j], noise=0,
                                fthreshold = fthreshold, n= 1000)
            rms= np.sqrt(tot.var())
            tpres.append(rms)
            tpres_err.append(rms/np.sqrt(2*len(tot)))
        print
        result[key]= np.array(tpres)
        result[key+'_err']= np.array(tpres_err)

# <codecell>

result['npelist'] = pelist

# <codecell>

pickle.dump(result, open('../data/timing/tprecision_pet_1.p', 'wb'))

# <codecell>

result.keys()

# <codecell>

plt.plot(result['npelist'], result['BaF2:SL-APD3mm'], 'bo')
plt.xscale('log')
plt.yscale('log')

# <codecell>


