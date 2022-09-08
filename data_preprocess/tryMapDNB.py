"""
Gravity Waves Research

Try Reading DNB Data.

Filename Tested:
filename = 'npp_d20181010_t1853414_e1855055_b36028_c20220118200341966425'

Filename TC Case 1 (23 N, -69 E):
filesuffix = '_nobc_ops.h5'
fileList = ['npp_d20171016_t0619049_e0624453_b30927_c20220118194618899804',
 'npp_d20171016_t0624466_e0630252_b30927_c20220118194615235230']

Filename TC Case 2 (14 N, -121 E):
filesuffix = '_noac_ops.h5'
Storm:
fileList = ['npp_d20170719_t1056184_e1057426_b29667_c20220118195338307107',
 'npp_d20170719_t1057438_e1059080_b29667_c20220118195338307107',
 'npp_d20170719_t1059092_e1100334_b29667_c20220118195338307107']

Gravity Waves:
fileList = ['npp_d20170719_t0916454_e0918096_b29666_c20220118195134555715',
 'npp_d20170719_t0918108_e0919350_b29666_c20220118195134555715']

Filename TC Case 3 (16 N, -130 E):
NO GRAVITY WAVES

Filename TC Case 4 (39 N, -66 E):
filesuffix = '_noac_ops.h5'
fileList = ['npp_d20180711_t0553263_e0554505_b34729_c20220118200228744535',
 'npp_d20180711_t0554518_e0556159_b34729_c20220118200250204856',
 'npp_d20180711_t0556172_e0557413_b34729_c20220118200250204856']

fileList = ['j01_d20180711_t0641492_e0643138_b03333_c20220118200127645306',
 'j01_d20180711_t0643150_e0644377_b03333_c20220118200127645306',
 'j01_d20180711_t0644390_e0646035_b03333_c20220118200127645306',
 'j01_d20180711_t0646047_e0647292_b03333_c20220118200206197883']

Filename TC Case 5 (28 N, -86 E):
filesuffix = '_noac_ops.h5'
fileList = ['npp_d20181010_t0732173_e0733415_b36021_c20220118200327774728',
 'npp_d20181010_t0733427_e0735069_b36021_c20220118200327774728']

# J01 East Side of TC
fileList = ['j01_d20181010_t0641060_e0642305_b04624_c20220118195630621950',
 'j01_d20181010_t0642317_e0643545_b04624_c20220118195630621950']

# J02 West Side of TC
fileList = ['j01_d20181010_t0820403_e0822048_b04625_c20220118200333725852',
 'j01_d20181010_t0822061_e0823288_b04625_c20220118200333725852']

Modified: 2022/03
"""

# %%
# Import libraries
import numpy as np
import functions_map as kfm
from cv2 import resize
from math import erf, sqrt
from functions_viirs import read_dnb_sdr, read_GDNBO
from functions_util import checkNaN, get_valid_squares
from functions_util import scale_eds
from var_opts import case20200424 as caseOpts
from var_opts import dataOpts001 as dataOpts

from importlib import reload


# %%
# User Options
# dirname = '/Users/kdhaynes/Data/cira/gravity_waves/images_class/'
dirData = '/mnt/data1/kdhaynes/gravity_waves/dnb_data/GravityWaves/'

scale_method = 'log'  # 'eds' or 'log' or 'custom'

createMap = False
createMapRefStart = 1000
createMapRefStop = 3200
createMapFactor = 0.10
plotRGB = True
saveMap = False

checkSpecific = False
checkLat = 28
checkLon = -86

createSquares = True
findSpecific = False
latSpecific = 27
lonSpecific = -102

createSquareMap = False
createSquareNum = 32
saveSquare = False

mapSquareLocation = True
sqLocRefStart = 1000
sqLocRefStop = 3200
sqLocMapFactor = 0.05
sqLocSquareNum = 32

showAllSquares = True
sqAllRefStart = 1000
sqAllRefStop = 3200
sqAllMapFactor = 0.1


# %%
# Read data and ancillary information
data = None
lat = None
lon = None
dataMeta = None
fileList = caseOpts['fileList']
for filename in fileList:
    fName = dirData + caseOpts['filePrefix'] + \
        filename + caseOpts['fileSuffix']
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
# Create map of data
if createMap:
    radMap = radScaled[:, createMapRefStart:createMapRefStop].copy()
    latMap = lat[:, createMapRefStart:createMapRefStop].copy()
    lonMap = lon[:, createMapRefStart:createMapRefStop].copy()

    xnew = int(radMap.shape[0] * createMapFactor)
    ynew = int(radMap.shape[1] * createMapFactor)
    radPlot = resize(radMap, dsize=(ynew, xnew))
    latPlot = resize(latMap, dsize=(ynew, xnew))
    lonPlot = resize(lonMap, dsize=(ynew, xnew))

    if plotRGB:
        radPlot = radPlot * 255.
        contourMin = 0
        contourMax = 255
    else:
        radPlot = radPlot
        contourMin = 0.
        contourMax = 1.
    print("Resized shape: {}, min: {:.2f}, and max: {:.2f}".format(
        radPlot.shape, radPlot.min(), radPlot.max()))

    if saveMap:
        indx = filename.index('_t')
        fileSave = filename + '_rscaled.png'
    else:
        fileSave = ''
    kfm.map_labels(radPlot, lonPlot, latPlot,
                   contourMin=contourMin,
                   contourMax=contourMax,
                   labelFormat='% .0f',
                   saveFile=fileSave,
                   title=filename)


# %%
# Check for specific lat/lon
if checkSpecific:
    latMin = lat.min()
    latMax = lat.max()
    lonMin = lon.min()
    lonMax = lon.max()
    if checkLat > latMin and checkLat < latMax \
            and checkLon > lonMin and checkLon < lonMax:
        print("Specific Lat/Lon May Be In File!")
    else:
        print("Specific Lat/Lon NOT In File.")


# %%
# Subset data into squares
if createSquares:
    radSquares, latSquares, lonSquares, yRefs, xRefs = get_valid_squares(
        radiance, dataOpts, lat=lat, lon=lon, returnRefs=True)
    nSquares = radSquares.shape[0]
    print("Created {} squares of {} x {}.".format(
        nSquares, radSquares.shape[1], radSquares.shape[2]))


# %%
# Find square with lat/lon specific
if createSquares and findSpecific:
    latMin = latSquares.min()
    latMax = latSquares.max()
    lonMin = lonSquares.min()
    lonMax = lonSquares.max()

    indxSpecific = None
    if latSpecific > latMin and latSpecific < latMax \
            and lonSpecific > lonMin and lonSpecific < lonMax:
        indxSpecific = None
        for i in range(radSquares.shape[0]):
            latMin = latSquares[i, ...].min()
            latMax = latSquares[i, ...].max()
            lonMin = lonSquares[i, ...].min()
            lonMax = lonSquares[i, ...].max()
            if latSpecific > latMin and latSpecific < latMax \
                    and lonSpecific > lonMin and lonSpecific < lonMax:
                indxSpecific = i
                print("Specific Index: {}".format(indxSpecific))

    if indxSpecific is None:
        print("Specific Lat/Lon Not In Squares Created From File!")
        print("   Lat Min= {:.2f}, Max= {:.2f}, Specific= {:.2f}".format(
            latMin, latMax, latSpecific))
        print("   Lon Min= {:.2f}, Max= {:.2f}, Specific= {:.2f}".format(
            lonMin, lonMax, lonSpecific))


# %%
# Create map of square
if createSquares and createSquareMap \
        and createSquareNum < nSquares:
    radPlotSq = radSquares[createSquareNum, :, :]
    latPlotSq = latSquares[createSquareNum, :, :]
    lonPlotSq = lonSquares[createSquareNum, :, :]
    reload(kfm)
    if saveSquare:
        fileSave = filename + '_square{}'.format(createSquareNum) + '.png'
    else:
        fileSave = ''

    contourMin = 0.
    contourMax = 1.
    kfm.map_labels(radPlotSq, lonPlotSq, latPlotSq,
                   contourMin=contourMin, contourMax=contourMax,
                   saveFile=fileSave)


# %%
# Create map of square location
if createSquares and mapSquareLocation \
        and sqLocSquareNum < nSquares:
    radScaledH = rad255[:, sqLocRefStart:sqLocRefStop]
    latH = lat[:, sqLocRefStart:sqLocRefStop]
    lonH = lon[:, sqLocRefStart:sqLocRefStop]
    xnew = int(radScaledH.shape[0] * sqLocMapFactor)
    ynew = int(radScaledH.shape[1] * sqLocMapFactor)
    radPlot = resize(radScaledH.copy(), dsize=(ynew, xnew))
    latPlot = resize(latH, dsize=(ynew, xnew))
    lonPlot = resize(lonH, dsize=(ynew, xnew))

    latSq = latSquares[sqLocSquareNum, :, :]
    lonSq = lonSquares[sqLocSquareNum, :, :]

    side1 = [[lonSq[0, 0], lonSq[0, -1]], [latSq[0, 0], latSq[0, -1]]]
    side2 = [[lonSq[0, 0], lonSq[-1, 0]], [latSq[0, 0], latSq[-1, 0]]]
    side3 = [[lonSq[-1, -1], lonSq[0, -1]], [latSq[-1, -1], latSq[0, -1]]]
    side4 = [[lonSq[-1, -1], lonSq[-1, 0]], [latSq[-1, -1], latSq[-1, 0]]]
    reload(kfm)
    kfm.map_labels_with_square(radPlot, lonPlot, latPlot,
                               squareSide1=side1,
                               squareSide2=side2,
                               squareSide3=side3,
                               squareSide4=side4)


# %%
# Create a map with all square locations shown
if createSquares and showAllSquares:
    radScaledH = rad255[:, sqAllRefStart:sqAllRefStop]
    latH = lat[:, sqAllRefStart:sqAllRefStop]
    lonH = lon[:, sqAllRefStart:sqAllRefStop]
    xnew = int(radScaledH.shape[0] * sqAllMapFactor)
    ynew = int(radScaledH.shape[1] * sqAllMapFactor)
    radPlot = resize(radScaledH.copy(), dsize=(ynew, xnew))
    latPlot = resize(latH.copy(), dsize=(ynew, xnew))
    lonPlot = resize(lonH.copy(), dsize=(ynew, xnew))

    reload(kfm)
    kfm.map_labels_with_squares(radPlot, lonPlot, latPlot,
                                lonSquares, latSquares)
