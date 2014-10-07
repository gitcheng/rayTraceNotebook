'''
Generate 100000 photons in a BaF2 crystal defined in geometry_collection_1.py
1x1x2 cm crystal (could be use in PET scanner)
Run it like
python time_baf2_pet_G2.py >& ../log/timing/ts_baf2_pet_1_1_2_n100k_0001.log
''' 
ngen= 100000
allpos= gen_uniform_pos(-0.5,0.5, -0.5,0.5, 0, 2, ngen)
ts_pet_baf2= sim_timing(cpet_baf2, allpos, t0origin=[0,0,2], mfp=170, seed=0)
np.save('../data/timing/ts_baf2_pet_1_1_2_n100k_0001', ts_pet_baf2)
ndet= len(ts_pet_baf2)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))
