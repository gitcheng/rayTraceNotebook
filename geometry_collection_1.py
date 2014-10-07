# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Geometry collection</h1>
# 
# Define a few crystals. To use it, import all
# 
# [1]: from geometry_collection_1 import *

# <codecell>

#%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from pycrysray import *
from surface_collection_1 import *
from gen_utilities import *

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

#fig= plt.figure(figsize=(20,10))
#for i, crys in enumerate([chex_lyso, chex_baf2, chex_csi, cpet_lyso, cpet_baf2, cpet_csi]):
#    ax = fig.add_subplot(161+i, projection='3d')
#    draw_one_crystal(ax, crys)

