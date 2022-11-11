# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:27:44 2015
Test of the destriping function DNBdstrp.HistEqPeriodToPeriod

@author: Stephen Mills
copyright 2015, Renaissance Man Engineering, all rights reserved

"""
import sys
import DNBdstrp
import numpy as np
import matplotlib.pyplot as plt
import granulemodVIIRS as grnV

"""
examples of valid line command calls:
>DNBdestripeTestPerPeriod.py l:/NPP_data/ 20140922 t0115285_e0155168 new Lhi=2.e-9
>DNBdestripeTestPerPeriod.py l:/NPP_data/ 20140922 t0115285_e0155168 new prcntl_pltlim=[5,95]
>DNBdestripeTestPerPeriod.py l:/NPP_data/ 20141007 t1659160_e1704564 full prcntl_pltlim=[5,99.5] Lhi=8.e-8 Loffref=2.e-9

example with two time periods
>DNBdestripeTestPerGranule.py l:/NPP_data/ 20140922 t0115285_e0155168 new Lhi=2.e-9 datestr2=20140909 time_from_to2=t0018299_e0058182

"""
# line command parameters
narg=len(sys.argv)
pathgen=sys.argv[1]# the general directory path, e.g. L:\NPP_data\
datestr1=sys.argv[2]# e.g. for Sept. 22, 2014 enter 20140922
time_from_to1=sys.argv[3]# same format as time spans in file names, e.g. 
                  # t2310231_e2345388 for the period 23:10:23.1 to 23:45:38.8
illumination=sys.argv[4]#  may be day, full, quarter or new (for lunar phase) 
# path to hdf files
pathhdf1=pathgen+datestr1+'/hdf/'
pathtbl=pathgen+'destripe_tables/'
# get a list of all files within the time range
t_fromtostr1='_d'+datestr1+'_'+time_from_to1

prcntl_pltlim=[2,98]
#default parameters
uniformity=.5
nhist=6
excldZones=[]
# day
if illumination[0]=='d':
    del_lo=1.e-4
    Lhi=1.e-1
    Llo=1.e-4
    Loffref=2.e-4
#full moon
elif illumination[0]=='f':
    del_lo=1.e-10
    Lhi=1e-7
    Llo=1.e-10
    Loffref=1.e-9
#quarter moon
elif illumination[0]=='q':
    del_lo=1.e-10
    Lhi=1e-8
    Llo=-2.e-10
    Loffref=del_lo
# new moon or no moon
elif illumination[0]=='n':
    del_lo=1.e-10
    Lhi=3.e-9
    Llo=-2.e-10
    Loffref=del_lo
    excldZones=np.arange(16,64-16,dtype=int)    
else:
    print(illumination+' is not a valid illumination value')

plots=True
datestr2=datestr1# assumes table applied to the same date
time_from_to2=time_from_to1 # assumes table applied to the same time period
name_extnd=''

# additonal line command parameters can be added to modify the default 
#parameters above, e.g. Llo=-1e-10 (no spaces are allowed in expression)
narg=len(sys.argv)
for iarg in range(5,narg):
    print(sys.argv[iarg])
    exec(sys.argv[iarg])
    
pathhdf2=pathgen+datestr2+'/hdf/'
t_fromtostr2='_d'+datestr2+'_'+time_from_to2
saveTable=pathtbl+'destripingTable_'+illumination+t_fromtostr1+'_'+str(nhist)+name_extnd+'.pkl'
# Run the destriping routine
Dout=DNBdstrp.HistEqPeriodToPeriod(pathhdf1,t_fromtostr1,pathhdf2,
                    t_fromtostr2,nhist,uniformity=uniformity,del_lo=del_lo,
                    Lhi=Lhi,Llo=Llo,Loffref=Loffref,saveTable=saveTable,
                    name_extnd=name_extnd,excldZones=excldZones)
file_list=Dout[6]
if plots:
    for filenm in file_list:
        for datasetnm in ['Radiance','Radiance_destriped']:
            L=grnV.get_radiance(pathhdf2,filenm,'DNB',datasetnm=datasetnm)
            (vmin,vmax)=np.percentile(L,prcntl_pltlim)
            plt.imshow(L,vmin=vmin,vmax=vmax,cmap='gray')
            plt.axis('equal')
            plt.colorbar()
            str_title=datasetnm+' '+filenm[0:50]
            plt.title(str_title)
            plt.show()                                             