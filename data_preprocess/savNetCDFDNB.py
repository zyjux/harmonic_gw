"""
Gravity Waves Research

Create Images of DNB Data.

By Katherine Haynes
Edited by Lander Ver Hoef

Modified: 2022/09
"""

# %%
# Import libraries
import numpy as np
import xarray as xr
import pandas as pd
import os
import functions_map as kfm
from math import erf, sqrt
from functions_viirs import read_dnb_sdr, read_GDNBO
from functions_util import checkNaN, find_index_of_nearest_xy
from functions_util import scale_eds
from var_opts import caseOpts
import var_opts
import gc

caseList = [
    'bore20180114',
    'bore20180211_01',
    'bore20180211_02',
    'bore20180211_03',
    'bore20180320_01',
    'bore20180320_02',
    'bore20180320_03',
    'bore20180414_01',
    'bore20180414_02',
    'bore20180414_03',
    'bore20180415_01',
    'bore20180415_02',
    # 'bore20180415_03',
    'bore20180422_01',
    'bore20180422_02',
    'bore20180513_01',
    'bore20180513_02',
    # 'bore20200424'
    'bore20180519_01',
    'bore20180519_02',
    'bore20180519_03',
    'bore20180715',
    'bore20180808_01',
    'bore20180808_02',
    'bore20180813_01',
    'bore20180813_02',
    'bore20180813_03',
    'bore20180815_01',
    'bore20180815_02',
    'bore20181010_01',
    'bore20181010_02',
    'bore20181010_03',
    'bore20181010_04',
    'bore20181011_01',
    'bore20181011_02',
    'bore20181203_01',
    'bore20181203_02',
    'bore20181203_03',
    'bore20190531_01',
    'bore20190531_02',
    'bore20190609_01',
    'bore20190609_02',
    'bore20190609_03',
    'bore20190609_04',
    'bore20190609_05',
    'bore20190628_01',
    'bore20190628_02',
    'bore20190702_01',
    'bore20190702_02',
    'bore20190704_01',
    'bore20190704_02',
    'bore20190706_01',
    'bore20190706_02',
    'bore20190706_03',
    'bore20190730_01',
    'bore20190730_02',
    'bore20190730_03',
    'bore20200320_01',
    'bore20200320_02',
    'bore20200324',
    'bore20200424_01',
    'bore20200424_02',
    'bore20200616_01',
    'bore20200616_02',
]

# %%
# User Options
dirData = 'E:/research_data/2022_harmonic_gravity_waves/'
nc_savefn = 'E:/research_data/2022_harmonic_gravity_waves/preprocessed_images/bore_ex.nc'

scale_method = 'log'  # 'eds' or 'log' or 'custom'

ds = None

for case in caseList:

    caseDict = getattr(var_opts, case)

    # %%
    # Read data and ancillary information
    data = None
    lat = None
    lon = None
    dataMeta = None
    fileList = caseDict['fileList']
    for filename in fileList:
        fName = dirData + caseDict['filePrefix'] + filename + caseDict['fileSuffix']
        dataT = read_dnb_sdr(fName, allow_qf=list(range(256)))
        (lonT, latT, dataMetaT) = read_GDNBO(
            fName, return_pos=True, return_lunar=True)
        dataMetaT['datetime'] = [pd.to_datetime(filename[0:17], format="d%Y%m%d_t%H%M%S")]

        dataT = checkNaN(dataT)

        if data is None:
            data = dataT
        else:
            data = np.concatenate((data, dataT), axis=0)

        if lat is None:
            lat = latT
        else:
            lat = np.concatenate((lat, latT), axis=0)

        if lon is None:
            lon = lonT
        else:
            lon = np.concatenate((lon, lonT), axis=0)

        if dataMeta is None:
            dataMeta = dataMetaT
        else:
            for key in list(dataMeta.keys()):
                arrOld = dataMeta[key]
                arrNew = dataMetaT[key]
                dataMeta[key] = np.concatenate((arrOld, arrNew), axis=0)
    del dataT
    del lonT
    del latT
    del dataMetaT

    dataGoodRef = np.where(data >= 0.)
    dataGoodRef0 = np.where(data > 0.)
    print(f'Case: ' + case)
    print("Read data and ancillary information.")
    print("   Data shape= {}, min= {:.12f}, max= {:.12f}".format(
        data.shape, data[dataGoodRef].min(), data[dataGoodRef].max()))
    print("   Lat shape= {}, min= {:.2f}, and max= {:.2f}".format(
        lat.shape, lat.min(), lat.max()))
    print("   Lon shape= {}, min= {:.2f}, and max= {:.2f}".format(
        lon.shape, lon.min(), lon.max()))
    print("   Number of points non-NaN: {}, >0: {}".format(
        dataGoodRef[0].shape[0], dataGoodRef0[0].shape[0]))


    # %%
    # Determine contour levels
    if scale_method == 'eds':
        solar_zenith_array = dataMeta['solzen']
        solar_zenith = np.nanmean(solar_zenith_array)

        lunar_zenith_array = dataMeta['lunzen']
        lunar_zenith = np.nanmean(lunar_zenith_array)

        lunar_fraction_array = dataMeta['lunif']
        lunar_fraction = np.nanmean(lunar_fraction_array)

        lunar_fraction *= 0.01  # convert from % to decimal

        moon_factor1 = 0.7 * (1.0 - lunar_fraction)
        moon_factor2 = lunar_zenith * 0.0022

        maxval = 10. ** (-1.7 - (((2.65 + moon_factor1 + moon_factor2))
                                 * (1 + erf((solar_zenith - 95.)
                                            / (5. * sqrt(2.0))))))
        minval = 10. ** (-4. - ((2.95 + moon_factor2)
                                * (1 + erf((solar_zenith - 95.)
                                           / (5. * sqrt(2.0))))))

        rangeval = maxval - minval
        print("Calculated Minval= {:.12f} and Maxval={:.12f}".format(
            minval, maxval))

        minval1, maxval1 = scale_eds(solar_zenith, lunar_zenith, lunar_fraction)
        # if minval != minval1 or maxval != maxval1:
        #    print("Error in scale_eds routine!")
        #    print("    Scale_eds Minval= {:.12f} and Maxval={:.12f}".
        #      format(minval1, maxval1))
        rootbase = 2.
        radTemp = data.copy()

    elif scale_method == 'log':
        radLog = data.copy()
        radLog[dataGoodRef0] = np.log10(radLog[dataGoodRef0])
        print("Log Min={:.2f} and Max={:.2f}".format(
            np.min(radLog[dataGoodRef0]), np.max(radLog[dataGoodRef0])))
        radTemp = radLog
        del radLog

        minval = -10.25
        maxval = -8.75
        rangeval = maxval - minval
        rootbase = 1.

    elif scale_method == 'custom':
        radTemp = data.copy()
        minval = 2.6e-11
        maxval = 8.6e-10
        rangeval = maxval - minval
        rootbase = 3.

    else:
        print("Invalid scale_method: {}".format(scale_method))
        print("   Please change to eds, log, or custom.")
    del data

    # %%
    # Scale data
    radTemp = np.divide(np.subtract(radTemp, minval), rangeval, dtype=np.double)
    radTemp = np.where(radTemp < 0., 0., radTemp)
    radTemp = radTemp ** (1. / rootbase)  # np.sqrt(radTemp)

    radiance = radTemp
    del radTemp
    radMax = np.max(radiance)
    radMin = np.min(radiance)
    radScaled = np.where(radiance > 1.0, 1.0, radiance)
    print("Scaled Radiance Minval= {:.5f} and Maxval={:.5f}".format(
        radMin, radMax))


    # %%
    # Created scaled data ranging from 0-255
    rad255 = radScaled.copy() * 255
    print("0-255 Scaled Radiance Minval= {:.4f} and Maxval= {:.2f}".format(
        np.nanmin(rad255), np.nanmax(rad255)))
    del radScaled
    del radiance


    # %%
    # Create DataArray of data and concatenate into dataset
    case_ds = xr.Dataset(
        data_vars=dict(
            rad255=(["x", "y", "time"], np.expand_dims(rad255, axis=-1)),
            **{
                key: (["x", "y", "time"], np.expand_dims(dataMeta[key], axis=-1)) for key in [
                    'senzen',
                    'senazi',
                    'senrange',
                    'solzen',
                    'solazi',
                    'lunzen',
                    'lunazi',
                ]
            }
        ),
        coords=dict(
            lon=(["x", "y", "time"], np.expand_dims(lon, axis=-1)),
            lat=(["x", "y", "time"], np.expand_dims(lat, axis=-1)),
            time=(["time"], dataMeta['datetime'][0:1])
        )
    )
    if ds is None:
        ds = case_ds
        ds.to_netcdf(nc_savefn)
    else:
        ds = xr.open_dataset(nc_savefn)
        ds = xr.concat([ds, case_ds], dim="time")
        ds.to_netcdf(nc_savefn)

    del ds
    del case_ds
    del rad255

    ds = 1

    gc.collect()
