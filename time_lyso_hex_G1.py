'''
Generate 1000000 photons in a LYSO crystal defined in geometry_collection_1.py
Run it like
python time_lyso_hex_G1.py >& ../log/timing/ts_lyso_hex_33_110_n1000k_0001.log
'''
from geometry_collection_1 import *
from gen_utilities import *
from timing_utilities import *

ngen= 1000000
allpos= gen_gamma_func_shower1(z1=lenlyso, z2=0, rmax=hexwidth/2., size= ngen)
ts_hex_lyso= sim_timing(chex_lyso, allpos, t0origin=[0,0,lenlyso], mfp=170,
                        seed=0, print_prog= True)
np.save('../data/timing/ts_lyso_hex_33_110_n1000k_0001', ts_hex_lyso)
ndet= len(ts_hex_lyso)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))
