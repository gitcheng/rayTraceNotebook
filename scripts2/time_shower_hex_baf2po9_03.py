import sys
basedir = '/home/chcheng/Work/mu2e/LightCollectionStudy/'
print sys.path
import numpy as np
from root_numpy import *
from gen_utilities import *
from timing_utilities import *
from geometry_collection_2 import *
shower = root2rec(basedir+"data/shower_baf2.root", "ntp1")
np.random.seed(0)

data= sim_timing_shower(chexes['baf2po9'], shower[400:600], nep=1000, t0origin=[0,0,20.000000], shdir=-1, showerunit=0.1, mfp=170, print_prog= True)
sfile = basedir+'data/timing/time_geom2_shower_hex_baf2po9_03'
np.save(sfile, data)
print 'Save file at', sfile
