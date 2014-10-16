from geometry_collection_2 import *
from gen_utilities import *
from timing_utilities import *
import numpy as np
ngen= 100000
np.random.seed(0)
allpos= gen_uniform_pos(-0.150,0.150,-0.150,0.150,0,3,ngen)
data= sim_timing(crects['baf2ra3'], allpos, t0origin=[0,0,3],mfp=170,print_prog= True)
np.save('../data/timing/time_geom2_rect_baf2ra3', data)
ndet= len(data)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))