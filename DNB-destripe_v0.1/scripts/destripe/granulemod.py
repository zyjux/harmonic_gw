# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:03:44 2013

@author: Ren
"""

import numpy as np
import math as mt

import time, calendar
import h5py
import os
import pickler


def filestr2time(filestr,noff,errval=99.9999 ):
    #Purpose - converts a string commonly used in file names to indicate time
    # of day into a floating point number in hours. The time string is assumed
    # to be seven numeric characters of the form hhmmsss, where sss indicates 
    # tenths of a second
    #return errval if the format does not correspond to a time         
    try:
        ntime=int(filestr[noff:noff+7])
    except ValueError:
        return errval
    nhrs=int(ntime/1e5)
    if nhrs>24:
        return errval
    minsec=int(ntime-nhrs*1e5)
    nminut=int(minsec*1.e-3)
    if nminut>=60:
        return errval
    sec=int(minsec-nminut*1e3)/10
    if sec>=60.0:
        return errval
    timehrs=nhrs+nminut/60+sec/3600
    timesecs=timehrs*60*60
    return timesecs
def filestr2period(filename):
    noff=filename.find('_d')
    timestr=filename[noff:noff+28]    
    timerng=str2period(timestr)    
    return timerng    

def str2period(timestr):
    """    
    Format 1 - Used as part of the file name to indicate start and end of a 
        granules, e.g. '_d20121029_t0213041_e1343244' 
                                  = 29 Oct 2012 from 02:13:04.1 to 13:43:24.4
        For periods that span day boundary, the end time is assigned to the
        next date.
    Format 1a - Uses the same form, but allows inclusion of white spaces, '-', 
        ':', comma or period for claity. These characters are striped before 
        parsing. Always use a leading zero for months, day, hrs min and sec < 10
        e.g. '_d2012-10-29 _t02:13:04.1 _e13:43:24.4' is same time as above.
    Format 2 - For long periods, use a 2 string list for start and end date 
        and time. This function recognizes the data type as list and interprets
        it differently. Here the '_d', '_t' & '_e' is not used. As with Format 
        1a, Format 2 allows, but does not require, inclusion of white spaces, 
        '-', ':', a comma or period for claity.
        If time-of-day is left off of start or end, then whole day is assumed.
        e.g. ['2012-10-29 02:13:04.1', '2012-11-02 13:43:24.4']
        e.g. ['2012-10-29', '2012-11-02']
    """
    if type(timestr)==list and len(timestr)==2:
        timestr_frm=strip_time_str(timestr[0])        
        timestr_to=strip_time_str(timestr[1])        
        dateday=time.strptime(timestr_frm[0:8],'%Y%m%d')    
        tday=calendar.timegm(dateday)
        if len(timestr_frm)==8:
            tstrt=0.
        else:
            tstrt=filestr2time(timestr_frm,8)
        dateday=time.strptime(timestr_to[0:8],'%Y%m%d')    
        tdayend=calendar.timegm(dateday)
        if len(timestr_to)==8:
            tend=24+60+60.
        else:
            tend=filestr2time(timestr_to,8)

    elif timestr=='':
        return [-1.e-30,1.e30]
    else:
        timestr2=strip_time_str(timestr)
        dateday=time.strptime(timestr2[2:10],'%Y%m%d')    
        tday=calendar.timegm(dateday)
        tstrt=filestr2time(timestr2,12)
        tend=filestr2time(timestr2,21)
        if tstrt>tend:
            tdayend=tday+24*60*60.
        else:
            tdayend=tday
    timerng=[tstrt+tday,tend+tdayend]
    return timerng 
def strip_time_str(timestr):
    timestrout=timestr.replace(' ','')    
    timestrout=timestrout.replace(':','')    
    timestrout=timestrout.replace('-','')    
    timestrout=timestrout.replace('.','')
    timestrout=timestrout.replace('.','')
    timestrout=timestrout.replace(',','')
    return timestrout

def fileperiod2str(timerng):
    
    timstrtstrct=time.gmtime(timerng[0])
    timendstrct=time.gmtime(timerng[1])
    outstr='_d'+time.strftime('%Y%m%d',timstrtstrct)    
    outstr+='_t'+time.strftime('%H%M%S',timstrtstrct)    
    tenthstr=str(int(round((timerng[0]%1)*10)))    
    outstr+=tenthstr
    outstr+='_e'+time.strftime('%H%M%S',timendstrct)    
    tenthstr=str(int(round((timerng[1]%1)*10)))    
    outstr+=tenthstr
    return outstr

def period_day_hr_min_sec(timerng):
    del_time=timerng[1]-timerng[0]
    days=int(del_time/3600/24)
    hrs=int(del_time/3600)-days*24
    mins=int(del_time/60)-days*24*60-hrs*60
    secs=del_time-days*24*3600-hrs*3600-mins*60
    return (days,hrs,mins,secs)

def get_h5(pathnm,filenm,datasetgrp,datasetnm): 
    #basic read of h5 array data without scaling or removing of fill
    try:    
        file=h5py.File(pathnm+filenm,'r')
    except OSError:
        return None
    try:
        dat=file[datasetgrp+datasetnm]
    except KeyError:
        print('Error: data key '+datasetgrp+datasetnm+' not found')
        return None
    d=np.array(dat)
    file.close()
    return d
    
def get_h5_data(pathnm,filenm,datasetgrp,datasetnm,ndet,nscanpergran=48):
    try:    
        f=h5py.File(pathnm+filenm,'r')
    except OSError:
        return None
    # for reading float values SDRs and EDRs (not scaled integers)
    #Removes fill scan at the end for short granules
    try:    
        dat=f[datasetgrp+datasetnm]
    except KeyError:
        return None
    d=np.array(dat)
    shp=d.shape 
    if ndet!=0:
        Nscan=np.array(f[datasetgrp+'NumberOfScans'],int)
        ngran=len(Nscan)
        fullgran=(Nscan%nscanpergran)==0
        nr=np.sum(Nscan)
        if nr<=0:
            d=None
            return d
        if ~all(fullgran):
            if all(fullgran[0:ngran-1]):
                if shp[1]>=nr*ndet:               
                    d=d[0:nr*ndet,:]
                else:
                    print('Size of Data does not match number of scans')
            else:
                L_temp=np.zeros((nr*ndet,shp[1]),float)
                kto=0            
                for i in list(range(0,ngran)):
                    jfrm=i*nscanpergran*ndet
                    jto=jfrm+Nscan[i]*ndet
                    kfrm=kto
                    kto=np.sum(Nscan[0:i+1])*ndet  
                    if shp[1]>=jto:               
                        L_temp[kfrm:kto,:]=d[jfrm:jto,:]
                    else:
                        print('Size of Data does not match number of scans')

                d=L_temp
    f.close()
    return d
def get_h5_data_scaled(pathnm,filenm,datasetgrp,datasetnm,ndet,nscanpergran=48,
                       fillvalint=65529,fillvalflt=-999.):
    #for reading scaled integer SDRs and EDRs.
    #Removes fill scan at the end for short granules
    d=get_h5(pathnm,filenm,datasetgrp,datasetnm)
    if d==None:
        return None
    datscale=get_h5(pathnm,filenm,datasetgrp,datasetnm+'Factors')
    if ndet!=0:
        Nscan=get_h5(pathnm,filenm,datasetgrp,'NumberOfScans')
        ngran=len(Nscan)
        nr=np.sum(Nscan)
        if nr<=0:
            d=None
            return d
        shp=d.shape
        L_temp=np.zeros((nr*ndet,shp[1]),float)
        kto=0            
        for i in list(range(0,ngran)):
            jfrm=i*nscanpergran*ndet
            jto=jfrm+Nscan[i]*ndet
            kfrm=kto
            kto=np.sum(Nscan[0:i+1])*ndet
            dtemp=d[jfrm:jto,:]*datscale[2*i]+datscale[2*i+1]
            dtemp[d[jfrm:jto,:]>=fillvalint]=fillvalflt
            L_temp[kfrm:kto,:]=dtemp
        d=L_temp
    return d   
def get_h5_data_int(pathnm,filenm,datasetgrp,datasetnm,ndet,nscanpergran=48,Nscan=None):
    #for reading integer SDRs and EDRs arrays that are not scaled (e.g. quality flags).
    #Removes fill scan at the end for short granules. If NumberOfScans is not 
    #a field, then Nscan must be included as an input.
    d=get_h5(pathnm,filenm,datasetgrp,datasetnm)
    if d==None:
        return None
    if Nscan==None:
        Nscan=get_h5(pathnm,filenm,datasetgrp,'NumberOfScans')
    if Nscan==None:
        return None

    ngran=len(Nscan)
    nr=np.sum(Nscan)
    if nr<=0:
        d=None
        return d
    shp=d.shape
    I_temp=np.zeros((nr*ndet,shp[1]),int)
    kto=0            
    for i in list(range(0,ngran)):
        jfrm=i*nscanpergran*ndet
        jto=jfrm+Nscan[i]*ndet
        kfrm=kto
        kto=np.sum(Nscan[0:i+1])*ndet
        if jto-jfrm ==kto-kfrm:        
            dtemp=d[jfrm:jto,:]
            I_temp[kfrm:kto,:]=dtemp
        else:
            return None
    return I_temp  
def get_h5_imag(pathnm,filenm,datasetgrp,datasetnm,fillval=65529):    
    #for reading imagery data in GTM. Removes fill scan lines
    d=get_h5(pathnm,filenm,datasetgrp,datasetnm)
    if d==None:
        return d
    scanlineflg=np.zeros((d.shape[0]),bool)
    for i in range(0,len(scanlineflg)):
        if all(d[i,:]>=fillval):
            scanlineflg[i]=False
        else:
            scanlineflg[i]=True
    d=d[scanlineflg,:]
    return d
def get_h5_imag_float(pathnm,filenm,datasetgrp,datasetnm,fillval=-999.): 
    try:    
        file=h5py.File(pathnm+filenm,'r')
    except OSError:
        return None

    try:    
        dat=file[datasetgrp+datasetnm]
    except KeyError:
        return None
    d=np.array(dat,float)
    scanlineflg=np.zeros((d.shape[0]),bool)
    for i in range(0,len(scanlineflg)):
        if all(d[i,:]<=fillval):
            scanlineflg[i]=False
        else:
            scanlineflg[i]=True
    file.close()
    d=d[scanlineflg,:]
    return d

def threshold_dat(d,dat_low,dat_hi):
    dat_x=(d>dat_low)*d+(d<=dat_low)*dat_low
    dat_x=(dat_x<dat_hi)*dat_x+(dat_x>=dat_hi)*dat_hi
    return dat_x
def granulefile_list(pathnm,prefix,suffix):
    lstfile=os.listdir(pathnm)
    lsfil=lstfile
    ngran=0
    lsfil=[]
    for filenm in lstfile:
        tst=filenm.endswith(suffix) and (filenm.find(prefix)!=-1)
        if tst:
            lsfil.append(filenm)
            ngran+=1
    return lsfil
def granulefile_times(lsfil,sort=True,t_fromtostr=''):
    ngran=len(lsfil)
    grantimes=np.zeros((2,ngran), dtype=float)
    tstrtend_all=str2period(t_fromtostr)  
    ifil=0
    lsfil_select=[]
    for filenm in lsfil:
        tstrtend=filestr2period(filenm)  
        if tstrtend[0]>=tstrtend_all[0] and tstrtend[1]<=tstrtend_all[1]:      
            grantimes[0:2,ifil]=tstrtend[0:2]
            lsfil_select.append(filenm)
            ifil=ifil+1
    if sort and len(lsfil_select)>0:
        tstarts=grantimes[0,0:ifil]
        isort=np.argsort(tstarts)
        grantimes_srt=grantimes[:,isort]
        lsfil_srt=reindex_strlist(lsfil_select,isort)
        return (grantimes_srt,lsfil_srt)
    else:
        return (grantimes,lsfil_select)
def reindex_strlist(strlist,indx):
        strlist_reind=[]
        for i in range(0,len(indx)):
            strlist_reind.append(strlist[indx[i]])
        return strlist_reind

def granulefile_list_sort(pathnm,prefix,suffix,t_fromtostr=''):
    lsfil=granulefile_list(pathnm,prefix,suffix)
    (grantimes,lsfil_select)=granulefile_times(lsfil,sort=True,t_fromtostr=t_fromtostr)
    return (grantimes,lsfil_select)
def granulefile_list_sort_pare(pathnm,prefix,suffix,t_fromtostr='',
                               t_create_prefix='_c',t_create_len=20):
    (grantimes,lsfil)=granulefile_list_sort(pathnm,prefix,suffix,
            t_fromtostr)
    latest=pare_by_creation(lsfil,grantimes,t_create_prefix,t_create_len)
    n=0
    N=latest.sum()
    grantimes_out=np.zeros([2,N])
    lsfil_out=[]
    for i in range(0,len(lsfil)):
        if latest[i]:
            lsfil_out.append(lsfil[i])
            grantimes_out[:,n]=grantimes[:,i]
            n+=1
    return (grantimes_out,lsfil_out)
def pare_by_creation(lsfil,grantimes,t_create_prefix='_c',t_create_len=20):
    #assumes that files are alread sorted by grantime
    nfiles=len(lsfil)
    t_create=np.zeros(nfiles)
    latest=np.ones(nfiles,bool)
    for i in range(0,nfiles):
        nstr=lsfil[i].find(t_create_prefix)
        nstr+=len(t_create_prefix)        
        t_create[i]=float(lsfil[i][nstr:nstr+t_create_len])
    i=1
    while i < nfiles:
        tlatest=t_create[i-1]
        while np.all(grantimes[0,i-1]==grantimes[0,i]):
            if tlatest<t_create[i] :
                tlatest=t_create[i]
                latest[i-1]=False
            else:
                latest[i]=False
            i+=1
        i+=1
    return latest

def granulefile_group(grantimes,tgapmax,tgroupmax):
    tstrt=grantimes[0,0]
    #grouplistplt.show()=[0]
    nshp=grantimes.shape
    ngran=nshp[1]
    grouplist=np.array(int(0))
    for i in range(0,ngran-1):
        tdelgran=grantimes[0,i+1]-grantimes[1,i]
        if ((grantimes[1,i+1]-tstrt < tgroupmax) & (tdelgran<tgapmax)):
            continue
        else:
            grouplist=np.append(grouplist,i+1)
            tstrt= grantimes[0,i+1]
    grouplist=np.append(grouplist,ngran)
    return grouplist

def get_h5_groups(filename):
    f=h5py.File(filename)
    nds=getnode(f)
    f.close()
    return nds
def getnode(nodelist):   
    nodes=[]
    for name in nodelist:
        nd=nodelist[name]
        if type(nd)==h5py._hl.dataset.Dataset:
            nodesub=[]
            dtype=str(nd.dtype)
            shape=nd.shape
        elif type(nd)==h5py._hl.group.Group:
            nodesub=getnode(nd)
            dtype='Node'
            shape=(len(nodesub),)
        else:
            return []
        node=dict({"name":name,"subnode":nodesub,'dtype':dtype,'shape':shape})
        nodes.append(node)
    return nodes
def get_h5_dat(pathnm,filenm,datasetgrp,datasetnm):
    f=h5py.File(pathnm+filenm,'r')    
    dat=f[datasetgrp+datasetnm]
    if type(dat)==h5py._hl.dataset.Dataset:    
        dtyp=dat.dtype
    else:
        return []
    d=np.array(dat,dtype=dtyp)
    f.close()
    return d
def file_dict_h5(filelist,DatasetGrp,pathhdf,dictlist):
        rngfiles=list(range(0,len(filelist)))
        Dat=[]
        for ifile in rngfiles:
            dictval=[]
            for j in range(0,len(dictlist)):
                dictval.append(get_h5_dat(pathhdf,filelist[ifile],DatasetGrp,
                                          dictlist[j]))
            Dat.append(dict(zip(dictlist,dictval)))
        return Dat

def file_group_h5(pathhdf,pathdat,tmaxgroup,tmaxgap,prefix,ID,DatasetGrp,
                  dictlist,suffix='h5',picklezip=False,logfile=False,
                  t_fromtostr=''):    
    files0=granulefile_list(pathhdf,prefix,suffix)
    (grantimes,files)=granulefile_times(files0,True,t_fromtostr)
    grangroups=granulefile_group(grantimes,tmaxgap,tmaxgroup)
    ngroup=len(grangroups)-1
    rnggrp=list(range(0,ngroup))
    grouptimes=np.zeros((2,ngroup),dtype=float)
    try:
        os.listdir(pathdat)
    except FileNotFoundError:
        os.mkdir(pathdat)
    if logfile:
        flog=open(pathdat+ID+'logfile.txt',mode='w')
        print(grangroups,file=flog) 
        for i in range(0,len(files)):
            print(files[i],grantimes[0:2,i]-grantimes[0,0],file=flog)    
    for igrp in rnggrp:
        igrnstrt=grangroups[igrp]
        igrnend=grangroups[igrp+1]
        tmstrt=time.gmtime(grantimes[0,igrnstrt])
        tmend=time.gmtime(grantimes[1,igrnend-1])
        grouptimes[:,igrp]=[grantimes[0,igrnstrt],grantimes[1,igrnend-1]]
        s_date=time.strftime("%d %b %Y",tmstrt)
        s_strt=time.strftime("%H:%M:%S",tmstrt)
        #s_dateend=time.strftime("%d %b %Y",tmend)
        s_end=time.strftime("%H:%M:%S",tmend) 
        filetimestamp=fileperiod2str(grouptimes[:,igrp])    
        fileout=prefix+'_'+ID+filetimestamp+'.pkl'
        #print('group#',igrp,'granule#', igrnstrt, 'to ',igrnend-1,
        #' on '+s_date+' from '+s_strt+' to '+s_end)   
        filelist=files[igrnstrt:igrnend]        
        Dat=file_dict_h5(filelist,DatasetGrp,pathhdf,dictlist)        
        if logfile:
            print(fileout,file=flog)
        if pickler.export_pickler(Dat,pathdat+fileout,picklezip)==False:
                print([fileout+' not saved'])
    flog.close()
    return True
def dict_group_h5(pathhdf,prefix,DatasetGrp,dictlist,suffix='h5',t_fromtostr=''):    
    files0=granulefile_list(pathhdf,prefix,suffix)
    (grantimes,files)=granulefile_times(files0,True,t_fromtostr)
    Dat=file_dict_h5(files,DatasetGrp,pathhdf,dictlist)        
    return Dat
def any_str(S,s):
    #for lists of strings
    n=len(S)   
    for i in range(0,n):
        if S[i]==s:
            return True
    return False
def SDR_DayNite(pathhdf,filename,SDRname):
    DatasetGrp='/Data_Products/'+SDRname+'/'
    dat=h5py.File(pathhdf+filename,'r')
    d=dat[DatasetGrp + SDRname + '_Aggr']
    ngran=d.attrs['AggregateNumberGranules']
    Ngran=ngran[0,0]
    D_N=[]
    for i in range(0,Ngran):
        d=dat[DatasetGrp+SDRname+'_Gran_'+str(i)]
        Day_Nite=d.attrs['N_Day_Night_Flag']
        D_N.append(Day_Nite[0,0])
    dat.close()   
    return D_N
    
def FindMatchInList(grantime,lsfil):
    time_str=fileperiod2str(grantime)
    grndat=granulefile_times(lsfil,t_fromtostr=time_str[1:])               
    for j in range(0,len(grndat[1])):
        if grantime[0]==grndat[0][0,j] and grantime[1]==grndat[0][1,j]:        
            return grndat[1][j]  
def get_subdir(pathnm,listpathx):
    """iterative routine that finds all the subdirectories under a given path
    """
    listing=os.listdir(pathnm)
    if len(listing)>0:
        for lis in listing:
            pathnm_sub=pathnm+'/'+lis+'/'
            if os.path.isdir(pathnm_sub):
                #print(pathnm_sub)
                listpathx.append(pathnm_sub)
                listpathx=get_subdir(pathnm_sub,listpathx)
                
    return listpathx
def FileIndex(pathlist,prefixlist,suffix='h5',date_range='',sortpare=True,
              t_create_prefix='_c', t_create_len=20):
    """produces a file index of all files under a set of directories that 
    satisfy a set of naming criterion"""                
    files_all=[]
    path_all=[]
    prefix_all=np.zeros(0,int)
    grantimes_all=np.zeros([2,0],float)
    for pathgen in pathlist:
        listpath=[]
        listpath=get_subdir(pathgen,listpath)
        for pathnm in listpath:
            for m in range(0, len(prefixlist)):
                prefix=prefixlist[m]
                (grantimes,lsfil)=granulefile_list_sort_pare(pathnm,prefix,
                                    suffix,date_range)
                grantimes_all=np.append(grantimes_all,grantimes,1)
                files_all+=lsfil
                for i in range(0,len(lsfil)):
                    path_all.append(pathnm)
                    prefix_all=np.append(prefix_all,m)
    Nall=len(files_all)
    if sortpare and Nall>0:
        tstarts=grantimes_all[0,:]
        isort=np.argsort(tstarts)        
        prefix_all=prefix_all[isort]
        files_all=reindex_strlist(files_all,isort)
        path_all=reindex_strlist(path_all,isort)
        grantimes_all=grantimes_all[:,isort]
        latest=np.ones(Nall,bool)        
        for m in range(0, len(prefixlist)):
            ind=prefix_all==m
            files=[]
            for i in range(0,Nall):
                if ind[i]:
                    files.append(files_all[i])
            latest[ind]=pare_by_creation(files,grantimes_all[:,ind],t_create_prefix,t_create_len)
        grantimes_all=grantimes_all[:,latest]
        prefix_all=prefix_all[:,latest]
        path_allx=[]
        files_allx=[]
        for i in range(0,Nall):
            if latest[i]:
                files_allx.append(files_all[i])
                path_allx.append(path_all[i])
        path_all=path_allx
        files_all=files_allx
    return (files_all,path_all,prefix_all,grantimes_all)
def IndexByDate(Index):
    (files_all,path_all,prefix_all,grantimes_all)=Index
    secPerDay=24*3600.0
    t=(grantimes_all[0,:]+grantimes_all[1,:])*.5
    #isort=list(np.argsort(t))
    #tsort=t[isort]
    n=len(t)
    m=prefix_all.max()+1  
    t_day1=secPerDay*int(t.min()/secPerDay)
    t_strct=time.gmtime(t_day1)
    datestr=time.strftime('%m %d %Y',t_strct)
    
    tmax=t.max()
    t_strct=time.gmtime(tmax)
    datestr=time.strftime('%m %d %Y',t_strct)

    idays=np.array((t-t_day1)/secPerDay,int)
    t_days=t_day1+np.arange(0,tmax-t_day1,secPerDay)    
    ndays=int((tmax-t_day1)/secPerDay)+1
    filecounts=np.zeros((m,ndays),int)
    for i in range(0,n):
        filecounts[prefix_all[i],idays[i]]+=1
    return (t_days,filecounts)
