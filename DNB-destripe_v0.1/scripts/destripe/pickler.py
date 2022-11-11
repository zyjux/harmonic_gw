# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:08:01 2014

@author: Stephen Mills
copyright 2014, Renaissance Man Engineering Inc., all rights reserved

"""
import pickle
import gzip
import os
import sys
def export_pickle(a,filenm):
    fh=None
    try:
        fh = open(filenm,'wb')
        pickle.dump(a,fh,pickle.HIGHEST_PROTOCOL)
    except (EnvironmentError, pickle.PicklingError) as err:
        print("{0}: export error: {1}",format(os.path.basename(sys.argv[0]),err))
        return False
    finally:
        if fh is not None:
            fh.close()
            return True
        else:
            return False
def export_pickle_zip(a,filenm):
    fh=None
    try:
        fh = gzip.open(filenm,'wb')
        pickle.dump(a,fh,pickle.HIGHEST_PROTOCOL)
    except (EnvironmentError, pickle.PicklingError) as err:
        print("{0}: export error: {1}",format(os.path.basename(sys.argv[0]),err))
        return False
    finally:
        if fh is not None:
            fh.close()
            return True
        else:
            return False
def export_pickler(a,filnm,zipflg=False):
    if zipflg:
        ret=export_pickle_zip(a,filnm)
    else:
        ret=export_pickle(a,filnm)
    return ret            
def import_pickle(filenm,GZIP_MAGIC=b'\x1F\x8B'):    
    fh=None
    try:
        fh=open(filenm,'rb')
        magic=fh.read(len(GZIP_MAGIC))        
        if magic==GZIP_MAGIC:
            fh.close()
            fh=gzip.open(filenm,'rb')
        else:
            fh.seek(0)
        a=pickle.load(fh)
        return a
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("{0}: import error: {1}".format(os.path.basename(sys.argv[0]),err))
        return []