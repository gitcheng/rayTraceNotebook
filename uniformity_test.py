# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import pylab as P
from pycrysray import *
arr = np.array

# <codecell>

# Geometry
center= arr([0,0,5.5])
dims = arr([3,3,11])/2.0
ref= {'random_reflect' : 0.00,
      'diffuse_reflect': 0.99,
      'diffuse_sigma'  : 10 } 
plist = rect_prism(center, dims, **ref)
# Sensor box
dx = 0.5 / 2
dy = 1.0 / 2
z= 0.0
p_apd1= arr([[0.5-dx,dy,z],[0.5+dx,dy,z],[0.5+dx,-dy,z],[0.5-dx,-dy,z]])
p_apd2= arr([[-0.5-dx,dy,z],[-0.5+dx,dy,z],[-0.5+dx,-dy,z],[-0.5-dx,-dy,z]])
P.plot(p_apd1[:,0],p_apd1[:,1])
P.plot(p_apd2[:,0],p_apd2[:,1])
P.xlim(-1.5,1.5)
P.ylim(-1.5,1.5)

sensor= {'random_reflect' : 0.0,
         'diffuse_reflect': 0.0,
         'diffuse_sigma'  : 0.0,
         'sensitive' : True} 
apd1= Plane(p_apd1, **sensor)
apd2= Plane(p_apd2, **sensor)
sensors = [apd1, apd2]

# <codecell>

np.random.seed(31416)
nphs= 1000   # number of photons
mfp = 1000   # mean free path
eff = []     # efficiency
for z in arange(1.0, 10.1, 1.0):
    # photon origin location. Z is fixed, (x,y) randomized over a square
    ox = np.random.random( nphs ) *2 -1   # -1,+1
    oy = np.random.random( nphs ) *2 -1   # -1,+1
    oz = np.ones( nphs )*z
    orig = arr([ox,oy,oz]).transpose()
    # randomize angles
    cth = np.random.uniform(-1,1, nphs)
    phi = np.random.uniform(-np.pi,np.pi, nphs)
    sth = np.sqrt(1-cth**2)
    xdir = sth * np.cos(phi)
    ydir = sth * np.sin(phi)
    zdir = cth
    dir = arr([xdir, ydir, zdir]).transpose()
    # create photons
    nhits = 0
    for oo, dd in zip(orig,dir):
        ph = Photon(x=oo, dir=dd, mfp=mfp)
        hit = None
        while ( ph.alive ):
            hit = ph.propagate(plist, black_regions=sensors)
        if ( hit!=None):
            if ( hit.sensitive ):
                nhits= nhits+1
    eff.append( float(nhits)/float(nphs) )
    print 'nhits = ', nhits, '    eff = ', eff[-1]

# <codecell>


