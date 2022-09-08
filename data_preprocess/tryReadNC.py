import netCDF4
import numpy as np

filename = "/Users/kdhaynes/Desktop/out.nc"

dataset = netCDF4.Dataset(filename)
lat = np.array(dataset.variables['lat'])
print("Lat Shape: {}, Min: {:.2f} and Max: {:.2f}".format(
    lat.shape, lat.min(), lat.max()))

lon = dataset.variables['lon'][:]
print("Lat Shape: {}, Min: {:.2f} and Max: {:.2f}".format(
    lon.shape, lon.min(), lon.max()))

rscaled = dataset.variables['rscaled'][:]
print("RScaled Shape: {}, Min: {:.2f} and Max: {:.2f}".format(
    rscaled.shape, np.nanmin(rscaled), np.nanmax(rscaled)))

rdnb = dataset.variables['rdnb'][:]
print("RDNB Shape: {}, Min: {:.2f} and Max: {:.2f}".format(
    rdnb.shape, np.nanmin(rdnb), np.nanmax(rdnb)))
dataset.close()
