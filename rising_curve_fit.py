# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Fit to rising curve</h1>

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt

# <codecell>

import numpy as np
import pickle
rand = np.random
from timing_utilities import *
from iminuit import Minuit
from probfit import Chi2Regression

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

slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')
apdmodel = fill_pmodel_gaps(slapd3mm, 10)

# <codecell>

fig= plt.figure()
ax= fig.add_subplot(111)
draw_pulse_samples(ax, rectdata['baf2ra3'].t, npe0= 10000, scinttau= 0.9, jittersigma= 0.1, noise= 100, pulsemodel= apdmodel, 
                   n=1, color='b', alpha=1, marker='o')
plt.xlim(10,25)

# <codecell>

rand.seed(0)
tevent= event_pulse(rectdata['baf2ra3'].t, npe0=10000, scinttau= 0.9, jittersigma= 0.1, noise= 100, pulsemodel= apdmodel)

# <codecell>

imax= np.argmax(tevent.p)
print imax, tevent.t[imax]
imax= imax

# <codecell>

plt.plot(tevent.t[:imax], tevent.p[:imax], '.')

# <codecell>

xt = tevent.t
pulse = tevent.p
fthreshold= 0.1
idxmax = find_nearest_index(pulse, pulse.max())
threshold = pulse.max() * fthreshold
# rising part
prise = pulse[:idxmax]
tpr = xt[:idxmax]

# <codecell>

print idxmax, pulse.max()

# <codecell>

jt = find_nearest_index(prise, threshold)
j1 = max(0, jt-10)
j2 = min(jt+10, idxmax)

# <codecell>

plt.plot(tpr, prise,'-')
plt.plot(tpr[j1:j2], prise[j1:j2], 'o')
plt.plot([0,18],[threshold,threshold])
plt.xlim(13.5,14.5)
plt.ylim(0,2000)

# <codecell>

def poly1(x, a0, a1):
    return a0+x*a1
def poly2(x, a0, a1, a2):
    return a0+x*(a1+x*a2)
def poly3(x, a0, a1, a2, a3):
    return a0+x*(a1+x*(a2+x*a3))
def poly4(x, a0, a1, a2, a3, a4):
    return a0+x*(a1+x*(a2+x*(a3+x*a4)))
def poly5(x, a0, a1, a2, a3, a4, a5):
    return a0+x*(a1+x*(a2+x*(a3+x*(a4+x*a5))))

# <codecell>

x2reg= Chi2Regression(poly3, tpr[j1:j2], prise[j1:j2])#, error=np.sqrt(np.abs(prise[j1:j2])))
m= Minuit(x2reg, print_level=0, pedantic=False)

# <codecell>

m.migrad()

# <codecell>

x2reg.draw(m);

# <codecell>

print m.values
c = [m.values['a3'],m.values['a2'],m.values['a1'], m.values['a0']]
c[-1]-= threshold
print c

# <codecell>

np.roots(c)

# <codecell>

apdmodel.dtype

# <codecell>

def fill_gaps(x, y, ndivs=10, dtype=None):
    '''
    Insert points by dividing each consecutive pair into *ndivs* using linear interpolation for a set of (*x*, *y*), 
    and return a recarray with dtype = *dtype*
    '''
    if len(x)!= len(y):
        raise ValueError('Input x and y must have the same length')
    ntotal = (len(x)-1)*ndivs + 1
    xf = np.zeros(ntotal)
    yf = np.zeros(ntotal)
    for j in xrange(len(x)-1):
        x1, x2= x[j], x[j+1]
        y1, y2= y[j], y[j+1]
        dx = (x2-x1)/float(ndivs)
        dy = (y2-y1)/float(ndivs)
        for k in xrange(ndivs):
            xf[j*ndivs+k]= x1 + k*dx
            yf[j*ndivs+k]= y1 + k*dy
    xf[-1]= x[-1]
    yf[-1]= y[-1]
    if dtype is None:
        dtype= dtype([('x', '<f8'), ('y', '<f8')])
    retval= np.array(zip(xf,yf), dtype= dtype).view(np.recarray)
    return retval

# <codecell>

def fill_pmodel_gaps(pmodel, ndivs):
    return fill_gaps(pmodel.t, pmodel.p, ndivs, pmodel.dtype)

# <codecell>

nmodel = fill_gaps(apdmodel.t, apdmodel.p, dtype=apdmodel.dtype)

# <codecell>

len(nmodel)

# <codecell>

plt.plot(nmodel.t, nmodel.p, '.')
plt.plot(apdmodel.t, apdmodel.p, 'o')
plt.xlim(12,14)

# <codecell>

plt.plot(nmodel.t)

# <codecell>


