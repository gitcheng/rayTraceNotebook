from geometry_collection_2 import *
from gen_utilities import *
from timing_utilities import *
import numpy as np
ngen= 100000
np.random.seed(0)
allpos= gen_uniform_pos(-0.150,0.150,-0.150,0.150,0,1,ngen)
data= sim_timing(crects['csira1'], allpos, t0origin=[0,0,1],mfp=170,print_prog= True)
np.save('../data/timing/time_geom2_rect_csira1', data)
ndet= len(data)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))