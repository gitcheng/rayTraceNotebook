import sys
basedir = '/home/chcheng/Work/mu2e/LightCollectionStudy/'
print sys.path
import numpy as np
from root_numpy import *
from gen_utilities import *
from timing_utilities import *
from geometry_collection_2 import *
shower = root2rec(basedir+"data/shower_csi.root", "ntp1")
np.random.seed(0)

data= sim_timing_shower(chexes['csipo9'], shower[:200], nep=1000, t0origin=[0,0,19.0], shdir=-1, showerunit=0.1, mfp=170, print_prog= True)
sfile = basedir+'data/timing/time_geom2_shower_hex_csipo9_01'
np.save(sfile, data)
print 'Save file at', sfile
