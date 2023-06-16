# Argo-NetCDF for ArcGIS
Thin pre-processor for NetCDF[^netcdf] files from ARGO project[^argo] to make them compatible with ArcGIS import

## Bit of a history
I am looking into profile floats data from the ARGO project[^argo], hosted at Global Ocean Data Assimilation Experiment (GODAE) [^GODAE] :

I was hoping to do quick data-viz with ArcGIS [^arcgis] for they already have tools to import NetCDF data as part of their Multidimensional toolkit. [Read more about it in their post](https://pro.arcgis.com/en/pro-app/latest/help/data/multidimensional/a-quick-tour-of-netcdf-data.htm)

Unfortunately, I encountered are mismatch in expected import standard.

A week ago Mohamed (mahmed@esri.ca), demonstrated that NetCDF outputs
from ARGO, does not set the "Coordinates" of their outputs.

So, I made this stop-gap Python script pre-process NetCDFs so you may
may import them as Feature Layers in your ArcGIS project.

## Usage
So far this script has been tested in an Ubuntu 20.04 and Windows 10
machines with in a Python 3.9 environment with the following libraries:
 * xarray 2022.11.0
 * 

[^netcdf]: Network Common Data Form (NetCDF): https://www.unidata.ucar.edu/software/netcdf/  
[^argo]: ARGO project website https://argo.ucsd.edu/
[^GODAE]: GODAE website (might give warning, I recommend opening with a ftp client): https://www.usgodae.org/ftp/outgoing/argo/.
[^arcgis]: ArcGIS Online: https://www.arcgis.com/index.html
