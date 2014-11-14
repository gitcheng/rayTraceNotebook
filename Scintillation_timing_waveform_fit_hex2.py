# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Scintillation timing waveform fit precision for hexagonal-cross-section crystal bars</h1>

# <markdowncell>

# * Use data produced by <b><code>scripts/time\_geom2\_hex\_*.py</code></b>
# * Geometry defined in <b><code>geometry_collection_2</code></b>
# * See more detail in <b><code>Scintillation_timing_precision_hex2</code></b>

# <markdowncell>

# <h2>Waveform fit</h2>
# 
# After an event pulse is formed (see Scintillation_timing_precision_hex2), we sample the pulse into a digitized waveform. The sampling frequency is possibly a few hundred MHz, that is, the interval is a few ns. We test a few different intervals to show the effect on the interval.
# 
# The waveform is then fit with a model, $A(t) = e^{-(t-t_0)/\tau_d}-e^{-(t-t_0)/\tau_r}$ convolved with a Gaussian. The range of the fit is to be optimized. The time shift parameter $t_0$ is approximately the time the curve crosses 50% (?) of the maximum. We simulate a number (1000) of signals in each setting, sample the waveform with a random starting time of the bins, then fit for the model. We record all parameters in each fit. The distribution of $t_0$ can be viewed as the timing precision. We can also reconstruct the function and examine the distribution of the time a curve reaches 10% of the maximum, which may have a better precision.

# <markdowncell>

# The pdf function of an exponential convolved with a Gaussian can be expressed as
# 
# $\begin{equation}
# G_{\rm exp}(t; \sigma, \tau) = \frac{1}{2\tau} e^{\sigma^2/2\tau^2}\left[ 1- {\rm erf}(\frac{-t}{\sqrt{2}\sigma} + \frac{\sigma}{\sqrt{2}\tau})\right]
# \end{equation}$
# 
# Therefore, the function $A(t)$ convolved with a Gaussian is
# 
# $\begin{equation}
# B(t; t_0, \sigma, \tau_1, \tau_2) = \frac{1}{\tau_1-\tau_2}\left[\tau_1 G_{\rm exp}(t-t_0, \sigma, \tau_1)- \tau_2 G_{\rm exp}(t-t_0, \sigma, \tau_2) \right]
# \end{equation}$

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
from fit_utilities import *
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
# Sensors: two 9 mm X 9 mm photosensors (ignore 3x3 case).

# <codecell>

fig= plt.figure(figsize=(9,10))
cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
i=0
for mat in ['lyso','baf2','csi']:
    for sd in ['9']:
        key = mat+'po'+sd
        ax = fig.add_subplot(131+i, projection='3d')
        ax.set_title(cnames[mat])
        draw_one_crystal(ax, chexes[key])
        i+= 1

# <codecell>

# The timing population to sample from
# Only need polished, 9x9
hexdata= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po']:
        for sd in ['9']:
            key= mat+sur+sd
            filename= '../data/timing/time_geom2_hex_%s.npy'%(key)
            data = np.load(filename).view(np.recarray)
            hexdata[key]= data
            print '%s population : %d'%(key,len(data))

# <markdowncell>

# <h2>APD pulse model</h2>

# <codecell>

slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
# Fill in points using linear interpolation
slapd9mm = fill_pmodel_gaps(slapd9mm, ndivs=5)
# t>=0
slapd9mm = slapd9mm[slapd9mm.t>0]

# <codecell>

t= slapd9mm.t
ps= pulse_shape_simple(t, 6.0, 15.0, 1.0)
pream= np.array(zip(t,ps), dtype=slapd9mm.dtype).view(np.recarray)
plt.plot(pream.t, pream.p)
plt.title('Preamp model');
plt.xlabel('ns');

# <codecell>

pmslapd9mm= convolve_two_pulse_model(slapd9mm, pream)

# <codecell>

plt.plot(pmslapd9mm.t, pmslapd9mm.p/pmslapd9mm.p.max(), label='SL-APD 9mm');
plt.xlim(0,200)
plt.ylim(-0.2,1.1)
plt.plot([0,200],[0,0], 'k-')
plt.legend()
plt.xlabel('ns');
plt.title('APD+Preamp response time');

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

def draw_waveform(ax, event, title=None, **kwargs):
    bins= make_bins(event.t)
    ax.hist(event.t, bins=bins, weights=event.p, **kwargs)
    ax.plot([event.t.min(),event.t.max()],[0,0], 'k-')
    ax.set_xlim(event.t.min(), event.t.max())
    if title is not None:
        ax.set_title(title)
    ax.set_xlabel('ns')
    ax.set_ylabel('Arbitrary unit')
    ax.grid()

# <codecell>

def draw_one_set(ax, dtpop, scinttau, npe0, pulsemodel, title):
    draw_pulse_samples(ax, dtpop, npe0= npe0, scinttau= scinttau, jittersigma= 0.1, noise= 0, pulsemodel= pulsemodel, n=20,
                       color='b', alpha=0.2)
    ax.set_title(title)

# <codecell>

tbaf29mm = event_pulse(hexdata['baf2po9'].t, npe_baf2, tau_baf2, 0.1, 0, pmslapd9mm)
tlyso9mm = event_pulse(hexdata['lysopo9'].t, npe_lyso, tau_lyso, 0.1, 0, pmslapd9mm)
tcsi9mm = event_pulse(hexdata['csipo9'].t, npe_csi, tau_csi, 0.1, 0, pmslapd9mm)

# <codecell>

wfbaf29mm5ns = digiwaveform(tbaf29mm, 5.0)
wflyso9mm5ns = digiwaveform(tlyso9mm, 5.0)
wfcsi9mm5ns = digiwaveform(tcsi9mm, 5.0)

# <codecell>

fig= plt.figure(figsize=(18,4))
ax= fig.add_subplot(131)
draw_waveform(ax, wfbaf29mm5ns, title='BaF2', histtype='step')
ax= fig.add_subplot(132)
draw_waveform(ax, wflyso9mm5ns, title='LYSO', histtype='step')
ax= fig.add_subplot(133)
draw_waveform(ax, wfcsi9mm5ns, title='CsI', histtype='step')
fig.savefig('../plots/waveform_9mm5ns.pdf')

# <codecell>

def waveformfit(wf, fitrange=None):
    '''
    *wf*: waveform
    *fitrange* is the total range of the fit centered at the estimated time over 50% maximum threshold
    '''
    # t reaching half maximum, used for initial value of x0
    t50 = time_reach_threshold(wf.t, wf.p, 0.5)
    tmax = wf.t[wf.p.argmax()]
    # estimate integral
    bins = make_bins(wf.t)
    bw= bins[1:]-bins[:-1]
    intl= float((wf.p*bw).sum())
    
    if fitrange is not None:
        sel = (wf.t>=t50-fitrange/2.)&(wf.t<=t50+fitrange/2.)
        wf= wf[sel]
    initpars= dict(x0=t50, error_x0=1, N= intl, error_N=sqrt(intl), sigma=5, error_sigma=1,\
                   tau1= 70, error_tau1=1, tau2=5, error_tau2=1)
    limits= dict(limit_x0=(0,200), limit_N=(0,intl*5), limit_tau1=(10,200), limit_tau2=(0.1,100), limit_sigma=(0.1,100))
    initpars = dict(initpars.items() + limits.items())
    x2, mn = fit_gexp(wf.t, wf.p, print_level=0, **initpars)
    return x2, mn

# <codecell>

def waveformfitset(dtpop, npe, tau, jittersigma, noise, apdmodel, binwidth, nfits, fitrange):
    results= []
    for i in xrange(nfits):
        pulse = event_pulse(dtpop, npe, tau, jittersigma, noise, apdmodel)
        wf = digiwaveform(pulse, binwidth, nprnd.uniform())
        x2, mn= waveformfit(wf, fitrange)
        results.append(mn.values)
    return results

# <codecell>

# Test one fit
pulse = event_pulse(hexdata['baf2po9'].t, 1000, 0.9, 0.1, 0.0, pmslapd9mm)
wf = digiwaveform(pulse, binwidth=5.0, tshift=0.2)
x2, mn = waveformfit(wf, 100)

# <codecell>

x2.draw(mn);
plt.xlabel('ns')
plt.savefig('../plots/waveform_fit_exp.pdf')

# <codecell>

# Test another fit
wf2 = digiwaveform(pulse, binwidth=2.0, tshift=0.2)
x2, mn = waveformfit(wf2, 100)
x2.draw(mn);
plt.xlabel('ns')
plt.savefig('../plots/waveform_fit_exp2ns.pdf')

# <markdowncell>

# <h2>Start toys</h2>

# <codecell>

nfits= 1000
binwidths= [1, 2, 3, 5, 7, 10]
npes = [300, 1000, 3000, 10000]
fitrange= 100
nprnd.seed(0)
for bw in binwidths:  
    for npe in npes:
        results= waveformfitset(hexdata['baf2po9'].t, npe= npe, tau= tau_baf2, jittersigma=0.1, noise=0.0, apdmodel= pmslapd9mm,
                                binwidth=bw, nfits=nfits, fitrange=fitrange)
        fn = '../data/timing/wffit_baf2po9_npe%d_bw%d_fr%d.p'%(npe,bw,fitrange)
        print fn
        pickle.dump(results, open(fn, 'wb'))

# <codecell>

nfits= 1000
binwidths= [10]
npes = [300, 1000, 3000, 10000]
fitrange= 100
nprnd.seed(0)
for bw in binwidths:  
    for npe in npes:
        results= waveformfitset(hexdata['baf2po9'].t, npe= npe, tau= tau_baf2, jittersigma=0.1, noise=0.0, apdmodel= pmslapd9mm,
                                binwidth=bw, nfits=nfits, fitrange=fitrange)
        fn = '../data/timing/wffit_baf2po9_npe%d_bw%d_fr%d.p'%(npe,bw,fitrange)
        print fn
        pickle.dump(results, open(fn, 'wb'))

# <codecell>

s= [0,1,2]
s= s[:-1]
print s
s= s[1:]
print s
print len(s)

# <codecell>


# <codecell>


# <codecell>


# <codecell>


# <codecell>

plt.plot(wf1.t, wf1.p, 'bo-')
plt.plot(wf2.t, wf2.p, 'rx-')

# <codecell>

ts = tevent.t
ys = GExp2(ts, 30, 10, 50, 10, 400)
plt.plot(wf.t, wf.p, 'bo')
plt.plot(ts, ys, 'r-')

# <codecell>

x2reg= Chi2Regression(GExp2, wf.t, wf.p)
m= Minuit(x2reg, print_level=1, x0=30, sigma=5, tau1= 50, tau2=10, N=500)
m.migrad()
m.hesse()

# <codecell>

x2reg.draw(m);

# <codecell>


# <codecell>


# <codecell>


# <codecell>


# <codecell>

x2reg, m= fit_pulse_simple(tevent.t, tevent.p, None, x0=20, tauR=10, tauD=20, A=100)

# <codecell>

x2reg.draw(m);

# <codecell>

plt.plot(tb, hist, 'bo', ms=1)
plt.plot(tevent.t, tevent.p*200)

# <codecell>

plt.plot(tb, hist-tevent.p*200, 'bo')

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

# <h3>SL APD 3mm pulse model</h3>

# <codecell>

fig= plt.figure(figsize=(12,3.5))
ax= fig.add_subplot(131)
draw_one_set(ax, hexdata['baf2po3'].t, tau_baf2, npe_baf2, pmslapd3mm, 'BaF2')
ax= fig.add_subplot(132)
draw_one_set(ax, hexdata['lysopo3'].t, tau_lyso, npe_lyso, pmslapd3mm, 'LYSO')
ax= fig.add_subplot(133)
draw_one_set(ax, hexdata['csipo3'].t, tau_csi, npe_csi, pmslapd3mm, 'CsI')

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
apdlist = [pmslapd9mm, pmslapd3mm, pmstdapd9mm]
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

###pickle.dump(result, open('../data/timing/tprecision_hex_preamp_geocolls2.p', 'wb'))

# <codecell>

result.keys()

# <codecell>

mn.print_param()

# <codecell>


