# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# <h1>Photon collection efficiencies</h1>
# 
# For geometries defined in <b><code>geometry_collection2.ipynb</code></b>

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt

# <codecell>

import numpy as np
#from IPython.display import display_latex
from IPython.display import display_html
from IPython.display import Latex

# <headingcell level=2>

# <h2>Get efficiencies from log files</h2>

# <codecell>

def get_eff_from_log(fname, tag='efficiency='):
    '''
    Get the efficiency from a text/log file by getting the number right after
    *tag*
    '''
    eff= None
    f= open(fname, 'r')
    for gl in f:
        fields = gl.split()
        if tag in fields:
            idx = fields.index(tag)+1
            while idx < len(fields):
                try:
                    eff= float(fields[idx])
                    break
                except:
                    pass
                idx+= 1
        if eff is not None:
            break
    f.close()
    return eff

# <codecell>

eff_hex={}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for sd in ['3','9']:
            key= mat+sur+sd
            logname= '../log/timing/time_geom2_hex_%s.log'%(key)
            eff_hex[key]= get_eff_from_log(logname)
eff_rect={}
for mat in ['lyso','baf2','csi']:
    for sur in ['po','ra']:
        for lg in [1,2,3]:
            key= mat+sur+str(lg)
            logname= '../log/timing/time_geom2_rect_%s.log'%(key)
            eff_rect[key]= get_eff_from_log(logname)

# <codecell>

table1=u'''
<table>
<tr><td>Surface</td><td>Polished</td><td>Polished</td><td>Roughened</td><td>Roughened</td></tr>
<tr><td>Sensor</td><td>2x 9mmX9mm </td><td>2x 3mmX3mm </td><td>2x 9mmX9mm </td><td>2x 3mmX3mm </td></tr>
'''
cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
for mat in ['lyso','baf2','csi']:
    table1+= '<tr><td>%s</td>'%cnames[mat]
    for sur in ['po','ra']:
        for sd in ['9','3']:
            key= mat+sur+sd
            table1+= '<td>%.3f</td>'%(eff_hex[key])
    table1+= '</tr>\n'
table1+= '</table>\n'

# <codecell>

table2=u'''
<table border="0" rules="rows">
<tr><td>Surface</td><td>Polished</td><td>Polished</td><td>Polished</td><td>
  Roughened</td><td>Roughened</td><td>Roughened</td></tr>
<tr><td>Length</td><td>10 mm</td><td>20 mm</td><td>30 mm</td><td>10 mm</td><td>20 mm</td><td>30 mm</td></tr>
'''
cnames=dict(lyso='LYSO', baf2='BaF2', csi='CsI')
for mat in ['lyso','baf2','csi']:
    table2+= '<tr><td>%s</td>'%cnames[mat]
    for sur in ['po','ra']:
        for lg in [1,2,3]:
            key= mat+sur+str(lg)
            table2+= '<td>%.3f</td>'%(eff_rect[key])
    table2+= '</tr>\n'
table2+= '</table>\n'

# <codecell>

print 'photon collection efficiencies for mu2e-like hexagonal bars'
display_html(table1, raw=True)

# <codecell>

print 'photon collection efficiencies for small rectangular prisms'
display_html(table2, raw=True)

# <codecell>


