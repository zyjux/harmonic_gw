"""
Functions for JPSS VIIRS processing
John M. Haynes (john.haynes@colostate.edu)
Last update: 2022/02/11 (update 0)

Data reading and writing:
    read_GMTCO
    read_GNBDO
    read_mband_sdr
    read_mmband_sdr
    read_dnb_sdr
"""

import glob
import h5py
import numpy as np
import os
import sys


def read_GMTCO(fin, return_pos=False):
    """
    Read geolocation (terrain corrected) and other data from a GMTCO granule

    Inputs:
      fin          a VIIRS GMTCO file
      return_pos   set to True to return solar/sensor zenith/azimuth
                   angles in dictionary d

    Returns:
      (longitude, latitude, d)

    Examples:
      Read longitude and latitude from file:

      >>> lon, lat, _ = read_GMTCO('GMTCO_npp_[...].h5')

      Also return solar zenith angle:

      >>> lon, lat, d = read_GMTCO('GMTCO_npp_[...].h5', return_pos=True)
      >>> print(d['solzen'])

    Modification history:
      2022/02/11  Written by John M. Haynes (john.haynes@colostate.edu)
    """

    f = h5py.File(fin, 'r')
    lon = np.array(f['All_Data/VIIRS-MOD-GEO-TC_All/Longitude'])
    lat = np.array(f['All_Data/VIIRS-MOD-GEO-TC_All/Latitude'])
    d = {}
    if return_pos:
        d['senazi'] = np.array(
            f['All_Data/VIIRS-MOD-GEO-TC_All/SatelliteAzimuthAngle'])
        d['senzen'] = np.array(
            f['All_Data/VIIRS-MOD-GEO-TC_All/SatelliteZenithAngle'])
        d['senrange'] = np.array(
            f['All_Data/VIIRS-MOD-GEO-TC_All/SatelliteRange'])
        d['solzen'] = np.array(
            f['All_Data/VIIRS-MOD-GEO-TC_All/SolarZenithAngle'])
        d['solazi'] = np.array(
            f['All_Data/VIIRS-MOD-GEO-TC_All/SolarAzimuthAngle'])

    f.close()
    return lon, lat, d


def read_GDNBO(fin, return_pos=False, return_lunar=False):
    """
    Read geolocation (terrain corrected) and other data from a GDNBO granule

    Inputs:
      fin            a VIIRS GDNBO file
      return_pos     set to True to return solar/sensor zenith/azimuth
                     angles in dictionary d
      return_lunar   set to True to return lunar zenith/azimuth angles, as
                     well as moon illumination fraction and phase, in
                     dictionary d

    Returns:
      (longitude, latitude, d)

    Examples:
      Read longitude and latitude from file:

      >>> lon, lat, _ = read_GDNBO('GDNBO_SVDNB_npp_[...].h5')

      Also return solar zenith angle:

      >>> lon, lat, d = read_GDNBO('GDNBO_SVDNB_npp_[...].h5', return_pos=True)
      >>> print(d['solzen'])

    Modification history:
      2022/02/28  Written by John M. Haynes (john.haynes@colostate.edu)
    """

    f = h5py.File(fin, 'r')
    lon = np.array(f['All_Data/VIIRS-DNB-GEO_All/Longitude_TC'])
    lat = np.array(f['All_Data/VIIRS-DNB-GEO_All/Latitude_TC'])
    d = {}
    if return_pos:
        d['senazi'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/SatelliteAzimuthAngle'])
        d['senzen'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/SatelliteZenithAngle'])
        d['senrange'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/SatelliteRange'])
        d['solzen'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/SolarZenithAngle'])
        d['solazi'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/SolarAzimuthAngle'])
    if return_lunar:
        d['lunzen'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/LunarZenithAngle'])
        d['lunazi'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/LunarAzimuthAngle'])
        d['lunif'] = np.array(
            f['All_Data/VIIRS-DNB-GEO_All/MoonIllumFraction'])
        d['lunpa'] = np.array(f['All_Data/VIIRS-DNB-GEO_All/MoonPhaseAngle'])

    f.close()
    return lon, lat, d


def read_mband_sdr(fin, allow_qf=None):
    """
    Read M-band data from a single VIIRS SDR

    Inputs:
      fin        a VIIRS SDR file
      allow_qf   a list of QF values (besides zero) that will not be set to
                 NaN in the returned data [values in list from 0..255]

    Returns:
      Data of shape (768, 3200). NaN is returned for missing/fill
      data, including any pixels where quality flag is not zero.

    Example:
      Read data from a single SDR:

      >>> dat = read_mband_sdr('SVM15_npp_[...].h5')

    Modification history:
      2022/02/10  Written by John M. Haynes (john.haynes@colostate.edu)
    """

    # Get band

    ch_s = os.path.basename(fin)[3:5]
    chi = int(ch_s)

    # Quality flag

    if not allow_qf:
        allow_qf = [0]
    else:
        allow_qf.extend([0])

    # Read data

    f = h5py.File(fin, 'r')
    vdata = _read_sdr_data(f, chi, allow_qf)
    f.close()

    return(vdata)


def read_mmband_sdr(data_dir, dt_qualifier, bands=None, allow_qf=None):
    """
    Read M-band data from multiple SDRs given a directory containing the
    granules and a data/time qualifier to match

    Inputs:
      data_dir       directory containing VIIRS SDR file(s)
      dt_qualifier   a date/time qualifier, like 'd20220131_t1723249_e1724491'
      bands          a list containing integers of M-bands to read (1..16);
                     default is to read all bands
      allow_qf       a list of QF values (besides zero) that will not be set
                     to NaN in the returned data [values in list from 0..255]

    Returns:
      Data for specified channels. Array will be of shape (768, 3200, nband).
      NaN is returned for missing/fill data, including any pixels where
      quality flag is not zero.

    Example:
      Read all data from a set of 16 SDRs:

      >>> dat = read_mmband_sdr('/mydata', 'd20220131_t1723249_e1724491')

      As above, but only for bands 1 through 3:

      >>> dat = read_mmband_sdr('/mydata', 'd20220131_t1723249_e1724491',
                                bands=[1,2,3])

    Modification history:
      2022/02/10  Written by John M. Haynes (john.haynes@colostate.edu)
    """

    # Bands to read

    if bands:
        band_list = ['{:0>2d}'.format(x) for x in bands]  # '01','02',..,'16'
    else:
        band_list = ['{:0>2d}'.format(x + 1) for x in range(16)]
    nband = len(band_list)

    # Output array

    vdata = np.empty((768, 3200, nband), dtype='float32')

    # Quality flag

    if not allow_qf:
        allow_qf = [0]
    else:
        allow_qf.extend([0])

    # Loop over bands

    for i, ch in enumerate(band_list):
        match_s = os.path.join(data_dir, 'SVM' + ch + '*' + dt_qualifier + '*')
        chi = int(ch)
        fname = glob.glob(match_s)
        if len(fname) != 1:
            print('Error finding VIIRS data:', match_s)
            sys.exit(1)

        # Read data

        f = h5py.File(fname[0], 'r')
        vdata[:, :, i] = _read_sdr_data(f, chi, allow_qf)
        f.close()

    return(vdata)


def read_dnb_sdr(fin, allow_qf=None):
    """
    Read DNB data from a single VIIRS SDR

    Inputs:
      fin        a VIIRS DNB SDR file
      allow_qf   a list of QF values (besides zero) that will not be set to
                 NaN in the returned data [values in list from 0..255]

    Returns:
      Data of shape (768, 3200). NaN is returned for missing/fill
      data, including any pixels where quality flag is not zero.

    Example:
      Read data from a single SDR:

      >>> dat = read_dnb_sdr('GDNBO-SVDNB_npp_[...].h5')

    Modification history:
      2022/02/10  Written by John M. Haynes (john.haynes@colostate.edu)
    """

    # Band is DNB

    chi = 'DNB'

    # Quality flag

    if not allow_qf:
        allow_qf = [0]
    else:
        allow_qf.extend([0])

    # Read data

    f = h5py.File(fin, 'r')
    vdata = _read_sdr_data(f, chi, allow_qf)
    f.close()

    return(vdata)


def _read_sdr_data(f, chi, allow_qf):
    """
    Internal SDR read procedure; not intended for user interface

    Inputs:
        f          file handle
        chi        integer M-band number [1..16], OR 'DNB'
        allow_qf   list of allowable quality flags

    Returns:
        SDR data
    """

    if chi == 'DNB':
        # DNB
        qf = np.array(f['/All_Data/VIIRS-DNB-SDR_All/QF1_VIIRSDNBSDR'])
        rad = np.array(f['/All_Data/VIIRS-DNB-SDR_All/Radiance'])
        bad_point = np.logical_or(rad < -990, ~np.isin(qf, allow_qf))
        vdata_ch = np.where(bad_point, np.nan, rad)

    else:
        if chi <= 11:
            # Channels 1-11 (indices 0-10) contain reflectances
            refl = np.array(
                f['/All_Data/VIIRS-M' + str(chi) + '-SDR_All/Reflectance'])
            try:
                factor = np.array(
                    f['/All_Data/VIIRS-M' + str(chi)
                        + '-SDR_All/ReflectanceFactors'])
                bad_point = np.logical_or(
                    refl >= 65528, ~np.isin(qf, allow_qf))
                vdata_ch = np.where(bad_point, np.nan,
                                    refl * factor[0] + factor[1])
            except KeyError:
                bad_point = np.logical_or(refl < -990, ~np.isin(qf, allow_qf))
                vdata_ch = np.where(bad_point, np.nan, refl)
        else:
            # Channels 12-16 (indices 11-15) contain brightness temperatures
            tb = np.array(f['/All_Data/VIIRS-M' + str(chi)
                            + '-SDR_All/BrightnessTemperature'])
            try:
                factor = np.array(
                    f['/All_Data/VIIRS-M' + str(chi)
                        + '-SDR_All/BrightnessTemperatureFactors'])
                bad_point = np.logical_or(tb >= 65528, ~np.isin(qf, allow_qf))
                vdata_ch = np.where(bad_point, np.nan,
                                    tb * factor[0] + factor[1])
            except KeyError:
                bad_point = np.logical_or(tb < -990, ~np.isin(qf, allow_qf))
                vdata_ch = np.where(bad_point, np.nan, tb)

    return(vdata_ch)
