# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw waveform fit results</h1>
# 
# Draw results from <b><tt>Scintillation_timing_waveform_fit_hex2</tt></b>

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import pickle
from timing_utilities import *
from fit_utilities import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator
from matplotlib.ticker import ScalarFormatter

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

def bnkeys(bw, npe):
    return '%d-%d'%(bw, npe)

# <codecell>

majorLocator   = MultipleLocator(0.5)
majorFormatter = FormatStrFormatter('%.1f')

# <markdowncell>

# <h2>t0 distribution</h2>

# <codecell>

binwidths= [1, 2, 3, 5, 7, 10]
npes = [300, 1000, 3000, 10000]
fitrange= 100

# <codecell>

t0dists= {}
fig= plt.figure(figsize=(15, 18))
i= 1
for bw in binwidths:  
    for npe in npes:
        ax = plt.subplot(6,4,i)
        i+= 1
        fn = '../data/timing/wffit_baf2po9_npe%d_bw%d_fr%d.p'%(npe,bw,fitrange)
        wffit = pickle.load(open(fn))
        x0s = np.array([d['x0'] for d in wffit])
        t0dists[bnkeys(bw,npe)] = np.sqrt(x0s.var())
        plt.hist(x0s, bins=40, histtype='step');
        plt.title('%d ns, %d p.e.'%(bw, npe))
        ax.xaxis.set_major_locator(MaxNLocator(5))
fig.savefig('../plots/waveform_baf2po9_t0fitshist.pdf')

# <markdowncell>

# <h2>Timing at fixed fraction threshold</h2>

# <codecell>

def ts_atfrac(threshold, draw=False):
    
    results= {}
    if draw:
        fig= plt.figure(figsize=(15, 18))
    i= 1
    for bw in binwidths:  
        for npe in npes:
            print bw, npe,
            fn = '../data/timing/wffit_baf2po9_npe%d_bw%d_fr%d.p'%(npe,bw,fitrange)
            wffit = pickle.load(open(fn))
            x= np.linspace(0, 100, 10001)
            ttr=[]
            for pars in wffit:
                y = GExp2(x, **pars)
                ttr.append(time_reach_threshold(x, y, threshold))
            results[bnkeys(bw,npe)] = np.sqrt(np.array(ttr).var())
            if draw:
                ax = plt.subplot(6,4,i)
                i+= 1
                plt.hist(ttr, bins=40, histtype='step');
                plt.title('%d ns, %d p.e.'%(bw, npe))
                ax.xaxis.set_major_locator(MaxNLocator(5))
    return results

# <codecell>


# <codecell>

result01= ts_atfrac(threshold=0.1, draw=True)
plt.savefig('../plots/waveform_baf2po9_th01_fitshist.pdf')

# <codecell>

result02= ts_atfrac(threshold=0.2, draw=False)

# <codecell>

result03= ts_atfrac(threshold=0.3, draw=False)

# <codecell>

result005= ts_atfrac(threshold=0.05, draw=False)

# <markdowncell>

# <h3>Timing precision at threshold of 0.1</h3>

# <codecell>

fig= plt.figure(figsize=(8,6))
mks= ['o','s','^','d']
for npe,mk in zip(npes,mks):
    rr= []
    for bw in binwidths:
        rr.append(result01[bnkeys(bw,npe)]*1e3)
    plt.errorbar(binwidths, rr, fmt=mk+'-', label='%d p.e.'%(npe))
plt.yscale('log')
plt.xlim(0, 11)
plt.ylim(10,400)
plt.axes().get_yaxis().set_major_formatter(ScalarFormatter())
plt.xlabel('Digi binwidth (ns)', fontsize='x-large')
plt.ylabel('Timing precision (ps)', fontsize='x-large')
plt.legend(fontsize='large', loc='lower right')
plt.grid(which='major')
plt.grid(which='minor')
fig.savefig('../plots/timing_digibinwidth_baf2po9_th01.pdf')

# <markdowncell>

# <h3>Timing precision of the fit parameter x0</h3>

# <codecell>

fig= plt.figure(figsize=(8,6))
mks= ['o','s','^','d']
for npe,mk in zip(npes,mks):
    rr= []
    for bw in binwidths:
        rr.append(t0dists[bnkeys(bw,npe)]*1e3)
    plt.errorbar(binwidths, rr, fmt=mk+'-', label='%d p.e.'%(npe))
plt.yscale('log')
plt.xlim(0, 11)
plt.ylim(10,700)
plt.axes().get_yaxis().set_major_formatter(ScalarFormatter())
plt.xlabel('Digi binwidth (ns)', fontsize='x-large')
plt.ylabel('Timing precision (ps)', fontsize='x-large')
plt.legend(fontsize='large', loc='lower right')
plt.grid(which='major')
plt.grid(which='minor')
plt.savefig('../plots/timing_digibinwidth_baf2po9_t0.pdf')

# <codecell>


# <codecell>


# <headingcell level=2>

# ==============================================================================

# <codecell>


# <codecell>

results= [result005, result01, result02, result03]
ths = [0.05, 0.1, 0.2, 0.3]
rr= []
for res in results:
    rr.append(res[bnkeys(2,1000)])
plt.plot(ths, rr)

# <codecell>


# <codecell>


# <codecell>


# <codecell>

print wffits[1]

# <codecell>

x = np.linspace(0, 100, 1001)
y = GExp2(x, **wffits[1])

# <codecell>

plt.plot(x,y)

# <codecell>

x= np.linspace(0, 100, 10001)
ttr=[]
for pars in wffits:
    y = GExp2(x, **pars)
    ttr.append(time_reach_threshold(x, y, 0.1))

# <codecell>

ttr= np.array(ttr)
print np.sqrt(ttr.var())
plt.hist(ttr, bins=40, histtype='step');

# <codecell>

x= np.linspace(0, 150, 1501)
y1= GExp(x, x0=50, sigma=5.0, tau=10, N=1)
y1a= GExp(x, x0=50, sigma=5.0, tau=5, N=1)
y2= GExp2(x, x0=50, sigma=5.0, tau1= 10.0, tau2= 5.0, N=1)

# <codecell>

plt.plot(x,y1, '-')
plt.plot(x,y1a)
plt.plot(x,y2)
plt.plot(x, (10*y1-5*y1a)/5)
print y1.sum()
print y1a.sum()
print y2.sum()

# <codecell>

from math import pi, sqrt
s2pi = sqrt(2*pi)
def gaudexp(x1, x2, sigma, tau):
    retval= 1.0/(s2pi*sigma) * np.exp(-x2/tau) * np.exp(-0.5*((x1-x2)/sigma)**2)
    sel= x2>=0
    retval = retval*sel
    return retval
def numGexp(x, x0, sigma, tau):
    pp = np.linspace(-1000, 1000, 20001)
    dp = pp[1]-pp[0]
    y = gaudexp(x-x0, pp, sigma, tau) * dp
    return y.sum()

# <codecell>

print numGexp(60,50, 10, 10)
print GExp(60, 50, 10, 10, 1)

# <codecell>

print numGexp(60,50, 4, 10)
print GExp(60, 50, 4, 10, 1)

# <codecell>

x= np.linspace(-100,100,201)
y= gaudexp(10, x, 10, 10)

# <codecell>

plt.plot(x,y)

