# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:38:53 2015

@author: Ren
"""


import numpy as np
import granulemod as grn
import h5py
npixDNB=4064
fillval=-999.9
nscanpergran=48           
def DNB_CloudMask(pathhdf,filenmDNB,filenmCM,DNB_to_MOD,cldthresh=7):
    datasetgrp='/All_Data/VIIRS-DNB-SDR_All/'
    datasetgrpCM='/All_Data/VIIRS-CM-IP_All/'
    ndet=16
    Nscan=grn.get_h5(pathhdf,filenmDNB,datasetgrp,'NumberOfScans')  
    CldMsk=grn.get_h5_data_int(pathhdf,filenmCM,datasetgrpCM,'QF1_VIIRSCMIP',ndet,Nscan=Nscan)      
    if CldMsk==None:
        return None
    L_cldmsk=CldMsk>cldthresh
    CldMsk_DNB=remap(L_cldmsk,DNB_to_MOD)    
    return CldMsk_DNB
def remap(A, B_to_A,ndet_A=16,interpl=False):
    #print('A',A.mean(),A.max(),A.min())
    if A==None or B_to_A==None:
        return None
    BtoA_ind0=np.array(np.round(B_to_A[0]),int)
    BtoA_ind1=np.array(np.round(B_to_A[1]),int)
    #print('Number==',ndet_A,(BtoA_ind0==ndet_A).sum(),BtoA_ind0.max())    
    #print('Number>',ndet_A,(BtoA_ind0>ndet_A).sum(),BtoA_ind0.min())    
    #print('Number==',0,(BtoA_ind0==0).sum(),BtoA_ind0.min())    
    #print('Number==',ndet_A-1,(BtoA_ind0==ndet_A-1).sum(),BtoA_ind0.min())    
    BtoA_ind0[BtoA_ind0>=ndet_A]=ndet_A-1  
    nanval=np.logical_or(np.isnan(B_to_A[0]),np.isnan(B_to_A[1]))
    BtoA_ind0[nanval]=0
    BtoA_ind1[nanval]=0
    if interpl:
        BtoAind0_rem=B_to_A[0]-BtoA_ind0
        BtoAind1_rem=B_to_A[1]-BtoA_ind1
        BtoAind0_rem[nanval]=0
        BtoAind1_rem[nanval]=0
        iqnn=np.logical_and(BtoAind0_rem<=0,BtoAind1_rem<=0)
        iqnp=np.logical_and(BtoAind0_rem<=0,BtoAind1_rem>0)
        iqpn=np.logical_and(BtoAind0_rem>0,BtoAind1_rem<=0)
        iqpp=np.logical_and(BtoAind0_rem>0,BtoAind1_rem>0)
        d0=np.abs(BtoAind0_rem)        
        d1=np.abs(BtoAind1_rem)
        #print('delta',d0.min(),d0.max(),d1.min(),d1.max())        
        Wdenom= (1-d1)*(1-d0) + (1-d0)*d1+ (1-d1)*d0
        Wdenom= (1-d1)*(1-d0) + d1+ d0
        Wz=(1-d1)*(1-d0)/Wdenom
        W1=(1-d0)*d1/Wdenom
        W0=(1-d1)*d0/Wdenom
        W1=d1/Wdenom
        W0=d0/Wdenom
        #print(Wz.mean(),Wz.max(),Wz.min())
        #print(W0.mean(),W0.max(),W0.min()) 
        #print(W1.mean(),W1.max(),W1.min())
    shp=A.shape    
    shp_ind=BtoA_ind1.shape
    npixB=shp_ind[1]
    Nscn=int(shp[0]/ndet_A)
    shpB=[shp_ind[0]*Nscn,npixB]
    typeA=type(A[0,0])
    B=np.zeros(shpB,dtype=typeA)
    for i in range(0,Nscn):
        n=i*shp_ind[0]
        for j in range(0,shp_ind[0]):
            inds0=i*ndet_A+BtoA_ind0[j,:]
            inds1=BtoA_ind1[j,:]
            #notnan=np.logical_not(np.isnan(inds1))
            #print(i,j,A.shape,inds0.max(),BtoA_ind0.max())
            Az=A[inds0,inds1]
            if interpl:
                inds0p=inds0+1
                inds0p[inds0p>=shp[0]]=shp[0]-1                
                Ap0=A[inds0p,inds1]
                inds0m=inds0-1
                inds0m[inds0m<0]=0                
                An0=A[inds0m,inds1]
                inds1m=inds1+1
                inds1m[inds1m<0]=0                                
                A0n=A[inds0,inds1m]
                inds1p=inds1+1
                inds1p[inds1p>=shp[1]]=shp[1]-1                
                A0p=A[inds0,inds1p]

                Wz_=Wz[j,:]
                W0_=W0[j,:]
                W1_=W1[j,:]
                A0=Wz_*Az
                iqnn_=iqnn[j,:]
                iqnp_=iqnp[j,:]
                iqpn_=iqpn[j,:]
                iqpp_=iqpp[j,:]
                A0[iqnn_]+=W0_[iqnn_]*An0[iqnn_]+W1_[iqnn_]*A0n[iqnn_]
                A0[iqnp_]+=W0_[iqnp_]*An0[iqnp_]+W1_[iqnp_]*A0p[iqnp_]
                A0[iqpn_]+=W0_[iqpn_]*Ap0[iqpn_]+W1_[iqpn_]*A0n[iqpn_]
                A0[iqpp_]+=W0_[iqpp_]*Ap0[iqpp_]+W1_[iqpp_]*A0p[iqpp_]
                B[n+j,:]=A0                
            else:
                B[n+j,:]=Az
            B[n+j,nanval[j,:]]=fillval
    Bx=B[np.logical_not(np.isnan(B))]
    #print('B',Bx.mean(),Bx.max(),Bx.min())
    return B

def CloudMaskFilter(CldMsk,indx):
    if CldMsk==None:
        return None
    if indx==None:
        return None
    
    iscld=CldMsk[indx[:,0],indx[:,1]]
    return iscld

def get_radiance(pathhdf,filenm,band,datasetnm='Radiance'):
    if band[1]=='0':
        bnd=band[0]+band[2]
    else:
        bnd=band
    if bnd[0]=='M':
        ndet=16
        nbnd=int(bnd[1:])
    elif bnd[0]=='D':
        ndet=16
        nbnd=0
    elif bnd[0]=='I':
        ndet=32
        nbnd=16+int(bnd[1:])
    else:
        print('Invalid band name')
        return None
    datasetgrp='/All_Data/VIIRS-'+bnd+'-SDR_All/'    
    if np.any(nbnd==np.array([0,1,2,3,4,5,7,13])):             
        L=grn.get_h5_data(pathhdf,filenm,datasetgrp,datasetnm,ndet)
    else:
        L=grn.get_h5_data_scaled(pathhdf,filenm,datasetgrp,datasetnm,ndet)
    return L

def get_geoloc(pathhdf,filenm,BandGroup,datasetnm,terrain_corr=False):
    if BandGroup[0:3]=='MOD' or BandGroup=='DNB':
        ndet=16
    elif BandGroup[0:3]=='IMG':
        ndet=32
    else:
        print('Invalid band name')
        return None
    if terrain_corr:
        str_tc='-TC'
    else:
        str_tc=''
    datasetgrp='/All_Data/VIIRS-'+BandGroup+'-GEO'+str_tc+'_All/'    
    G=grn.get_h5_data(pathhdf,filenm,datasetgrp,datasetnm,ndet)
    return G
def matchRdncGeoFiles(pathhdf,t_fromtostr,band):
    #format for band, caps only, 2 digit band no. e.g. 'I01', 'DNB', 'M06'    
    prefix='SV'+band
    if band=='DNB':
        gprefix='GDNBO'
    elif band[0]=='I':
        gprefix=='GIMGO'
    elif band[0]=='M':
        gprefix=='GMODO'
    else:
        print('band name not recognized')
        return None
    (grntm_G,GeoFileList)=grn.granulefile_list_sort_pare(pathhdf,gprefix,
                                    'h5',t_fromtostr)
    (grntm_R,RadFileList)=grn.granulefile_list_sort_pare(pathhdf,prefix,
                                    'h5',t_fromtostr)
    nRfile=len(RadFileList)
    nGfile=len(GeoFileList)
    GeoFileListOut=[]
    RadFileListOut=[]
    for i in range(0,nGfile):
        for j in range(0,nRfile):
            if np.all(grntm_R[:,j]==grntm_G[:,i]):
                GeoFileListOut.append(GeoFileList[i])
                RadFileListOut.append(RadFileList[j])
    return (RadFileListOut,GeoFileListOut)
def lat_lon_dist(Lat1,Lon1,Lat2,Lon2):
    Re=6378.14    
    cosLatmn=np.cos(np.deg2rad(Lat1+Lat2)/2)
    x=np.deg2rad(Lon2-Lon1)*cosLatmn     
    y=np.deg2rad(Lat2-Lat1)
    d=np.sqrt(x**2+y**2)
    return d*Re
def make_geo_remap(pathhdf,datatypes,time_rng,delt_thresh,nwindow=[-4,4]):
    suffix='h5'
    Lat=[]
    Lon=[]
    inscnoff=[]
    sz=[]
    ndets=[]
    for datatype in datatypes:
        prefix='G'+datatype+'O'
        filelist=grn.granulefile_list_sort(pathhdf,prefix,suffix,time_rng)
        filenms=filelist[1]
        if len(filenms)>1:
            print('time_rng not specific enough')
        filenm=filenms[0]
        if(datatype=='IMG'):
            ndet=32
        else:
            ndet=16
        if(datatype=='DNB'):
            inscnoff.append(9)
        else:
            inscnoff.append(0)
        datasetgrp='/All_Data/VIIRS-'+datatype+'-GEO_All/'
        Lt=grn.get_h5_data(pathhdf,filenm,datasetgrp,'Latitude',ndet)
        Lat.append(Lt)
        Ln=grn.get_h5_data(pathhdf,filenm,datasetgrp,'Longitude',ndet)
        Lon.append(Ln)
        ndets.append(ndet)
        sz.append(Lt.shape)
    Nscns=sz[0][0]/ndets[0]
    print(Nscns)
    Nscns=int(Nscns)
    ind_inscn=np.zeros([ndets[0],sz[0][1]])
    ind_intrk=np.zeros([ndets[0],sz[0][1]])
    delta=np.zeros([ndets[0],sz[0][1]])
    i=0
    mfrm=i*ndets[1]
    mto=mfrm+ndets[1]
    for j in range(0,ndets[0]):
        #print(i,j)
        md=i*ndets[0]+j        
        n=inscnoff[1]        
        for k in range(inscnoff[0],sz[0][1]):
            nfrm=max(0,n+nwindow[0])
            nto=min(n+nwindow[1],sz[1][1])
            #print(nfrm,nto)
            lat=Lat[0][md,k]
            lon=Lon[0][md,k]
            d=lat_lon_dist(lat,lon,Lat[1][mfrm:mto,nfrm:nto],Lon[1][mfrm:mto,nfrm:nto])
            szd=d.shape            
            q=np.argmin(d)
            delt=np.min(d)
            if delt>delt_thresh:
                pass                
                #print('fail threshold ',i,j,k,delt)
            mm=int(q/szd[1])
            kk=q%szd[1]
            n=nfrm+kk
            m=mm+mfrm
            ind_inscn[md,k]=n
            ind_intrk[md,k]=m
            m_nxt=[max(m-1,0),min(m+1,sz[1][0]-1)]
            n_nxt=[max(n-1,0),min(n+1,sz[1][1]-1)]
            lat_nr=Lat[1][m,n]
            lon_nr=Lon[1][m,n]
            dm=lat_lon_dist(lat,lon,Lat[1][m_nxt,n],Lon[1][m_nxt,n])
            qm=np.argmin(dm)
            m_x=m_nxt[qm]
            dincr_m=lat_lon_dist(lat_nr,lon_nr,Lat[1][m_x,n],Lon[1][m_x,n])
            dn=lat_lon_dist(lat,lon,Lat[1][m,n_nxt],Lon[1][m,n_nxt])
            qn=np.argmin(dn)
            n_x=n_nxt[qn]
            dincr_n=lat_lon_dist(lat_nr,lon_nr,Lat[1][m,n_x],Lon[1][m,n_x])
            #print(dm[qm],dn[qn],dincr_m,dincr_n,n,n_x,m,m_x)
            if dincr_n !=0:                
                ind_inscn[md,k]+=dn[qn]/dincr_n*(n_x-n)
            if dincr_m !=0: 
                ind_intrk[md,k]+=dm[qm]/dincr_m*(m_x-m)
            delta[md,k]=delt
            
            #print(i,j,k,mm,kk,d.shape)
            if delt!=d[mm,kk]:
               print('miscalculation ',i,j,k,delt,mm,kk)
    #points not mapped
    n_notmapped=np.isnan(ind_inscn).sum()
    if n_notmapped>0:
        print(n_notmapped,' points do not intersect')
    return (ind_intrk,ind_inscn,delta)
    
def add_EV_field(pathhdf,filename,DatasetGrp,datasetnm,Lc,datatype):
    if(datatype=='IMG'):
        ndet=32
    else:
        ndet=16
    try:
        dat=h5py.File(pathhdf+filename,'r')
    except OSError:
        print(filename+' not found')
        return None
    try:    
        Nscan=np.array(dat[DatasetGrp+'NumberOfScans'],int)
    except KeyError:
        print('number of scans not found')
        return None
    nr=Nscan.sum()*ndet

    if nr!=Lc.shape[0]:
        print('Size does not match',nr,Lc.shape[0],Nscan)
        return False
    else:
        ngran=len(Nscan)
        Lc_out=np.zeros([ndet*ngran*nscanpergran,Lc.shape[1]],type(Lc[0,0]))
    fullgran=(Nscan%nscanpergran)==0
    if np.all(fullgran):
        Lc_out=Lc
    else:
        mfrm=0
        for i in range(0,ngran):
            nscanlines=Nscan[i]*ndet
            nfrm=i*nscanpergran*ndet
            nto=nfrm+nscanlines
            mto=mfrm+nscanlines
            Lc_out[nfrm:nto,:]=Lc[mfrm:mto,:]
            mfrm=mto
    dat.close()
    try:
        dat2=h5py.File(pathhdf+filename,'r+')

    except OSError:
        print(pathhdf+filename+' not able to open to modify')
        return False    
    print(pathhdf+filename+' opened to modify')
    subdat=dat2[DatasetGrp]
    Lrev=subdat.get(datasetnm)
    if Lrev==None:
        print('Modifying '+filename+' by adding '+datasetnm+' field')                
        a=subdat.create_dataset(datasetnm, data=Lc_out,dtype='float32',compression="gzip")
    else:
        Ldat=subdat[datasetnm]
        if Ldat.shape==Lc_out.shape:
            print('Modifying '+filename+' by modifying '+datasetnm+' field')                
            Ldat[:,:]=Lc_out[:,:]
        else:
            print('size mismatch error')
    dat2.close()
    return True
def SDR_DayNite(pathhdf,filename,SDRname):
    DatasetGrp='/Data_Products/'+SDRname+'/'
    dat=h5py.File(pathhdf+filename,'r')
    d=dat[DatasetGrp + SDRname + '_Aggr']
    ngran=d.attrs['AggregateNumberGranules']
    Ngran=ngran[0,0]
    D_N=[]
    for i in range(0,Ngran):
        #print(i,DatasetGrp+SDRname+'_Gran_'+str(i),Ngran)
        d=dat[DatasetGrp+SDRname+'_Gran_'+str(i)]
        Day_Nite=d.attrs['N_Day_Night_Flag']
        D_N.append(Day_Nite[0,0])
        #print(D_N)
    dat.close()   
    return D_N

        
