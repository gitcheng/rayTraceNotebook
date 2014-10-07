# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Scintillation timing precision</h1>

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
# $

# <markdowncell>

# <h2>Event timing precision</h2>
# 
# <h3>Simulate one event of incident particle</h3>
# 
# 1. Given $\hat \Npe$ the expected number of detected p.e. (energy times p.e./MeV), $\Npe = {\rm Poisson}(\Npe)$.
# 2. Random sample $\Npe$ arrival times from ray-tracing simulation
# 3. Convolve with the scintillator decay time $e^{-t/\tau_d}$ (ignoring the scintilattor rise time, which is much smaller than the decay time).
# 4. Convolve with the photodetector time jitter, modeled by a Gaussian.
# 5. Convolve with the photodetector pulse shape model.
# 6. Electronic noise (how?)
# 
# <h3>Event timing</h3>
# 
# Set at threshold. Find the time at which the pulse reaches the threshold.
# 
# <h3>Precision</h3>
# 
# Repeat above steps. Study event timing distribution.

# <markdowncell>

# <h2> Sample </h2>

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
rand = np.random
from timing_utilities import *
import matplotlib.pyplot as plt

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

# The timing population to sample from
dtpop = np.load('timing/arrival_time_hex_bf2_21cm_gaussianshower.npy')
print 'Population ' , len(dtpop)

# <codecell>

slapd9mm = pulse_model('SLAPD_RiseTime.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('SLAPD_RiseTime.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('SLAPD_RiseTime.csv', 'time_ns', 'slapd3mm', normtype='peak')

# <codecell>

def timing_samples(nevts, dtpop, npe, scinttau, jittersigma, pulsemodel, threshold):
    '''
    *nevts* : number of events
    *dtpop* : photon arrival time population to sample from
    *npe* : number of expected photoelectrons
    *scinttau* : scintillator decay time
    *jittersigma* : sigma of photodetector time jitter
    *pulsemodel* : pulse model
    *threshold* : threshold of timing trigger (fraction of the pulse maximum)
    '''
    fig = plt.figure(figsize=(12,4))
    ncurves = 20
    xtot= np.zeros(nevts)
    plt.subplot(121)
    for j in xrange(nevts):
        tevent = event_pulse(dtpop, npe, scinttau= scinttau, jittersigma= jittersigma, pmodel= pulsemodel)
        if j < ncurves:
            plt.plot(tevent.t, tevent.p, 'b', alpha=0.2)
        plt.plot([0,200],[0,0], 'k-')
        plt.xlabel('ns')
        xtot[j] = time_over_threshold(tevent.t, tevent.p, threshold)
    plt.title('Pulses of %d event'%(ncurves))

    plt.subplot(122)
    plt.hist(xtot, bins=40, histtype='step')
    plt.xlabel('ns')
    plt.title('Trigger times of %d events'%(nevts))
    print 'RMS of time distribution = %.3f ns' % (np.sqrt(xtot.var()))

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

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=1000, scinttau=0.9, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.5)

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=1000, scinttau=0.9, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.1)

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=10000, scinttau=40.0, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.1)

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=1000, scinttau=40.0, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.5)

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=10000, scinttau=40.0, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.5)

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=1000, scinttau=40.0, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.1)

# <codecell>

timing_samples(nevts=1000, dtpop=dtpop, npe=750, scinttau=30.0, jittersigma=0.2, pulsemodel=slapd9mm, threshold=0.1)

# <codecell>


