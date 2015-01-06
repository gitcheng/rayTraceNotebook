# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%matplotlib inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import pickle

# <codecell>

data = pickle.load(open('../data/timing/wffit_baf2po9_npe1000_bw5_fr100.p', 'rb'))

# <codecell>

x0s = np.array([d['x0'] for d in data])
sigmas = np.array([d['sigma'] for d in data])
tau1s = np.array([d['tau1'] for d in data])
tau2s = np.array([d['tau2'] for d in data])

# <codecell>

plt.scatter(x0s, sigmas, alpha=0.3)

# <codecell>

plt.scatter(x0s, tau1s, alpha=0.3)

# <codecell>

plt.scatter(x0s, tau2s, alpha=0.3)

# <codecell>

plt.scatter(tau1s, tau2s, alpha=0.3)

# <codecell>


