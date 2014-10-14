# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Surface collection #2</h1>
# 
# Define a few surfaces. To use it, just import everything
# 
# [1]: from surface_collection_2 import *

# <codecell>

import numpy as np

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
# * polished surface: $\sigma$ of reflection = 0.1 degree<br>
# * roughened surface: $\sigma$ of reflection = 20 degree<br>
# 
# If the photon is transmitted out of the crystal and hit the wrapper:
# * 10% probability of random reflaction
# * 89% probability of diffused reflection: $\sigma$ of diffused reflection = 20 degrees
# * 1% probability of absorption (disappearance)
# 
# For photons reflecting in the sensor area<br>
# Assume photons going from crystal (LYSO $n=1.82$ or BaF2 $n=1.47$, or CsI $n=1.79$) to optical glue ($n= 1.45$).

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

def change_index_in(dict_orig, idx_in):
    '''
    Take a dictionary for a wrapped surface and change the refractive index inside.
    *dict_orig*: original surface properties
    *idx_in*: index of refraction of the material inside the crystal
    '''
    retval= dict_orig.copy()
    retval['idx_refract_in']= idx_in
    return retval

# <codecell>

# Indices of refraction
nlyso, nbaf2, ncsi = 1.82, 1.47, 1.79
nglue = 1.45
nair = 1.0
# Wrapped surface: polished
base_polish= dict(sigdif_crys=0.1, pdif_crys=1.0, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
                    idx_refract_out=nair, sensitive=False, wrapped=True)
base_rough= dict(sigdif_crys=20.0, pdif_crys=1.0, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
                    idx_refract_out=nair, sensitive=False, wrapped=True)

# polished surface
lyso_polish= change_index_in(base_polish, nlyso)
baf2_polish= change_index_in(base_polish, nbaf2)
csi_polish= change_index_in(base_polish, ncsi)

# roughened surface
lyso_rough = change_index_in(base_rough, nlyso)
baf2_rough = change_index_in(base_rough, nbaf2)
csi_rough = change_index_in(base_rough, ncsi)

# sensitive surface (polished)
lyso_glue= sensitive_surface(lyso_polish, nglue)
baf2_glue= sensitive_surface(baf2_polish, nglue)
csi_glue= sensitive_surface(csi_polish, nglue)

# <codecell>


