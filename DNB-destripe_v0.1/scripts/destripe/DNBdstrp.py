# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:34:16 2014

DNB destriping functions that use the histogram equalization method

@author: Stephen Mills
copyright 2015, Renaissance Man Engineering, all rights reserved
"""
import granulemod as grn
import granulemodVIIRS as grnV
import pickler
import numpy as np
import scipy.interpolate as intrplt
import DNBcal
import os
ndet=16
Nshort=16
fillshort=-999.8
fillskipscan=-999.2
t_scan_period=1779268.75
SDRname='VIIRS-DNB-SDR'
DatasetGrp='/All_Data/'+SDRname+'_All/'
suffix='h5'
prefix='SVDNB'
prefix2='IVOBC'
# information identifying the OBC data files
DatasetGrp2='/All_Data/VIIRS-OBC-IP_All/'


"""
_____________________________________________________________________
                 DNB Histogram Equalization Functions
_____________________________________________________________________
"""    
def DNBCumHist(L,nhist,del_lo=1.e-10, uniformity=.5, Lhi=1.e-1, Llo=1.e-11,
               Loffref=0.0,mask=None,excldZones=[]):
    """
    Purpose: The Histogram equalization method assumes that the true radiance 
       histograms taken over a very large ensemble of values are the same shape
       for all detectors, so any differences must be due to calibration errors
       and uncorrected nonlinearities. This method takes histograms of each 
       individual detector and compares it with the histogram of the combined 
       ensemble of all detectors. This routine produces a cumulative histogram 
       of each detector for each aggregation zone, and also a cumulative 
       histogram of the combined ensemble of all detectors. 
       
       But before producing the ensemble, the data is filtered for non-uniform-
       ities because stong nonuniformities cause crosstalk which can 
       contaminate the ensemble. Also, since striping is only apparent for 
       relatively uniform scenes, uniformity filtering selects the parts of the
       scenes where striping is most evident.
       
       The cumulative histograms that are produced are actualkly inverse 
       histograms because the output is radiance as a function of cumulative 
       fraction. The ensemble is divided into a set number of steps given by 
       nhist, and the output is the radiance values at each step.
    Inputs:
    L - Rance matrix for which the 
    nhist - the number of histogram levels. (integer)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
             radiance resulting from uniformity test is lest than this then it 
             passes regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    mask - This optional mask must be the same size as L, and flags which array
           elements to process. This mask is used to select by geolocation 
           values, especially solar or lunar solar zenith angle. If  equal to 
           None, then it does not mask any elements of L. (numpy bool array)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)
    
    Outputs:
    Lhistcum - Cumulative histogram radiance array gives the radiance value of 
            the cumulative histogram and is taken over an ensemble of data 
            per detector, per aggregation zone, per histogram level. Its size 
            is [ndet,Nagg,nhist], where ndet is the number of detectors, 16, 
            Nagg is the number of aggregation zones, 64, and nhist is the 
            input value giving the number of histogram levels (numpy)
    Lhistall- Combined cumulative histogram radiance array gives the radiance 
              value of the cumulative histogram taken over the combined 
              ensemble of all detectors per aggregation zone (Agg. Zone) per 
              histogram level.  
    Loff - Radiance offset determined at the Loffref value for each detector 
           and aggregation zone. Its size is [ndet,Nagg] (numpy float array)
    ExcldZones - Aggregation Zones excluded from destriping correction tables. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy integer 1-D integer array)

    """
    # the number of samples for each agg zone by reflecting
    nsampagg=DNBcal.EV_agg_samples()    
    # number of agg zones across swath from agg seq. array
    nagg=len(nsampagg) 
    # get the absolute radiance difference from one scan to the next
    dL=np.abs(L[ndet:,:]-L[:-ndet,:])
    # get the mean radiance for the same detectors from one scan to next
    mnL=(L[ndet:,:]+L[:-ndet,:])*.5
    shp=mnL.shape
    #------------- Logic tests for uniformity matrix ----------
    nscans=int(shp[0]/ndet)
    if mask!=None:
        dmask=np.logical_and(mask[ndet:,:],mask[:-ndet,:])
        if np.all(dmask.shape!=shp):
            print('Mask size, ', dmask.shape, ' does not match data size',shp)
            return None
                        
    else:
        dmask=np.ones(shp,bool)
        
    for j in range(0,nscans):
        k=j*ndet            
        mnLdet=mnL[k:k+ndet,:].mean(axis=0)
        inrng=np.logical_and(mnLdet<Lhi,mnLdet>=Llo)
        for n in range(0,ndet):  
           dmask[k:k+ndet,:]=inrng
    # is the difference less than threshold or fractional uniformity?
    unif_thresh=np.logical_or(dL<del_lo,dL<uniformity*mnL)
    dmask=np.logical_and(dmask,unif_thresh)   
    # is value is real , noninfinite number?        
    dmask=np.logical_and(dmask,~np.isnan(mnL),~np.isinf(mnL))
        
    # first in-scan pixel of agg zone (skip first pixel which is corrupted)
    Lhistcum=np.zeros([ndet,nagg,nhist]) 
    Lhistcumall=np.zeros([nagg,nhist])
    Loff=np.zeros([ndet,nagg])
    nfirst=1
    # loop through aggregtion zones
    ExcldZones=np.array(excldZones)
    for j in range(0,nagg):
        print("Aggregate zone: {}/{}".format(j,nagg))
        if  np.any(j==ExcldZones):
            continue
        Lpassall=np.array([])
        LpasssortHold=[]
        nend=sum(nsampagg[0:j+1])
        for i in range(0,ndet):
            print("\tDetector: {}/{}".format(i,ndet))
            Lpass=np.array([])
            for l in range(0,nscans):
                print("\t\tScan: {}/{}".format(l,nscans))
                k=l*ndet            
                print("\t\tk: {}".format(k))
                mnLdet=mnL[k+i,nfirst:nend]
                dmaskdet=dmask[k+i,nfirst:nend]
                # set last pixel in aggregation zone
                Lsub=mnLdet[dmaskdet]
                Lpass=np.append(Lpass,Lsub)
                Lpassall=np.append(Lpassall,Lsub)
            Lpasssort=np.sort(Lpass)
            LpasssortHold.append(Lpasssort)
            nstep=int(len(Lpass)/nhist)            
            print("\tLpass {}".format(Lpass))
            print("\tnhist: {} nstep: {}".format(nhist,nstep))
            Lhistcum[i,j,:]=Lpasssort[:nstep*nhist:nstep]
            # print("\tLhistcum[{}][{}][:]: {}".format(i,j,Lhistcum[i,j,:]))
        nfirst=nend
        Lpassallsort=np.sort(Lpassall)
        npassall=len(Lpassall)
        nstep=int(npassall/nhist)
        nzeroall=np.argmin(np.abs(Lpassallsort-Loffref))
        for i in range(0,ndet):
            nl=len(LpasssortHold[i])
            nzero=int(nzeroall*nl/npassall-1)
            if nzero<0:
                nzero=0
            Loff[i,j]=LpasssortHold[i][nzero]-Loffref
        Lhistcumall[j,:]=Lpassallsort[:nstep*nhist:nstep]
    return(Lhistcum,Lhistcumall,Loff,ExcldZones)
    
def HistEqPerGrn(pathhdf,filename,nhist,apply=True,addfield=True,
                         del_lo=1.e-10,uniformity=.5,Lhi=1.e-1, Llo=1.e-11,
                         Loffref=0.,name_extnd='',saveTable='',
                         remakeTable=False,excldZones=[]):
    """
    Purpose: This routine creates tables for destriping DNB radiances 
    using the histogram equalization method. It takes a single DNB HDF5 
    radiance file and produces a set of tables output as numpy arrays. These 
    tables are applied to the radiances in the granule to produce destriped 
    radiances. There is an option to add a field to the HDF5 file with the 
    destriped radiances. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    filename - full name of the DNB HDF5 file with radiance being processed 
               (string)
    nhist - the number of histogram levels. (integer)
    apply -  This enables the option to apply the corrections defined by the 
             created destriping tables to the radiance. If this is False, only 
             the tables are output, if True the radiance is also output. (bool)
    addField - If True, a field will be added to HDF5 file called 
               'Radiance_destriped' if it does not already exist or to revise 
               it if it does exist. Default is True. If addField is True and 
               apply is False, then addField has no effect.(bool)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
             radiance resulting from uniformity test is lest than this then it 
             passes regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs.(string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)

    Output:
    gain - This array gives the gains for each histogram level for each 
            aggregation zone for each detector. Its size is 
            [ndet,Nagg,nhist-1], where ndet is the number of detectors, 16, and
            Nagg is the number of aggregation zones, 64. The reason that it is 
            nhist-1 is because the first histogram level is always dropped. 
            (numpy array)
    Loff - Radiance offset determined at the Loffref value for each detector 
           and aggregation zone. Its size is [ndet,Nagg] (numpy array)
    Lhist - Cumulative histogram radiance array gives the radiance value of 
            the cumulative histogram per detector, per aggregation zone, per 
            histogram level. Its size is [ndet,Nagg,nhist-1]. (numpy)
    ExcldZones - Aggregation Zones excluded in destriping correction tables. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)
    Lc - If apply==True the corrected radiances are output      

    """
    if not remakeTable and os.path.exists(saveTable):
        (gain,Loff,Lhist,ExcldZones)=pickler.import_pickle(saveTable)
    else:
        (gain,Loff,Lhist,ExcldZones)=HistEqMakeTable(pathhdf,[filename],nhist,
                    del_lo=del_lo,uniformity=uniformity,Lhi=Lhi, Llo=Llo,
                    Loffref=Loffref,excldZones=excldZones)    

    datasetnm_out='Radiance_destriped'+name_extnd
    Loffall=Loff.mean(axis=0)
    Nagg=Lhist.shape[1]
    if apply:
        L=grnV.get_radiance(pathhdf,filename,'DNB')
        shp=L.shape
        Lc=np.zeros(shp)
        Nscan=int(shp[0]/ndet)
        for n in range(0,Nscan):
            for i in range(0,ndet):
                k=n*ndet+i
                for iagg in range(0,Nagg):
                    (ifrm,ito)=DNBcal.EV_agg_samp_accum(iagg)
                    Lsamp=L[k,ifrm:ito]
                    Lsamp-=Loff[i,iagg]
                    gainsamp=np.interp(Lsamp,Lhist[i,iagg,:],gain[i,iagg,:])
                    Lc[k,ifrm:ito]=Lsamp/gainsamp+Loffall[iagg]
 
    if apply and addfield:
        grnV.add_EV_field(pathhdf,filename,DatasetGrp,datasetnm_out,Lc,'DNB')
    if saveTable!='':
        pickler.export_pickle((gain,Loff,Lhist,excldZones),saveTable)
    if apply:
        return (gain,Loff,Lhist,ExcldZones,Lc)
    else:
        return (gain,Loff,Lhist,ExcldZones)
        
def HistEqFrmTable(pathhdf,t_fromtostr,pathdat,tablename,name_extnd=''):
    """
    Purpose: This routine uses tables for destriping DNB radiances 
    using the histogram equalization method. The tables are applied to destripe
    DNB HDF5 radiance files within a given time range.
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 files resides 
              (string)
    pathdat - Path to the directory containing the file with the destriping 
    correction tables. (string)
    tablename - filename containing the correction tables to be used.
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    
    Output:
    list_files - List of files which have been processed for corrections 
                 (string list)
    """
    (grantimes_out,list_files)=grn.granulefile_list_sort_pare(pathhdf,prefix,
                                    'h5',t_fromtostr)
    D=pickler.import_pickle(pathdat+tablename)
    (gain,Loff,Lhist)=D[0:3]
    excldZones=D[3]
    for filename in list_files:
        HistEqApplyTable(pathhdf,filename,gain,Loff,Lhist,
                                 addfield=True,name_extnd=name_extnd,
                                 excldZones=excldZones)
    return list_files                
        
def HistEqMakeTable(pathhdf,FileList,nhist,del_lo=1.e-10,
                         uniformity=.5,Lhi=1.e-1, Llo=1.e-11,Loffref=0.,
                         saveTable='',remakeTable=False,excldZones=[]):
    """
    Purpose: This routine creates tables for destriping DNB radiances 
    using the histogram equalization method. It takes a single DNB HDF5 
    radiance file and produces a set of tables output as numpy arrays.
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    FileList - list with full name of the DNB HDF5 file with radiance being 
                  processed (string list)
    nhist - the number of histogram levels. (integer)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
             radiance resulting from uniformity test is lest than this then it  
             pases regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs.(string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    Output:
    gain - This array gives the gains for each histogram level for each 
            aggregation zone for each detector. Its size is 
            [ndet,Nagg,nhist-1], where ndet is the number of detectors, 16, and
            Nagg is the number of aggregation zones, 64. The reason that it is 
            nhist-1 is because the first histogram level is always dropped. 
            (numpy array)
    Loff - Radiance offset determined at the Loffref value for each detector 
           and aggregation zone. Its size is [ndet,Nagg] (numpy array)
    Lhist - Cumulative histogram radiance array gives the radiance value of 
            the cumulative histogram per detector, per aggregation zone, per 
            histogram level. Its size is [ndet,Nagg,nhist-1]. (numpy)
    ExcldZones - Aggregation Zones excluded from destriping correction tables. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy integer 1-D integer array)
    """
    if not remakeTable and os.path.exists(saveTable):
        (gain,Loff,Lhist,ExcldZones)=pickler.import_pickle(saveTable)
        return (gain,Loff,Lhist,ExcldZones)

    L=None
    for filename in FileList:
        Lv=grnV.get_radiance(pathhdf,filename,'DNB')
        print(filename)
        if L==None:
            L=Lv
        else:
            L=np.append(L,Lv,axis=0)
    D=DNBCumHist(L,nhist,del_lo,uniformity,Lhi,Llo,Loffref,excldZones=excldZones)
    print('DNBCumHist complete')    
    Loff=D[2]
    Loffall=Loff.mean(axis=0)
    Lhist=D[0]
    Nagg=Lhist.shape[1]
    Lhistall=D[1]
    gain=np.ones([ndet,Nagg,nhist-1])
    # loop through aggregation zones
    ExcldZones=D[3]    
    for iagg in range(0,Nagg):
        if  np.any(iagg==ExcldZones):
            continue
        Lhisti=Lhist[:,iagg,:]
        Lhistalli=Lhistall[iagg,:]
        Lhistalli-=Loffall[iagg]
        for i in range(0,ndet):
            Lhisti[i,:]-=Loff[i,iagg]
            gain[i,iagg,:]=Lhisti[i,1:]/Lhistalli[1:]
    gain[gain<=0.]=1.
    Lhist=Lhist[:,:,1:]
    if saveTable!='':
            pickler.export_pickle((gain,Loff,Lhist,ExcldZones),saveTable)
    return (gain,Loff,Lhist,ExcldZones)
    
def HistEqPerGrnInPeriod(pathhdf,t_fromtostr,nhist,del_lo=1e-10,
                         uniformity=.5,Lhi=1.e-1, Llo=1.e-11,Loffref=0.,
                         name_extnd='',excldZones=[]):
    """
    Purpose: This routine creates tables for destriping DNB radiances 
    using the histogram equalization method. For granules within a given time 
    period each DNB HDF5 radiance file is used to produce stripping corrections
    to produce destriped radiances, and a field is added or revised with 
    corrected radiances in each HDF5 file. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    t_fromtostr - Time period over which files used in performing corrections 
             are performed. String using the same format as used in the file 
             naming convention in order to describe a period of time within a 
             one day period for determining the tables used for destriping. The 
             convention is _dYYYYMMDD_tHHmmSSS_eHHmmSSS. Here YYYYMMDD gives 
             the year, month and day, and HHmmSSS gives UTC time in hours, 
             minutes and seconds down to a tenth of a second. the part after 
             '_t' indicates the start time and '_e' indicates the end time, 
             e.g. _d20140922_t2310231_e2345388 is on Sept. 09, 2014 for the 
             period 23:10:23.1 to 23:45:38.8 UTC.  
    nhist - the number of histogram levels. (integer)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
             radiance resulting from uniformity test is lest than this then it 
             passes regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)
          
    Output:
    list_files - List of files which have been processed for corrections 
                 (string list)

    """
    (grantimes_out,list_files)=grn.granulefile_list_sort_pare(pathhdf,prefix,
                                    'h5',t_fromtostr)
    for filename in list_files:
        HistEqPerGrn(pathhdf,filename,nhist,addfield=True,
                             del_lo=del_lo,uniformity=uniformity,Lhi=Lhi,
                             Llo=Llo,Loffref=Loffref,name_extnd=name_extnd,
                             excldZones=excldZones)
    return list_files

def HistEqGrnToGrn(pathhdfIn,filenameIn,pathhdfOut,filenameOut,nhist,
                           addfield=True,del_lo=1.e-10,uniformity=.5,
                           Lhi=1.e-1, Llo=1.e-11,Loffref=0.,name_extnd='',
                           saveTable='',remakeTable=False,excldZones=[]):
    """
    Purpose: This routine creates tables for destriping DNB radiances 
    using the histogram equalization method. It takes a single DNB HDF5 
    radiance file and produces a set of tables output as numpy arrays. These 
    tables are applied to the radiances in another granule to produce destriped 
    radiances. There is an option to add a field to the HDF5 file with the 
    destriped radiances. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    filename - full name of the DNB HDF5 file with radiance being processed 
               (string)
    nhist - the number of histogram levels. (integer)
    addField - If True, a field will be added to HDF5 file called 
               'Radiance_destriped' if it does not already exist or to revise 
               it if it does exist. Default is True. If addField is True and 
               apply is False, then addField has no effect.(bool)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
      radiance resulting from uniformity test is lest than this then it passes 
      regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs.(string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)

    Output:
    Lc - Corrected DNB radiance (numpy2-D array) 
    """
    (gain,Loff,Lhist,ExldZones)=HistEqPerGrn(pathhdfIn,filenameIn,nhist,
                apply=False,addfield=False,del_lo=del_lo,uniformity=uniformity,
                Lhi=Lhi,Llo=Llo,Loffref=Loffref,saveTable=saveTable,
                remakeTable=remakeTable,excldZones=excldZones)
    Lc=HistEqApplyTable(pathhdfOut,filenameOut,gain,Loff,Lhist,
                                addfield=addfield,name_extnd=name_extnd,
                                excldZones=excldZones)
    return Lc

def HistEqGrpToGrp(pathhdfIn,FileListIn,pathhdfOut,FileListOut,nhist,
                           del_lo=1.e-10,uniformity=.5,Lhi=1.e-1, Llo=1.e-11,
                           Loffref=0.,name_extnd='',saveTable='',remakeTable=False,
                           excldZones=[]):
    """
    Purpose: This routine creates tables for destriping DNB radiances 
    using the histogram equalization method. It takes a list of DNB HDF5 
    radiance files and from this ensemble produces a set of tables output as 
    numpy arrays. These tables are applied to another list of DNB HDF5 
    radiance files to produce destriped radiances, and a field is added or 
    revised in each output file to the HDF5 file giving destriped radiances. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    FileListIn - list with full name of the DNB HDF5 file with radiance being 
                  processed to produce correction tables. (string list)
    FileListOut - list with full name of the DNB HDF5 file with radiance being 
                  corrected for striping. (string list)
    nhist - the number of histogram levels. (integer)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
             radiance resulting from uniformity test is lest than this then it  
             passes regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs.(string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)

    Output:
    gain - This array gives the gains for each histogram level for each 
            aggregation zone for each detector. Its size is 
            [ndet,Nagg,nhist-1], where ndet is the number of detectors, 16, and
            Nagg is the number of aggregation zones, 64. The reason that it is 
            nhist-1 is because the first histogram level is always dropped. 
            (numpy array)
    Loff - Radiance offset determined at the Loffref value for each detector 
           and aggregation zone. Its size is [ndet,Nagg] (numpy array)
    Lhist - Cumulative histogram radiance array gives the radiance value of 
            the cumulative histogram per detector, per aggregation zone, per 
            histogram level. Its size is [ndet,Nagg,nhist-1]. (numpy)
    ExcldZones - Aggregation Zones that are excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy 1-D integer array)
    Lout- merged DNB radiance data used for producing the correction tables. 
          (numpy 2-D array) 

    """
    (gain,Loff,Lhist,ExcldZones)=HistEqMakeTable(pathhdfIn,FileListIn,nhist,
                    del_lo=del_lo,uniformity=uniformity,Lhi=Lhi, Llo=Llo,
                    Loffref=Loffref,saveTable=saveTable,
                    remakeTable=remakeTable,excldZones=excldZones)    
    Lout=[]    
    for filenameOut in FileListOut:
        print(filenameOut)
        Lc=HistEqApplyTable(pathhdfOut,filenameOut,gain,Loff,Lhist,
                                    name_extnd=name_extnd,excldZones=excldZones)
        Lout.append(Lc)    
    return (gain,Loff,Lhist,ExcldZones,Lout)

def HistEqPeriodToPeriod(pathhdfIn,filePrdIn,pathhdfOut,filePrdOut,
                        nhist,del_lo=1.e-10,uniformity=.5,Lhi=1.e-1, 
                        Llo=1.e-11,Loffref=0.,name_extnd='',saveTable='',
                        remakeTable=False,excldZones=[]):
    """
    Purpose: This routine creates tables for destriping DNB radiances 
    using the histogram equalization method. It takes a period of time and all 
    DNB HDF5 radiance files falling within that time period are used to produce
    a set of tables output as numpy arrays. These tables are applied to another 
    set of DNB HDF5 radiance files from another time period to produce 
    destriped radiances, and a field is added or revised in each output file 
    to the HDF5 file giving destriped radiances. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    filePrdIn - Time period over which files used for creating corrections are 
             taken. String using the same format as used in the file naming 
             convention in order to describe a period of time within a one day 
             period for determining the tables used for destriping. The 
             convention is _dYYYYMMDD_tHHmmSSS_eHHmmSSS. Here YYYYMMDD gives 
             the year, month and day, and HHmmSSS gives UTC time in hours, 
             minutes and seconds down to a tenth of a second. the part after 
             '_t' indicates the start time and '_e' indicates the end time, 
             e.g. _d20140922_t2310231_e2345388 is on Sept. 09, 2014 for the 
             period 23:10:23.1 to 23:45:38.8 UTC.  
    filePrdOut - Time period over which files used for creating corrections are 
             made. String using the same format as filePrdIn described above. 
             The time period in and time period out may overlap or may be 
             entirely the same.
    nhist - the number of histogram levels. (integer)
    del_lo - low delta radiance used in uniformity test. If the absolute delta 
             radiance resulting from uniformity test is lest than this then it 
             passes regardless of relative uniformity. (float)
    uniformity - relative uniformity threshhold. If the ratio of delta radiance
            to the mean radiance is less than this, then it is considered 
            uniform and is used for producing histograms. (float)
    Lhi - high radiance limit used for excluding high radiances that are 
           outside the normal range (float)
    Llo -  low radiance limit used for excluding low radiances that are 
           outside the normal range (float)
    Loffref - This is used for determining the radiance offset. The default is 
              zero, but for radiance distributions that do not extend to zero 
              such as full day or twilight or where the entire nightime has 
              strong lunar illumination, there are no radiances near zero, 
              so a low-radiance reference is used for finding offset.(float)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file. (string)
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs. (string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (integer list)
           
    Output:
    gain - This array gives the gains for each histogram level for each 
            aggregation zone for each detector. Its size is 
            [ndet,Nagg,nhist-1], where ndet is the number of detectors, 16, and
            Nagg is the number of aggregation zones, 64. The reason that it is 
            nhist-1 is because the first histogram level is always dropped. 
            (numpy array)
    Loff - Radiance offset determined at the Loffref value for each detector 
           and aggregation zone. Its size is [ndet,Nagg] (numpy array)
    Lhist - Cumulative histogram radiance array gives the radiance value of 
            the cumulative histogram per detector, per aggregation zone, per 
            histogram level. Its size is [ndet,Nagg,nhist-1]. (numpy)
    ExcldZones - Aggregation Zones excluded from destriping correction tables. 
       Zones are numbered from 0 to 63, starting at beginning of scan. 
       (numpy integer 1-D array)
    Lout- merged radiance data used for producing the correction tables. (numpy
          2-D array)
    FileListIn - File names of files that were used to create tables
    FileListOut - File names of files for which tables are applied

    """
    (grantimesIn,FileListIn)=grn.granulefile_list_sort_pare(pathhdfIn,prefix,
                                    'h5',filePrdIn)
    (grantimesOut,FileListOut)=grn.granulefile_list_sort_pare(pathhdfOut,prefix,
                                    'h5',filePrdOut)

    Dout=HistEqGrpToGrp(pathhdfIn,FileListIn,pathhdfOut,FileListOut,
                                nhist,del_lo=del_lo,uniformity=uniformity,
                                Lhi=Lhi, Llo=Llo,Loffref=Loffref,
                                name_extnd=name_extnd,excldZones=excldZones,
                                saveTable=saveTable,remakeTable=remakeTable)
    (gain,Loff,Lhist,ExcldZones,Lout)=Dout    
    return (gain,Loff,Lhist,ExcldZones,Lout,FileListIn,FileListOut)

def HistEqApplyTable(pathhdf,filename,gain,Loff,Lhist,addfield=True,
                             name_extnd='',excldZones=[]):
    """
    Purpose: This routine uses tables for destriping DNB radiances 
    using the histogram equalization method. The tables are applied to destripe
    a DNB HDF5 radiance file. There is an option to add a field to the HDF5 
    file with the destriped radiances.
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 files resides 
              (string)

    filename - full name of the DNB HDF5 file with radiance being processed 
               (string)
    gain - This array gives the gains for each histogram level for each 
            aggregation zone for each detector. Its size is 
            [ndet,Nagg,nhist-1] (numpy array)
    Loff - Radiance offset determined at the Loffref value for each detector 
           and aggregation zone. Its size is [ndet,Nagg] (numpy array)
    Lhist - Cumulative histogram radiance array gives the radiance value of 
            the cumulative histogram per detector, per aggregation zone, per 
            histogram level. Its size is [ndet,Nagg,nhist-1]. (numpy)
    addfield - If True, a field will be added to HDF5 file called 
               'Radiance_destriped' if it does not already exist or to revise 
               it if it does exist. Default is True.(bool)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (integer list)
    
    Output:
    Lc - Corrected radiance. (numpy 2-D array)
    """
    datasetnm_out='Radiance_destriped'+name_extnd
    L=grnV.get_radiance(pathhdf,filename,'DNB')
    shp=L.shape
    Lc=np.zeros(shp)
    Nscan=int(shp[0]/ndet)
    Nagg=gain.shape[1]
    Loffall=Loff.mean(axis=0)
    # loop through aggregtion zones
    ExcldZones=np.array(excldZones)
    for n in range(0,Nscan):
        for i in range(0,ndet):
            k=n*ndet+i
            for iagg in range(0,Nagg):
                (ifrm,ito)=DNBcal.EV_agg_samp_accum(iagg)
                Lsamp=L[k,ifrm:ito]
                Lsamp-=Loff[i,iagg]
                gainsamp=np.interp(Lsamp,Lhist[i,iagg,:],gain[i,iagg,:])
                if  np.any(iagg==ExcldZones):
                    Lc[k,ifrm:ito]=Lsamp
                else:
                    Lc[k,ifrm:ito]=Lsamp/gainsamp+Loffall[iagg]
    if addfield:
        grnV.add_EV_field(pathhdf,filename,DatasetGrp,datasetnm_out,Lc,'DNB')
    return Lc

def HistEqMkTblTwilight(pathhdf,RdncFileList,GeoFileList,nhist,
                    SolZen=[84.,87.,90.,93.,96.,99.],del_lo=None,
                    uniformity=[.5,.5,.5,.5,.5],
                    Lhi=[1.e-3,1.e-3,3.e-4,1.e-4,3.e-5],Llo=None,Loffref=None,
                    saveTable='',remakeTable=False,excldZones=[]):
    """
    Purpose: This routine creates tables for destriping twilight DNB radiances 
    using the histogram equalization method. It takes a list of DNB HDF5 
    radiance files matched with a corresponding list of geolocation files and 
    produces a set of tables output as numpy arrays for each twilight zone 
    defined by solar zenith angle limits. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    RdncFileList - list with full name of the DNB HDF5 file with radiance being 
                  processed (string list)
    GeoFileList - list with full name of the DNB HDF5 file with geolocation 
                  being processed. These files should be matched one-to-one 
                  with the files in RdncFileList. Thes may be the same files as 
                  the radiance files if geolocation and radiance is aggregated. 
                  (string list)
    nhist - the number of histogram levels. (integer)
    SolZen - List of solar zenith limits for the twilight zones in degrees. 
             Therefore, if n is the number of zones, its length is n+1. (float 
             list)
    del_lo - list of low delta radiance for each twilight zone. See 
             documentation for DNBcumHist for how del_lo is used. If it is set 
             to None, then it is set equal to Llo. (float list)
    uniformity - list of uniformity threshhold for each twilight zone. See 
             documentation for DNBcumHist for how uniformity is used. Its 
             default is 0.15 for all zones (float list)
    Lhi - list of high radiance limit for each twilight zone. See documentation 
           for DNBcumHist for details of how Lhi is used.(float list)
    Llo - list of low radiance limit for each twilight zone. See documentation 
           for DNBcumHist for details of how Llo is used. If it is set to 
           None, then it is set equal to 0.005*Lhi.(float list)
    Loffref - list of radiances used to determine offset for each twilight 
           zone. See documentation for DNBcumHist for details of how Loffref is
           used. If it is set to None, then it is set equal to Llo.(float list)
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs.(string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (integer list)

    Output:
    gainTwi - List of cumulative histogram gain tables, with one table per
            twilight zone. Refer to HistEqMakeTable documentation for 
            details on histogram gain tables. (list of numpy arrays) 
    LoffTwi - List of cumulative histogram radiance offset tables, with one 
            table per twilight zone. See HistMakeTable documentation for 
            details on histogram radiance offset tables. (list of numpy arrays)
    LhistTwi - List of cumulative histogram radiance tables, with one 
            table per twilight zone. See HistMakeTable documentation for 
            details on histogram radiance tables. (list of numpy arrays)
    SolZen - List of solar zenith angle limits, same as input. (float list)
    ExcldZones - Aggregation Zones excluded from destriping correction tables. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy integer 1-D array)

    """
    if not remakeTable and os.path.exists(saveTable):
        (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)=pickler.import_pickle(saveTable)
        return (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)

    Lhi=np.array(Lhi)
    if Llo==None:
        Llo=Lhi*.0005
    else:
        Llo=np.array(Llo)
    Llo=np.array(Llo)
    if del_lo==None:
        del_lo=Llo
    if Loffref==None:
        Loffref=Llo
    L=None
    nfiles=len(RdncFileList)
    nSZA=len(SolZen)-1
    if nfiles!=len(GeoFileList):
        print('number of geo files do not match # of radiance files')
        return None
    
    for ifile in range(0,nfiles):
        RdncFilenm=RdncFileList[ifile]
        geofilenm=GeoFileList[ifile]
        L_=grnV.get_radiance(pathhdf,RdncFilenm,'DNB')
        SolZA_=grnV.get_geoloc(pathhdf,geofilenm,'DNB','SolarZenithAngle')
        inRng=np.logical_and(SolZA_>=SolZen[0],SolZA_<=SolZen[-1])
        if not(np.any(inRng)):
            continue
        if L_.shape!=SolZA_.shape:
            print(ifile,'Shape Mismatch',L_.shape,SolZA_.shape,RdncFilenm,geofilenm)
        if L==None:
            L=L_
            SolZA=SolZA_
        else:
            L=np.append(L,L_,axis=0)
            SolZA=np.append(SolZA,SolZA_,axis=0)
    gainTwi=[]
    LoffTwi=[]
    LhistTwi=[] 
    for iSZA in range(0,nSZA):
        print('Making Twilight Table for SZA ',SolZen[iSZA],' to ',SolZen[iSZA+1] )
        SolZAinRng=np.logical_and(SolZA>=SolZen[iSZA],SolZA<SolZen[iSZA+1])
        D=DNBCumHist(L,nhist,del_lo[iSZA],uniformity[iSZA],Lhi[iSZA],
                     Llo[[iSZA]],Loffref[iSZA],mask=SolZAinRng,excldZones=excldZones)
        Loff=D[2]
        Loffall=Loff.mean(axis=0)
        Lhist=D[0]
        ExcldZones=D[3]
        Nagg=Lhist.shape[1]
        Lhistall=D[1]
        gain=np.ones([ndet,Nagg,nhist-1])
        
        for iagg in range(0,Nagg):
            if  np.any(iagg==ExcldZones):
                continue
            Lhisti=Lhist[:,iagg,:]
            Lhistalli=Lhistall[iagg,:]
            Lhistalli-=Loffall[iagg]
            for i in range(0,ndet):
                Lhisti[i,:]-=Loff[i,iagg]
                gain[i,iagg,:]=Lhisti[i,1:]/Lhistalli[1:]
        gain[gain<=0.]=1.
        Lhist=Lhist[:,:,1:]
        gainTwi.append(gain)
        LhistTwi.append(Lhist)
        LoffTwi.append(Loff)
    if saveTable!='':
            pickler.export_pickle((gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones),
                                  saveTable)
    return (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)    
    
def HistEqMkTblTwlghtPeriod(pathhdf,nhist,t_fromtostr,
                    SolZen=[84.,87.,90.,93.,96.,99.],del_lo=None,
                    uniformity=[.5,.5,.5,.5,.5],
                    Lhi=[1.e-3,1.e-3,3.e-4,1.e-4,3.e-5],Llo=None,Loffref=None,
                    saveTable='',remakeTable=False,excldZones=[]):
    """
    Purpose: This routine creates tables for destriping twilight DNB radiances 
    using the histogram equalization method. It takes as input a timperiod in 
    order to produce a list of DNB HDF5 radiance files matched with a 
    corresponding list of geolocation files and produces a set of tables output
    as numpy arrays for each twilight zone defined by solar zenith angle limits. 
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    nhist - the number of histogram levels. (integer)
    t_fromtostr - String using the same format as used in the file naming 
             convention in order to describe a period of time within a one day 
             period for determining the tables used for destriping. The 
             convention is _dYYYYMMDD_tHHmmSSS_eHHmmSSS. Here YYYYMMDD gives 
             the year, month and day, and HHmmSSS gives UTC time in hours, 
             minutes and seconds down to a tenth of a second. the part after 
             '_t' indicates the start time and '_e' indicates the end time, 
             e.g. _d20140922_t2310231_e2345388 is on Sept. 09, 2014 for the 
             period 23:10:23.1 to 23:45:38.8 UTC.  
    SolZen - List of solar zenith limits for the twilight zones in degrees. 
             Therefore, if n is the number of zones, its length is n+1. (float 
             list)
    del_lo - list of low delta radiance for each twilight zone. See 
             documentation for DNBcumHist for how del_lo is used. If it is set 
             to None, then it is set equal to Llo. (float list)
    uniformity - list of uniformity threshhold for each twilight zone. See 
             documentation for DNBcumHist for how uniformity is used. Its 
             default is 0.15 for all zones (float list)
    Lhi - list of high radiance limit for each twilight zone. See documentation 
           for DNBcumHist for details of how Lhi is used.(float list)
    Llo - list of low radiance limit for each twilight zone. See documentation 
           for DNBcumHist for details of how Llo is used. If it is set to 
           None, then it is set equal to 0.005*Lhi.(float list)
    Loffref - list of radiances used to determine offset for each twilight 
           zone. See documentation for DNBcumHist for details of how Loffref is
           used. If it is set to None, then it is set equal to Llo.(float list)
    saveTable - If not an empty string, this gives a file path and name to save
           the outputs.(string)
    remakeTable - If the table file given in saveTable already exists, this 
          determines whether to remake the file if =True or use the existing 
          file if =False. (bool)
    excldZones - Aggregation Zones to be excluded in destriping correction. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (integer list)

    Output:
    gainTwi - List of cumulative histogram gain tables, with one table per
            twilight zone. Refer to HistEqMakeTable documentation for 
            details on histogram gain tables. (list of numpy arrays) 
    LoffTwi - List of cumulative histogram radiance offset tables, with one 
            table per twilight zone. Refer to HistEqMakeTable document-
            ation for details on histogram radiance offset tables. (list of 
            numpy arrays)
    LhistTwi - List of cumulative histogram radiance tables, with one 
            table per twilight zone. Refer to HistEqMakeTable 
            documentation for details on histogram radiance tables. (list of 
            numpy arrays)
    SolZen - List of solar zenith angle limits, same as input. (float list)
    ExcldZones - Aggregation Zones excluded from destriping correction tables. 
           Zones are numbered from 0 to 63, starting at beginning of scan. 
           (numpy integer 1-D array)

    """
    if not remakeTable and os.path.exists(saveTable):
        (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)=pickler.import_pickle(saveTable)
        return (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)
    (RdncFileList,GeoFileList)=grnV.matchRdncGeoFiles(pathhdf,t_fromtostr,'DNB')
    Dout=HistEqMkTblTwilight(pathhdf,RdncFileList,GeoFileList,nhist,
                SolZen=SolZen,del_lo=del_lo,uniformity=uniformity,Lhi=Lhi,
                Llo=Llo,Loffref=Loffref,saveTable=saveTable,remakeTable=False,
                excldZones=excldZones)  
    (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)=Dout
    return (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)
    
def HistEqApplyTblTwilight(pathhdf,RdncFilename,GeoFilename,
                                  day_tablename,twilight_tablename,
                                  night_tablename,addfield=True,name_extnd=''):
    """
    Purpose: This routine uses tables for destriping DNB radiances 
    using the histogram equalization method for twilight granules using input 
    correction tables. Since twilight granules often contain pixels in night-
    time or daytime, correction tables for these are also used. The tables 
    are applied to destripe a DNB HDF5 radiance file.
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 files resides 
              (string)
    RdncFilename - full name of the DNB HDF5 file with radiance being processed 
               (string)
    GeoFilename - full name of the DNB HDF5 file with geolocation corresponding
                to radiances being processed (string)
    day_tablename - filename with path containing the correction tables to be used 
                    for daytime, which is defined as any pixel where the solar 
                    zenith angle (SZA) is less than the minimum SZA in for the 
                    twilight zones. (string)
    twilight_tablename - filename with path containing the correction tables to  
                    be used for for twilight, which is defined as any pixel where  
                    the solar zenith angle (SZA) is within the range of twilight  
                    zones defined in the table set. (string)
    night_tablename - filename with path containing the correction tables to be  
                    used for nighttime, which is defined as any pixel where the  
                    solar zenith angle (SZA) is > than the minimum SZA in for the 
                    twilight zones. (string)
    addfield - If True, a field will be added to HDF5 file called 
               'Radiance_destriped' if it does not already exist or to revise 
               it if it does exist. Default is True.(bool)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    
    Output:
    Lc - Corrected DNB radiance (numpy2-D array) 
    """
    # read in the tables    
    (gainDay,LoffDay,LhistDay,ExcldZonesDay)=pickler.import_pickle(day_tablename)
    (gainNight,LoffNight,LhistNight,ExcldZonesNight)=pickler.import_pickle(night_tablename)
    (gainTwi,LoffTwi,LhistTwi,SolZen,ExcldZones)=pickler.import_pickle(twilight_tablename)
    ntwi=len(gainTwi) 

    # read in SDR file    
    datasetnm_out='Radiance_destriped'+name_extnd
    L=grnV.get_radiance(pathhdf,RdncFilename,'DNB')
    SZA=grnV.get_geoloc(pathhdf,GeoFilename,'DNB','SolarZenithAngle')
    shp=L.shape
    Lc=np.zeros(shp)
    Nscan=int(shp[0]/ndet)
    Nagg=gainDay.shape[1]
    LoffallDay=LoffDay.mean(axis=0)
    LoffallNight=LoffNight.mean(axis=0)
    LoffallTwi=[]
    for j in range(0,ntwi):
        LoffallTwi.append(LoffTwi[j].mean(axis=0))
    for n in range(0,Nscan):
        for i in range(0,ndet):
            k=n*ndet+i
            for iagg in range(0,Nagg):
                (ifrm,ito)=DNBcal.EV_agg_samp_accum(iagg)
                Lsamp=L[k,ifrm:ito]
                Loffall=np.zeros(Lsamp.shape)
                gainsamp=np.ones(Lsamp.shape)
                SZAsamp=SZA[k,ifrm:ito]
                #day correction
                isday=SZAsamp<SolZen[0]
                if np.any(isday) and not np.any(iagg==ExcldZonesDay):
                    Lsamp[isday]-=LoffDay[i,iagg]
                    gainsamp[isday]=np.interp(Lsamp[isday],LhistDay[i,iagg,:],
                                                gainDay[i,iagg,:])
                    Loffall[isday]=LoffallDay[iagg]
                #night correction
                isnight=SZAsamp>=SolZen[-1]
                if np.any(isnight) and not np.any(iagg==ExcldZonesNight):
                    Lsamp[isnight]-=LoffNight[i,iagg]
                    gainsamp[isnight]=np.interp(Lsamp[isnight],
                                      LhistNight[i,iagg,:],gainNight[i,iagg,:])
                    Loffall[isnight]=LoffallNight[iagg]
                #twilight correction loop
                for m in range(0,ntwi):
                    inzone=np.logical_and(SZAsamp>=SolZen[m],SZAsamp<SolZen[m+1])
                    if np.any(inzone) and  not np.any(iagg==ExcldZones):
                        Lsamp[inzone]-=LoffTwi[m][i,iagg]
                        gainsamp[inzone]=np.interp(Lsamp[inzone],
                                   LhistTwi[m][i,iagg,:],gainTwi[m][i,iagg,:])
                        Loffall[inzone]=LoffallTwi[m][iagg]
                Lc[k,ifrm:ito]=Lsamp/gainsamp+Loffall
    if addfield:
        grnV.add_EV_field(pathhdf,RdncFilename,DatasetGrp,datasetnm_out,Lc,'DNB')
    return Lc

def HistEqApplyTblTwilightPeriod(pathhdf,t_fromtostr,day_tablename,
                                twilight_tablename,night_tablename,
                                addfield=True,name_extnd=''):
    """
    Purpose: This routine uses tables for destriping DNB radiances 
    using the histogram equalization method for twilight granules using input 
    correction tables. Since twilight granules often contain pixels in night-
    time or daytime, correction tables for these are also used. The tables 
    are applied to destripe a set of DNB HDF5 radiance files that fall within 
    the speciufied time period.
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 files resides 
              (string)
    pathdat - Path to the directory containing the files with the destriping 
              correction tables. (string)
    t_fromtostr - String using the same format as used in the file naming 
             convention in order to describe a period of time within a one day 
             period for determining the files to apply destriping. The 
             convention is _dYYYYMMDD_tHHmmSSS_eHHmmSSS. Here YYYYMMDD gives 
             the year, month and day, and HHmmSSS gives UTC time in hours, 
             minutes and seconds down to a tenth of a second. the part after 
             '_t' indicates the start time and '_e' indicates the end time, 
             e.g. _d20140922_t2310231_e2345388 is on Sept. 09, 2014 for the 
    day_tablename - filename with path containing the correction tables to be used 
                    for daytime, which is defined as any pixel where the solar 
                    zenith angle (SZA) is less than the minimum SZA in for the 
                    twilight zones. (string)
    twilight_tablename - filename with path containing the correction tables to  
                    be used for for twilight, which is defined as any pixel where  
                    the solar zenith angle (SZA) is within the range of twilight  
                    zones defined in the table set. (string)
    night_tablename - filename with path containing the correction tables to be  
                    used for nighttime, which is defined as any pixel where the  
                    solar zenith angle (SZA) is > than the minimum SZA in for the 
                    twilight zones. (string)
    addfield - If True, a field will be added to HDF5 file called 
               'Radiance_destriped' if it does not already exist or to revise 
               it if it does exist. Default is True.(bool)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file.
    
    Output:
    RdncFileList - List of radiance files which have been processed for cor-
                   rections (string list) 
    GeoFileList - List of geolocation files which have been processed for 
                 corrections (string list) 
    """
    (RdncFileList,GeoFileList)=grnV.matchRdncGeoFiles(pathhdf,t_fromtostr,'DNB')
    for i in range(len(RdncFileList)):
        HistEqApplyTblTwilight(pathhdf,RdncFileList[i],GeoFileList[i],
                        day_tablename,twilight_tablename,night_tablename,
                        addfield=addfield,name_extnd=name_extnd)
    return (RdncFileList,GeoFileList)
    
def NearConstantContrast(pathhdf,filename,Lmin,destriped=False,addField=True,
                         reviseField=True,name_extnd=''):
    """
    Purpose: This routine takes DNB radiances and produces a Near Constant 
    Contrast (NCC) image that can be saved as a field on the HDF5 file and is 
    also the output for this routine.
    
    Inputs:
    pathhdf - full path to the directory where the DNB HDF5 file resides (string)
    filename - full name of the DNB HDF5 file being processed (string)
    Lmin - Minimum radiance in W/(cm^2 str) for which NCC will be equalized (float)
    addField - If True, a field will be added to HDF5 file called "NCC" if it 
                does not already exist.(bool)
    destriped - If True, apply NCC to destriped DNB radiance field named 
                'Radiance_destriped' if it exists.
    reviseField - If both addField and reviseField are True, then the NCC is 
                  computed and the NCC field in the HDF5 is revised. If the 
                  field does not exist, it is added. If reviseField is False 
                  but an NCC field already exists in the HDF5 file, then it is
                  not recomputed and the existing field is returned. (bool)
    name_extnd - If not an empty string, this is an additional string added to
           the field name 'Radiance_destriped'. With this multiple versions 
           destriping can be compared in the same HDF5 file. The output field, 
           'NCC_destriped', also will be created with this extension.

    Output:
    NCC - Unitless NCC image corresponding to the DNB radiances. (numpy 2-d 
          float array)
    """
    epsil=1.e-13
    mj=127
    mi=96
    iskp=3
    jskp=5
    scaleFac=.3
    prcntl_lo=2
    fieldname='Radiance'
    fieldnameout='NCC'
    if destriped==True:
        fieldname+='_destriped'+name_extnd
        fieldnameout+='_destriped'+name_extnd
    print(fieldname,fieldnameout)
    #NCC=grnV.get_radiance(pathhdf,filename,'DNB',datasetnm=fieldnameout)
    #if NCC!=None and reviseField==False:
    #    print('NCC is already computed')
    #    return NCC
    L=grnV.get_radiance(pathhdf,filename,'DNB',datasetnm=fieldname)
    shp=L.shape
    i_=[0,mi]
    while i_[-1]<=shp[0]-mi:
        i_.append(i_[-1]+iskp*mi)
        if i_[-1]>shp[0]:
            i_[-1]=shp[0]
    j_=[0,mj]
    while j_[-1]<=shp[1]-mj:
        j_.append(j_[-1]+jskp*mj)
        if j_[-1]>shp[1]:
            j_[-1]=shp[1]
    i_=np.array(i_)
    j_=np.array(j_)
    i_mid=(i_[0:-1]+i_[1:])/2
    j_mid=(j_[0:-1]+j_[1:])/2
    ni=len(i_mid)
    nj=len(j_mid)
    
    Lmd=np.zeros([len(i_mid),len(j_mid)],float)
    L[np.isnan(L)]=epsil
    L[np.isinf(L)]=epsil
    L+=np.percentile(L,prcntl_lo)
    for i in range(0,ni):
        for j in range(0,nj):
            Lmd[i,j]=np.median(L[i_[i]:i_[i+1],j_[j]:j_[j+1]])
    Lmd[Lmd<Lmin]=Lmin

    logLmd=np.log(Lmd)
    print('logLmd',logLmd.min(),logLmd.max(),logLmd.mean())
    print('L',L.min(),L.max(),L.mean())
    logLfunc = intrplt.RectBivariateSpline(i_mid,j_mid,logLmd)
    i_ind=np.arange(0,shp[0])
    j_ind=np.arange(0,shp[1])    
    Lncc=np.exp(logLfunc(i_ind,j_ind))
    NCC=L/Lncc*scaleFac
    if addField:
        print('adding field')
                         
        grnV.add_EV_field(pathhdf,filename,DatasetGrp,fieldnameout,NCC,'DNB')
    return NCC
                        
