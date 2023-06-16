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

## Pre-Usage
So far this script has been tested in an Ubuntu 20.04 and Windows 10
machines with in a Python 3.9 environment with the following libraries:
 * xarray 2022.11.0
 * netcdf4 1.6.2
 * numpy 1.23.4
 * pandas 1.5.2

 For a minimal install, use the following install lines for conda
 ```BASH
 conda install xarray pandas numpy=1.23.4
 conda install -c conda-forge netcdf4
 ```
For a detailed and maximal list of libraries, open
https://github.com/avinaba/argoNetCDFtoArcGIS/conda_envs
and replicate my Ubuntu 20.04 or Windows 10 environment.

## Usage
Open a terminal or command prompt and activate the appropriate
environment.

Pass the NetCDF file as a command line input

Example usage for "sample_ARGO_profile.nc"
```BASH
python3 convert_ARGO_CLI.py sample_ARGO_profile.nc --verbose=true
Openinng :  sample_ARGO_profile.nc
Processed to :  sample_ARGO_profile_processed.nc
```

Example help print
```BASH
$ python3 convert_ARGO_CLI.py --help

usage: convert_ARGO_CLI.py [-h] [-v VERBOSE] [--version] input_ARGO_netcdf_file

positional arguments:
  input_ARGO_netcdf_file
                        Specify the URI of the ARGO NetCDF file

optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSE, --verbose VERBOSE
                        flag for verbose output (default: False)
  --version             show program's version number and exit
```

## Acknowledgement
Could not have quickly made this script without the generous
contributors of the ArgoPy project https://github.com/euroargodev/argopy/.
Big shout out for licensing their work under EUPL-1.2.  

[^netcdf]: Network Common Data Form (NetCDF): https://www.unidata.ucar.edu/software/netcdf/  
[^argo]: ARGO project website https://argo.ucsd.edu/
[^GODAE]: GODAE website (might give warning, I recommend opening with a ftp client): https://www.usgodae.org/ftp/outgoing/argo/.
[^arcgis]: ArcGIS Online: https://www.arcgis.com/index.html
