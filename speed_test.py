# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Speed test</h1>

# <codecell>

import numpy as np
import numpy.random as nprnd
import time
import matplotlib.pyplot as plt
from pycrysray import *

# <codecell>

%load_ext cythonmagic

# <codecell>


# <codecell>

a= np.array([1,2,3], np.float64)
%timeit unit_vect(a)   # 8.5 us

# <codecell>

%timeit vect_norm(a)   # 2.2 us

# <codecell>

%%cython
cimport numpy as np
def scalearray(np.ndarray a, double s):
    return s*a

# <codecell>

%timeit scalearray(a,0.4)

# <codecell>

%timeit (1.0/0.5)*a

# <codecell>

a= np.array([1,2,3], np.float64)
b= np.array([4,2,7], np.float64)
c= np.array([0,1,-1], np.float64)
%timeit sine_angle(a,b,c)    # 50 us

# <codecell>

print rotate_vector(a,c)

# <codecell>

print rotate_vector(a,c)

# <codecell>

%timeit rotate_vector(a,c)   # 82 us

# <codecell>

stheta= math.sin(1)
ctheta= math.cos(1)
sphi= math.sin(1)
cphi= math.cos(1)
Ry= np.matrix([ [ctheta, 0.0, stheta], [0.0,1.0,0.0], [-stheta, 0.0, ctheta] ], dtype=np.float64 )
Rz = np.matrix([ [cphi,-sphi,0.0],[sphi,cphi,0.0],[0.0,0.0,1.0] ], dtype=np.float64)
print Ry.shape, Rz.shape
print Ry*Rz

# <codecell>

%timeit Ry*Rz

# <codecell>

%%cython
cimport numpy as np
cdef mproduct(a, b):
    ret= np.zeros(9).reshape(3,3)
    for i in range(3):
        for j in range(3):
            ret[i][j]= a[i,0]*b[0,j] + a[i,1]*b[1,j] + a[i,2]*b[2,j]
    return ret

# <codecell>

print mproduct(Ry,Rz)

# <codecell>

%timeit mproduct(Ry,Rz)

# <codecell>

# Surface
surf= dict(sigdif_crys=0.1, sigdif_wrap=20, pdif_wrap=0.89, prand_wrap=0.10,
            idx_refract_in=1.82, idx_refract_out=1.0, sensitive=False, wrapped=True)
# Square
rw1= 3.0
grec= rect_prism([0,0,5.5], length=11, xlen=rw1, ylen=rw1, **surf)
# Crystals
crec= Crystal('crec', grec)

# <codecell>

nprnd.seed(0)
# Photon
pos, dir= generate_p6(np.array([0.0,0.0,8.0]), 0.1, 1.0)
photon= Photon(pos, dir, mfp= 500)

# <codecell>

photon.propagate(crec)
fig=figure(figsize=(11,12))
ax = fig.add_subplot(221, projection='3d')
draw_one_crystal(ax, crec, photon) 
print 'n_reflects=', photon.n_reflects, '; pahtlength=', photon.pathlength

# <codecell>

def test_run(crystal, n=1, seed=0):
    nprnd.seed(seed)
    for i in range(n):
        pos, dir= generate_p6(np.array([0.0,0.0,8.0]), 0.1, 1.0)
        photon= Photon(pos, dir, mfp= 500, trackvtx=True)
        photon.propagate(crystal)

# <codecell>

%timeit test_run(crec, 10, seed=10)

# <codecell>


# <codecell>


# <codecell>


# <codecell>


# <codecell>


# <codecell>

# http://docs.cython.org/src/userguide/early_binding_for_speed.html

# <codecell>

# Simple python
class Rectangle:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
    def area(self):
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea(x0, y0, x1, y1):
    rect = Rectangle(x0, y0, x1, y1)
    return rect.area()

# <codecell>

%timeit rectArea(1,2,3,4)

# <codecell>

# Cython-1

# <codecell>

%%cython
cdef class Rectangle1:
    cdef int x0, y0
    cdef int x1, y1
    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
    def area(self):
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea1(x0, y0, x1, y1):
    rect = Rectangle1(x0, y0, x1, y1)
    return rect.area()

# <codecell>

%timeit rectArea1(1,2,3,4)

# <codecell>

# Cython-2

# <codecell>

%%cython
cdef class Rectangle2:
    cdef int x0, y0
    cdef int x1, y1
    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
    cdef int _area(self):
        cdef int area
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area
    def area(self):
        return self._area()

def rectArea2(x0, y0, x1, y1):
    cdef Rectangle2 rect
    rect = Rectangle2(x0, y0, x1, y1)
    return rect._area()

# <codecell>

%timeit rectArea2(1,2,3,4)

# <codecell>

# Cython-3

# <codecell>

%%cython
cdef class Rectangle3:
    cdef int x0, y0
    cdef int x1, y1
    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
    cpdef int area(self):
        cdef int area
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea3(x0, y0, x1, y1):
    cdef Rectangle3 rect
    rect = Rectangle3(x0, y0, x1, y1)
    return rect.area()

# <codecell>

%timeit rectArea3(1,2,3,4)

# <codecell>

# Cython-4

# <codecell>

%%cython
cdef class Rectangle4:
    cdef int x0, y0
    cdef int x1, y1
    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0; self.y0 = y0; self.x1 = x1; self.y1 = y1
    cpdef int area(self):
        cdef int area
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea4(int x0, int y0, int x1, int y1):
    cdef Rectangle4 rect
    rect = Rectangle4(x0, y0, x1, y1)
    return rect.area()

# <codecell>

%timeit rectArea4(1,2,3,4)

# <codecell>


