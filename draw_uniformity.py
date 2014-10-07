# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt

# <codecell>

data1 = np.load('data/effz_polish_1_two10x10apd.npz')
data2 = np.load('data/effz_polish_1_two5x10apd.npz')
data3 = np.load('data/effz_polish_1_two5x5apd.npz')
d1= data1['data']
d2= data2['data']
d3= data3['data']
print 'data1:', data1['meta']
print 'data2:', data2['meta']
print 'data3:', data3['meta']

# <codecell>

fig1= plt.figure(figsize=(8,6))
plt.errorbar(d1[:,0], d1[:,1], yerr= d1[:,2], fmt='o', label='two 10x10 APD')
plt.errorbar(d2[:,0], d2[:,1], yerr= d2[:,2], fmt='o', label='two 5x10 APD')
plt.errorbar(d3[:,0], d3[:,1], yerr= d3[:,2], fmt='o', label='two 5x5 APD')
plt.legend(loc='upper right')
plt.xlim(0,11)
plt.ylim(ymin=0)
plt.ylabel('Efficiency', fontsize='xx-large')
plt.xlabel('Distance from sensors (cm)', fontsize='xx-large')
plt.grid()

# <codecell>


