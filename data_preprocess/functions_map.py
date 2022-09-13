"""
Common mapping routines.

Katherine Haynes
Edited by Lander Ver Hoef
Modified: 2022/09
"""

# %%
# Import Libraries
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
import matplotlib.patches as patches


# %%
DEFAULT_COLOR_LIST = ['red', 'blue', 'green', 'orange']


# %%
# Plot interactivity functions
def print_click_xy(event):
    print(f'x: {event.xdata} and y: {event.ydata}')


def print_imloc_click_xy(fig, ax, event, imLocLatStart, imLocLonStart, squareSize):
    print(f'x: {event.xdata + imLocLonStart} and y: {event.ydata + imLocLatStart}')
    rect = patches.Rectangle(
        (event.xdata, event.ydata),
        squareSize,
        squareSize,
        edgecolor='cyan',
        facecolor=None
    )
    ax.add_patch(rect)
    fig.canvas.draw()


# %%
# Color Functions
def select_cmap(cmapString):
    """Select a colormap for contour plots."""

    vmin = None
    vmax = None
    if cmapString == 'brbg':
        cmap = 'BrBG'
    elif cmapString == 'cool':
        cmap = 'cool'
    elif cmapString == 'gray':
        cmap = 'gray'
    elif cmapString == 'green':
        cmap = 'Greens'
    elif cmapString == 'puor':
        cmap = 'PuOr'
    elif cmapString == 'pubu':
        cmap = 'PuBu'
    elif cmapString == 'rdbu':
        cmap = 'RdBu'
    elif cmapString == 'ylwrd':
        cmap = 'YlOrRd'
    else:
        print("Unknown Colormap: {}".format(cmapString))
        cmap = None

    return cmap, vmin, vmax


# %%
# Image Functions
def image_labels(data,
                 axisOff=True,
                 cmap='gray',
                 figSize=(12, 6),
                 fontSize=12,
                 saveFile='',
                 showColorBar=False,
                 title=''):

    cmap, vmin, vmax = select_cmap(cmap)
    fig, ax = plt.subplots(1, 1, figsize=figSize)
    im1 = ax.imshow(data, cmap=cmap, vmax=vmax, vmin=vmin)
    ax.set_title(title, fontsize=fontSize)
    if axisOff:
        ax.axis('off')
    if showColorBar:
        fig.colorbar(im1, ax=ax,
                     orientation='horizontal',
                     shrink=0.74, pad=0,
                     format='%.2f')

    if saveFile:
        save_figure(saveFile, plt)
    else:
        cid = fig.canvas.mpl_connect('button_press_event', print_click_xy)
        plt.show()
    plt.close()
    return


def image_labels_with_square(labels, xRefList, yRefList, squareSize,
                             imLocLatStart=None, imLocLonStart=None,
                             colorList=DEFAULT_COLOR_LIST,
                             cmap='gray', cvmin=None, cvmax=None,
                             figSize=(12, 6),
                             lineWidth=2, saveFile=''):

    cmap, vmin, vmax = select_cmap(cmap)
    if cvmin is not None:
        vmin = cvmin
    if cvmax is not None:
        vmax = cvmax

    fig, ax = plt.subplots(1, 1, figsize=figSize)

    for sq in range(len(xRefList)):
        xRefStart = xRefList[sq]
        yRefStart = yRefList[sq]
        xRefStop = xRefStart + squareSize
        yRefStop = yRefStart + squareSize

        side1 = [[xRefStart, xRefStart], [yRefStart, yRefStop]]
        side2 = [[xRefStop, xRefStop], [yRefStart, yRefStop]]
        side3 = [[xRefStart, xRefStop], [yRefStart, yRefStart]]
        side4 = [[xRefStart, xRefStop], [yRefStop, yRefStop]]

        ax.plot(side1[0], side1[1], color=colorList[sq], linewidth=lineWidth)
        ax.plot(side2[0], side2[1], color=colorList[sq], linewidth=lineWidth)
        ax.plot(side3[0], side3[1], color=colorList[sq], linewidth=lineWidth)
        ax.plot(side4[0], side4[1], color=colorList[sq], linewidth=lineWidth)

    ax.imshow(labels, cmap=cmap, vmax=vmax, vmin=vmin)
    ax.axis('off')

    if saveFile:
        save_figure(saveFile, plt)
    else:
        cid = fig.canvas.mpl_connect('button_press_event',
            lambda event: print_imloc_click_xy(fig, ax, event, imLocLatStart, imLocLonStart, squareSize))
        plt.show()
    plt.close()
    return


def image_labels_zoom(labels, xRefList, yRefList, squareSize,
                      colorList=DEFAULT_COLOR_LIST,
                      cmap='gray', cvmin=None, cvmax=None,
                      figSize=(12, 6),
                      saveFile='', titleList=None):

    cmap, vmin, vmax = select_cmap(cmap)
    if cvmin is not None:
        vmin = cvmin
    if cvmax is not None:
        vmax = cvmax

    for sq in range(len(xRefList)):
        xRefStart = xRefList[sq]
        yRefStart = yRefList[sq]
        xRefStop = xRefStart + squareSize
        yRefStop = yRefStart + squareSize

        fig, ax = plt.subplots(1, 1, figsize=figSize)
        ax.imshow(labels[yRefStart:yRefStop, xRefStart:xRefStop],
                  cmap=cmap, vmax=vmax, vmin=vmin)
        ax.axis('off')

        if titleList is None:
            ax.set_title('Square {} ({})'.format(sq + 1, colorList[sq]))
        else:
            ax.set_title(titleList[sq])

        if saveFile:
            sFile = saveFile + '{}'.format(sq + 1) + colorList[sq] + '.png'
            save_figure(sFile, plt)
        else:
            plt.show()

        plt.close()

    return


# %%
# Mapping Functions
def map_labels(labels, lon, lat,
               contours=None,
               contourMin=0.0,
               contourMax=1.0,
               checkContours=False,
               clabel='', cmap='gray',
               cShrink=0.74, cTicks=None,
               figSize=(14, 8), fontSize=16, gridLines=True,
               labelFormat=None,
               title='', saveFile=''):
    """Map Features With No Missing Data"""

    # Get valid data
    if contourMin is None:
        contourMin = np.nanmin(labels)
    if contourMax is None:
        contourMax = np.nanmax(labels)

    if contours is None:
        myNLevs = 32
        myAdd = (contourMax - contourMin) / (myNLevs - 2)
        contours = np.empty(myNLevs)
        for i in range(myNLevs):
            contours[i] = contourMin + i * myAdd - 0.5 * myAdd

    if contours[0] < 0. and contours[1] > 0.:
        labels = np.where(labels == 0., 1.e-6, labels)
        contours[0] = 0.

    if checkContours:
        print('Data Min: {:.3f} and Max {:.3f}'.format(
            labels.min(), labels.max()))
        print('Contours: {}'.format(contours))

    # Setup lat/lon
    minLat = np.nanmin(lat)
    maxLat = np.nanmax(lat)
    minLon = np.nanmin(lon)
    maxLon = np.nanmin(lon)
    if len(lat.shape) < 2:
        cLat = lat[int(np.size(lat) * 0.5)]
        cLon = lon[int(np.size(lon) * 0.5)]
        lon_2d, lat_2d = np.meshgrid(lon, lat)
    else:
        cLat = minLat + (maxLat - minLat) * 0.5
        cLon = minLon + (maxLon - minLon) * 0.5
        lon_2d = lon
        lat_2d = lat
    crs = ccrs.LambertConformal(central_longitude=cLon, central_latitude=cLat)

    # Create the figure and plot background
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=figSize,
                           subplot_kw={'projection': crs})

    # ax.set_extent([minLon, maxLon, minLat, maxLat])
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    # Draw the maps
    cmap, vmin, vmax = select_cmap(cmap)
    if labelFormat is None:
        labelFormat = '%.2f'
    cf = ax.contourf(lon_2d, lat_2d, labels, contours,
                     vmin=vmin, vmax=vmax,
                     cmap=cmap, transform=ccrs.PlateCarree())
    ax.set_title(title, fontsize=fontSize)
    if gridLines:
        ax.gridlines()
    cb = fig.colorbar(cf, ax=ax, format=labelFormat,
                      orientation='horizontal', shrink=cShrink, pad=0)
    cb.set_label(clabel, size='x-large')

    if cTicks is not None:
        tick_locator = ticker.MaxNLocator(nbins=cTicks)
        cb.locator = tick_locator
        cb.update_ticks()

    if saveFile == '':
        plt.show()
    else:
        save_figure(saveFile, plt)
    plt.close()

    return None


def map_labels_with_square(labels, lon, lat,
                           squareSide1=None,
                           squareSide2=None,
                           squareSide3=None,
                           squareSide4=None,
                           squareColor='blue',
                           squareWidth=2,
                           contours=None,
                           checkContours=False,
                           clabel='',
                           cmap='gray',
                           figSize=(14, 8),
                           gridLines=True,
                           labelFormat=None,
                           missingValue=-999,
                           saveFile='',
                           title=''):
    """Map Data With Square Outline."""

    # Get valid data
    goodRef = np.where(labels > missingValue)
    myMin = np.min(labels[goodRef])
    myMax = np.max(labels[goodRef])

    if contours is None:
        myNLevs = 32
        myAdd = (myMax - myMin) / (myNLevs - 2)
        contours = np.empty(myNLevs)
        for i in range(myNLevs):
            contours[i] = myMin + i * myAdd - 0.5 * myAdd

    if contours[0] < 0. and contours[1] > 0.:
        labels = np.where(labels == 0., 1.e-6, labels)
        contours[0] = 0.

    if checkContours:
        print('Data Min: {:.3f} and Max {:.3f}'.format(myMin, myMax))
        print('Contours: {}'.format(contours))

    # Setup lat/lon
    minLat = np.nanmin(lat)
    maxLat = np.nanmax(lat)
    minLon = np.nanmin(lon)
    maxLon = np.nanmin(lon)
    if len(lat.shape) < 2:
        cLat = lat[int(np.size(lat) * 0.5)]
        cLon = lon[int(np.size(lon) * 0.5)]
        lon_2d, lat_2d = np.meshgrid(lon, lat)
    else:
        cLat = minLat + (maxLat - minLat) * 0.5
        cLon = minLon + (maxLon - minLon) * 0.5
        lon_2d = lon
        lat_2d = lat
    crs = ccrs.LambertConformal(central_longitude=cLon, central_latitude=cLat)

    # Create the figure and plot background
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=figSize,
                           subplot_kw={'projection': crs})

    # ax.set_extent([minLon, maxLon, minLat, maxLat])
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    # Draw the maps
    cmap, vmin, vmax = select_cmap(cmap)
    if labelFormat is None:
        labelFormat = '%.0f'
    cf = ax.contourf(lon_2d, lat_2d, labels, contours,
                     vmin=vmin, vmax=vmax,
                     cmap=cmap, transform=ccrs.PlateCarree())
    ax.set_title(title, fontsize=16)
    if gridLines:
        ax.gridlines()
    cb = fig.colorbar(cf, ax=ax, format=labelFormat,
                      orientation='horizontal', shrink=0.74, pad=0)
    cb.set_label(clabel, size='x-large')

    # Add square
    squareTransform = ccrs.PlateCarree()
    if squareSide1 is not None:
        ax.plot(squareSide1[0], squareSide1[1],
                color=squareColor, linewidth=squareWidth,
                transform=squareTransform)
    if squareSide2 is not None:
        ax.plot(squareSide2[0], squareSide2[1],
                color=squareColor, linewidth=squareWidth,
                transform=squareTransform)
    if squareSide3 is not None:
        ax.plot(squareSide3[0], squareSide3[1],
                color=squareColor, linewidth=squareWidth,
                transform=squareTransform)
    if squareSide4 is not None:
        ax.plot(squareSide4[0], squareSide4[1],
                color=squareColor, linewidth=squareWidth,
                transform=squareTransform)

    if saveFile == '':
        plt.show()
    else:
        save_figure(saveFile, plt)
    plt.close()

    return None


def map_labels_with_squares(labels, lon, lat,
                            lonSquares, latSquares,
                            squareWidth=2,
                            contours=None,
                            checkContours=False,
                            clabel='',
                            cmap='gray',
                            figSize=(14, 8),
                            gridLines=True,
                            labelFormat=None,
                            missingValue=-999,
                            saveFile='',
                            title=''):
    """Map Data With Square Outline."""

    # Get valid data
    goodRef = np.where(labels > missingValue)
    myMin = np.min(labels[goodRef])
    myMax = np.max(labels[goodRef])

    if contours is None:
        myNLevs = 32
        myAdd = (myMax - myMin) / (myNLevs - 2)
        contours = np.empty(myNLevs)
        for i in range(myNLevs):
            contours[i] = myMin + i * myAdd - 0.5 * myAdd

    if contours[0] < 0. and contours[1] > 0.:
        labels = np.where(labels == 0., 1.e-6, labels)
        contours[0] = 0.

    if checkContours:
        print('Data Min: {:.3f} and Max {:.3f}'.format(myMin, myMax))
        print('Contours: {}'.format(contours))

    # Setup lat/lon
    minLat = np.nanmin(lat)
    maxLat = np.nanmax(lat)
    minLon = np.nanmin(lon)
    maxLon = np.nanmax(lon)
    if len(lat.shape) < 2:
        cLat = lat[int(np.size(lat) * 0.5)]
        cLon = lon[int(np.size(lon) * 0.5)]
        lon_2d, lat_2d = np.meshgrid(lon, lat)
    else:
        cLat = minLat + (maxLat - minLat) * 0.5
        cLon = minLon + (maxLon - minLon) * 0.5
        lon_2d = lon
        lat_2d = lat
    crs = ccrs.LambertConformal(central_longitude=cLon, central_latitude=cLat)

    # Create the figure and plot background
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=figSize,
                           subplot_kw={'projection': crs})

    # ax.set_extent([minLon, maxLon, minLat, maxLat])
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.5)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    # Draw the maps
    cmap, vmin, vmax = select_cmap(cmap)
    if labelFormat is None:
        labelFormat = '%.0f'
    cf = ax.contourf(lon_2d, lat_2d, labels, contours,
                     vmin=vmin, vmax=vmax,
                     cmap=cmap, transform=ccrs.PlateCarree())
    ax.set_title(title, fontsize=16)
    if gridLines:
        ax.gridlines()
    cb = fig.colorbar(cf, ax=ax, format=labelFormat,
                      orientation='horizontal', shrink=0.74, pad=0)
    cb.set_label(clabel, size='x-large')

    # Add squares
    squareTransform = ccrs.PlateCarree()
    nSquares = latSquares.shape[0]
    squareColorDict = {0: 'blue', 1: 'red', 2: 'green',
                       3: 'orange', 4: 'purple', 5: 'pink'}
    nSquareColors = len(list(squareColorDict.keys()))
    for i in range(nSquares):

        lonSqFirst = lonSquares[i, 0, 0]
        lonSqLast = lonSquares[i, -1, -1]
        lonSqM1 = lonSquares[i, 0, -1]
        lonSqM2 = lonSquares[i, -1, 0]
        latSqFirst = latSquares[i, 0, 0]
        latSqLast = latSquares[i, -1, -1]
        latSqM1 = latSquares[i, 0, -1]
        latSqM2 = latSquares[i, -1, 0]

        lonCond1 = lonSqFirst >= minLon and lonSqFirst <= maxLon
        lonCond2 = lonSqLast >= minLon and lonSqLast <= maxLon
        latCond1 = latSqFirst >= minLat and latSqFirst <= maxLat
        latCond2 = latSqLast >= minLat and latSqLast <= maxLat
        if lonCond1 and lonCond2 and latCond1 and latCond2:
            squareColor = squareColorDict[i % nSquareColors]
            ax.plot([lonSqFirst, lonSqM1],
                    [latSqFirst, latSqM1],
                    color=squareColor, linewidth=squareWidth,
                    transform=squareTransform)
            ax.plot([lonSqFirst, lonSqM2],
                    [latSqFirst, latSqM2],
                    color=squareColor, linewidth=squareWidth,
                    transform=squareTransform)
            ax.plot([lonSqLast, lonSqM1],
                    [latSqLast, latSqM1],
                    color=squareColor, linewidth=squareWidth,
                    transform=squareTransform)
            ax.plot([lonSqLast, lonSqM2],
                    [latSqLast, latSqM2],
                    color=squareColor, linewidth=squareWidth,
                    transform=squareTransform)

    if saveFile == '':
        plt.show()
    else:
        save_figure(saveFile, plt)
    plt.close()

    return None


# %%
# Misc Functions
def save_figure(fileName, fig, dpi=200):
    """Save a figure (e.g. png or eps)"""

    myType = fileName[-3:]
    if myType not in ['png', 'eps']:
        print("Expecting to save a png or eps file.")
    else:
        plt.savefig(fileName, bbox_inches="tight", format=myType, dpi=dpi)
        print("Saved File: {}".format(fileName))

    return
