# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Sanity checks</h1>

# <codecell>

import numpy as np
import numpy.random as nprnd
import time
import math
import matplotlib.pyplot as plt
from pycrysray import *

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

def critical_angle(n1, n2):
    '''
    Critical angle (degrees) of total internal reflection. From n1 to n2.
    '''
    sinthc= n2/float(n1)
    if sinthc>=1:
        return 90.0
    return math.degrees(math.asin(sinthc))

# <markdowncell>

# <h2>Define surface and photon properties </h2>
# 
# We assume the crystal is tightly wrapped or painted, so the index of refraction is irrelevant. Set the inside and outside the same. The reflection of the surface has two components. One is random reflection. The reflected photon is uniformly distributed over the entire semi-hemisphere. The second component is diffused reflection. The reflected photon follows the law of reflection smeared by a Gaussian distribution. 
# 
# If the photon hits a sensor, it follows the Fresnel's equations of reflection and transmission http://en.wikipedia.org/wiki/Fresnel_equations. The reflection part is calculated using diffused reflection mentioned above.
# 
# Here we assume the following,
# 
# For photons reflecting on crystal surface/wrapping/painting material:<br>
# Random reflaction probability = 0.0<br>
# Diffused reflection probability = 1.0<br>
# $\sigma$ of diffused reflection = 0.01 degrees<br>
# Ignore the index of refraction
# 
# For photons reflecting in the sensor area<br>
# Diffused reflection probability = 1.0<br>
# $\sigma$ of diffused reflection = 0.01 degree<br>
# Assume photons going from crystal (LYSO $n=1.82$ or BaF2 $n=1.47$) to glass ($n= 1.52$).

# <codecell>

# Surface property
nlyso, nbaf2, nglass, nair = 1.82, 1.47, 1.52, 1.0

#lyso_wrap= dict(sigdif_crys=0.1, pdif_crys=0.99, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.87, prand_wrap=0.10,
#                idx_refract_in=nlyso, idx_refract_out=nair, sensitive=False, wrapped=True)

# Wrapped surface
lyso_wrap= dict(sigdif_crys=0.1, pdif_crys=0.99, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.87, prand_wrap=0.10,
                idx_refract_in=nlyso, idx_refract_out=nair, sensitive=False, wrapped=True)
baf2_wrap= lyso_wrap.copy()
baf2_wrap['idx_refract_in']= nbaf2

# sensitive surface
lyso_glass= dict(sigdif_crys=0.1, pdif_crys=1.0, prand_crys=0.0,
                 idx_refract_in=nlyso, idx_refract_out=nglass, sensitive=True, wrapped=False)
lyso_air= lyso_glass.copy()
lyso_air['idx_refract_out']= nair
baf2_glass= lyso_glass.copy()
baf2_glass['idx_refract_in']= nbaf2
baf2_air= baf2_glass.copy()
baf2_air['idx_refract_out']= nair

# <codecell>

print lyso_air
print lyso_glass
print baf2_air
print baf2_glass

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

# Rectangle
grec_lyso= rect_prism([0,0,5.5], length=11, xlen=3.0, ylen=3.0, **lyso_wrap)
grec_baf2= rect_prism([0,0,5.5], length=11, xlen=3.0, ylen=3.0, **baf2_wrap)

# Sensors
location1= [0,0,0]
xlen, ylen=  1.0, 1.0
sen1_lg = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_glass)
sen1_bg = rectangle(location1, xlen=xlen, ylen=ylen, **baf2_glass)
sen1_la = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_air)
sen1_ba = rectangle(location1, xlen=xlen, ylen=ylen, **baf2_air)

# <codecell>

# Define crystals
crec0= Crystal('crec0', grec_lyso)
crec_lg= Crystal('crec_lg', grec_lyso+[sen1_lg])
crec_bg= Crystal('crec_bg', grec_baf2+[sen1_bg])

crec_la= Crystal('crec_la', grec_lyso+[sen1_la])
crec_ba= Crystal('crec_ba', grec_baf2+[sen1_ba])

# <codecell>

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

# Define crystals
crec0= Crystal('crec0', grec_lyso)
crec_lg= Crystal('crec_lg', grec_lyso+[sen1_lg,sen2_lg])
crec_bg= Crystal('crec_bg', grec_baf2+[sen1_bg,sen2_bg])

crec_la= Crystal('crec_la', grec_lyso+[sen1_la,sen2_la])
crec_ba= Crystal('crec_ba', grec_baf2+[sen1_ba,sen2_ba])

# <codecell>

fig=figure()
ax= fig.add_subplot(111, projection='3d')
draw_one_crystal(ax, crec_lg)

# <markdowncell>

# <h2>Test photon</h2>

# <codecell>

nprnd.seed(0)
pos0= np.array([0.0, 0.0, 0.5])  # initial position
dir0= np.array([0.0,0.4,+0.5])    # initial direction
photon1= Photon(pos0, dir0 , mfp=170, trackvtx=True)
photon2= Photon(pos0, dir0 , mfp=170, trackvtx=True)

# <codecell>

final_plane1= photon1.propagate(crec_la)

# <codecell>

print photon1.pathlength, photon1.status
photon1.lastplane.print_properties()
print photon1.n_reflects

# <codecell>

fig=figure()
ax = fig.add_subplot(111, projection='3d')
draw_one_crystal(ax, crec_lg, photon1, xlim=(-1,1), ylim=(-1,1))

# <codecell>

print critical_angle(nlyso, nglass)
print critical_angle(nlyso, nair)
print critical_angle(nbaf2, nair)
print 1-cos(math.radians(33.3))
print 1-cos(math.radians(42.9))
#print photon1.incident_costh
#print math.degrees(np.arccos(-photon1.incident_costh))

# <codecell>

def short_mfp_test(crystal, origin, mfp, nphotons, dz=0.0, dr=0.0, verbose=False):
    '''
    Photons generated in random directions.
    Return the number of photons that are detected and a list of incident angles at the detection.
    *origin*: The origin of photons
    *mfp: Mean free path of photon
    '''
    acriticals=[]
    ndet=0
    for i in range(nphotons):
        if verbose:
            if i%(nphotons/10.)==0:
                print i,
        x, r= generate_p6(np.array(origin), dz, dr)
        photon= Photon(x, r , mfp=mfp, trackvtx=False)
        photon.propagate(crystal)
        if photon.status != photon.transmitted:
            continue
        if photon.lastplane is None:
            continue
        if photon.lastplane.sensitive:
            ndet= ndet+1
            acriticals.append( math.degrees(math.acos(-photon.incident_costh)) )
    if verbose: print
    return ndet, acriticals    

# <codecell>

nprnd.seed(0)

# <codecell>

ndet_la, acrts_la= short_mfp_test(crec_la, [0,0,5.5], 170, 1000, dz=0.2, dr=1.1, verbose=True)
print ndet_la

# <codecell>

ndet_ba, acrts_ba= short_mfp_test(crec_ba, [0,0,5.5], 170, 1000, dz=0.2, dr=1.1, verbose=True)
print ndet_ba

# <codecell>

print ndet_ba/float(ndet_la)

# <codecell>

crec_ba.planes[1].print_properties()

# <codecell>

cr_la= critical_angle(nlyso, nair)
print cr_la
print 1-cos(math.radians(cr_la))
cr_ba= critical_angle(nbaf2, nair)
print cr_ba
print 1-cos(math.radians(cr_ba))
print (1-cos(math.radians(cr_ba)))/(1-cos(math.radians(cr_la)))

# <codecell>

plt.hist(acrts_la);

# <codecell>

ndet_lg, acrts_lg= short_mfp_test(crec_lg, [0,0,2.0], 170, 1000, verbose=True)
print ndet_lg

# <codecell>

print critical_angle(nlyso, nglass)
print 1-cos(math.radians(56.6))

# <codecell>

print 0.45/0.164
print 2068/735.

# <codecell>

bins= np.linspace(0,60,61)
plt.hist(acrts_lg, bins, histtype='step', alpha=0.9);
plt.hist(acrts_la, bins, histtype='step', alpha=0.9);

# <codecell>

print ndet_lg/float(ndet_la)

# <codecell>


# <codecell>

# Rectangle
grec_lyso= rect_prism([0,0,5.5], length=11, xlen=3.0, ylen=3.0, **lyso_wrap)

# Sensors
location1= [0,+0.7,0]
location2= [0,-0.7,0]
xlen, ylen=  1.0, 1.0
sen1_lg = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_glass)
sen1_la = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_air)
sen2_lg = rectangle(location2, xlen=xlen, ylen=ylen, **lyso_glass)
sen2_la = rectangle(location2, xlen=xlen, ylen=ylen, **lyso_air)

# Crystal
crec_la = Crystal('crec_la', grec_lyso+[sen1_la,sen2_la])
crec_lg = Crystal('crec_lg', grec_lyso+[sen1_lg,sen2_lg])

# <codecell>

nprnd.seed(0)
ndet_la, acrts_la= short_mfp_test(crec_la, [0,0,5.5], 1000, 1000, dz=0.2, dr=0.2, verbose=True)
print ndet_la

# <codecell>

nprnd.seed(0)
ndet_lg, acrts_lg= short_mfp_test(crec_lg, [0,0,5.5], 1000, 1000, dz=0.2, dr=0.2, verbose=True)
print ndet_lg

# <codecell>

bins= np.linspace(0,60,61)
plt.hist(acrts_lg, bins, histtype='step', alpha=0.9);
plt.hist(acrts_la, bins, histtype='step', alpha=0.9);

# <codecell>

bins= np.linspace(0,60,61)
plt.hist(acrts_lg, bins, histtype='step', alpha=0.9);
plt.hist(acrts_la, bins, histtype='step', alpha=0.9);

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

nprnd.seed(0)
results= {}
starttime= time.time()
for crystal in [chex_la, chex_lg, chex_ba, chex_bg, crec_la, crec_lg, crec_ba, crec_bg]:
    zmin, zmax= crystal_zrange(crystal)
    zpoints= np.linspace(zmin+0.5,zmax-0.5,11)
    zpoints= np.array([np.zeros(11), np.zeros(11), zpoints])
    zpoints= zpoints.transpose()
    kwargs= dict(zpoints= zpoints, dz= 0.2, dr= 1.1, nperz= 1000, verbose=True)
    
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
xpl= np.linspace(0.5,10.5,11)/11.0
xpb= np.linspace(0.5,20.5,11)/21.0

ax= plt.subplot(121)
eff_vs_z(ax, xpl, results, 'chex_lg', fmt='bo-', label='LYSO-Glass')
eff_vs_z(ax, xpl, results, 'chex_la', fmt='go-', label='LYSO-Air', mfc='w', mec='g', mew=2)
eff_vs_z(ax, xpb, results, 'chex_bg', fmt='rx--', label='BaF2-Glass', mew=2)
eff_vs_z(ax, xpb, results, 'chex_ba', fmt='cd--', label='BaF2-Air', mfc='w', mec='c', mew=2)
ax.set_title('Hexagon', fontsize='x-large')
ax.set_xlabel('Distance from sensor face/crystal length', fontsize='x-large')
ax.set_ylabel('Efficiency', fontsize='x-large')
ax.set_ylim(0,0.8)
ax.grid()
ax.legend(numpoints=1, framealpha=0.5, fontsize='x-large', loc='center right')

ax= plt.subplot(122)
eff_vs_z(ax, xpl, results, 'crec_lg', fmt='bo-', label='LYSO-Glass')
eff_vs_z(ax, xpl, results, 'crec_la', fmt='go-', label='LYSO-Air', mfc='w', mec='g', mew=2)
eff_vs_z(ax, xpb, results, 'crec_bg', fmt='rx--', label='BaF2-Glass', mew=2)
eff_vs_z(ax, xpb, results, 'crec_ba', fmt='cd--', label='BaF2-Air', mfc='w', mec='c', mew=2)
ax.set_title('Square', fontsize='x-large')
ax.set_xlabel('Distance from sensor face/crystal length', fontsize='x-large')
ax.set_ylabel('Efficiency', fontsize='x-large')
ax.set_ylim(0,0.8)
ax.grid()
ax.legend(numpoints=1, framealpha=0.5, fontsize='x-large', loc='center right')

# <codecell>

fig.savefig('plots/photon_collection_eff_result.pdf')

# <codecell>


# <codecell>


# <codecell>

# Reflection test

# <codecell>

surface= dict(sigdif_crys=0.1, pdif_crys=1.0, prand_crys=0.0, sigdif_wrap=10.0, pdif_wrap=1.0, prand_wrap=0.0,
                idx_refract_in=nlyso, idx_refract_out=nair, sensitive=False, wrapped=True)
pl= rectangle([0.,0.,0.], 100.0, 100.0, **surface)
crys= Crystal('ctest', [pl])
print pl.normal

# <codecell>

def test_reflects(theta,n):
    rangle= np.zeros(n)
    status= np.zeros(n)
    rtheta= math.radians(theta)
    vdir= np.array([sin(rtheta), 0, -cos(rtheta)])
    for i in range(len(rangle)):
        photon= Photon([0,0,1.], vdir, mfp=1000)
        photon.propagate(crys)
        rangle[i]= math.degrees(math.acos(photon.dir[2]))
        status[i]= photon.status
    return rangle, status

# <codecell>

rangle, status= test_reflects(20, 1000)

# <codecell>

plt.hist(rangle[status==5], bins=100);

# <codecell>

(status==5).sum()

# <codecell>

print photon.status
print photon.dir
v2= photon.dir
print photon.n_reflects
print 'angle= ', math.degrees(math.acos(v2[2]))

# <codecell>


