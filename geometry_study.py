# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Geometry study</h1>
# Study crystal geometry effect on light transmission to the rear face. Simplify other variables as much as possible. Compare hexagon and square cross sections, and straight vs. tapered.

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

# <h2>Define surface and photon properties</h2>
# 
# Assume polished surface. Reflecting on the crystal surface has a 0.1-degree sigma. 
# 
# If transmitted on the wrapped surface, there is a 10%-chance of random reflection, and a 89%-chance of diffused reflection with a sigma of 20 degrees. The outside index of refraction is assume to be 1 (air).
# 
# At a sensitive surface, if transmitted, the photon is killed and recorded. The index of refraction outside the sensitive area is 1.52 (glass)

# <codecell>

# Surface
surf= dict(sigdif_crys=0.1, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
            idx_refract_in=1.82, idx_refract_out=1.0, sensitive=False, wrapped=True)
sens= dict(sigdif_crys=0.1, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
            idx_refract_in=1.82, idx_refract_out=1.52, sensitive=True, wrapped=False)

# <markdowncell>

# <h2>Define geometries</h2>
# 
# Length= 11 cm.
# 
# The side of square is 3.0 cm. The distance between opposite sides of the hexagon is 3.224 cm, so that the areas are the same as the square.
# 
# When tapered, the dimension of the other end is 80% of the larger end.
# 
# Set the entire bottom surface "sensitive".

# <codecell>

# Hexagon
hw1= 3.224
hw2= hw1*0.8
ghex_st= hex_prism([0,0,5.5], length=11, width=hw1, **surf)
ghex_tp= hex_taper([0,0,5.5], length=11, width1=hw1 , width2=hw2, **surf)

# Square
rw1= 3.0
rw2= rw1*0.8
grec_st= rect_prism([0,0,5.5], length=11, xlen=rw1, ylen=rw1, **surf)
grec_tp= rect_taper([0,0,5.5], length=11, xlen1=rw1, ylen1=rw1, xlen2=rw2, ylen2=rw2, **surf)

# sensitive area
shex1= hexagon([0,0,0], hw1, **sens)
shex2= hexagon([0,0,0], hw1, **sens)
srec1= rectangle([0,0,0], rw1, rw1, **sens)
srec2= rectangle([0,0,0], rw1, rw1, **sens)

# <codecell>

# Crystals
chex_st= Crystal('chex_st', ghex_st+[shex2])
chex_tp= Crystal('chex_tp', ghex_tp+[shex1])
crec_st= Crystal('crec_st', grec_st+[srec2])
crec_tp= Crystal('crec_tp', grec_tp+[srec1])

# <codecell>

def draw_one_crystal(ax, crystal, photon=None):
    ax.view_init(elev= 20, azim=40)
    crystal.draw(ax, photon)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)

# <codecell>

fig=figure(figsize=(11,12))
ax = fig.add_subplot(221, projection='3d')
draw_one_crystal(ax, chex_st)
ax = fig.add_subplot(222, projection='3d')
draw_one_crystal(ax, chex_tp)
ax = fig.add_subplot(223, projection='3d')
draw_one_crystal(ax, crec_st)
ax = fig.add_subplot(224, projection='3d')
draw_one_crystal(ax, crec_tp)

# <markdowncell>

# <h2>Test photon</h2>

# <codecell>

nprnd.seed(0)
mfp= 500
pos0= np.array([0.0, 0.0, 8.0])  # initial position
dir0= np.array([0.3,0.4,0.1])    # initial direction
photon1= Photon(pos0, dir0 , mfp=mfp)
photon2= Photon(pos0, dir0 , mfp=mfp)
photon3= Photon(pos0, dir0 , mfp=mfp)
photon4= Photon(pos0, dir0 , mfp=mfp)

# <codecell>

photon1.propagate(chex_st)
photon2.propagate(chex_tp)
photon3.propagate(crec_st)
photon4.propagate(crec_tp)

# <codecell>

fig=figure(figsize=(11,12))
ax = fig.add_subplot(221, projection='3d')
draw_one_crystal(ax, chex_st, photon1)
ax = fig.add_subplot(222, projection='3d')
draw_one_crystal(ax, chex_tp, photon2)
ax = fig.add_subplot(223, projection='3d')
draw_one_crystal(ax, crec_st, photon3)
ax = fig.add_subplot(224, projection='3d')
draw_one_crystal(ax, crec_tp, photon4)

# <markdowncell>

# <h2>Run experiments</h2>

# <codecell>

nprnd.seed(0)
results= {}
zpoints= np.linspace(0.5,10.5,11)
zpoints= np.array([np.zeros(11), np.zeros(11), zpoints])
zpoints= zpoints.transpose()

kwargs= dict(zpoints= zpoints, dz= 0.2, dr= 1.1, nperz= 1000, verbose=True) # mean free path= 1000 cm
starttime= time.time()
for crystal in [chex_st, chex_tp, crec_st, crec_tp]:
    print 'processing ', crystal.name, 
    effs, errs= run_exp(crystal, **kwargs)
    results[crystal.name+'_effs']= effs
    results[crystal.name+'_errs']= errs
    print '  time %.1f s' % (time.time() - starttime )

# <codecell>

import pickle
pickle.dump(results, open('geometry_study_result.p', 'wb'))

# <codecell>

print results

# <codecell>

def eff_vs_z(ax, zp, results, key, **kwargs):
    y= results[key+'_effs']
    ey = results[key+'_errs']
    ax.errorbar(zp, y, ey, **kwargs)

# <codecell>

fig= figure(figsize=(7,5))
zp= np.linspace(0.5,10.5,11)
ax= plt.subplot(111)
[chex_st, chex_tp, crec_st, crec_tp]
eff_vs_z(ax, zp, results, 'chex_st', fmt='bo-', label='Hexagon-straight')
eff_vs_z(ax, zp, results, 'chex_tp', fmt='go-', label='Hexagon-tapered', mfc='w', mec='g', mew=2)
eff_vs_z(ax, zp, results, 'crec_st', fmt='rx--', label='Square-straight', mew=2)
eff_vs_z(ax, zp, results, 'crec_tp', fmt='cd--', label='Square-tapered', mfc='w', mec='c', mew=2)
ax.set_title('Probability of transmitting through the bottom face')
ax.set_xlabel('Distance from bottom face', fontsize='x-large')
ax.set_ylabel('Probability', fontsize='x-large')
ax.set_ylim(ymin=0)
ax.grid()
ax.legend(numpoints=2, framealpha=0.5, loc='lower right', fontsize='x-large')

# <codecell>

fig.savefig('../plots/geometry_study_result.pdf')

# <codecell>


