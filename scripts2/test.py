import sys
sys.path += ['/Users/chcheng/Work/mu2e/LightCollectionStudy/rayTraceNotebook']
from geometry_collection_2 import *
from gen_utilities import *
from timing_utilities import *
import numpy as np
from root_numpy import *
shower = root2rec("../data/shower_baf2.root", "ntp1")
np.random.seed(0)

data= sim_timing_shower(chexes['baf2po9'], shower[:20], nep=100, t0origin=[0,0,20.000000], shdir=-1, showerunit=0.1, mfp=170, print_prog= True)
sfile = '../data/timing/time_geom2_shower_hex_baf2po9'
np.save(sfile, data)
print 'Save file at', sfile
