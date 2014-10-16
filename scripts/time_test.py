'''

'''
from geometry_collection_2 import *
from gen_utilities import *
from timing_utilities import *

ngen= 10000
allpos= gen_gamma_func_shower1(z1=lenbaf2, z2=0, rmax=hexwidth/2., size= ngen)
gdata = sim_timing(chexes['baf2po9'], allpos, t0origin=[0,0,lenbaf2], mfp=170,
                   seed=0, print_prog= True)
np.save('../data/timing/ts_baf2_test', gdata)
ndet= len(gdata)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))
