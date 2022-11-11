# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:04:11 2015

Apply Destriping tables to a twilight granule period using the function 
DNBdstrp.HistEqApplyTblTwilightPeriod.py. Tables for day and night are also 
needed for any parts of granule outside twilight. For this to work for a given 
granule, both the SVDNB*.h5 file and the GDNBO*.h5 file for that granule must 
exist in the directory specified. The function does test the granule using the 
geolocation data to determine if the file is in one of the twilight zones. 

sample line command:
>ApplyDestripeTwilightTable.py l:/NPP_data/ 20140922 t0012543_e0024145 new 20140922 t0132334_e0149370_6 t0000000_e1020000_6 t1027243_e1118358_6

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
illumination=sys.argv[4]
datetbl=sys.argv[5] # this assumes that all the tables are from the same date
NightTableID=sys.argv[6]
TwilightTableID=sys.argv[7]
DayTableID=sys.argv[8]

# path to hdf files
pathhdf=pathgen+datestr+'/hdf/'
# get a list of all files within the time range
t_fromtostr='_d'+datestr+'_'+time_from_to

# path to data files
pathtbl=pathgen+'destripe_tables/'

#Table Names
TwilightTable=pathtbl+'destripingTable_twilight_d'+datetbl+'_'+TwilightTableID+'.pkl'
NightTable=pathtbl+'destripingTable_'+illumination+'_d'+datetbl+'_'+NightTableID+'.pkl'
DayTable=pathtbl+'destripingTable_day_d'+datetbl+'_'+DayTableID+'.pkl'
print(TwilightTable)
print(NightTable)
print(DayTable)
DNBdstrp.HistEqApplyTblTwilightPeriod(pathhdf,t_fromtostr,DayTable,
                                     TwilightTable,NightTable)