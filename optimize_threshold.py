# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Optimize threshold</h1>
# 
# Optimize trigger threshold to minimize the timing uncertainty

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
rand = np.random
from timing_utilities import *
from geometry_collection_1 import *
from gen_utilities import *

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

# The timing population to sample from
dtpop = np.load('../data/timing/ts_baf2_hex_33_200_n200k_0001.npy')
print 'Population ' , len(dtpop)

# <codecell>

slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')

# <codecell>

dtrms= []
dtrmse= []
thrs= [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.3, 0.5, 0.7, 0.8, 0.9]
for th in thrs:
    tot = timing_samples(dtpop, 1000, 0.9, 0.2, slapd9mm, noise= 10, fthreshold= th, n=1000)
    rms= np.sqrt(tot.var())
    dtrms.append(rms)
    dtrmse.append(rms/np.sqrt(2*len(tot)))

# <codecell>

plt.errorbar(thrs, dtrms, dtrmse, fmt='bo')
plt.ylim(0,1)

# <codecell>

tot = timing_samples(dtpop, 1000, 0.9, 0.2, slapd9mm, noise= 10, fthreshold= 0.1, n=1000)
print tot.var()

# <codecell>

plt.hist(tot, bins=40, histtype='step');

# <codecell>


