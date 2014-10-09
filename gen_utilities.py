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

def draw_one_crystal(ax, crystal, xr=3, yr=3, zr= 22, nbins=5, 
                     elev=5, azim=40, photon=None):
    ax.view_init(elev= elev, azim= azim)
    crystal.draw(ax, photon)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(-xr,xr)
    ax.set_ylim(-yr,yr)
    ax.set_zlim(0,zr)
    ax.locator_params(tight=True, nbins=nbins)
#    ax.set_xticks([-2,0,2])
#    ax.set_yticks([-2,0,2])

