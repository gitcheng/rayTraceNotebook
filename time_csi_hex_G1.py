'''
Generate 200000 photons in a CsI crystal defined in geometry_collection_1.py
Run it like
python time_csi_hex_G1.py >& ../log/timing/ts_csi_hex_33_190_n200k_0001.log
'''
from geometry_collection_1 import *
from gen_utilities import *
from timing_utilities import *

ngen= 200000
allpos= gen_gamma_func_shower1(z1=lencsi, z2=0, rmax=hexwidth/2., size= ngen)
ts_hex_csi= sim_timing(chex_csi, allpos, t0origin=[0,0,lencsi], mfp=170,
                       seed=0, print_prog= True)
np.save('../data/timing/ts_csi_hex_33_190_n200k_0001', ts_hex_csi)
ndet= len(ts_hex_csi)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))
