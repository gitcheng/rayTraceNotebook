#!/bin/usr/python

# create a set of scripts for timing studies under different geometries
# and conditions. 
# Geommetries are defined in geometry_collection_2.
# 

from geometry_collection_2 import *
ngen= 200000
clengths= dict(lyso=lenlyso, baf2=lenbaf2, csi=lencsi)

header= 'from geometry_collection_2 import *\n'+\
        'from gen_utilities import *\n'+\
        'from timing_utilities import *\n'+\
        'import numpy as np\n'

header+= 'ngen= %d\n'%ngen
header+= 'np.random.seed(0)\n'

#print header

footer= 'ndet= len(data)\n'+\
        'print ndet\n'+\
        'print \'efficiency= %.3f\' % (ndet/float(ngen))'

for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd in ['3','9']:
            key= mat+sur+sd
            basename= 'time_geom2_hex_'+key
            scriptname= 'scripts/'+basename+'.py'
            dataname= '../data/timing/%s'%(basename)
            logname= '../log/timing/%s.log'%(basename)

            body= 'allpos= gen_gamma_func_shower1(z1=%f, z2=0, rmax=%f/2., size= ngen)\n'%(clengths[mat],hexwidth)
            body+= 'data= sim_timing(chexes[\'%s\'], allpos, t0origin=[0,0,%f], mfp=170,print_prog= True)\n'%(key, clengths[mat])
            body+= 'np.save(\'%s\', data)\n'%(dataname)

            script= header+body+footer

            f= open(scriptname, 'w')
            f.write(script)
            f.close()

            print 'bsub -q xlong -R rhel60 -oo %s python %s'%(logname, scriptname)

