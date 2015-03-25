# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from root_numpy import *
from gen_utilities import getflat
from matplotlib.colors import LogNorm

# <codecell>

shower_baf2 = root2rec('../data/shower_baf2.root', 'ntp1')
shower_lyso = root2rec('../data/shower_lyso.root', 'ntp1')
shower_csi = root2rec('../data/shower_csi.root', 'ntp1')

# <codecell>

bins = np.linspace(0, 500, 100)
plt.hist(getflat(shower_baf2.hitZ), bins= bins, weights= getflat(shower_baf2.hitEdep));

# <codecell>

fig = plt.figure(figsize=(8,4))
x = getflat(shower_baf2.hitX)
y = getflat(shower_baf2.hitY)
rho = np.sqrt(x*x + y*y)
z = getflat(shower_baf2.hitZ)
bins = [np.linspace(0, 300, 30), np.linspace(-30, 30, 30)]
plt.hist2d(z, x, bins = bins, weights = getflat(shower_baf2.hitEdep), norm = LogNorm());
plt.colorbar()
plt.xlabel('z (mm)', fontsize='x-large')
plt.ylabel('x (mm)', fontsize='x-large')
plt.title('Energy-weighted distribution', fontsize='x-large')
plt.savefig('../plots/shower/G4shower_baf2_2D.pdf')

# <codecell>

bins = np.linspace(0, 350, 35)
j= 10
plt.hist(shower_baf2.hitZ[j], bins=bins, weights = shower_baf2.hitEdep[j], histtype='stepfilled', alpha= 0.5);
j= 20
plt.hist(shower_baf2.hitZ[j], bins=bins, weights = shower_baf2.hitEdep[j], histtype='stepfilled', alpha= 0.5);
j= 30
plt.hist(shower_baf2.hitZ[j], bins=bins, weights = shower_baf2.hitEdep[j], histtype='stepfilled', alpha= 0.5);
plt.xlabel('z (mm)', fontsize='x-large')
plt.title('Energy-weighted distributions of three events', fontsize='x-large')
plt.savefig('../plots/shower/G4shower_baf2_1D_3events.pdf')

# <codecell>

bins = np.linspace(0, 350, 35)
tt = getflat(shower_baf2.hitT)
plt.hist(tt, bins=100, weights = getflat(shower_baf2.hitEdep), histtype='stepfilled');
plt.xlabel('t (ns)', fontsize='x-large')
plt.title('Energy-weighted distributions', fontsize='x-large')
plt.savefig('../plots/shower/G4shower_baf2_time.pdf')

# <codecell>


