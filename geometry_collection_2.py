# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Geometry collection #2</h1>
# 
# Define a few crystals. To use it, import all
# 
# [1]: from geometry_collection_2 import *

# <codecell>

#%matplotlib inline
#import matplotlib.pyplot as plt

# <codecell>

import numpy as np
from pycrysray import *
from surface_collection_2 import *
from gen_utilities import *

# <markdowncell>

# <h2>Define geometries</h2>
# 
# Mu2e crystals<br>
# Hexagon: edge-to-edge width= 3.3 cm<br>
# Length:
# * LYSO: 11 cm
# * BaF2: 20 cm
# * CsI:  19 cm
# 
# Square: 3cm by 3cm<br>
# Length:
# * LYSO: 11 cm
# * BaF2: 20 cm
# * CsI:  19 cm
# 
# PET scan crystals
# * Cross section 3 mm X 3 mm
# * Length: 1 cm, 2 cm, or 3 cm
# 
# Sensors for hexagonal crystals<br>
# * Two 9 mm X 9 mm photo sensors
# * Two 3 mm X 3 mm photo sensors
# 
# Sensors for PET crystals
# * One 3 mm X 3 mm photo sensor

# <codecell>

## dimensions
# --- hexagon
lenlyso, lenbaf2, lencsi = 11.0, 20.0, 19.0
hexwidth= 3.3
hexgoes={}
#   polished
hexgoes['lyso_po']= hex_prism(center=[0,0,lenlyso/2.0], length=lenlyso, width=hexwidth, **lyso_polish)
hexgoes['baf2_po']= hex_prism(center=[0,0,lenbaf2/2.0], length=lenbaf2, width=hexwidth, **baf2_polish)
hexgoes['csi_po']=  hex_prism(center=[0,0,lencsi/2.0],  length=lencsi,  width=hexwidth, **csi_polish)
#   all sides roughened
hexgoes['lyso_ra']= hex_prism(center=[0,0,lenlyso/2.0], length=lenlyso, width=hexwidth, **lyso_rough)
hexgoes['baf2_ra']= hex_prism(center=[0,0,lenbaf2/2.0], length=lenbaf2, width=hexwidth, **baf2_rough)
hexgoes['csi_ra']=  hex_prism(center=[0,0,lencsi/2.0],  length=lencsi,  width=hexwidth, **csi_rough)

# --- square 
sqside = 3.0
squgeos = {}
#  polished
squgeos['lyso_po'] = rect_prism(center=[0,0,lenlyso/2.0], length=lenlyso, xlen=sqside, ylen=sqside, **lyso_polish)
squgeos['baf2_po'] = rect_prism(center=[0,0,lenbaf2/2.0], length=lenbaf2, xlen=sqside, ylen=sqside, **baf2_polish)
squgeos['csi_po'] =  rect_prism(center=[0,0,lencsi/2.0],  length=lencsi,  xlen=sqside, ylen=sqside, **csi_polish)
#   all sides roughened
squgeos['lyso_ra'] = rect_prism(center=[0,0,lenlyso/2.0], length=lenlyso, xlen=sqside, ylen=sqside, **lyso_rough)
squgeos['baf2_ra'] = rect_prism(center=[0,0,lenbaf2/2.0], length=lenbaf2, xlen=sqside, ylen=sqside, **baf2_rough)
squgeos['csi_ra'] =  rect_prism(center=[0,0,lencsi/2.0],  length=lencsi,  xlen=sqside, ylen=sqside, **csi_rough)

# PET Rectangle
def rect_list(lengths, width, **surface):
    retval=[]
    for lg in lengths:
        rec = rect_prism(center=[0,0,lg/2.0], length=lg, xlen=width, ylen=width, **surface)
        retval.append(rec)
    return retval
petw= 0.3
recgoes={}
#    polished
recgoes['lyso_po1'], recgoes['lyso_po2'], recgoes['lyso_po3'] = rect_list([1,2,3], petw, **lyso_polish)
recgoes['baf2_po1'], recgoes['baf2_po2'], recgoes['baf2_po3'] = rect_list([1,2,3], petw, **baf2_polish)
recgoes['csi_po1'],  recgoes['csi_po2'],  recgoes['csi_po3']  = rect_list([1,2,3], petw, **csi_polish)
#    roughened
recgoes['lyso_ra1'], recgoes['lyso_ra2'], recgoes['lyso_ra3'] = rect_list([1,2,3], petw, **lyso_rough)
recgoes['baf2_ra1'], recgoes['baf2_ra2'], recgoes['baf2_ra3'] = rect_list([1,2,3], petw, **baf2_rough)
recgoes['csi_ra1'],  recgoes['csi_ra2'],  recgoes['csi_ra3']  = rect_list([1,2,3], petw, **csi_rough)

# <codecell>

# Sensors
#  For hexagon
#     locations
loc1= [0,+0.7,0]
loc2= [0,-0.7,0]
def get_sensors(locations, xlen, ylen, **surface):
    retval=[]
    for loc in locations:
        retval.append(rectangle(loc, xlen=xlen, ylen=ylen, **surface))
    return retval
sensors={}
#     two 9x9mm
xlen, ylen=  0.9, 0.9
sensors['s1_lysog9'], sensors['s2_lysog9'] = get_sensors([loc1, loc2], xlen, ylen, **lyso_glue)
sensors['s1_baf2g9'], sensors['s2_baf2g9'] = get_sensors([loc1, loc2], xlen, ylen, **baf2_glue)
sensors['s1_csig9'], sensors['s2_csig9'] = get_sensors([loc1, loc2], xlen, ylen, **csi_glue)
#      two 3x3mm
xlen, ylen=  0.3, 0.3
sensors['s1_lysog3'], sensors['s2_lysog3'] = get_sensors([loc1, loc2], xlen, ylen, **lyso_glue)
sensors['s1_baf2g3'], sensors['s2_baf2g3'] = get_sensors([loc1, loc2], xlen, ylen, **baf2_glue)
sensors['s1_csig3'], sensors['s2_csig3'] = get_sensors([loc1, loc2], xlen, ylen, **csi_glue)

#  For PET
#     one 3x3mm
location= [0,0,0]
xlen, ylen= 0.3, 0.3
sensors['s0_lysog'] = rectangle(location, xlen=xlen, ylen=ylen, **lyso_glue)
sensors['s0_baf2g'] = rectangle(location, xlen=xlen, ylen=ylen, **baf2_glue)
sensors['s0_csig'] = rectangle(location, xlen=xlen, ylen=ylen, **csi_glue)

# <markdowncell>

# <h2>Define crystals</h2>

# <codecell>

# Define crystals
#  hexagons
chexes={}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd in ['3','9']:
            key= mat+sur+sd
            k2= mat+'g'+sd
            chexes[key] = Crystal(key, hexgoes[mat+'_'+sur] + [sensors['s1_'+k2],sensors['s2_'+k2]])
            
# long squares for mu2e
csquares= {}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd in ['3','9']:
            key= mat+sur+sd
            k2= mat+'g'+sd
            csquares[key] = Crystal(key, squgeos[mat+'_'+sur] + [sensors['s1_'+k2],sensors['s2_'+k2]])

            
# rectangles (square cross section, actualy, for PET)
crects={}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for lg in ['1','2','3']:
            key= mat+sur+lg
            crects[key] = Crystal(key, recgoes[mat+'_'+sur+lg] + [sensors['s0_'+mat+'g']])

# <codecell>

#fig= plt.figure(figsize=(20,10))
#i=0
#for mat in ['lyso','baf2','csi']:
#    for sur in ['po','ra']:
#        crys = chexes[mat+sur+'3']
#        ax= fig.add_subplot(161+i, projection='3d')
#        draw_one_crystal(ax, crys)
#        i+= 1

# <codecell>

#fig= plt.figure(figsize=(20,10))
#i=0
#for mat in ['lyso','baf2','csi']:
#    for sur in ['po','ra']:
#        crys = crects[mat+sur+'3']
#        ax= fig.add_subplot(161+i, projection='3d')
#        draw_one_crystal(ax, crys, 0.5,0.5,3)
#        i+= 1

# <codecell>


