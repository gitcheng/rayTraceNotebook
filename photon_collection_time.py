# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Photon collection time study</h1>
# 
# Study the time distribution of photons hitting the sensors.
# 
# Generate photon timings for a few different crystals/geometries

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import time
import matplotlib.pyplot as plt
from pycrysray import *
import numpy.random as rand

# <codecell>

#from scipy.constants import c as clight
clight = 299792458.0
clightcm = clight * 100
clightcmns = clightcm * 1e-9  ## speed of light in cm/ns

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
# Assume photons going from crystal (LYSO $n=1.82$ or BaF2 $n=1.47$, or CsI $n=1.79$) to glass ($n= 1.52$) or air ($n= 1.0$).

# <codecell>

def sensitive_surface(dict_orig, idx_out):
    '''
    Take a dictionary for a wrapped surface and return a sensitive surface.
    *dict_orig*: original surface properties
    *idx_out*: index of refraction of the material outside the window
    '''
    retval= dict_orig.copy()
    retval['sensitive']= True
    retval['wrapped']= False
    retval['idx_refract_out']= idx_out
    return retval

# <codecell>

# Indices of refraction
nlyso, nbaf2, nglass, nair, ncsi = 1.82, 1.47, 1.52, 1.0, 1.79
# Wrapped surface
lyso_wrap= dict(sigdif_crys=0.1, pdif_crys=1.0, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
                idx_refract_in=nlyso, idx_refract_out=nair, sensitive=False, wrapped=True)
baf2_wrap= lyso_wrap.copy()
baf2_wrap['idx_refract_in']= nbaf2
csi_wrap= lyso_wrap.copy()
csi_wrap['idx_refract_in']= ncsi
# sensitive surface
lyso_glass= sensitive_surface(lyso_wrap, nglass)
baf2_glass= sensitive_surface(baf2_wrap, nglass)
csi_glass= sensitive_surface(csi_wrap, nglass)

# <codecell>

print lyso_glass
print baf2_glass
print csi_glass

# <markdowncell>

# <h2>Define geometries</h2>
# 
# Mu2e crystals<br>
# Hexagon: edge-to-edge width= 3.3 cm<br>
# Length= 11 cm for LYSO,  20 cm for BaF2, 19 cm for CsI
# 
# PET scan crystals<br>
# 1cm X 1cm X 2cm
# 
# Sensors<br>
# Two 1 cm X 1 cm photo sensors

# <codecell>

## dimensions
lenlyso, lenbaf2, lencsi = 11.0, 20.0, 19.0
hexwidth= 3.3

# <codecell>

# Hexagon
hex_lyso= hex_prism(center=[0,0,lenlyso/2.0], length=lenlyso, width=hexwidth, **lyso_wrap)
hex_baf2= hex_prism(center=[0,0,lenbaf2/2.0], length=lenbaf2, width=hexwidth, **baf2_wrap)
hex_csi=  hex_prism(center=[0,0,lencsi/2.0],  length=lencsi,  width=hexwidth, **csi_wrap)
# PET Rectangle
rec_lyso= rect_prism(center=[0,0,1.0], length=2.0, xlen=1.0, ylen=1.0, **lyso_wrap)
rec_baf2= rect_prism(center=[0,0,1.0], length=2.0, xlen=1.0, ylen=1.0, **baf2_wrap)
rec_csi=  rect_prism(center=[0,0,1.0], length=2.0, xlen=1.0, ylen=1.0, **csi_wrap)

# Sensors
#  For mu2e
location1= [0,+0.7,0]
location2= [0,-0.7,0]
xlen, ylen=  1.0, 1.0
s1_lysog = rectangle(location1, xlen=xlen, ylen=ylen, **lyso_glass)
s2_lysog = rectangle(location2, xlen=xlen, ylen=ylen, **lyso_glass)
s1_baf2g = rectangle(location1, xlen=xlen, ylen=ylen, **baf2_glass)
s2_baf2g = rectangle(location2, xlen=xlen, ylen=ylen, **baf2_glass)
s1_csig = rectangle(location1, xlen=xlen, ylen=ylen, **csi_glass)
s2_csig = rectangle(location2, xlen=xlen, ylen=ylen, **csi_glass)
#  For PET
location= [0,0,0]
xlen, ylen= 0.5, 0.5
s_lysog = rectangle(location, xlen=xlen, ylen=ylen, **lyso_glass)
s_baf2g = rectangle(location, xlen=xlen, ylen=ylen, **baf2_glass)
s_csig = rectangle(location, xlen=xlen, ylen=ylen, **csi_glass)

# <codecell>

# Define crystals
chex_lyso = Crystal('chex_lyso', hex_lyso+[s1_lysog, s2_lysog])
chex_baf2 = Crystal('chex_baf2', hex_baf2+[s1_baf2g, s2_baf2g])
chex_csi = Crystal('chex_csi', hex_csi+[s1_csig, s2_csig])

cpet_lyso = Crystal('cpet_lyso', rec_lyso+[s_lysog])
cpet_baf2 = Crystal('cpet_baf2', rec_baf2+[s_baf2g])
cpet_csi = Crystal('cpet_csi', rec_csi+[s_csig])

# <codecell>

def draw_one_crystal(ax, crystal, photon=None, zmax=22):
    ax.view_init(elev= 5, azim=40)
    crystal.draw(ax, photon)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(0, zmax)
    ax.set_xticks([-2,0,2])
    ax.set_yticks([-2,0,2])

# <codecell>

fig= plt.figure(figsize=(20,10))
for i, crys in enumerate([chex_lyso, chex_baf2, chex_csi, cpet_lyso, cpet_baf2, cpet_csi]):
    ax = fig.add_subplot(161+i, projection='3d')
    draw_one_crystal(ax, crys)

# <markdowncell>

# <h2>Jobs below are now in separate scripts</h2>
# 
# E.g., time_baf2_hex_G1.py, time_lyso_pet_G2.py, etc.

# <headingcell level=3>

# ============================================================================
# 
# ============================================================================

# <codecell>

# Gamma function
z= rand.gamma(3.5, 2, 1000000)
plt.hist(z, bins=100, histtype='step');

# <markdowncell>

# <h3>Simple shower shape model</h3>
#  
# Use a gamma function to model the distribution along the z axis.

# <codecell>

def gen_positions(z1, z2, rmax, size):
    '''
    Generate a set of positions, where the z-corrdinate is between z1 and z2, and x-y is in a circle
    of radius rmas
    '''
    zpos = rand.gamma(shape=3.5, scale=2, size=size*2)
    # Make a cut on zpos at 20 furst, than re-scale zpos so it starts at z2 and ends at z2
    zpos= zpos[zpos<20]
    zpos= z1 + (z2-z1)/20.0 * zpos
    # x-y distribution is simply a uniform circle
    rdis= rand.uniform(0, 1, size=size)
    phis= rand.uniform(0, np.pi*2, size=size)
    xpos= rmax*rdis * np.cos(phis)
    ypos= rmax*rdis * np.sin(phis)
    return np.array(zip(xpos, ypos, zpos[:size]))

# <codecell>

def gen_uniform_pos(x1, x2, y1, y2, z1, z2, size):
    '''
    Generate a set of positions, uniformly distributed
    '''
    xpos = rand.uniform(x1, x2, size)
    ypos = rand.uniform(y1, y2, size)
    zpos = rand.uniform(z1, z2, size)
    return np.array(zip(xpos, ypos, zpos))

# <codecell>

def sim_timing(crystal, allpos, t0origin, mfp=170, seed=0):
    '''
    *t0origin* : the position at which t= 0
    '''
    start= time.time()
    rand.seed(seed)
    timings=[]
    nums= len(allpos)
    for j,pos in enumerate(allpos):
        if j%(nums/10)==1:
            print '[%.0f%% t=%d s];'%(j/float(nums)*100, time.time()-start),
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
    print
    return np.array(timings)

# <markdowncell>

# <h3>BaF2 hexagon</h3>

# <codecell>

ngen= 200000
allpos= gen_positions(z1=lenbaf2, z2=0, rmax=hexwidth/2., size= ngen)
ts_hex_baf2= sim_timing(chex_baf2, allpos, t0origin=[0,0,lenbaf2], mfp=170, seed=0)
np.save('../data/timing/ts_baf2_hex_33_200_n200k_0001', ts_hex_baf2)
ndet= len(ts_hex_baf2)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))

# <markdowncell>

# <h3>LYSO hexagon</h3>

# <codecell>

ngen= 1000000
allpos= gen_positions(z1=lenlyso, z2=0, rmax=hexwidth/2., size= ngen)
ts_hex_lyso= sim_timing(chex_lyso, allpos, t0origin=[0,0,lenlyso], mfp=170, seed=0)
np.save('../data/timing/ts_lyso_hex_33_110_n1000k_0001', ts_hex_lyso)
ndet= len(ts_hex_lyso)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))

# <markdowncell>

# <h3>CsI hexagon</h3>

# <codecell>

ngen= 200000
allpos= gen_positions(z1=lencsi, z2=0, rmax=hexwidth/2., size= ngen)
ts_hex_csi= sim_timing(chex_csi, allpos, t0origin=[0,0,lencsi], mfp=170, seed=0)
np.save('../data/timing/ts_csi_hex_33_190_n200k_0001', ts_hex_csi)
ndet= len(ts_hex_csi)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))

# <markdowncell>

# <h3>Small 1x1x2 BaF2 crystal</h3>

# <codecell>

ngen= 100000
allpos= gen_uniform_pos(-0.5,0.5, -0.5,0.5, 0, 2, ngen)
ts_pet_baf2= sim_timing(cpet_baf2, allpos, t0origin=[0,0,2], mfp=170, seed=0)
np.save('../data/timing/ts_baf2_pet_1_1_2_n100k_0001', ts_pet_baf2)
ndet= len(ts_pet_baf2)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))

# <markdowncell>

# <h3>Small 1x1x2 LYSO crystal</h3>

# <codecell>

ngen= 500000
allpos= gen_uniform_pos(-0.5,0.5, -0.5,0.5, 0, 2, ngen)
ts_pet_lyso= sim_timing(cpet_lyso, allpos, t0origin=[0,0,2], mfp=170, seed=0)
np.save('../data/timing/ts_lyso_pet_1_1_2_n500k_0001', ts_pet_lyso)
ndet= len(ts_pet_lyso)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))

# <markdowncell>

# <h3>Small 1x1x2 CsI crystal</h3>

# <codecell>

ngen= 100000
allpos= gen_uniform_pos(-0.5,0.5, -0.5,0.5, 0, 2, ngen)
ts_pet_csi= sim_timing(cpet_csi, allpos, t0origin=[0,0,2], mfp=170, seed=0)
np.save('../data/timing/ts_csi_pet_1_1_2_n100k_0001', ts_pet_csi)
ndet= len(ts_pet_csi)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen)

# <codecell>


# <markdowncell>

# #======================================================================================
# #======================================================================================

# <codecell>


# <codecell>

mfp= 170   # cm
rand.seed(0)
pos0= np.array([0.0, 0.5, 20.999])  # initial position
dir0= np.array([0.1, 0.05, -1])    # initial direction
photon1= Photon(pos0, dir0 , mfp=mfp, trackvtx=True)
photon2= Photon(pos0, dir0 , mfp=mfp, trackvtx=True)

# <codecell>

final_plane1= photon1.propagate(chex_bg)

# <codecell>

photon1.print_properties()
print photon1.pathlength, photon1.status, photon1.t0, photon1.t
photon1.lastplane.print_properties()

# <codecell>

fig= plt.figure(figsize=(5,10))
ax = fig.add_subplot(121, projection='3d')
draw_one_crystal(ax, chex_bg, photon1)
fig.savefig('plots/hex_21cm.pdf')

# <markdowncell>

# <h2>Run experiments</h2>

# <markdowncell>

# <h3>Point source</h3>

# <codecell>

dt_point=[]   # Store the detection time
N = 50000  # number of generated photons
for i in xrange(N):
    x0, d0 = generate_p6(np.array([0,0,20.99]), 0.001, 0.001)
    photon = Photon(x0, d0, t=0, mfp=mfp)
    plane= photon.propagate(chex_bg)
    if photon.status != photon.transmitted: continue
    if photon.lastplane is None: continue
    if photon.lastplane.sensitive:
        dt_point.append(photon.t)
dt_point= np.array(dt_point)

# <codecell>

fig= plt.figure(figsize=(10,4))
plt.subplot(121)
plt.hist(dt_point, bins=100, histtype='step');
plt.subplot(122)
plt.hist(dt_point[dt_point<10], bins=100, histtype='step');
plt.xlim(0,10)
fig.savefig('../plots/timing_hex_bf2_21cm_pointsource.pdf')

# <markdowncell>

# <h3>Spreadout source: normal incidence</h3>

# <codecell>

z_hi= 20.9999    ## top of the crystal
shower_max= 5    # show maximum at 5 cm into the crystal
shower_sigmaz= 5  # sigma in z of a Gaussian to model the shower
shower_sigmax= 2  # sigma in x of a Gaussian to model the shower
shower_sigmay= 2  # sigma in y of a Gaussian to model the shower

# <codecell>

N= 400000
rand.seed(0)
zgen = rand.normal(shower_max, shower_sigmaz, size=N)
zgen = z_hi- zgen
xgen = rand.normal(0, shower_sigmax, size=N)
ygen = rand.normal(0, shower_sigmay, size=N)
sel= (zgen<21)&(zgen>0)&(np.sqrt(xgen**2+ygen**2)<1.9)
zgen= zgen[sel]
xgen= xgen[sel]
ygen= ygen[sel]
print len(zgen)

# <codecell>

dt_lin1=[]   # Store the arrival time
startxx=[]
for x,y,z in zip(xgen,ygen,zgen):
    x0, d0 = generate_p6(np.array([x,y,z]), 0.001, 0.001)
    t0 = abs(z_hi-z)/clightcmns
    photon = Photon(x0, d0, t=t0, mfp=mfp)
    plane= photon.propagate(chex_bg)
    if photon.status != photon.transmitted: continue
    if photon.lastplane is None: continue
    if photon.lastplane.sensitive:
        dt_lin1.append(photon.t)
        startxx.append(photon.startx)
dt_lin1= np.array(dt_lin1)
startxx= np.array(startxx)

# <codecell>

fig= plt.figure(figsize= (14,4))
plt.subplot(131)
plt.hist(np.array(startxx)[:,0], bins=40, histtype='step');
plt.xlabel('Photon creation x (cm)')
plt.subplot(132)
plt.hist(np.array(startxx)[:,1], bins=40, histtype='step');
plt.xlabel('Photon creation y (cm)')
plt.subplot(133)
plt.hist(np.array(startxx)[:,2], bins=40, histtype='step');
plt.xlabel('Photon creation z (cm)')
fig.savefig('../plots/genposition_gaussianshower.pdf')

# <codecell>

fig= plt.figure(figsize=(10,4))
plt.subplot(121)
plt.hist(dt_lin1, bins=100, histtype='step');
plt.xlabel('t (ns)')
plt.title('Photon traveling time')

plt.subplot(122)
plt.hist(dt_lin1[dt_lin1<4], bins=40, histtype='step');
plt.xlim(0,4)
plt.xlabel('t (ns)')
plt.title('Photon traveling time (zoom in)')
fig.savefig('../plots/timing_hex_bf2_21cm_gaussianshower.pdf')

# <codecell>

np.save('../data/timing/arrival_time_hex_bf2_21cm_pointsource.npy', dt_point)
np.save('../data/timing/arrival_time_hex_bf2_21cm_gaussianshower.npy', dt_lin1)

# <codecell>

x= rand.gamma(shape=4, scale=2, size=100000)
plt.hist(x, bins=50, histtype='step');
x= rand.gamma(shape=3, scale=2, size=100000)
plt.hist(x, bins=50, histtype='step');

# <codecell>


