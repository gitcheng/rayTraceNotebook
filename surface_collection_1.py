# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Surface collection</h1>
# 
# Define a few surfaces. To use it, just import everything
# 
# [1]: from surface_collection_1 import *

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
# $\sigma$ of reflection = 0.1 degree<br>
# 
# If the photon is transmitted out of the crystal and hit the wrapper:
# * 10% probability of random reflaction
# * 89% probability of diffused reflection: $\sigma$ of diffused reflection = 20 degrees
# * 1% probability of absorption (disappearance)
# 
# For photons hitting in the sensor area:
# * Assume photons going from crystal (LYSO $n=1.82$ or BaF2 $n=1.47$, or CsI $n=1.79$) to glass ($n= 1.52$).

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
base_wrap= dict(sigdif_crys=0.1, pdif_crys=1.0, prand_crys=0.0, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
                idx_refract_out=nair, sensitive=False, wrapped=True)
lyso_wrap= base_wrap.copy()
baf2_wrap= base_wrap.copy()
csi_wrap= base_wrap.copy()
##
lyso_wrap['idx_refract_in']= nlyso
baf2_wrap['idx_refract_in']= nbaf2
csi_wrap['idx_refract_in']= ncsi
# sensitive surface
lyso_glass= sensitive_surface(lyso_wrap, nglass)
baf2_glass= sensitive_surface(baf2_wrap, nglass)
csi_glass= sensitive_surface(csi_wrap, nglass)

