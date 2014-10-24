# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Draw Geometry collection #2</h1>
# 
# Draw some crystals defined in geometry_collection_2.py

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt

# <codecell>

import numpy as np
from geometry_collection_2 import *

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

cnames= dict(lyso='LYSO', baf2='BaF2', csi='CsI')

# <codecell>

fig= plt.figure(figsize=(20,10))
i=0
for mat in ['lyso','baf2','csi']:
    for sd in ['9','3']:
        crys = chexes[mat+'po'+sd]
        ax= fig.add_subplot(161+i, projection='3d')
        draw_one_crystal(ax, crys, sensor_color='r', xlabel='cm', ylabel='cm', zlabel='cm', zlim=(0,21))
        ax.set_title(cnames[mat], fontsize='x-large')
        i+= 1
fig.savefig('../plots/geometry_coll2_hex.pdf')

# <codecell>

fig= plt.figure(figsize=(10,9))
i=0
for lg in [1,2,3]:
    crys = crects['baf2po'+str(lg)]
    ax= fig.add_subplot(131+i, projection='3d')
    draw_one_crystal(ax, crys, sensor_color='r', xlabel='cm', ylabel='cm', zlabel='cm', zlim=(0,3.1), xlim=(-0.5,0.5),
                     ylim=(-0.5,0.5))
    i+= 1
fig.savefig('../plots/geometry_coll2_rect.pdf')

# <codecell>

pos= np.array([0.,0.,19.])
dir= np.array([1.,2.,-1.])
photon1= Photon(pos, dir, mfp=170, trackvtx=True)
photon2= Photon(pos, dir, mfp=170, trackvtx=True)

fig= plt.figure(figsize=(8,10))

ax= fig.add_subplot(121, projection='3d')
crystal= chexes['baf2po9']
np.random.seed(0)
photon1.propagate(crystal)
draw_one_crystal(ax, crystal, sensor_color='r', photon=photon1, xlabel='cm', ylabel='cm', zlabel='cm',)

ax= fig.add_subplot(122, projection='3d')
crystal= chexes['baf2ra9']
np.random.seed(0)
photon2.propagate(crystal)
draw_one_crystal(ax, crystal, sensor_color='r', photon=photon2, xlabel='cm', ylabel='cm', zlabel='cm',)

fig.savefig('../plots/geometry_coll2_hex_photons.pdf')

# <codecell>

from timing_utilities import *
slapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd9mm', normtype='peak')
stdapd9mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'stdapd9mm', normtype='peak')
slapd3mm = pulse_model('../data/SLAPD_RiseTime_20140926.csv', 'time_ns', 'slapd3mm', normtype='peak')
# Fill in points using linear interpolation
slapd9mm = fill_pmodel_gaps(slapd9mm, ndivs=5)
stdapd9mm = fill_pmodel_gaps(stdapd9mm, ndivs=5)
slapd3mm = fill_pmodel_gaps(slapd3mm, ndivs=5)

# <codecell>

plt.plot(slapd9mm.t, slapd9mm.p, label='SL-APD 9mm');
plt.plot(slapd9mm.t, stdapd9mm.p, label='Std-APD 9mm');
plt.plot(slapd9mm.t, slapd3mm.p, label='SL-APD 3mm');
plt.xlim(0,200)
plt.ylim(-0.2,1.1)
plt.plot([0,200],[0,0], 'k-')
plt.legend()
plt.xlabel('ns')
plt.title('APD response time')
plt.savefig('../plots/apd_response_time.pdf')

# <codecell>

# Gamma function
z= rand.gamma(3.5, 2, 1000000)
plt.hist(z, bins=100, histtype='step');
plt.xlim(0,35)
plt.xlabel('z (cm)')
plt.savefig('../plots/gamma_distribution_3520.pdf')

# <codecell>


