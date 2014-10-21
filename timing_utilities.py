#!/usr/bin/python

import numpy as np
import time
from iminuit import Minuit
from probfit import Chi2Regression
from pycrysray import *

rand = np.random

def sim_timing(crystal, allpos, t0origin, mfp=170, seed=0, print_prog=False):
    '''
    Do the ray-tracing on in the crystal given the initial positions
    of photons. Return a list of times when photons hit the sensor.
    *crystal* : a Crystal
    *allpos* : a 2d array of shape (N, 3) for N space points
    *t0origin* : the position at which t= 0
    *mfp* : mean free path of the photon
    *seed* : random number seed
    *print_prog* : print progress
    '''
    start= time.time()
    rand.seed(seed)
    timings= []
    startpos= []
    nums= len(allpos)
    for j,pos in enumerate(allpos):
        if print_prog and (j+1)%(nums/10)==0:
            print '%.0f%%  t=%d s'%(j/float(nums)*100, time.time()-start)
        x0, d0 = generate_p6(center=pos, dz=1e-6, dr=1e-6)
        # distance between pos and (0,0,z1)
        dist= np.sqrt(((pos-np.array(t0origin))**2).sum())
        # time to travel by speed of light
        t0 = dist/clightcmns
        # create a photon
        photon = Photon(pos, d0, t=t0, mfp=mfp)
        # propagate in the crystal
        pl = photon.propagate(crystal)
        if photon.status != photon.transmitted: continue
        if photon.lastplane is None: continue
        if photon.lastplane.sensitive:
            timings.append(photon.t)
            startpos.append(photon.startx)

    startpos= np.array(startpos)
    zips= zip(timings, startpos[:,0], startpos[:,1], startpos[:,2])
    return np.array(zips, dtype=[('t', '<f8'), ('x0', '<f8'), ('y0', '<f8'),
                                 ('z0', '<f8')])


def sample_arrival_times(dtpop, npe):
    '''
    Random sample from an array of times. Return an array of times.
    Entries are allowed to be repeated (sample with replacement).
    *dtpop* : the timing population array to sample from
    *npe* : number of entries to sample.
    '''
    idx = rand.random_integers(0, len(dtpop)-1, size= npe);
    return dtpop[idx]

def convolve_decay(dt, tau):
    '''
    Convolve dt array with an exponential decay of lifetime tau
    '''
    return dt + rand.exponential(tau, size= len(dt))

def convolve_gaussian(dt, sigma, mean=0):
    '''
    Convolve dt array with a Gaussian
    '''
    return dt + rand.normal(mean, sigma, size= len(dt))

def make_bins(x, subdiv=1):
    '''
    Create bin edges so that the bin centers are x.
    Then divide bins into subdiv subdivisions.
    '''
    bins = 0.5*(x[1:]+x[:-1])
    bins = np.concatenate([[2*x[0]-bins[0]], bins, [2*x[-1]-bins[-1]]])
    subdiv = int(subdiv)
    retval=[]
    if subdiv > 0:
        for i in xrange(subdiv):
            dx = i/float(subdiv)
            retval.append(bins[:-1]*(1-dx) + bins[1:]*dx)
        retval.append([bins[-1]])
    retval = np.sort(np.concatenate(retval))
    return retval

def pulse_model(filename, vtime, vpulse, normtype=None, normalize=1.0):
    '''
    Get a photodetector pulse model.
    Return a recarray of dtype 't' and 'p'.
    *filename* : a csv file name
    *vtime* : field name for the time
    *vpulse* : field name for the pulse
    *normtype* : 'peak' (maximum normalized to *normalize*)
                 'sum' (sum normalized to *normalize*)
                 'area' (integral normalized to *normalize*)
    '''
    X = np.recfromcsv(filename)
    X = X[[vtime, vpulse]].view(np.recarray)
    X.dtype.names = 't', 'p'
    if normtype == 'peak':
        X.p = X.p / X.p.max() * normalize
    elif normtype == 'sum':
        X.p = X.p / X.p.sum() * normalize
    elif normtype == 'area':
        bs = make_bins(X.t)
        deltat = bs[1:]-bs[:-1]
        area = (deltat*X.p).sum()
        X.p = X.p / area * normalize
    return X

def fill_gaps(x, y, ndivs=10, dtype=None):
    '''
    Insert points by dividing each consecutive pair into *ndivs* using linear
    interpolation for a set of (*x*, *y*), and return a recarray with 
    dtype = *dtype*
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

def fill_pmodel_gaps(pmodel, ndivs):
    return fill_gaps(pmodel.t, pmodel.p, ndivs, pmodel.dtype)

def convolve_pulse_model(dt, pulsemodel):
    '''
    *dt* : an array of timing values of N photoelectrons
    *pulsemodel* : a recarray with fields 't' and 'p' to model a pulse
    Return a recarray with fields 't' and 'p' after convolving these two
    timing distribution.
    Note, the region of t<0 are removed. Returning timing maximum is the same
    as that in *pulsemodel*.
    '''
    # Remove t<0
    pm = pulsemodel[pulsemodel.t>=0]
    # Fill dt to a histogram.
    bins = make_bins(pm.t)
    hdt, be = np.histogram(dt, bins=bins)
    # convolve
    dtconv = np.convolve(hdt, pm.p)[:len(pm)]
    # build a recarray
    retval= np.array(zip(pm.t, dtconv), dtype=pm.dtype).view(np.recarray)
    retval = retval[(retval.t>=pm.t[0])&(retval.t<=pm.t[-1])].view(np.recarray)
    return retval

def event_pulse(dtpop, npe0, scinttau, jittersigma, noise, pulsemodel):
    '''
    Random sample a set of times, where the number of entries is a Poisson
    distribution with the mean=npe0. They are then convolved with the
    scintillator decay time, photodetector time jitter, and the pulse model.

    Return a recarray with fields 't' and 'p' to represent a signal
    pulse of an incident particle at a scintillator detector.
    All time unit is in ns.

    *dtpop* : the arrival time sample population (from ray-tracing simulation)
    *npe0* : expected number of detected photoelectrons
    *scinttau* : scintillator decay time
    *jittersigma* : photodetector time jitter sigma
    *noise* : each point on the pulse curve (for entire event) is added a 
              random number generated from a normal distribution with width
              equal to *noise*.
    *pulsemodel* : photodetector pulse model
    '''
    npe = rand.poisson(npe0)
    tsample = sample_arrival_times(dtpop, npe)
    dt1 = convolve_decay(tsample, tau=scinttau)
    dt2 = convolve_gaussian(dt1, sigma= jittersigma, mean=0)
    dtrec = convolve_pulse_model(dt2, pulsemodel)
    if noise>0:
        ndt = rand.normal(0, noise, size=len(dtrec))
        dtrec.p = dtrec.p+ ndt
    return dtrec

def find_nearest_index(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def interpo(y, t1, t2, y1, y2):
    return t1 + (t2-t1)/(y2-y1)*(y-y1)

def interpolinear(y, xi, yi):
    '''
    Given an array *xi* and an array *yi*, fit a linear function.
    Then solve x for a given y.
    '''
    # fitting y= mx + b
    xybar = (xi*yi).mean()
    xbar = xi.mean()
    ybar = yi.mean()
    x2bar = (xi**2).mean()
    m = (xybar - xbar*ybar)/(x2bar-xbar**2)
    b = ybar - m*xbar
    return (y-b)/m

def poly3(x, a0, a1, a2, a3):
    return a0+x*(a1+x*(a2+x*a3))

def interpo_poly3(y, xi, yi, xref):
    '''
    Given an array *xi* and an array *yi*, fit a 3rd-order polynomial.
    Then solve x for a given y.
    '''
    x2reg= Chi2Regression(poly3, xi, yi)
    m= Minuit(x2reg, print_level=0, pedantic=False)
    m.migrad()
    # Solve x for a given y
    coefs= [m.values[k] for k in ['a3','a2','a1','a0']]
    coefs[-1]-= y
    roots = np.roots(coefs)
    # get the one that is closest to xref
    dist= 1e9
    rt= None
    for r in roots:
        if np.abs(xref-r) < dist:
            dist=  np.abs(xref-r)
            rt = r
    if r is None:
        raise ValueError('Cannot find the proper root')
    return r

def time_reach_threshold(xt0, pulse, fthreshold):
    '''
    Find the time at which pulse goes pass the threshold
    *xt0*: an array of times
    *pulse*: an array of pulse height (at time of *xt*)
    *fthreshold*: a fraction of the pulse maximum
    '''
    if len(xt0)!=len(pulse):
        raise ValueError('The lengths of xt and pulse are different')

    idxmax = find_nearest_index(pulse, pulse.max())
    threshold = pulse.max() * fthreshold
    # rising part
    prise = pulse[:idxmax]
    xt = xt0[:idxmax]
    if len(prise)==0:
        return None
    # find the point near the threshold

    jt = find_nearest_index(prise, threshold)
    # select +-0.25 ns region and above certain level, then do linear
    # interpolation
    sel = (xt>=xt[jt]-0.25)&(xt<=xt[jt]+0.25)&(prise>0.2*threshold)
    return interpolinear(threshold, xt[sel], prise[sel])


def timing_samples(dtpop, npe0, scinttau, jittersigma, pulsemodel, noise,
                   fthreshold, n):
    '''
    Return an array of the trigger times over threshold
    *dtpop* : photon arrival time population to sample from
    *npe0* : number of expected photoelectrons
    *scinttau* : scintillator decay time
    *jittersigma* : sigma of photodetector time jitter
    *pulsemodel* : pulse model
    *fthreshold* : threshold of timing trigger (fraction of the pulse maximum)
    *noise* : each point on the pulse curve (for entire event) is added a 
              random number generated from a normal distribution with width
              equal to *noise*.
    *n* : number of event samples
    '''
    xtot = np.zeros(n)
    tot = None
    for j in xrange(n):
        while tot is None:
            tevent = event_pulse(dtpop, npe0, scinttau, jittersigma, noise,
                                 pulsemodel)
            tot= time_reach_threshold(tevent.t, tevent.p, fthreshold)
        xtot[j] = tot
        tot = None
    return xtot

def draw_pulse_samples(ax, dtpop, npe0, scinttau, jittersigma, noise, 
                       pulsemodel, n, **kwargs):
    '''
    Draw *n* sample event pulse curves
    *ax* : plot axis
    Other arguments are the same as timing_samples
    '''
    for j in xrange(n):
        tevent = event_pulse(dtpop, npe0, scinttau, jittersigma, noise,
                             pulsemodel)
        ax.plot(tevent.t, tevent.p, **kwargs)
    ax.plot([tevent.t[0], tevent.t[-1]], [0,0], 'k')
    ax.set_xlabel('ns', fontsize='large')
    #ax.set_ylabel('arbitrary unit', fontsize='large')
    return ax
