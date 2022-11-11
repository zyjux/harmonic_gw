# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:27:44 2015
Plot striped and destriped DNB SDRs in a period

@author: Stephen Mills
copyright 2015, Renaissance Man Engineering, all rights reserved
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import granulemodVIIRS as grnV
import granulemod as grn

# line command parameters
narg=len(sys.argv)
pathgen=sys.argv[1]# the general directory path, e.g. L:\NPP_data\
datestr=sys.argv[2]# e.g. for Sept. 22, 2014 enter 20140922
time_from_to=sys.argv[3]# same format as time spans in file names, e.g. 
                  # t2310231_ 2345388 for the period 23:10:23.1 to 23:45:38.8
# path to hdf files
pathhdf=pathgen+datestr+'/hdf/'
# get a list of all files within the time range
t_fromtostr='_d'+datestr+'_'+time_from_to


#default parameters
prcntl_pltlim=[2,98]
name_extnd=''
# additonal line command parameters can be added to modify the default 
#parameters above, e.g. name_extnd='abc' (no spaces are allowed in expression)
narg=len(sys.argv)
for iarg in range(4,narg):
    print(sys.argv[iarg])
    exec(sys.argv[iarg])
    

[time_list,file_list]=grn.granulefile_list_sort_pare(pathhdf,'SVDNB','h5',t_fromtostr)
dataset_names=['Radiance'+name_extnd]
if int(input('destriped? (0=no, 1=yes)'))==1:
    dataset_names.append('Radiance_destriped'+name_extnd)
print(dataset_names)
for filenm in file_list:
    for datasetnm in dataset_names:
        L=grnV.get_radiance(pathhdf,filenm,'DNB',datasetnm=datasetnm)
        (vmin,vmax)=np.percentile(L,prcntl_pltlim)
        plt.imshow(L,vmin=vmin,vmax=vmax,cmap='gray')
        plt.axis('equal')
        plt.colorbar()
        str_title=datasetnm+' '+filenm[0:50]
        plt.title(str_title)
        plt.show()                                             