## STAC - S5P

https://radiantearth.github.io/stac-browser/#/external/dev.stac.eodc.eu/api/v1/collections/Sentinel-5P?.language=de

-  **Asset Organization**
-  **One Collection = one Zarr store**  
-  **Each asset = one Zarr group**  
-  **Bands = variables inside that group**  
-  **`cube:variables` describes structure**  
-  **`raster:bands.name` = array names**
-  one link for zarr store: **media_type="application/octet-stream"** because **"application/vnd.zarr; version=3"** not supported
-  Extensions:
	- Datacube extension
	- Projection Extension
	- Raster Extension
