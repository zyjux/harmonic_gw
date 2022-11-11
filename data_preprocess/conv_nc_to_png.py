import xarray as xr
from PIL import Image
import re
import pandas as pd
from tqdm import tqdm

ds_fn = "E:/research_data/2022_harmonic_gravity_waves/preprocessed_images/bore_ex.nc"
ds = xr.open_dataset(ds_fn, cache=False)
ds['time'] = pd.to_datetime(ds.time)

for time in tqdm(ds.time):
    #print(time.values)
    patch = ds.rad255.sel(time=time).values
    sav_fn = "E:/research_data/2022_harmonic_gravity_waves/preprocessed_images/full_ims/" + re.sub(":", "-", str(time.values)[:-10]) + "_log_image.png"

    im = Image.fromarray(patch).convert('L')
    im.save(sav_fn)
