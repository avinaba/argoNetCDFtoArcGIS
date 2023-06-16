#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  ARGO NetCDF to ArcGIS parsable 
"""

__author__ = "Avin https://github.com/avinaba"
__version__ = "unofficial 0.0.1"
__license__ = "EUPL-1.2"

import argparse

import xarray as xr

#%% From argopy
# Author: ArgoPy contributers 
# License: EUPL 1.2
# Ref: https://github.com/euroargodev/argopy/blob/master/argopy/utilities.py

import sys
import numpy as np
import pandas as pd

# https://github.com/euroargodev/argopy/blob/e684df7b86b7062c48d385830b14e3a2f228d344/argopy/utilities.py#LL3643C33-L3643C33
def cast_Argo_variable_type(ds):
    """ Ensure that all dataset variables are of the appropriate types according to Argo references

    Parameter
    ---------
    :class:`xarray.DataSet`

    Returns
    -------
    :class:`xarray.DataSet`
    """

    list_str = [
        "PLATFORM_NUMBER",
        "DATA_MODE",
        "DIRECTION",
        "DATA_CENTRE",
        "DATA_TYPE",
        "FORMAT_VERSION",
        "HANDBOOK_VERSION",
        "PROJECT_NAME",
        "PI_NAME",
        "STATION_PARAMETERS",
        "DATA_CENTER",
        "DC_REFERENCE",
        "DATA_STATE_INDICATOR",
        "PLATFORM_TYPE",
        "FIRMWARE_VERSION",
        "POSITIONING_SYSTEM",
        "PARAMETER",
        "SCIENTIFIC_CALIB_EQUATION",
        "SCIENTIFIC_CALIB_COEFFICIENT",
        "SCIENTIFIC_CALIB_COMMENT",
        "HISTORY_INSTITUTION",
        "HISTORY_STEP",
        "HISTORY_SOFTWARE",
        "HISTORY_SOFTWARE_RELEASE",
        "HISTORY_REFERENCE",
        "HISTORY_QCTEST",
        "HISTORY_ACTION",
        "HISTORY_PARAMETER",
        "VERTICAL_SAMPLING_SCHEME",
        "FLOAT_SERIAL_NO",
        "PARAMETER_DATA_MODE",

        # Trajectory file variables:
        'TRAJECTORY_PARAMETERS', 'POSITION_ACCURACY', 'GROUNDED', 'SATELLITE_NAME', 'HISTORY_INDEX_DIMENSION',

        # Technical file variables:
        'TECHNICAL_PARAMETER_NAME', 'TECHNICAL_PARAMETER_VALUE', 'PTT',

        # Metadata file variables:
        'END_MISSION_STATUS',
        'TRANS_SYSTEM',
         'TRANS_SYSTEM_ID',
         'TRANS_FREQUENCY',
         'PLATFORM_FAMILY',
         'PLATFORM_MAKER',
         'MANUAL_VERSION',
         'STANDARD_FORMAT_ID',
         'DAC_FORMAT_ID',
         'ANOMALY',
         'BATTERY_TYPE',
         'BATTERY_PACKS',
         'CONTROLLER_BOARD_TYPE_PRIMARY',
         'CONTROLLER_BOARD_TYPE_SECONDARY',
         'CONTROLLER_BOARD_SERIAL_NO_PRIMARY',
         'CONTROLLER_BOARD_SERIAL_NO_SECONDARY',
         'SPECIAL_FEATURES',
         'FLOAT_OWNER',
         'OPERATING_INSTITUTION',
         'CUSTOMISATION',
         'DEPLOYMENT_PLATFORM',
         'DEPLOYMENT_CRUISE_ID',
         'DEPLOYMENT_REFERENCE_STATION_ID',
         'LAUNCH_CONFIG_PARAMETER_NAME',
         'CONFIG_PARAMETER_NAME',
         'CONFIG_MISSION_COMMENT',
         'SENSOR',
         'SENSOR_MAKER',
         'SENSOR_MODEL',
         'SENSOR_SERIAL_NO',
         'PARAMETER_SENSOR',
         'PARAMETER_UNITS',
         'PARAMETER_ACCURACY',
         'PARAMETER_RESOLUTION',
         'PREDEPLOYMENT_CALIB_EQUATION',
         'PREDEPLOYMENT_CALIB_COEFFICIENT',
         'PREDEPLOYMENT_CALIB_COMMENT',
    ]

    # [list_str.append("PROFILE_{}_QC".format(v)) for v in list(ArgoNVSReferenceTables().tbl(3)["altLabel"])] # HACK

    list_int = [
        "PLATFORM_NUMBER",
        "WMO_INST_TYPE",
        "WMO_INST_TYPE",
        "CYCLE_NUMBER",
        "CONFIG_MISSION_NUMBER",

        # Trajectory file variables:
        'JULD_STATUS', 'JULD_ADJUSTED_STATUS', 'JULD_DESCENT_START_STATUS',
        'JULD_FIRST_STABILIZATION_STATUS', 'JULD_DESCENT_END_STATUS', 'JULD_PARK_START_STATUS', 'JULD_PARK_END_STATUS',
        'JULD_DEEP_DESCENT_END_STATUS', 'JULD_DEEP_PARK_START_STATUS', 'JULD_DEEP_ASCENT_START_STATUS',
        'JULD_ASCENT_START_STATUS', 'JULD_ASCENT_END_STATUS', 'JULD_TRANSMISSION_START_STATUS',
        'JULD_FIRST_MESSAGE_STATUS', 'JULD_FIRST_LOCATION_STATUS', 'JULD_LAST_LOCATION_STATUS',
        'JULD_LAST_MESSAGE_STATUS', 'JULD_TRANSMISSION_END_STATUS', 'REPRESENTATIVE_PARK_PRESSURE_STATUS',
    ]
    list_datetime = [
        "REFERENCE_DATE_TIME",
        "DATE_CREATION",
        "DATE_UPDATE",
        "JULD",
        "JULD_LOCATION",
        "SCIENTIFIC_CALIB_DATE",
        "HISTORY_DATE",
        "TIME",

        # Metadata file variables:
        'LAUNCH_DATE', 'START_DATE', 'STARTUP_DATE', 'END_MISSION_DATE',
    ]

    def cast_this(da, type):
        """ Low-level casting of DataArray values """
        try:
            # da.values = da.values.astype(type)
            da = da.astype(type)
            da.attrs["casted"] = 1
        except Exception:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Fail to cast %s[%s] from '%s' to %s" % (da.name, da.dims, da.dtype, type))
            try:
                print("Unique values:", np.unique(da))
            except:
                print("Can't read unique values !")
                pass
        return da

    def cast_this_da(da):
        """ Cast any DataArray """
        # print("Casting %s ..." % da.name)
        da.attrs["casted"] = 0

        if v in list_str and da.dtype == "O":  # Object
            da = cast_this(da, str)

        if v in list_int:  # and da.dtype == 'O':  # Object
            if (
                    "conventions" in da.attrs
                    and da.attrs["conventions"] in ["Argo reference table 19", "Argo reference table 21"]
            ):
                # Some values may be missing, and the _FillValue=" " cannot be casted as an integer.
                # so, we replace missing values with a 999:
                val = da.astype(str).values
                val[np.where(val == 'nan')] = '999'
                da.values = val
            da = cast_this(da, int)

        if v in list_datetime and da.dtype == "O":  # Object
            if (
                    "conventions" in da.attrs
                    and da.attrs["conventions"] == "YYYYMMDDHHMISS"
            ):
                if da.size != 0:
                    if len(da.dims) <= 1:
                        val = da.astype(str).values.astype("U14")
                        # This should not happen, but still ! That's real world data
                        val[val == "              "] = "nan"
                        da.values = pd.to_datetime(val, format="%Y%m%d%H%M%S")
                    else:
                        s = da.stack(dummy_index=da.dims)
                        val = s.astype(str).values.astype("U14")
                        # This should not happen, but still ! That's real world data
                        val[val == "              "] = "nan"
                        s.values = pd.to_datetime(val, format="%Y%m%d%H%M%S")
                        da.values = s.unstack("dummy_index")
                    da = cast_this(da, 'datetime64[s]')
                else:
                    da = cast_this(da, 'datetime64[s]')

            elif v == "SCIENTIFIC_CALIB_DATE":
                da = cast_this(da, str)
                s = da.stack(dummy_index=da.dims)
                s.values = pd.to_datetime(s.values, format="%Y%m%d%H%M%S")
                da.values = (s.unstack("dummy_index")).values
                da = cast_this(da, 'datetime64[s]')

        if "QC" in v and "PROFILE" not in v and "QCTEST" not in v:
            if da.dtype == "O":  # convert object to string
                da = cast_this(da, str)

            # Address weird string values:
            # (replace missing or nan values by a '0' that will be cast as an integer later

            if da.dtype == "<U3":  # string, len 3 because of a 'nan' somewhere
                ii = (
                        da == "   "
                )  # This should not happen, but still ! That's real world data
                da = xr.where(ii, "0", da)

                ii = (
                        da == "nan"
                )  # This should not happen, but still ! That's real world data
                da = xr.where(ii, "0", da)

                # Get back to regular U1 string
                da = cast_this(da, np.dtype("U1"))

            if da.dtype == "<U1":  # string
                ii = (
                        da == ""
                )  # This should not happen, but still ! That's real world data
                da = xr.where(ii, "0", da)

                ii = (
                        da == " "
                )  # This should not happen, but still ! That's real world data
                da = xr.where(ii, "0", da)

                ii = (
                        da == "n"
                )  # This should not happen, but still ! That's real world data
                da = xr.where(ii, "0", da)

            # finally convert QC strings to integers:
            da = cast_this(da, int)

        if da.dtype != "O":
            da.attrs["casted"] = 1

        return da

    for v in ds.variables:
        try:
            ds[v] = cast_this_da(ds[v])
        except Exception:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Fail to cast: %s " % v)
            print("Encountered unique values:", np.unique(ds[v]))
            raise

    return ds
    


#%% Main 
if __name__ == "__main__":
    
    #%% Setup command line arguments 
    
    # Ref: https://github.com/eriknyquist/duckargs
    parser = argparse.ArgumentParser(description='',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  
    # Input NetCDF file as 1st positional argument
    parser.add_argument('input_ARGO_netcdf_file', type = argparse.FileType('r'), help = 'Specify the URI of the ARGO NetCDF file')
  
    # Specify whether we need verbose output
    parser.add_argument('-v', '--verbose', default = False, type = bool, help = 'flag for verbose output')
  
    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action = "version",
        version="%(prog)s (version {version})".format(version=__version__)
        )
  
  
    version="%(prog)s (version {version})".format(version=__version__)
    args = parser.parse_args()
    
    #%% Begin processing
    
    # Extract CLI arguments
    infile_URI = args.input_ARGO_netcdf_file.name 
    isVerbose = args.verbose
    
    
    if isVerbose: 
        print("Openinng : ", infile_URI)
        
        
    # Open NetCDF as Xarray 
    xr_ARGO = xr.open_dataset(infile_URI, engine="netcdf4", decode_cf=1, use_cftime=0, mask_and_scale=1)
    
    
    # Cast ARGO NetCDF data writable formats
    cast_Argo_variable_type(xr_ARGO)


    # Attach coordinates 
    xr_ARGO_w_coord = xr_ARGO.assign_coords(lon = (xr_ARGO.LONGITUDE), 
                                            lat = (xr_ARGO.LATITUDE), 
                                            time = (xr_ARGO.JULD_LOCATION), 
                                            depth = (xr_ARGO.N_LEVELS) )
    
    # Hacky naming sequence, assumes filenames end with ".nc"
    # But is the fastest
    outfile_URI = infile_URI[:-3] + "_processed.nc"
    
    # Write ArcGIS compatible NetCDF
    xr_ARGO_w_coord.to_netcdf(path = outfile_URI)
    
    if isVerbose: 
        print("Processed to : ", outfile_URI)