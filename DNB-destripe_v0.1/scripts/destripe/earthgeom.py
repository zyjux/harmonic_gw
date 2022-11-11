# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:59:37 2015

@author: Ren
"""
import numpy as np
import math as mt
deg2rad=mt.pi/180
rad2deg=1./deg2rad
deg_default=999.

# earth radius
Re=6378.140
def EarthRad():
    return Re
def SatElev(h,ang_off_nadir):
    C=np.abs(np.deg2rad(ang_off_nadir))
    c=Re
    b=Re+h
    #law of sines
    sin_B=np.sin(C)/c*b
    B=np.arcsin(sin_B)
    SatElevAng=90-np.rad2deg(B)
    return SatElevAng
def SatToGroundDist(h,ang_off_nadir):
    C=np.abs(np.deg2rad(ang_off_nadir))
    c=Re
    b=Re+h
    cos_C=np.cos(C)
    #use law of cosines & quadratic eqn. to solve for a
    coef1=-2*b*cos_C
    coef0=b**2-c**2
    v=coef1**2-4*coef0
    if v<0:
        return None
    a=(-coef1-np.sqrt(v))/2
    return a
def GroundDist(h,ang_off_nadir):
    C=np.abs(np.deg2rad(ang_off_nadir))
    c=Re
    b=Re+h
    cos_C=np.cos(C)
    sin_C=np.sin(C)
    #use law of cosines & quadratic eqn. to solve for a
    coef1=-2*b*cos_C
    coef0=b**2-c**2
    v=coef1**2-4*coef0
    a=(-coef1-np.sqrt(v))/2
    #use law of sines
    sin_A=a*sin_C/c
    A=np.arcsin(sin_A)
    D=Re*A
    return D 
def AngOffNadir(h,ground_dist):
    c=Re
    b=Re+h
    A=ground_dist/Re
    cos_A=np.cos(A)
    sin_A=np.sin(A)
    #law of cosines
    a_sqr=c**2+b**2-2*c*b*cos_A
    a=np.sqrt(a_sqr)
    #law of sines
    sin_C=c*sin_A/a
    C=np.arcsin(sin_C)
    return np.rad2deg(C)

def great_circ(longfrm,latfrm,longto,latto,waypnts):
    lmda1=longfrm*deg2rad
    lmda2=longto*deg2rad
    phi1=latfrm*deg2rad
    phi2=latto*deg2rad
    lmda12=lmda2-lmda1
    sinlmda12=mt.sin(lmda12)     
    coslmda12=mt.cos(lmda12)
    cosphi1=mt.cos(phi1)     
    sinphi1=mt.sin(phi1)
    cosphi2=mt.cos(phi2)     
    sinphi2=mt.sin(phi2)
    if cosphi2!=0.:
        alph1=mt.atan2(sinlmda12,cosphi1*sinphi2/cosphi2-sinphi1*coslmda12) 
    else:
        alph1=0.
#    if cosphi1!=0.:
#        alph2=mt.atan2(sinlmda12,sinphi2*coslmda12-cosphi2*sinphi1/cosphi1) 
 #   else:
 #       alph2=0.
    sinalph1=mt.sin(alph1)
#    sinalph2=mt.sin(alph2)
    cosalph1=mt.cos(alph1)
#    cosalph2=mt.cos(alph2)
    sigma12=mt.atan2(mt.sqrt((cosphi1*sinphi2-sinphi1*cosphi2*coslmda12)**2
        +(cosphi2*sinlmda12)**2),sinphi1*sinphi2+cosphi1*cosphi2*coslmda12)  
    alph0=mt.atan2(sinalph1*cosphi1,mt.sqrt(cosalph1**2+(sinalph1*sinphi1)**2))
    cosalph0=mt.cos(alph0)
    sinalph0=mt.sin(alph0)
    if cosphi1!=0:
        sigma01 = mt.atan2(sinphi1/cosphi1,cosalph1)
    else:
        sigma01= 0.
    sigma02=sigma01+sigma12
    sinsigma01=mt.sin(sigma01)    
    cossigma01=mt.cos(sigma01)    
    sigma_wp=sigma01+waypnts*(sigma02-sigma01)
    sinsigma_wp=np.sin(sigma_wp)    
    cossigma_wp=np.cos(sigma_wp)    
    phi_wp=np.arctan2(cosalph0*sinsigma_wp,np.sqrt(cossigma_wp**2+sinalph0**2*sinsigma_wp**2))
    lmda01=mt.atan2(sinalph0*sinsigma01,cossigma01)    
    lmda0=lmda1-lmda01    
    lmda_wp=lmda0+np.arctan2(sinalph0*sinsigma_wp,cossigma_wp)
    lat_wp=phi_wp/deg2rad
    long_wp=lmda_wp/deg2rad
    return [long_wp,lat_wp]
def unit_sphere2cart(sphere):
    theta=sphere[0]
    phi=sphere[1]
    if theta.shape!=phi.shape: 
        return []
    costheta=np.cos(theta)
    x=costheta*np.cos(phi)
    y=costheta*np.sin(phi)
    z=np.sin(theta)
    return [x,y,z]
def unit_cart2sphere(cart):
    x=cart[0]
    y=cart[1]
    z=cart[2]
    #utest=np.sqrt(x**2+y**2+z**2)
    #meanutest=np.mean(utest)
    #stdutest=np.std(utest)
    #if abs(meanutest-1)>.0001 or stdutest>.0001:    
    #    print(np.mean(utest),np.std(utest))
    if x.shape!=y.shape or y.shape!=z.shape: 
        return []
    phi=np.arctan2(y,x)
    theta=np.arctan2(z,np.sqrt(x**2+y**2))
    return [theta,phi]
def unit_xrotate(cart,theta):
    #theta taken from y axis
    costheta=mt.cos(theta)
    sintheta=mt.sin(theta)
    y=cart[1]*costheta-cart[2]*sintheta
    z=cart[1]*sintheta+cart[2]*costheta
    x=cart[0]
    return[x,y,z]
def unit_yrotate(cart,theta):
    #theta from z axis
    costheta=mt.cos(theta)
    sintheta=mt.sin(theta)
    z=cart[2]*costheta-cart[0]*sintheta
    x=cart[2]*sintheta+cart[0]*costheta
    y=cart[1]
    return[x,y,z]
        
def unit_zrotate(cart,theta):
    #theta from x axis 
    costheta=mt.cos(theta)
    sintheta=mt.sin(theta)
    z=cart[2]
    x=cart[0]*costheta-cart[1]*sintheta
    y=cart[0]*sintheta+cart[1]*costheta
    return[x,y,z]
def unit_rotate_matrix(refaxis,theta):
    sintheta=mt.sin(theta)
    costheta=mt.cos(theta)
    u=refaxis/np.sqrt(np.sum(refaxis**2))
    R=np.zeros((3,3),float)
    R=np.array([[0,-u[2],u[1]],
                     [u[2],0,u[0]],
                    [-u[1],u[0],0]],float)*sintheta
    for i in range(0,3):
        R[i,i]=costheta
        for j in range(0,3):
            R[i,j]+=u[i]*u[j]*(1-costheta)
    return R
def unit_matrix_mult(R,cart):
    x=cart[0]
    y=cart[1]
    z=cart[2]
    xprime=R[0,0]*x+R[0,1]*y+R[0,2]*z
    yprime=R[1,0]*x+R[1,1]*y+R[1,2]*z
    zprime=R[2,0]*x+R[2,1]*y+R[2,2]*z
    return [xprime,yprime,zprime]
def delta_vector(x):
    dx=np.zeros(x.shape,float)                
    dx[1:]=x[1:]-x[0:-1]
    dx[0]=dx[1]
    return dx
def within180(xin):
    x=np.array(xin)   
    x[xin<-180.]+=360.                
    x[xin>=180.]-=360.                
    #x[x<-180.]+=360.                
    #x[x>180.]-=360.                
    return x                
def within360(xin):
    x=np.array(xin)   
    x[x<0.]+=360.                
    x[x>360.]-=360. 
    return x
    