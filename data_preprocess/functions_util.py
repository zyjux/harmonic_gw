"""
Common utility functions.

Katherine Haynes
Modified: 2022/02
"""

import numpy as np
import os
import pickle
from math import erf, sqrt

MISSING_VALUE = -999.


def checkNaN(Y, fillValue=MISSING_VALUE):
    """Routine to Ensure no NaNs occur"""
    YOut = Y.copy()
    nanRef = np.isfinite(Y)
    if (not np.all(nanRef)):
        print('NaNs in input!  Setting to {}'.format(fillValue))
        YOut[~nanRef] = fillValue
    return YOut


def find_index_of_nearest_xy(y_array, x_array, y_point, x_point):
    """Example Usage:
    # idy, idx = find_index_of_nearest_xy(\
    #       lat_array, lon_array, lat_point, lon_point)
    """
    distance = (y_array - y_point)**2 + (x_array - x_point)**2
    idy, idx = np.where(distance == distance.min())
    return idy[0], idx[0]


def find_square_refs_centered(array2D, squareSize):
    """Return lower-left references for centered square of specified size."""
    nx = np.shape(array2D)[1]
    ny = np.shape(array2D)[0]
    midx = int(nx / 2)
    midy = int(ny / 2)

    minDist = np.Inf
    badval = -999
    xRef = badval
    yRef = badval
    halfSquare = int(squareSize / 2)
    for i in range(nx - squareSize + 1):
        for j in range(ny - squareSize + 1):
            validSquare = array2D[j:j + squareSize, i:i + squareSize]
            validMin = np.min(validSquare)
            if validMin > badval:
                iMid = i + halfSquare
                jMid = j + halfSquare
                distNow = np.square(iMid - midx) + np.square(jMid - midy)
                if distNow < minDist:
                    xRef = i
                    yRef = j
                    minDist = distNow
    return xRef, yRef


def find_square_refs_left(array2D, squareSize):
    """Return left-most (lower) references for first valid square."""
    nx = np.shape(array2D)[1]
    ny = np.shape(array2D)[0]

    badval = -999
    xRef = badval
    yRef = badval

    i = 0
    while i < nx:
        j = 0
        while j < ny:
            iLast = i + squareSize
            jLast = j + squareSize
            if iLast < nx and jLast < ny:
                square = array2D[j:jLast, i:iLast]
                squareMin = np.min(square)
                if squareMin > badval:
                    xRef = i
                    yRef = j
                    i = nx
                    j = ny

            j += 1
        i += 1

    return xRef, yRef


def get_square_subsets_valid(array2D, squareSize, squareOverlap,
                             badval=MISSING_VALUE,
                             lat1D=None,
                             lon1D=None,
                             squareFirst='center',
                             squareOversize=None):
    """Return a dictionary containing the number and
    information for subsets of specific size (squareSize)
    covering a specific number of original pixels (squareSizeOversize)
    in data containing missing data."""

    aShape = np.shape(array2D)
    if len(aShape) == 3:
        array2D = array2D[0, :, :]

    nx = np.shape(array2D)[1]
    ny = np.shape(array2D)[0]
    if squareOversize is None:
        squareOversizex = nx
        squareOversizey = ny
    else:
        squareOversizex = squareOversize
        squareOversizey = squareOversize

    # ... Find first valid square references
    if squareFirst == 'center':
        xFirst, yFirst = find_square_refs_centered(array2D, squareSize)
    elif squareFirst == 'left':
        xFirst, yFirst = find_square_refs_left(array2D, squareSize)
    else:
        print("Invalid squareFirst option: {}".format(squareFirst))

    if xFirst < 0 or yFirst < 0:
        print("No valid squares found.")
        return None

    # ... find all possible squares
    xRefsPossible = []
    xNow = xFirst
    xNowLast = xFirst + squareSize
    xLast = np.max([xNowLast - squareOversizex, 0])
    while xNow >= xLast:
        xRefsPossible.append(xNow)
        xNow -= squareOverlap

    xNow = xFirst + squareOverlap
    xNowLast = xNow + squareSize
    xLast = np.min([xFirst + squareOversizex, nx])
    while xNowLast <= xLast:
        xRefsPossible.append(xNow)
        xNow += squareOverlap
        xNowLast += squareOverlap

    yRefsPossible = []
    yNow = yFirst
    yNowLast = yFirst + squareSize
    yLast = np.max([yNowLast - squareOversizey, 0])
    while yNow >= yLast:
        yRefsPossible.append(yNow)
        yNow -= squareOverlap

    yNow = yFirst + squareOverlap
    yNowLast = yNow + squareSize
    yLast = np.min([yFirst + squareOversizey, ny])
    while yNowLast < yLast:
        yRefsPossible.append(yNow)
        yNow += squareOverlap
        yNowLast += squareOverlap

    # ... save valid squares
    xRefsPossible.sort()
    yRefsPossible.sort()
    nSquares = 0
    xRefs = []
    yRefs = []
    squareTops = []
    squareBottoms = []
    squareLefts = []
    squareRights = []
    for i in xRefsPossible:
        iEnd = i + squareSize
        if iEnd <= nx:
            for j in yRefsPossible:
                jEnd = j + squareSize
                if jEnd <= ny:
                    square = array2D[j:jEnd, i:iEnd]
                    squareMin = np.min(square)
                    if squareMin > badval:
                        xRefs.append(i)
                        yRefs.append(j)
                        if lat1D is not None:
                            squareTops.append(lat1D[j + squareSize - 1])
                            squareBottoms.append(lat1D[j])
                        if lon1D is not None:
                            squareLefts.append(lon1D[i])
                            squareRights.append(lon1D[i + squareSize - 1])
                        nSquares += 1

    outLatLon = (lat1D is not None) or (lon1D is not None)
    if outLatLon:
        outDict = {
            'nSquares': nSquares,
            'squareBottoms': squareBottoms,
            'squareTops': squareTops,
            'squareLefts': squareLefts,
            'squareRights': squareRights,
            'xRefs': xRefs,
            'yRefs': yRefs}

        return outDict
    else:
        return xRefs, yRefs


def get_valid_squares(data, optDict, lat=None, lon=None,
                      returnRefs=False):
    """
    Take input images and subset them into
    squares for training, with only valid data.
    """

    errString = "GET_VALID_SQUARES ERROR:"
    try:
        subsetSquares = optDict['subsetSquares']
        squareSize = optDict['subsetSquareSize']
        squareOverlap = optDict['subsetSquareOverlap']
        squareOversize = optDict['subsetSquareOversize']
    except KeyError:
        print("{} Missing Data Options.".format(errString))
        return None

    if not subsetSquares:
        return np.expand_dims(data, axis=0)

    # ... find number of cases from subsetting
    xRefs, yRefs = get_square_subsets_valid(
        data, squareSize, squareOverlap,
        squareOversize=squareOversize)
    nSquares = len(xRefs)

    # ... put squares into data
    if len(data.shape) > 2:
        nFeats = np.shape(data)[2]
        dataNew = np.empty((nSquares, squareSize, squareSize, nFeats))
        if lon is not None:
            lonNew = np.empty((nSquares, squareSize, squareSize))
        if lat is not None:
            latNew = np.empty((nSquares, squareSize, squareSize))
        for s in range(nSquares):
            xStart = xRefs[s]
            xStop = xStart + squareSize
            yStart = yRefs[s]
            yStop = yStart + squareSize

            dataNew[s, :, :, :] = data[yStart:yStop, xStart:xStop, :]
            if lon is not None:
                lonNew[s, :, :] = lon[yStart:yStop, xStart:xStop]
            if lat is not None:
                latNew[s, :, :] = lat[yStart:yStop, xStart:xStop]
    else:
        dataNew = np.empty((nSquares, squareSize, squareSize))
        if lon is not None:
            lonNew = np.empty((nSquares, squareSize, squareSize))
        if lat is not None:
            latNew = np.empty((nSquares, squareSize, squareSize))
        for s in range(nSquares):
            xStart = xRefs[s]
            xStop = xStart + squareSize
            yStart = yRefs[s]
            yStop = yStart + squareSize
            dataNew[s, :, :] = data[yStart:yStop, xStart:xStop]
            if lon is not None:
                lonNew[s, :, :] = lon[yStart:yStop, xStart:xStop]
            if lat is not None:
                latNew[s, :, :] = lat[yStart:yStop, xStart:xStop]

    if lat is not None and lon is not None:
        if returnRefs:
            return dataNew, latNew, lonNew, yRefs, xRefs
        else:
            return dataNew, latNew, lonNew
    else:
        if returnRefs:
            return dataNew, yRefs, xRefs
        else:
            return dataNew


def pickle_dump(filename, data,
                protocol=pickle.DEFAULT_PROTOCOL,
                verbose=True):
    """
    Pickle file creation to dump variables.
    By default, use the default protocol.
    The other protocol option is pickle.HIGHEST_PROTOCOL
    """

    # check to make sure directory exists
    lRef = filename.rindex('/')
    filedir = filename[:lRef]
    if not os.path.isdir(filedir):
        os.makedirs(filedir)

    with open(filename, "wb") as handle:
        pickle.dump(data, handle, protocol=protocol)
    if verbose:
        print("Created File: {}".format(filename))
    return


def pickle_read(filename):
    """Pickle file read."""

    exists = os.path.isfile(filename)
    if exists:
        with open(filename, "rb") as handle:
            data = pickle.load(handle)
        return data
    else:
        print("PICKLE_READ FILE NOT FOUND: {}".format(filename))
        return None


def scale_eds(solar_zenith, lunar_zenith, lunar_fraction):
    """PURPOSE:
    Determine parameters for VIIRS Day/Night Band Enhanced Dynamic Scaling
    as described in Seamen et al. (2015)

    INPUTS:
    solar_zenith  solar zenith angle (deg)
    lunar_zenith  lunar zenith angle (deg)
    lunar_fraction  percent of lunar disk illuminated (0-100%)

    OUTPUTS:
        rmin, rmax   scaling parameters in equation (8) of Seamen et al. (2015)

    TO SCALE RADIANCE, COMMONLY:
        scaled_radiance = 255.*(((radiance-rmin)/(rmax-rmin))^0.5)

    REFERENCE:
        Seaman, C. J., and S. D. Miller, 2015: A dynamic scaling algorithm
        for the optimized digital display of VIIRS Day/Night Band imagery.
        Int. J. Remote Sens., 36, 1839–1854,
        https://doi.org/10.1080/01431161.2015.1029100.
    """

    lunar_fraction *= 0.01  # convert from % to decimal

    moon_factor1 = 0.7 * (1.0 - lunar_fraction)
    moon_factor2 = lunar_zenith * 0.0022

    maxval = 10. ** (-1.7 - (((2.65 + moon_factor1 + moon_factor2))
                             * (1 + erf((solar_zenith - 95.)
                                        / (5. * sqrt(2.0))))))
    minval = 10. ** (-4. - ((2.95 + moon_factor2)
                            * (1 + erf((solar_zenith - 95.)
                                       / (5. * sqrt(2.0))))))
    return minval, maxval
