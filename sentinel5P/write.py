import zarr 
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from scipy.interpolate import griddata
from pyproj import Transformer, CRS
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import calculate_default_transform, reproject, Resampling

import reprojection
import os

qa_value = 0.5
is_no2 = True

path_base = "/home/simon/eodc_datasync/products/copernicus.eu/.incoming/s5p/"

datasets = []
for file in os.listdir(path_base):
        print(file)
        path = os.path.join(path_base, file)
        print(path)
        if file.startswith("S5P_OFFL"):
            try:
                datasets.append(reprojection.reproject_data(path, qa_value, is_no2))
            except (ValueError) as e:
                print(f"Warning file {file}: {e}")
                continue
        else:
            continue


merged = reprojection.merge_mean_by_time(datasets)

product_type = "NO2"
store_path = "/eodc/private/eodc_logs/s5p/s5p.zarr"

store = zarr.storage.LocalStore(store_path)
group = zarr.group(store=store, path=product_type)

time_origin = np.datetime64("2018-04-01")
time_min = (merged.time.min().values.astype("datetime64[D]") - time_origin).astype("int64")
time_max = (merged.time.max().values.astype("datetime64[D]") - time_origin).astype("int64")


for var in merged.data_vars:
    scale = group[var].attrs["scale_factor"]
    fill_value = group[var].attrs["_FillValue"]
    data = np.nan_to_num(np.round(group[var].values/scale), nan=fill_value)
    group[var][time_min:time_max, :, :] = data