from geometry_collection_2 import *
from gen_utilities import *
from timing_utilities import *
import numpy as np
ngen= 200000
np.random.seed(0)
allpos= gen_gamma_func_shower1(z1=20.000000, z2=0, rmax=3.300000/2., size= ngen)
data= sim_timing(chexes['baf2po9'], allpos, t0origin=[0,0,20.000000], mfp=170,print_prog= True)
np.save('../data/timing/time_geom2_hex_baf2po9', data)
ndet= len(data)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))