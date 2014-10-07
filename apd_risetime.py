# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Rise time of APD signal of a shower</h1>
# 
# Load the result from photon arrival time calculated in photon_collection_time.ipynb. Convolute it with scintillation decay time. Then convolute it with the APD response time, to obtain the rise time of a shower signal.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rand

# <codecell>

# Load photon arrival time, assuming no scintillation decay time
dtarr0 = np.load('timing/arrival_time_hex_bf2_21cm_gaussianshower.npy')

# <markdowncell>

# <h2>Convolution with scintillation decay time</h2>

# <codecell>

# 0.9 ns decay time of BF2 fast component
tau_bf2= 0.9
sdt_bf2 = rand.exponential(tau_bf2, size=len(dtarr0))

# <codecell>

dt_lin2= dtarr0+sdt_bf2
fig= plt.figure(figsize=(10,4))
plt.subplot(121)
plt.hist(dt_lin2, bins=100, histtype='step');
plt.xlabel('t (ns)')
plt.title('Photon traveling+scintillation time')
plt.subplot(122)
plt.hist(dt_lin2[dt_lin2<4], bins=40, histtype='step');
plt.xlim(0,4)
plt.xlabel('t (ns)')
plt.title('Photon traveling+scintillation time')
fig.savefig('plots/timing_hex_bf2_21cm_gaussianshower_scint.pdf')

# <codecell>

print len(dtarr0)

# <markdowncell>

# <h2>APD response time measurement</h2>

# <codecell>

risetime = np.recfromcsv('SLAPD_RiseTime.csv')
print risetime.dtype
# Remove time<0
risetime= risetime[risetime.time_ns>0]

# <codecell>

plt.plot(risetime.time_ns, risetime.slapd9mm, label='SL-APD 9mm')
plt.plot(risetime.time_ns, risetime.stdapd9mm, label='Std-APD 9mm')
plt.plot(risetime.time_ns, risetime.slapd3mm, label='SL-APD 3mm')
plt.legend()
plt.xlabel('ns')
plt.title('APD response time')
plt.savefig('plots/timing_apdrise.pdf')

# <codecell>

# Create bins that center at time_ns
tbins= 0.5*(risetime.time_ns[1:]+risetime.time_ns[:-1])
# add an edge at the beginning
tbins = np.concatenate([[0],tbins])
# Fill an histogram of photon arrival time using the binning
harrival, binedges = np.histogram(dt_lin2, bins= tbins)

# <markdowncell>

# <h4>Plot photon arrival time in the same scale as the APD response time above</h4>

# <codecell>

plt.plot(risetime.time_ns[:798], harrival[:798])
plt.title('Photon Arrival Time')
plt.xlabel('ns')
plt.savefig('plots/timing_hex_bf2_21cm_gaussianshower_scint_scale.pdf')

# <markdowncell>

# <h4>Convolution of arrival time and APD response time</h4>

# <codecell>

tslapd9mm =  np.convolve(harrival, risetime.slapd9mm)
tstdapd9mm = np.convolve(harrival, risetime.stdapd9mm)
tslapd3mm =  np.convolve(harrival, risetime.slapd3mm)

# <codecell>

npt= len(risetime.time_ns)
plt.plot(risetime.time_ns, tslapd9mm[:npt], label='SL-APD 9mm')
plt.plot(risetime.time_ns, tstdapd9mm[:npt], label='Std-APD 9mm')
plt.plot(risetime.time_ns, tslapd3mm[:npt], label='SL-APD 3mm')
plt.legend()
plt.title('Photon Arrival Time Convoluted with APD Response Time')
plt.xlabel('ns')
plt.savefig('plots/timing_hex_bf2_21cm_gaussianshower_apd.pdf')

# <markdowncell>

# <h4>Zoom in </h4>

# <codecell>

npt= len(risetime.time_ns)
plt.plot(risetime.time_ns, tslapd9mm[:npt], label='SL-APD 9mm')
plt.plot(risetime.time_ns, tstdapd9mm[:npt], label='Std-APD 9mm')
plt.plot(risetime.time_ns, tslapd3mm[:npt], label='SL-APD 3mm')
plt.legend(loc='upper left')
plt.title('Photon Arrival Time Convoluted with APD Response Time')
plt.xlabel('ns')
plt.xlim(10,60)
plt.savefig('plots/timing_hex_bf2_21cm_gaussianshower_apd_zoom.pdf')

# <markdowncell>

# <h3>Calculate rise time</h3>
# 
# The time from 10% pulse height to 90% pulse height

# <codecell>

def find_nearest_index(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx
def interpo(y, t1, t2, y1, y2):
    return t1 + (t2-t1)/(y2-y1)*(y-y1)

# <codecell>

def rise_time(t, ph, plo=0.1, phi=0.9):
    '''
    Return time between pulse height from plo to phi
    *t*: time axis
    *ph*: pulse height at time t
    '''
    pheight = np.array(ph[:len(t)])
    # normalized pulse (max at 1)
    pheight = pheight/pheight.max()
    # find the maximum index
    idxmax= find_nearest_index(pheight, 1)
    # Remove everything after the maximum
    pheight = pheight[:idxmax]
    # Find the nearest at plo and phi
    j1= find_nearest_index(pheight, plo)
    j2= find_nearest_index(pheight, phi)
    # Interpolation
    k1, k2= j1, j1+1
    if ph[j1]>plo:
        k1, k2= j1-1, j1
    t1 = interpo(plo, t[k1], t[k2], pheight[k1], pheight[k2])
    k1, k2= j2, j2+1
    if ph[j2]>phi:
        k1, k2= j2-1, j2
    t2 = interpo(phi, t[k1], t[k2], pheight[k1], pheight[k2])
    return t2-t1

# <codecell>

rt_slapd9mm = rise_time(risetime.time_ns, tslapd9mm)
rt_stdapd9mm = rise_time(risetime.time_ns, tstdapd9mm)
rt_slapd3mm = rise_time(risetime.time_ns, tslapd3mm)

# <codecell>

print 'Rise time (ns)'
print '%12s : %5.1f' % ('SL-APD 9mm', rt_slapd9mm)
print '%12s : %5.1f' % ('STD-APD 9mm', rt_stdapd9mm)
print '%12s : %5.1f' % ('SL-APD 9mm', rt_slapd3mm)

# <codecell>


