# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np

# <codecell>

m1= np.matrix([[1,0,0],[0,1,1],[1,1,1]], dtype=np.float64) 
m2= np.matrix([[1,0,0],[0,1,1],[1,1,1]], dtype=np.float64) 

# <codecell>

def mprod(m1,m2):
    for i in range(1000):
        m3= m1*m2
    return m3

# <codecell>

%timeit mprod(m1,m2)

# <codecell>

%load_ext cythonmagic

# <codecell>

%%cython
cimport numpy as np
def cmprod(np.ndarray[np.float64_t, ndim=2] m1, np.ndarray[np.float64_t, ndim=2] m2):
    cdef np.ndarray[np.float64_t, ndim=2] m3
    cdef int i
    for i in range(1000):
        m3= m1*m2
    return m3

# <codecell>

%timeit cmprod(m1,m2)

# <codecell>

%%cython
cimport numpy as np
cpdef float cvdot(double[:] v1, double[:] v2, int n):
    cdef double sum=0
    cdef int i
    for i in range(n):
        sum+= v1[i]*v2[i]
    return sum

# <codecell>

v1= np.array([1,2,3], dtype=np.float64)
v2= np.array([4,5,6], dtype=np.float64)

%timeit cvdot(v1,v2,3)

# <codecell>

%%cython
def cvdot2(double v11, double v12, double v13, double v21, double v22, double v23):
    return v11*v21+v12*v22+v13*v23

# <codecell>

%timeit cvdot2(1,2,3,4,5,6)

# <codecell>

%%cython
cimport numpy as np
def cvdot3(np.ndarray[np.float64_t, ndim=1] v1, np.ndarray[np.float64_t, ndim=1] v2):
    return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
def cvdot4(np.ndarray[np.float64_t, ndim=1] v1, np.ndarray[np.float64_t, ndim=1] v2):
    return v1.dot(v2)

# <codecell>

%timeit cvdot3(v1,v2)

# <codecell>

%timeit cvdot4(v1,v2)

# <codecell>


# <codecell>

def pvdot2(v11,v12,v13,v21,v22,v23):
    return v11*v21+v12*v22+v13*v23

# <codecell>

%timeit pvdot2(1,2,3,4,5,6)

# <codecell>

%timeit vdot(v1,v2)

# <codecell>


# <codecell>

def pvdot(v1, v2):
    return v1.dot(v2)
def pvdotmany(v1,v2,k):
    sum=0
    for i in range(k):
        sum= v1.dot(v2)
    return sum

# <codecell>

%timeit pvdotmany(v1,v2, 1000)

# <codecell>


