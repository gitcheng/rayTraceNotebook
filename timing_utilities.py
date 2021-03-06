#!/usr/bin/python

import numpy as np
import time
from iminuit import Minuit
from probfit import Chi2Regression
from pycrysray import *

rand = np.random

def similar(a, epsilon=1e-12):
    '''
    Return True if a.max()-a.min()<epsilon.
    '''
    aa = np.array(a)
    return aa.max()-aa.min()<epsilon

def sim_timing(crystal, allpos, t0origin, mfp=170, seed=0, print_prog=False):
    '''
    Do the ray-tracing in the crystal given the initial positions
    of photons. Return a list of times when photons hit the sensor.
    Return a recdata with t the arrival time and (x0, y0, z0) the starting
    position of the photon.
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

def sim_timing_shower(crystal, shower, nep, t0origin=(0,0,0), shdir=-1,
                      showerunit= 0.1, mfp= 170, seed= 0, print_prog= False):
    '''
    Do the ray-tracing in the crystal given shower data.
    Return a list of length len(shower). Each element is a recarray of
    length nep with column names t, x0, y0, z0.
    *crystal* : a Crystal
    *shower* : shower data. Each data event contains arrays of hitX, hitY,
    hitZ, hitEdep.
    *nep* : number of photons to create per event
    *toorigin* : the coordinate where the particle hit the crystal.
    *shdir* : the direction of the particle: +1 or -1 (along the z-axis)
              in ray-tracing simulation.
    *showerunit* : the unit length in shower data in cm.
    *mfp* : mean free path of the photon (in cm).
    *seed* : random number seed
    *print_prog* : print progress
    '''
    start = time.time()
    rand.seed(seed)
    ret = []
    nums = len(shower)
    for j in xrange(len(shower)):
        if print_prog and (j+1)%(nums/10)==0:
            print '%.0f%%  t=%d s'%(j/float(nums)*100, time.time()-start)
        event = np.array([(0,)*4]*nep, dtype=[('t', '<f8'), ('x0', '<f8'), ('y0', '<f8'), ('z0', '<f8')])
        # generate a large set of event id with probability equal to Edep
        # Need to recast the type to f8 otherwise choice complains the 
        # normalization is not close enough to one.
        wgts = np.array(shower.hitEdep[j], dtype='<f8')
        wgts /= wgts.sum()
        ids = rand.choice(len(wgts), size=100000, replace=True, p=wgts)
        k = 0
        while k < nep:
            id = int(rand.random() * len(ids))
            x0 = shower.hitX[j][ids[id]] * showerunit
            y0 = shower.hitY[j][ids[id]] * showerunit
            z0 = shower.hitZ[j][ids[id]] * showerunit
            t0 = shower.hitT[j][ids[id]] - shower.hitT[j][0]
            # transform shower because shower data start at 0,0,0 and in +z
            # direction.
            x0 = x0*shdir + t0origin[0]
            y0 = y0*shdir + t0origin[1]
            z0 = z0*shdir + t0origin[2]
            ##print 'j=%d,k=%d, (%.2f,%.2f,%.2f,%.2f)'%(j,k,x0,y0,z0,t0)
            # generate position and direction
            pos, dp = generate_p6(np.array([x0,y0,z0]), dz=1e-6, dr=1e-6)
            # create a photon
            photon = Photon(pos, dp, t=t0, mfp=mfp)
            #propagate in the crystal
            pl = photon.propagate(crystal)
            if photon.status != photon.transmitted: continue
            if photon.lastplane is None: continue
            if photon.lastplane.sensitive:
                event['t'][k] = photon.t
                event['x0'][k] = photon.startx[0]
                event['y0'][k] = photon.startx[1]
                event['z0'][k] = photon.startx[2]
                k += 1
        ret.append(event)
    return ret

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

def convolve_two_pulse_model(pm1, pm2):
    '''
    Convolve two pulse models.
    *pm1*, *pm2*: recarrays with fields 't' and 'p' to model a pulse
    Return a recarray with the same fields after convolving the two shapes.
    The returned pulse covers the same time range as *pm1*.
    '''
    # make sure both models have the same (uniform) time spacing
    dt1 = (pm1.t[1:]-pm1.t[:-1])
    dt2 = (pm2.t[1:]-pm2.t[:-1])
    if not similar([dt1,dt2]):
        raise ValueError('The two models have different time spacing')
    # binwidth
    bw= dt1.mean()
    
    dtconv= np.convolve(pm1.p, pm2.p)[:len(pm1)] * bw
    # build a recarray
    retval= np.array(zip(pm1.t, dtconv), dtype=pm1.dtype).view(np.recarray)
    retval= retval[(retval.t>=pm1.t[0])&(retval.t<=pm1.t[-1])]
    return retval.view(np.recarray)


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
    # check t bins
    if not similar(pm.t[1:]-pm.t[:-1]):
        raise ValueError('Time spacing is not uniform')
    bw= (pm.t[1:]-pm.t[:-1]).mean()

    # Fill dt to a histogram.
    bins = make_bins(pm.t)
    hdt, be = np.histogram(dt, bins=bins)
    # convolve
    dtconv = np.convolve(hdt, pm.p)[:len(pm)] * bw
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
    # interpolation. If there are less than 3 points, force it to use
    # three points
    sel = (xt>=xt[jt]-0.25)&(xt<=xt[jt]+0.25)&(prise>0.2*threshold)
    if sel.sum()<3:
        sel = [jt-1, jt, jt+1]
        if jt+1 >= len(xt):
            sel = sel[:-1]
        if jt-1 <= 0:
            sel = sel[1:]
    if len(sel) < 2:
        return xt[jt]
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
    nd = np.ndim(dtpop)
    for j in xrange(n):
        while tot is None:
            if nd == 1:
                tevent = event_pulse(dtpop, npe0, scinttau, jittersigma, noise,
                                     pulsemodel)
            elif nd == 2:
                # random pick a row, then send that row for sampling
                k = int(rand.uniform() * dtpop.shape[0])
                tevent = event_pulse(dtpop[k], npe0, scinttau, jittersigma,
                                     noise, pulsemodel)
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
    nd = np.ndim(dtpop)
    for j in xrange(n):
        if nd == 1:
            tevent = event_pulse(dtpop, npe0, scinttau, jittersigma, noise,
                                 pulsemodel)
        elif nd == 2:
            # random pick a row, then send that row for sampling
            k = int(rand.uniform() * dtpop.shape[0])
            tevent = event_pulse(dtpop[k], npe0, scinttau, jittersigma, noise,
                                 pulsemodel)
        else:
            raise ValueError('Unknown ndim of dtpop %d'%nd)

        ax.plot(tevent.t, tevent.p, **kwargs)
    ax.plot([tevent.t[0], tevent.t[-1]], [0,0], 'k')
    ax.set_xlabel('ns', fontsize='large')
    #ax.set_ylabel('arbitrary unit', fontsize='large')
    return ax


def pulse_shape_simple(x, tauR, tauD, A, x0=0):
    #if x-x0<0: return 0
    return A* (np.exp(-(x-x0)/tauD)-np.exp(-(x-x0)/tauR))/float(tauD-tauR)
