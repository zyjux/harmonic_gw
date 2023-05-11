import xarray as xr
from PIL import Image
import re
import pandas as pd
from tqdm import tqdm
from pathlib import Path

ds_fn = Path.home() / 'research_data/GravityWaves/preprocessed_images/bore_ex.nc'
ds = xr.open_dataset(ds_fn, cache=False)
ds['time'] = pd.to_datetime(ds.time)

for time in tqdm(ds.time):
    #print(time.values)
    patch = ds.rad255.sel(time=time).values

    (Path.home() / 'research_data/GravityWaves/preprocessed_images/full_ims').mkdir(exist_ok=True)

    sav_fn = Path.home() / 'research_data/GravityWaves/preprocessed_images/full_ims' / (re.sub(":", "-", str(time.values)[:-10]) + "_" + str(ds.satellite.sel(time=time).values) + "_log_image.png")

    im = Image.fromarray(patch).convert('L')
    im.save(sav_fn)
