# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:27:44 2015
Test of the Near Constant Contast (NCC) function DNBdstrp.NearConstantContrast
@author: Stephen Mills
copyright 2015, Renaissance Man Engineering, all rights reserved

"""

import granulemod as grn
import sys
import matplotlib.pyplot as plt
import DNBdstrp
import numpy as np

# line command parameters
narg=len(sys.argv)
pathgen=sys.argv[1]# the general directory path, e.g. L:\NPP_data\
datestr=sys.argv[2]# e.g. for Sept. 22, 2014 enter 20140922
time_from_to=sys.argv[3]# same format as time spans in file names, e.g. 
                  # t2310231_e2345388 for the period 23:10:23.1 to 23:45:38.8
Lmin=float(sys.argv[4]) # minimum radiance to consider for near-constant contrast
if narg>5:
    prcntl_pltlim=eval(sys.argv[5]) #percentile limits for plotting
else:
    prcntl_pltlim=[2,98]
print(Lmin)
# path to hdf files
pathhdf=pathgen+datestr+'/hdf/'

# get a list of all files within the time range
t_fromtostr='_d'+datestr+'_'+time_from_to
print( t_fromtostr)
[timelims,filelist]=grn.granulefile_list_sort(pathhdf,'SVDNB','h5',t_fromtostr)

print('Number of files found in time range: ',len(filelist))

# console inputs
destriped=int(input('Destriped NCC? (0=False; 1=True: 2=both): '))
if destriped>=1:
    name_extnd=input('Field Name Extension:')
    destripePlot=np.arange
    destripePlot=np.arange(2-destriped,2)
else:
    name_extnd=''
    destripePlot=np.arange(0,1)
# loop through all files found and produce a plot
destripingStr=['NCC', 'NCC Destriped']
for filename in filelist:
    print(filename)
    for i in destripePlot:
        NCC=DNBdstrp.NearConstantContrast(pathhdf,filename,Lmin,addField=True,
                                        reviseField=True,destriped=i,
                                        name_extnd=name_extnd)
        NCC[np.isnan(NCC)]=0.
        NCC[np.isinf(NCC)]=1.
        print(NCC.max(),NCC.min(),NCC.mean())
        (vmin,vmax)=np.percentile(NCC,prcntl_pltlim)
        
        plt.imshow(NCC,vmin=vmin,vmax=vmax,cmap='gray')
        plt.axis('equal')
        plt.colorbar()
        plt.title(destripingStr[i]+', file='+filename[0:45])
        plt.show()
    
    
    
            
        