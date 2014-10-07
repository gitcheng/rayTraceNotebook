'''
Generate 500000 photons in a LYSO crystal defined in geometry_collection_1.py
1x1x2 cm crystal (could be use in PET scanner)
Run it like
python time_lyso_pet_G2.py >& ../log/timing/ts_lyso_pet_1_1_2_n500k_0001.log
''' 
ngen= 500000
allpos= gen_uniform_pos(-0.5,0.5, -0.5,0.5, 0, 2, ngen)
ts_pet_lyso= sim_timing(cpet_lyso, allpos, t0origin=[0,0,2], mfp=170, seed=0)
np.save('../data/timing/ts_lyso_pet_1_1_2_n500k_0001', ts_pet_lyso)
ndet= len(ts_pet_lyso)
print ndet
print 'efficiency= %.3f' % (ndet/float(ngen))
