'''
Generate 200000 photons in a BaF2 crystal defined in geometry_collection_1.py
Run it like
python time_baf2_hex_G1.py >& ../log/timing/ts_baf2_hex_33_200_n200k_0001.log
'''
from geometry_collection_1 import *
from gen_utilities import *
from timing_utilities import *

ngen= 200000
allpos= gen_gamma_func_shower1(z1=lenbaf2, z2=0, rmax=hexwidth/2., size= ngen)
ts_hex_baf2= sim_timing(chex_baf2, allpos, t0origin=[0,0,lenbaf2], mfp=170,
                        seed=0, print_prog= True)
np.save('../data/timing/ts_baf2_hex_33_200_n200k_0001', ts_hex_baf2)
ndet= len(ts_hex_baf2)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))
