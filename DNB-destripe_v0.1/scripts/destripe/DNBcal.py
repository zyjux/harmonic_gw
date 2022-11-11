# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:34:16 2014

DNB calibration routines including destriping
@author: Stephen Mills
copyright 2015, Renaissance Man Engineering, all rights reserved

"""
import granulemod as grn
import granulemodVIIRS as grnV
import pickler
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import earthgeom
import h5py

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



aggseqfact=np.array([[20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 
    27, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 42, 
    42, 42, 42, 42],
    [11, 12, 12, 13, 14, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28, 
     30, 33, 35, 38, 40, 43, 46, 49, 52, 55, 59, 62, 64, 66,
     128,256,512,66],
     [80, 16, 64, 64, 64, 32, 24, 72, 40, 56, 40, 48, 32, 48, 32, 72, 72,
      72, 80, 56, 80, 64, 64, 64, 64, 64, 72, 80, 72, 88, 72, 184,
      0, 0, 0, 0]],int)
NaggEV=32
npix_scan=4064
nEVrng=[0,npix_scan]
NaggEV_BL=NaggEV
npix_scan_BL=npix_scan
nEVrng_BL=nEVrng
aggseqfact_BL=aggseqfact

aggseqfact_21=np.array([[ 25, 26, 26, 27, 27, 28, 29, 30, 31, 32, 33, 34, 35, 
                         36, 37, 38, 39, 40, 41, 42, 42],
                        [ 20, 21, 22, 23, 24, 26, 28, 30, 33, 35, 38, 40, 43, 
                          46, 49, 52, 55, 59, 62, 64, 66],
                        [ 447, 32, 48, 32, 72, 72, 72, 80, 56, 80, 64, 64, 64, 
                          64, 64, 72, 80, 72, 88, 72, 184]],int)
NaggEV_21=21
nEVrng_21=[9,9+3774]

aggseqfact_21_26=np.array([[23, 25, 26, 26, 27, 27, 28, 29, 30, 31, 32, 33, 34, 35, 
                         36, 37, 38, 39, 40, 41, 42, 42],
                        [ 15, 20, 21, 22, 23, 24, 26, 28, 30, 33, 35, 38, 40, 43, 
                          46, 49, 52, 55, 59, 62, 64, 66],
                        [ 304,224, 32, 48, 32, 72, 72, 72, 80, 56, 80, 64, 64, 64, 
                          64, 64, 72, 80, 72, 88, 72, 184]],int)
NaggEV_21_26=22
nEVrng_21_26=[24,3944]

strcal=['SV_DNB','BB_DNB','SD_DNB']

L_cnt_pix=4.243e-08*np.array([1.,1.,250.,92925.])

"""
____________________________________________________________________
                         DNB Utility Functions
____________________________________________________________________
"""
def setPaths(datestr):
    pathgen = 'c:/Users/Ren/NPP_data/'#root directory for input and output
    pathhdf=pathgen+datestr+'/hdf/' #path for directory of hdf input files
    pathplt=pathgen+datestr+'/plots/' #path for directory of output plots
    pathdat=pathgen+datestr+'/data/' #path for directory of data
    return [pathhdf,pathplt,pathdat]

def SetConfig(config):
    if config=='BL':
        aggseqfact=aggseqfact_BL
        NaggEV=NaggEV_BL
        nEVrng=nEVrng_BL
    if config=='21':
        aggseqfact=aggseqfact_21
        NaggEV=NaggEV_21
        nEVrng=nEVrng_21
    if config=='21/26':
        aggseqfact=aggseqfact_21_26
        NaggEV=NaggEV_21_26
        nEVrng=nEVrng_21_26
    NaggEVtot=2*NaggEV
    return(aggseqfact,NaggEV,NaggEVtot,nEVrng)
def CalFac(n,istage,config='BL'):        
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    if n>=NaggEVtot:
        return None
    else:
        return L_cnt_pix[istage]/(aggseqfact[0,n]*aggseqfact[1,n])
def AggFac(n,config='BL'):        
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    if n>=NaggEVtot:
        return None
    else:
        return (aggseqfact[0,n],aggseqfact[1,n])
def AggModeNum(n,config='BL'):
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    if n>=NaggEVtot:
        return None
    else:
        NaggMd = NaggEV-AggSeqNum(n,config)
        if config=='21/26' and NaggMd==22:
            NaggMd=26
        return NaggMd
def AggSeqNum(n,config='BL'):
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    agg_seq_order=AggSeqOrder(config)
    if n>=NaggEVtot:
        return None
    else:
        return agg_seq_order[n]
def AggSeqOrder(config='BL'):
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    agg_seq_order=list(range(0,NaggEV))+list(range(NaggEV-1,-1,-1))
    return agg_seq_order
def EV_agg_samples(config='BL'):
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    # the number of samples for each agg zone by reflecting
    agg_seq_order=AggSeqOrder(config)
    nsampagg=aggseqfact[2,agg_seq_order]
    return nsampagg
def EV_agg_samp_accum(n,config='BL'):
    (aggseqfact,NaggEV,NaggEVtot,nEVrng)=SetConfig(config)    
    evsamp=EV_agg_samples(config)
    if n>=NaggEVtot:
        return None
    nfrm=evsamp[0:n].sum()+nEVrng[0]
    nto=evsamp[0:n+1].sum()+nEVrng[0]
    return (nfrm,nto)
def CalMerge(dat,istage,StrCal,DN0=None,t0seqref=None):

    dictlst=('DNcal','DNcalMean','DNcalStd','RdcalMean','dnCalMean','dnP')
    FLOATFILL=-999.
    DNsaturate=16383.

    DNcalDat=[]
    Nseq=np.zeros([0,1],int)
    tscan=np.zeros([0,1],float)
    Hamside=np.zeros([0,1],int)
    SAA=np.zeros([0,1],int)
    Nscan=0
    nscan=np.zeros([0,1],int)    
    Solar=np.zeros([0,3],float)
    Lunar=np.zeros([0,3],float)
    szgrn=(dat[0].get(StrCal)).shape
    NscanPerGran=len(dat[0].get('HAM_SIDE'))
    ndet=int(szgrn[0]/NscanPerGran)    #loop through files in orbits
    for j in range(0,len(dat)):
        d=dat[j]
        nscans=d.get('numScans')
        t=d.get('EV_START_TIME')
        saa=d.get('southAtlanticAnomalyFlag')
        solar=d.get('solar')
        lunar=d.get('lunar')
        Hside=d.get('HAM_SIDE')
        DNcal=d.get(StrCal)
        if t0seqref!=None:
            #t_scan_period=(t[1:]-t[0:-1]).mean()
            nseq=np.array(np.round((t-t0seqref)/t_scan_period)%72/2,int)
            isshortlast=False         
            for k in range(0,nscans):
                isshort=np.all(DNcal[(k*ndet):((k+1)*ndet),Nshort]==fillshort)
                if isshortlast and not isshort:
                    t0seqref=t[k]
                    nseq=np.array(np.round((t-t0seqref)/t_scan_period)%72/2,int)
                isshortlast=isshort
        else:
            nseq=d.get('DNB_sequence')-1
 
        for k in range(0,nscans):
            DNcalscan=DNcal[(k*ndet):((k+1)*ndet),:]
            DNcalMean=np.zeros(ndet)
            RdcalMean=np.zeros(ndet)
            dnCalMean=np.zeros(ndet)
            DNcalStd=np.zeros(ndet)
            dnP=np.zeros([2,ndet],float)
            nsq=nseq[k]
            nskip=1
            if nsq>=34:
                nsample=4
            else:
                nsample=16
            noff=istage*nsample
            nsampmin=nsample/2
            for kdet in range(0,ndet):
                DNcalLine=DNcalscan[kdet,noff+nskip:noff+nsample]
                testfill=np.array([True],bool)
                #eliminate fill values
                while np.any(testfill)and len(DNcalLine)>1:
                    testfill=np.logical_or(DNcalLine<=FLOATFILL,DNcalLine>=DNsaturate) 
                    DNcalLine=DNcalLine[~testfill]
                test3sigma=np.array([True],bool)
                #3 sigma test
                DNcalMn=FLOATFILL               
                DNcalSt=0.
                while np.any(test3sigma) and len(DNcalLine)>nsampmin:
                    DNcalSt=DNcalLine.std()
                    DNcalMn=DNcalLine.mean()
                    DNcalMd=np.median(DNcalLine)
                    test3sigma=np.abs(DNcalLine-DNcalMd)>DNcalSt*3.
                    DNcalLine=DNcalLine[~test3sigma]
                if len(DNcalLine)<=nsampmin:
                    DNcalMn=FLOATFILL               
                    DNcalSt=0.
                DNcalMean[kdet]=DNcalMn
                DNcalStd[kdet]=DNcalSt
                if len(DNcalLine)<=nsampmin or (nsq>33 and istage==3) or DN0==None:
                    dnCalMean[kdet]=float('nan')
                    RdcalMean[kdet]=float('nan')
                else:
                    dnCalMean[kdet]=DNcalMn-DN0[nsq,kdet]
                    RdcalMean[kdet]=dnCalMean[kdet]*CalFac(nsq,istage)
                    dnCal=DNcalLine-DN0[nsq,kdet]
                    dnP[:,kdet]=np.polyfit(np.arange(0,len(dnCal)), dnCal, 1)
    
            DNcalDat.append(dict(zip(dictlst,(DNcalscan,DNcalMean,DNcalStd,
                                              RdcalMean,dnCalMean,dnP))))
            tscan=np.append(tscan,t[k])
            Nseq=np.append(Nseq,nsq)
            Hamside=np.append(Hamside,Hside[k])
            SAA=np.append(SAA,saa[k])
            nscan=np.append(nscan,Nscan)
            lun=np.zeros([1,3],float)
            sol=np.zeros([1,3],float) 
            for l in range(0,3):
                sol[0,l]=solar[k,l]
                lun[0,l]=lunar[k,l]
            Lunar=np.append(Lunar,lun,0)
            Solar=np.append(Solar,sol,0)            
            Nscan+=1
    return (DNcalDat,tscan,Nseq,Hamside,SAA,Solar,Lunar)
def get_OBC_dat(pathhdf, filename):
    # data to be read from these files
    dictlist=('HAM_SIDE','EV_START_TIME','solar','lunar','numScans',
          'DNB_sequence','southAtlanticAnomalyFlag')
    # determine where the date starts in the name    
    noff=filename.find('_d')+1        
    #determine the from & to times for this file    
    t_fromtostr=filename[noff:noff+27]
    # from the OBC get the granules corresponding to the given time limits
    dat=grn.dict_group_h5(pathhdf,prefix2,DatasetGrp2,dictlist,suffix,t_fromtostr)
    #initialize angular arrays    
    Theta_sol=np.zeros([0],float)
    Phi_sol=np.zeros([0],float)
    Theta_lun=np.zeros([0],float)
    Phi_lun=np.zeros([0],float)
    HAM_side=np.zeros([0],int)
    DNB_seq=np.zeros([0],int)
    # loop over the granules
    for k in range(0,len(dat)):        
        nscans=dat[k].get('numScans')
        solar=dat[k].get('solar')
        lunar=dat[k].get('lunar')
        nseq=dat[k].get('DNB_sequence')
        hamside=dat[k].get('HAM_SIDE')
        
        [theta_s,phi_s]=earthgeom.unit_cart2sphere(solar.transpose())          
        [theta_l,phi_l]=earthgeom.unit_cart2sphere(lunar.transpose())          
        # append granule data to the arrays
        Theta_sol=np.append(Theta_sol,theta_s[0:nscans])            
        Phi_sol=np.append(Phi_sol,phi_s[0:nscans])
        Theta_lun=np.append(Theta_lun,theta_l[0:nscans])
        Phi_lun=np.append(Phi_lun,phi_l[0:nscans])
        HAM_side=np.append(HAM_side,hamside[0:nscans])
        DNB_seq=np.append(DNB_seq,nseq[0:nscans])
    # convert theta to deg.
    Theta_sol*=(180./np.pi)
    Theta_sol=(Theta_sol[0:-1]+Theta_sol[1:])/2  
    return [Theta_sol,Phi_sol,Theta_lun,Phi_lun, HAM_side,DNB_seq]
    
def DNB_Gain_Stage(L,LGS_DN0,MGS_DN0,HGS_DN0,transFrac=0.95,transZone=False,dnthresh=10):   
    gainState=np.zeros(L.shape,int)
    istrt=0
    DNthresh=transFrac * 2**14
    EVseq=AggSeqOrder()
    EVsmpls=EV_agg_samples()
    for iagg in range(0,64):
        ind=EVseq[iagg]
        Lsub=L[:,istrt:istrt+EVsmpls[iagg]]
        dn_HGS=Lsub/CalFac(ind,1)
        dn_MGS=Lsub/CalFac(ind,2)*2
        dn_LGS=Lsub/CalFac(ind,3)*2
        DN_HGS=dn_HGS + HGS_DN0[ind,:].mean()  
        DN_MGS=dn_MGS + MGS_DN0[ind,:].mean()   
        DN_LGS=dn_LGS + LGS_DN0[ind,:].mean()
        gainStatesub=np.zeros(Lsub.shape,int)
        gainStatesub[DN_HGS>DNthresh]+=1
        gainStatesub[DN_MGS>DNthresh]+=1
        if transZone:
            gainStatesub[dn_MGS>dnthresh]+=1
            gainStatesub[dn_LGS>dnthresh]+=1
        gainState[:,istrt:istrt+EVsmpls[iagg]]=gainStatesub   
        istrt+=EVsmpls[iagg]
    return gainState
def agg_zone_populate(pathdat,datfile,init=0,nfirst=1):
    if datfile==None:
            Val=None
    else:
        nsampagg=EV_agg_samples()
        Val_agg=pickler.import_pickle(pathdat+datfile)
        shp=Val_agg.shape
        ndet=shp[0]
        nagg=shp[1]    
        npix_scan=sum(nsampagg)
        Val=np.zeros([ndet,npix_scan],float)+init
        for j in range(0,nagg):
            nend=sum(nsampagg[0:j+1])
            for k in range(0,ndet):
                Val[k,nfirst:nend]=Val_agg[k,j]
            nfirst=nend
    return Val

def config_mapping(cnfg):
    if cnfg=='BL':
        aggseqfact_=aggseqfact_BL
        NaggEV_=NaggEV_BL
    if cnfg=='21':
        aggseqfact_=aggseqfact_21
        NaggEV_=NaggEV_21
    if cnfg=='21/26':
        aggseqfact_=aggseqfact_21_26
        NaggEV_=NaggEV_21_26
    npix=np.sum(aggseqfact_[2,:])
    subpix=aggseqfact_[1,0:NaggEV_]*aggseqfact_[2,0:NaggEV_]
    pix2subpix=np.zeros(npix)
    ipixstrt=0
    jpxstrt=0
    for j in range(0,NaggEV_):
        ipixend=np.sum(subpix[0:j+1])
        npx=aggseqfact_[2,j]
        jpxend=jpxstrt+npx
        iskip=aggseqfact_[1,j]
        pix2subpix[jpxstrt:jpxend]=np.arange(ipixstrt,ipixend,iskip)
        #print(jpxstrt,jpxend,ipixstrt,ipixend,iskip)
        ipixstrt=ipixend
        jpxstrt=jpxend
    pix2subpix=pix2subpix-pix2subpix[-2]
    pix2subpixout=pix2subpix#np.append(#,pix2subpix[-1:-npix:1])
    return pix2subpixout
def config_remap(cnfg_frm,cnfg_to):
    inds_to=config_mapping(cnfg_to)
    inds_frm=config_mapping(cnfg_frm)
    n_frm=int(inds_frm.shape[0])
    n_to=int(inds_to.shape[0])
    indx_to=np.arange(0,n_to)

    indx_frm=np.interp(inds_frm,inds_to,indx_to)
    indx_frm=np.append(indx_frm,2*n_to-indx_frm[-1:-n_frm-1:-1]-1)    
    return indx_frm
"""
______________________________________________________________________
                     DNB Plot Functions 
______________________________________________________________________        
"""
def plotMeanDif(pathgen, pathsub,refcal,naggs,pathsubref='',pltrad=True):
    StageName=['HGA','HGB','MGS','LGS']
    if len(pathsubref)==0:
        pathsubref=pathsub
    pathdat=pathgen+pathsub+'/data/'
    pathplot=pathgen+pathsub+'/plots/'
    pathdatref=pathgen+pathsubref+'/data/'
    mpl.rcParams['savefig.dpi']=300
    for istage in range(0,len(StageName)):
        filename=strcal[refcal]+StageName[istage]+'_DrkCal'
        ref_DNcalDrkmean=pickler.import_pickle(pathdatref+filename)
        #print(ref_DNcalDrkmean)
        #shp=ref_DNcalDrkmean.shape()
        ndet=16#shp[1]
        for ncal in range(0,len(strcal)):
                filename=strcal[ncal]+StageName[istage]+'_DrkCal'
                DNcalDrkmean=pickler.import_pickle(pathdat+filename)
                DNcalDelta=DNcalDrkmean-ref_DNcalDrkmean
                x=np.arange(1,naggs+1)
                clr='krgbycmkrgbycmrg'
                for k in range(0,ndet):
                    plt.plot(x,DNcalDelta[0:NaggEV,k],clr[k]+'x')
                plt.title(StageName[istage]+' Difference: ' +strcal[ncal]+' - '+ strcal[refcal] )
                plt.grid(True)                    
                plt.xlabel('Agg Seq.')
                plt.ylabel('counts')
                fileout=strcal[ncal]+'_'+strcal[refcal]+'_'+StageName[istage]+'_DrkDif'
                if pathsubref!=pathsub:
                    fileout=fileout+pathsubref    
                #print(pathplot+fileout+'.png')
                plt.savefig(pathplot+fileout+'.png')
                plt.close()
                if pltrad:
                    gain=CalFac(np.array(range(0,NaggEV)),istage)
                    for k in range(0,ndet):
                        plt.plot(x,gain*DNcalDelta[0:NaggEV,k],clr[k]+'x')
                    plt.title(StageName[istage]+' Difference: ' +strcal[ncal]+' - '+ strcal[refcal] )
                    plt.grid(True)                    
                    plt.xlabel('Agg Seq.')
                    plt.ylabel('W/(cm^2 sr)')
                    fileout=strcal[ncal]+'_'+strcal[refcal]+'_'+StageName[istage]+'_DrkDif'
                    if pathsubref!=pathsub:
                        fileout=fileout+pathsubref    
                    #print(pathplot+fileout+'rad.png')
                    plt.savefig(pathplot+fileout+'rad.png')
                    plt.close()
def plotDoubleDif(pathgen, pathsub,refcal,naggs,pathsub2,pltrad=True):
    StageName=['HGA','HGB','MGS','LGS']
    pathdat=pathgen+pathsub+'/data/'
    pathplot=pathgen+pathsub+'/plots/'
    pathdat2=pathgen+pathsub2+'/data/'
    mpl.rcParams['savefig.dpi']=300
    for istage in range(0,len(StageName)):
        #shp=ref_DNcalDrkmean.shape()
        ndet=16#shp[1]
        for ncal in range(0,len(strcal)):
                DNcalDrkmean=pickler.import_pickle(pathdat+strcal[ncal]+StageName[istage]+'_DrkCal')
                ref_DNcalDrkmean=pickler.import_pickle(pathdat+strcal[refcal]+StageName[istage]+'_DrkCal')
                DNcalDrkmean2=pickler.import_pickle(pathdat2+strcal[ncal]+StageName[istage]+'_DrkCal')
                ref_DNcalDrkmean2=pickler.import_pickle(pathdat2+strcal[refcal]+StageName[istage]+'_DrkCal')
                DNcalDelta=(DNcalDrkmean-ref_DNcalDrkmean)-(DNcalDrkmean2-ref_DNcalDrkmean2)
                x=np.arange(1,naggs+1)
                clr='krgbycmkrgbycmrg'
                for k in range(0,ndet):
                    plt.plot(x,DNcalDelta[0:NaggEV,k],clr[k]+'x')
                plt.title(StageName[istage]+' Difference: ' +strcal[ncal]+' - '+ strcal[refcal]+' Dates: '+pathsub+' & '+pathsub2 )
                plt.xlabel('Agg Seq.')
                plt.ylabel('counts')
                fileout=strcal[ncal]+'_'+strcal[refcal]+'_'+StageName[istage]+'_DoubleDrkDif'+pathsub2
                #print(pathplot+fileout+'.png')
                plt.grid(True)                    
                plt.savefig(pathplot+fileout+'.png')
                plt.close()
                if pltrad:
                    gain=CalFac(np.array(range(0,NaggEV)),istage)
                    for k in range(0,ndet):
                        plt.plot(x,gain*DNcalDelta[0:NaggEV,k],clr[k]+'x')
                    plt.title(StageName[istage]+' Difference: ' +strcal[ncal]+' - '+ strcal[refcal]+pathsub+'_'+pathsub2 )
                    plt.xlabel('Agg Seq.')
                    plt.ylabel('W/(cm^2 sr)')
                    fileout=strcal[ncal]+'_'+strcal[refcal]+'_'+StageName[istage]+'_DoubleDrkDif'+pathsub2
                    plt.grid(True)                    
                    plt.savefig(pathplot+fileout+'rad.png')
                    plt.close()
                    
"""
_____________________________________________________________________________
                    Moment Matching Destriping Technique
_____________________________________________________________________________
"""
def SDR_UniformityStats(pathhdf, pathdat, Nstage, sol_angl_thresh=[-90,90],
                    del_lo=1.e-10, uniformity=.05, Lhi=1.e-7, t_fromtostr=''):
    # determines mean and mean squared stats,used for moment-matching destrip 
    # information identifying the DNB SDR files

    ###########################Process Section#############################
    # get all the file names in the given directory
    lsfil=grn.granulefile_list(pathhdf,prefix,suffix)
    # select files within time range
    (grantimes,filename)=grn.granulefile_times(lsfil,t_fromtostr=t_fromtostr)
    nfiles=len(filename)
    # the number of samples for each agg zone by reflecting
    nsampagg=EV_agg_samples()    
    # number of agg zones across swath from agg seq. array
    nagg=len(nsampagg)
    # zero DN value without EV offset    
    LGS_DN0=pickler.import_pickle(pathdat+'BB_DNBLGS_DrkCal')
    MGS_DN0=pickler.import_pickle(pathdat+'BB_DNBMGS_DrkCal')
    HGS_DN0=pickler.import_pickle(pathdat+'BB_DNBHGA_DrkCal')    
    # initialize arrays
    N_samples=np.zeros([ndet,npix_scan],int)
    Lmn_sum=np.zeros([ndet,npix_scan],float)
    Lmn_sum_sqr=np.zeros([ndet,npix_scan],float)
    N_samples_agg=np.zeros([ndet,nagg],int)
    Lmn_sum_agg=np.zeros([ndet,nagg],float)
    Lmn_sum_sqr_agg=np.zeros([ndet,nagg],float)
    ## Loop over files
    for i in range(0,nfiles):
        [Theta_sol, Phi_sol, Theta_lun, Phi_lun, HAM_side,
         DNB_seq] = get_OBC_dat(pathhdf,filename[i])
        In_sol_rng=np.logical_and(Theta_sol>sol_angl_thresh[0],
                                  Theta_sol<=sol_angl_thresh[1])
        calseq=2*(DNB_seq-1)+HAM_side
        if Nstage==0:
            usescan=np.logical_or(calseq==0,calseq>8)
        else:
            usescan=np.ones(calseq.shape,bool)                         
        #print(np.any(In_sol_rng)) 
        if not np.any(In_sol_rng):
            continue
        # extract radiance from the file
        L=grn.get_h5_data(pathhdf,filename[i],DatasetGrp,'Radiance',ndet) 
        NstageL=DNB_Gain_Stage(L,LGS_DN0,MGS_DN0,HGS_DN0)
       # get the absolute radiance difference from one scan to the next
        dL=np.abs(L[ndet:,:]-L[:-ndet,:])
        # get the mean radiance for the same detectors from one scan to the enxt
        mnL=(L[ndet:,:]+L[:-ndet,:])*.5
        # mean gain stage (used to screen out mixed averages)        
        mnNstageL=np.array((NstageL[ndet:,:]+NstageL[:-ndet,:])/2,int)
        #uniformity tests
        nu=[]        
        uniform=np.logical_or(dL<del_lo,dL<uniformity*mnL)
        nu.append(np.sum(uniform))        
        uniform=np.logical_and(uniform,~np.isnan(mnL),~np.isinf(mnL))
        nu.append(np.sum(uniform))        
        uniform=np.logical_and(uniform,mnL<Lhi)
        nu.append(np.sum(uniform))        
        uniform=np.logical_and(uniform,mnNstageL==Nstage)
        nu.append(np.sum(uniform))
        #print(nu) 
        shp=L.shape
        # test to be sure that there SDR has factor of 16 in-track
        if len(Theta_sol)>0:        
            ratio=shp[0]/(len(Theta_sol)+1)
            #print('ratio',ratio)
        else:
            continue
        if ratio!=float(ndet):
            continue
        # determine number of scans from size of radiance array     
        shp=mnL.shape    
        nscn=int(shp[0]/ndet) 
        #print(nscn) 
       #loop thru scans
        for n in range(0,nscn):
            #criteria for selecting day data
             if In_sol_rng[n] and usescan[n]:
                unif_scn=uniform[n*ndet:(n+1)*ndet,:]
                mnL_scn=mnL[n*ndet:(n+1)*ndet,:]
                #add up number of samples passing tests            
                N_samples+=unif_scn
                #print('N_samples',N_samples.sum())                
                #sum for mean radiance            
                Lmn_sum+=mnL_scn*unif_scn      
                #sum for mean squared radiance            
                Lmn_sum_sqr+=(mnL_scn)**2*unif_scn      
    # first in-scan pixel of agg zone (skip first pixel which is corrupted)
    nfirst=1
    # loop through aggregtion zones
    for j in range(0,nagg):
        # set last pixel in aggregation zone    
        nend=sum(nsampagg[0:j+1])    
        #sum the radiances in-scan direction over the agg zone 
        Lmn_sum_agg[:,j]=np.sum(Lmn_sum[:,nfirst:nend],1)
        #sum the square of radiances in-scan direction over the agg zone 
        Lmn_sum_sqr_agg[:,j]=np.sum(Lmn_sum_sqr[:,nfirst:nend],1)
        #sum the number of samples that passed test    
        N_samples_agg[:,j]=np.sum(N_samples[:,nfirst:nend],1)
        nfirst=nend
    #Determine means from the sums divided by # of samples
    #print(N_samples_agg.max(),N_samples_agg.min(),N_samples_agg.mean())
    Lmn_agg=Lmn_sum_agg/N_samples_agg
    Lmn_sqr_agg=Lmn_sum_sqr_agg/N_samples_agg
    Lstdv_agg=np.sqrt(Lmn_sqr_agg-Lmn_agg**2)
    return [Lmn_agg,Lstdv_agg,N_samples_agg]
    
def destriping(L,gainStage,L_offset,Gain,nfirst=1):
    Lout=np.zeros(L.shape)  
    Lout[:,:]=L[:,:]    
    for i in range(0,3):
        if np.any(gainStage==i):
            if  Gain[i]!=None:
                shpgn=Gain[i].shape
                shpL=L.shape
                ndet=shpgn[0]
                nscans=int(shpL[0]/ndet)
                for n in range(0,nscans):
                    isStage=gainStage[n*ndet:(n+1)*ndet,:]==i
                    if np.any(isStage):                   
                        gain_mod=1/Gain[i]*isStage+(1-isStage)                                     
                        if np.all(L[n*ndet:(n+1)*ndet,:]<=fillskipscan):
                            #print('gain skipping ', n)                        
                            continue
                        #print(i,'gain',gain_mod.std())                    
                        Lout[n*ndet:(n+1)*ndet,nfirst:]*=gain_mod[:,nfirst:]
            if  L_offset[i]!=None:
                L_off=L_offset[i]
                shpLoff=L_off.shape
                shpL=L.shape
                ndet=shpLoff[0]
                nscans=int(shpL[0]/ndet)
                for n in range(0,nscans):
                    isStage=gainStage[n*ndet:(n+1)*ndet,:]==i
                    if np.all(Lout[n*ndet:(n+1)*ndet,:]<=fillskipscan):
                        #print('offset skipping ', n)                        
                        continue
                    if np.any(isStage[:,nfirst:]):                   
                        Loffmod=L_off*isStage           
                        print(i,'Loff std',Loffmod[:,nfirst:].std(),Loffmod[:,nfirst:].max(),Loffmod[:,nfirst:].min())                    
                        Lout[n*ndet:(n+1)*ndet,nfirst:]-=Loffmod[:,nfirst:]
    return Lout
def stage_file_merge(pathdat,stage_files,init=0):
    MergedArray=[]
    for i in range(0,3):
        if stage_files[i]==None:
            MergedArray.append(None)
        else:
            MergedArray.append(agg_zone_populate(pathdat,stage_files[i],init=init))
    return MergedArray
def destripeFiles(datestr,gain_files,L_offset_files,t_fromtostr='',Day=True,Night=True):
    datasetnm='Radiance'
    datasetnm2='Radiance_destriped'
    ###########################Process Section#############################
    [pathhdf,pathplt,pathdat]=setPaths(datestr)    
    # get all the file names in the given directory
    lsfil=grn.granulefile_list(pathhdf,prefix,suffix)
    # select files within time range
    (grantimes,filename)=grn.granulefile_times(lsfil,t_fromtostr=t_fromtostr)
    nfiles=len(filename)
    print(nfiles)
    # zero DN value without EV offset    
    LGS_DN0=pickler.import_pickle(pathdat+'BB_DNBLGS_DrkCal')
    MGS_DN0=pickler.import_pickle(pathdat+'BB_DNBMGS_DrkCal')
    HGS_DN0=pickler.import_pickle(pathdat+'BB_DNBHGA_DrkCal')    

    Gain=stage_file_merge(pathdat,gain_files,init=1.)
    L_offset=stage_file_merge(pathdat,L_offset_files,init=0)
    ## Loop over files
    for i in range(0,nfiles):
        DayNite=grnV.SDR_DayNite(pathhdf,filename[i],SDRname)
        #print(DayNite)            
        doDay= Day and (grn.any_str(DayNite,b'Day') or grn.any_str(DayNite,b'Both') )            
        doNite= Night and (grn.any_str(DayNite,b'Night') or grn.any_str(DayNite,b'Both') )            
        if not (doDay or doNite):
            #print(pltDay,pltNite,Day,Night)                
            continue
        # extract radiance from the file
        print('Destriping: '+filename[i])
        L=grn.get_h5(pathhdf,filename[i],DatasetGrp,datasetnm) 
        gainStage=DNB_Gain_Stage(L,LGS_DN0,MGS_DN0,HGS_DN0)
        Lmod=destriping(L,gainStage,L_offset,Gain)
        print('Std Dev',(Lmod-L).std()/L.std())        
        dat=h5py.File(pathhdf+filename[i],'r+')
        subdat=dat[DatasetGrp]
        Lrev=subdat.get(datasetnm2)
        print('Lrev',Lrev)        
        if Lrev==None:
            print('Lrev==None')
            a=subdat.create_dataset(datasetnm2, data=Lmod,dtype='float32',compression="gzip")
            print(a)
        else:
            Ldat=subdat[datasetnm2]
            if Ldat.shape==Lmod.shape:
                print('Modifying: '+filename[i])                
                Ldat[:,:]=Lmod[:,:]
        dat.close()

                        
