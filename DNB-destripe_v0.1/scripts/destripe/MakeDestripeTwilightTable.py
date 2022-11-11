# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:04:11 2015

Make DNB Twilight Tables based on a given period from a given day using the 
function DNBdstrp.HistEqMkTblTwlghtPeriod.py. Tables for day and night are also 
needed for any parts of granule outside twilight. For this to work for a given 
granule, both the SVDNB*.h5 file and the GDNBO*.h5 file for that granule must 
exist in the directory specified. The function does test the granule using the 
geolocation data to determine if the file is in one of the twilight zones. 

examples of valid line command calls:
>MakeDestripeTwilightTable.py l:/NPP_data/ 20140922 t0000000_e1020000
>MakeDestripeTwilightTable.py l:/NPP_data/ 20140922 t0000000_e1020000 nhist=8

@author: Stephen Mills
copyright 2015, Renaissance Man Engineering, all rights reserved

"""
import DNBdstrp
import sys
# line command parameters
narg=len(sys.argv)
pathgen=sys.argv[1]# the general directory path, e.g. L:\NPP_data\
datestr=sys.argv[2]# e.g. for Sept. 22, 2014 enter 20140922
time_from_to=sys.argv[3]# same format as time spans in file names, e.g. 
                  # t2310231_e2345388 for the period 23:10:23.1 to 23:45:38.8
# path to hdf files
pathhdf=pathgen+datestr+'/hdf/'
# path to table files
pathdat=pathgen+'destripe_tables/'

# get a list of all files within the time range
t_fromtostr='_d'+datestr+'_'+time_from_to
#defaults
nhist=6
name_extnd=''

# additonal line command parameters can be added to override the default 
#parameters above, e.g. nhist=4 (no spaces are allowed in expression)
for iarg in range(4,narg):
    print(sys.argv[iarg])
    exec(sys.argv[iarg])

TwilightTable=pathdat+'destripingTable_twilight'+t_fromtostr+'_'+str(nhist)+name_extnd+'.pkl'

D=DNBdstrp.HistEqMkTblTwlghtPeriod(pathhdf,nhist,t_fromtostr,
                                   saveTable=TwilightTable)