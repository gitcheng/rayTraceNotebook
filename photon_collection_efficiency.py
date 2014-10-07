# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Photon collection efficiency study</h1>
# 
# Compare photon collection efficiency between crystal geometries and between different crystal/sensor interface indexes of refraction.

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import numpy.random as nprnd
import time
import matplotlib.pyplot as plt
from pycrysray import *

# <codecell>

%load_ext autoreload
%autoreload 2

# <markdowncell>

# <h2>Define surface and photon properties </h2>
# 
# We assume the crystal is tightly wrapped or painted, so the index of refraction is irrelevant. Set the inside and outside the same. The reflection of the surface has two components. One is random reflection. The reflected photon is uniformly distributed over the entire semi-hemisphere. The second component is diffused reflection. The reflected photon follows the law of reflection smeared by a Gaussian distribution. 
# 
# If the photon hits a sensor, it follows the Fresnel's equations of reflection and transmission http://en.wikipedia.org/wiki/Fresnel_equations. The reflection part is calculated using diffused reflection mentioned above.
# 
# Here we assume the following,
# 
# For photons reflecting on crystal surface:<br>
# $\sigma$ of reflection = 0.1 degree<br>
# 
# If the photon is transmitted out of the crystal and hit the wrapper:
# Random reflaction probability = 0.10<br>
# Diffused reflection probability = 0.89<br>
# $\sigma$ of diffused reflection = 20 degrees<br>
# 
# For photons reflecting in the sensor area<br>
# Assume photons going from crystal (LYSO $n=1.82$ or BaF2 $n=1.47$) to glass ($n= 1.52$) or air ($n= 1.0$).

# <codecell>

# Surface property
nlyso, nbaf2, nglass, nair = 1.82, 1.47, 1.52, 1.0
# Wrapped surface
lyso_wrap= dict(sigdif_crys=0.1, pdif_crys=1.0, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
                idx_refract_in=nlyso, idx_refract_out=nair, sensitive=False, wrapped=True)
baf2_wrap= lyso_wrap.copy()
baf2_wrap['idx_refract_in']= nbaf2
# sensitive surface
lyso_air= lyso_wrap.copy()
lyso_air['sensitive']= True
lyso_air['wrapped']= False
lyso_glass= lyso_air.copy()
lyso_glass['idx_refract_out']= nglass
baf2_air= lyso_air.copy()
baf2_air['idx_refract_in']= nbaf2
baf2_glass= lyso_glass.copy()
baf2_glass['idx_refract_in']= nbaf2

# <codecell>

print lyso_air
print baf2_air

# <markdowncell>

# <h2>Define geometries</h2>
# Crystals<br>
# Hexagon: edge-to-edge width= 3.224 cm<br>
# Square: side= 3 cm<br>
# So that the areas are the same.
# 
# Length= 11 cm for LYSO,  21 cm for BaF2.
# 
# Sensors<br>
# Two 1 cm X 1 cm photo sensors

# <codecell>

# Hexagon
ghex_lyso= hex_prism([0,0,5.5], length=11, width=3.224, **lyso_wrap)
ghex_baf2= hex_prism([0,0,10.5], length=21, width=3.224, **baf2_wrap)
# Rectangle
grec_lyso= rect_prism([0,0,5.5], length=11, xlen=3.0, ylen=3.0, **lyso_wrap)
grec_baf2= rect_prism([0,0,10.5], length=21, xlen=3.0, ylen=3.0, **baf2_wrap)

# Sensors
location1= [0,+0.7,0]
location2= [0,-0.7,0]
xlen, ylen=  1.0, 1.0
sen1_lg = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_glass)
sen2_lg = rectangle(location2, xlen=xlen, ylen=ylen, **lyso_glass)
sen1_bg = rectangle(location1, xlen=xlen, ylen=ylen, **baf2_glass)
sen2_bg = rectangle(location2, xlen=xlen, ylen=ylen, **baf2_glass)
sen1_la = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_air)
sen2_la = rectangle(location2, xlen=xlen, ylen=ylen, **lyso_air)
sen1_ba = rectangle(location1, xlen=xlen, ylen=ylen, **baf2_air)
sen2_ba = rectangle(location2, xlen=xlen, ylen=ylen, **baf2_air)

# <codecell>

# Define crystals
chex_lg= Crystal('chex_lg', ghex_lyso+[sen1_lg, sen2_lg])
chex_bg= Crystal('chex_bg', ghex_baf2+[sen1_bg, sen2_bg])

crec_lg= Crystal('crec_lg', grec_lyso+[sen1_lg, sen2_lg])
crec_bg= Crystal('crec_bg', grec_baf2+[sen1_bg, sen2_bg])

chex_la= Crystal('chex_la', ghex_lyso+[sen1_la, sen2_la])
chex_ba= Crystal('chex_ba', ghex_baf2+[sen1_ba, sen2_ba])

crec_la= Crystal('crec_la', grec_lyso+[sen1_la, sen2_la])
crec_ba= Crystal('crec_ba', grec_baf2+[sen1_ba, sen2_ba])

# <codecell>

def draw_one_crystal(ax, crystal, photon=None):
    ax.view_init(elev= 5, azim=40)
    crystal.draw(ax, photon)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(0,22)
    ax.set_xticks([-2,0,2])
    ax.set_yticks([-2,0,2])

# <codecell>

fig=figure(figsize=(10,10))
for i, crys in enumerate([chex_lg, chex_bg, crec_lg, crec_bg]):
    ax = fig.add_subplot(141+i, projection='3d')
    draw_one_crystal(ax, crys)

# <markdowncell>

# <h2>Test photon</h2>

# <codecell>

mfp= 170   # cm
nprnd.seed(0)
pos0= np.array([0.0, 0.0, 3.0])  # initial position
dir0= np.array([0.3,0.4,0.5])    # initial direction
photon1= Photon(pos0, dir0 , mfp=mfp, trackvtx=True)
photon2= Photon(pos0, dir0 , mfp=mfp, trackvtx=True)

# <codecell>

final_plane1= photon1.propagate(chex_bg)
final_plane2= photon2.propagate(crec_lg)

# <codecell>

print photon1.pathlength, photon1.status
photon1.lastplane.print_properties()

# <codecell>

fig=figure(figsize=(5,10))
ax = fig.add_subplot(121, projection='3d')
draw_one_crystal(ax, chex_bg, photon1)

ax = fig.add_subplot(122, projection='3d')
draw_one_crystal(ax, crec_lg, photon2)

# <markdowncell>

# <h2>Run experiments</h2>

# <codecell>

def crystal_zrange(crystal):
    zp=[]
    for p in crystal.planes:
        for c in p.corners:
            zp.append(c[2])
    zp= np.array(zp)
    return zp.min(), zp.max()

# <codecell>

npoints= 5
nprnd.seed(0)
results= {}
starttime= time.time()
for crystal in [chex_la, chex_lg, chex_ba, chex_bg, crec_la, crec_lg, crec_ba, crec_bg]:
    zmin, zmax= crystal_zrange(crystal)
    zpoints= np.linspace(zmin+1.0,zmax-1.0, npoints)
    zpoints= np.array([np.zeros(npoints), np.zeros(npoints), zpoints])
    zpoints= zpoints.transpose()
    kwargs= dict(zpoints= zpoints, dz= 0.2, dr= 1.1, nperz= 2000, mfp=170, verbose=True)
    
    print 'processing ', crystal.name, 
    effs, errs= run_exp(crystal, **kwargs)
    results[crystal.name+'_effs']= effs
    results[crystal.name+'_errs']= errs
    print '  time %.1f s' % (time.time() - starttime )

# <codecell>

import pickle
pickle.dump(results, open('photon_collection_eff_result.p', 'wb'))

# <codecell>

def eff_vs_z(ax, xp, results, key, **kwargs):
    y= results[key+'_effs']
    ey = results[key+'_errs']
    ax.errorbar(xp, y, ey, **kwargs)

# <codecell>

fig= figure(figsize=(16,6))
xpl= np.linspace(1.0,10.0,npoints)/11.0
xpb= np.linspace(1.0,20.0,npoints)/21.0

ax= plt.subplot(121)
eff_vs_z(ax, xpl, results, 'chex_lg', fmt='bo-', label='LYSO-Glass')
eff_vs_z(ax, xpl, results, 'chex_la', fmt='go-', label='LYSO-Air', mfc='w', mec='g', mew=2)
eff_vs_z(ax, xpb, results, 'chex_bg', fmt='rx--', label='BaF2-Glass', mew=2)
eff_vs_z(ax, xpb, results, 'chex_ba', fmt='cd--', label='BaF2-Air', mfc='w', mec='c', mew=2)
ax.set_title('Hexagon', fontsize='x-large')
ax.set_xlabel('Distance from sensor face/crystal length', fontsize='x-large')
ax.set_ylabel('Efficiency', fontsize='x-large')
ax.set_ylim(0,0.35)
ax.grid()
ax.legend(numpoints=1, framealpha=0.5, fontsize='x-large', loc='upper right')

ax= plt.subplot(122)
eff_vs_z(ax, xpl, results, 'crec_lg', fmt='bo-', label='LYSO-Glass')
eff_vs_z(ax, xpl, results, 'crec_la', fmt='go-', label='LYSO-Air', mfc='w', mec='g', mew=2)
eff_vs_z(ax, xpb, results, 'crec_bg', fmt='rx--', label='BaF2-Glass', mew=2)
eff_vs_z(ax, xpb, results, 'crec_ba', fmt='cd--', label='BaF2-Air', mfc='w', mec='c', mew=2)
ax.set_title('Square', fontsize='x-large')
ax.set_xlabel('Distance from sensor face/crystal length', fontsize='x-large')
ax.set_ylabel('Efficiency', fontsize='x-large')
ax.set_ylim(0,0.35)
ax.grid()
ax.legend(numpoints=1, framealpha=0.5, fontsize='x-large', loc='upper right')

# <codecell>

fig.savefig('../plots/photon_collection_eff_result.pdf')

# <codecell>


