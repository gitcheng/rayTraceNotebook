#!/usr/bin/python
#
# General utilities

import numpy as np
rand = np.random

def gen_uniform_pos(x1, x2, y1, y2, z1, z2, size):
    '''
    Generate a set of positions, uniformly distributed
    '''
    xpos = rand.uniform(x1, x2, size)
    ypos = rand.uniform(y1, y2, size)
    zpos = rand.uniform(z1, z2, size)
    return np.array(zip(xpos, ypos, zpos))

def gen_gamma_func_shower1(z1, z2, rmax, size):
    '''
    Generate a set of positions, where the z-corrdinate is between z1 and z2, 
    and x-y is in a circle of radius rmas
    '''
    zpos = rand.gamma(shape=3.5, scale=2, size=size*2)
    # Make a cut on zpos at 20 furst, than re-scale zpos so it starts at z2 
    # and ends at z2
    zpos= zpos[zpos<20]
    zpos= z1 + (z2-z1)/20.0 * zpos
    # x-y distribution is simply a uniform circle
    rdis= rand.uniform(0, 1, size=size)
    phis= rand.uniform(0, np.pi*2, size=size)
    xpos= rmax*rdis * np.cos(phis)
    ypos= rmax*rdis * np.sin(phis)
    return np.array(zip(xpos, ypos, zpos[:size]))

def draw_one_crystal(ax, crystal, xlim=(-3,3), ylim=(-3,3), zlim=(0,22),
                     nbins=5, elev=5, azim=40, photon=None, crystal_color='b',
                     sensor_color='orange', photon_color='g', xlabel='x',
                     ylabel='y', zlabel='z'):
    '''
    Draw one crystal in 3D.
    *ax*: An axis instance with projection='3d'. E.g., fig.add_subplot(111,projection='3d')
    *crystal*: An instance of Crystal class
    *photon*: An instance of Photon class to be drawn.
    *xlim*, *ylim*, *zlim*: the limits in three coordinates.
    *crystal_color*: the color of crystal edges
    *sensor_color*: the color of sensor edges
    *photon_color*: the color of photon path
    *nbins*: the number of divisions by markers in the coordinates
    *elev*: elevation angle
    *azim*: azimuthal angle
    '''

    ax.view_init(elev= elev, azim= azim)
    crystal.draw(ax, photon, crystal_color=crystal_color,
                 sensor_color=sensor_color, photon_color=photon_color)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    ax.locator_params(tight=True, nbins=nbins)
#    ax.set_xticks([-2,0,2])
#    ax.set_yticks([-2,0,2])


def read_pulse(t, pulse):
    # find the closet point
    idx = (np.abs(pulse.t-t)).argmin()
    if idx==0 and t<=pulse.t[0]:
        return pulse.p[0]
    elif idx==len(pulse.t)-1 and t>=pulse.t[-1]:
        return pulse.p[-1]

    t1, t2= 0,0
    p1, p2= 0,0
    if t>pulse.t[idx]:
        t1= pulse.t[idx]
        t2= pulse.t[idx+1]
        p1= pulse.p[idx]
        p2= pulse.p[idx+1]
    else:
        t1= pulse.t[idx-1]
        t2= pulse.t[idx]
        p1= pulse.p[idx-1]
        p2= pulse.p[idx]

    return p1+ (t-t1)*(p2-p1)/(t2-t1)


def digiwaveform(tevent, binwidth, tshift=0):
    '''
    Return a digitized waveform of a given interval. The waveform sampling is
    to find the closest point at a 
    given interval from the original pulse shape.
    *tevent* : the densely sampled pulse shape
    *binwidth* : sampling binwidth
    *tshift* : a shift (zero to one, meaning a fraction of a bin) in time axis
    in order to randomize binning effect
    '''
    tbins= np.arange(tevent.t.min(), tevent.t.max(), binwidth)
    tbins= tbins+ tshift*(tbins[1]-tbins[0])
    
    pp = np.zeros(len(tbins))
    for i in xrange(len(pp)):
        pp[i] = read_pulse(tbins[i],tevent)
    return np.array(zip(tbins,pp), dtype=tevent.dtype).view(np.recarray)

