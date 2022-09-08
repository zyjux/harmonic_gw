"""
Gravity Waves Research

Create Images of DNB Data.

Modified: 2022/03
"""

# %%
# Import libraries
import numpy as np
import functions_map as kfm
from math import erf, sqrt
from functions_viirs import read_dnb_sdr, read_GDNBO
from functions_util import checkNaN, find_index_of_nearest_xy
from functions_util import scale_eds
from var_opts import case20200424 as caseDict
from var_opts import caseOpts


# %%
# User Options
# dirname = '/Users/kdhaynes/Data/cira/gravity_waves/images_class/'
dirData = '/mnt/data1/kdhaynes/gravity_waves/dnb_data/GravityWaves/'

scale_method = 'log'  # 'eds' or 'log' or 'custom'

createImage = True
createImageRefStartLat = 0
createImageRefStopLat = -1
createImageRefStartLon = 0
createImageRefStopLon = -1
saveImage = False

checkLatLon = False

cmap = 'gray'
cvmin = 40
cvmax = 255
imageSquareLocation = True
saveImSqLoc = False
saveImSqLocFile = '_zoom_squares.png'

imageSquareZoom = True
saveImSqZoom = False


# %%
# Read data and ancillary information
data = None
lat = None
lon = None
dataMeta = None
fileList = caseDict['fileList']
for filename in fileList:
    fName = dirData + caseDict['filePrefix'] + \
        filename + caseDict['fileSuffix']
    dataT = read_dnb_sdr(fName, allow_qf=list(range(256)))
    (lonT, latT, dataMetaT) = read_GDNBO(
        fName, return_pos=True, return_lunar=True)
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

dataGoodRef = np.where(data >= 0.)
dataGoodRef0 = np.where(data > 0.)
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


# %%
# Scale data
radTemp = np.divide(np.subtract(radTemp, minval), rangeval, dtype=np.double)
radTemp = np.where(radTemp < 0., 0., radTemp)
radTemp = radTemp ** (1. / rootbase)  # np.sqrt(radTemp)

radiance = radTemp
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


# %%
# Create image of data
if createImage:
    radImage = rad255[
        createImageRefStartLat:createImageRefStopLat,
        createImageRefStartLon:createImageRefStopLon]
    if saveImage:
        fileSaveImage = fileList[0] + '_' + scale_method + '_image.png'
    else:
        fileSaveImage = ''
    kfm.image_labels(radImage, saveFile=fileSaveImage)


# %%
# Check for specific lat/lon
if checkLatLon:
    checkLat = caseDict['caseLat']
    checkLon = caseDict['caseLon']
    idy, idx = find_index_of_nearest_xy(
        lat, lon, checkLat, checkLon)


# %%
if imageSquareLocation:
    try:
        imLocLatStart = caseDict['imLocLatStart']
    except KeyError:
        imLocLatStart = 0
    try:
        imLocLatStop = caseDict['imLocLatStop']
    except KeyError:
        imLocLatStop = -1

    try:
        imLocLonStart = caseDict['imLocLonStart']
    except KeyError:
        imLocLonStart = 0

    try:
        imLocLonStop = caseDict['imLocLonStop']
    except KeyError:
        imLocLonStop = -1

    squareSize = caseOpts['subsetSquareSize']
    radScaledH = rad255[imLocLatStart:imLocLatStop,
                        imLocLonStart:imLocLonStop]

    xRefList = np.array(caseDict['xRefList']) - imLocLonStart
    yRefList = np.array(caseDict['yRefList']) - imLocLatStart

    if saveImSqLoc:
        saveFile = fileList[0] + saveImSqLocFile
    else:
        saveFile = ''
    kfm.image_labels_with_square(radScaledH, xRefList, yRefList, squareSize,
                                 cmap=cmap, cvmin=cvmin, cvmax=cvmax,
                                 saveFile=saveFile)


# %%
if imageSquareZoom:
    xRefList = caseDict['xRefList']
    yRefList = caseDict['yRefList']
    squareSize = caseOpts['subsetSquareSize']
    if saveImSqZoom:
        saveFile = fileList[0] + '_square'
    else:
        saveFile = ''
    kfm.image_labels_zoom(rad255, xRefList, yRefList, squareSize,
                          cmap=cmap, cvmin=cvmin, cvmax=cvmax,
                          saveFile=saveFile)
