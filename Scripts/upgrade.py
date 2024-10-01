"""Description:
    This script iterates through all raster files in the scratch memory that start t_ and end .tif.  It converts this rasters in polygons which are then used
    to extract the high-resolution pixels.
Requirements:
    - ArcGIS Desktop or ArcGIS Pro with the Spatial Analyst extension licensed and enabled.
    - Python 3.2 or higher installed and configured with ArcGIS.
    - Pandas, sys, os and NumPy libraries installed in the Python environment used by ArcGIS.
Inputs:
    - param0, 1: Placeholder parameter (not used in the current implementation).
Outputs:
    - Clipped raster files saved in the ArcGIS workspace folder. 
Usage:
    The script is intended to be used as a Script Tool within an ArcGIS toolbox. 
    It requires setting up a tool interface with the appropriate parameters (param0 and param1) and configuring
    the environment settings, including the scratch folder location.
Author:
    Josep Serra Gallego
Date:
    01/09/2024
Version:
    1.0
ArcGIS Version:
    Tested on ArcGIS 3.2
Python Version:
    3.x
"""
import arcpy
from arcpy.sa import *
import arcgis
import pandas as pd
import numpy as np
import sys, os
def script_tool(param0, param1):
    arcpy.env.snapRaster = "baseline"
    # List all rasters in the scratch folder
    for raster in os.listdir(arcpy.env.scratchFolder):
        if (raster.endswith(".tif") and raster.startswith("t_")):
            arcpy.AddMessage("Processing " + raster)
            # Convert raster to polygon
            polygon_output = arcpy.env.workspace + "\\mask_" + os.path.splitext(raster)[0]
            arcpy.conversion.RasterToPolygon(arcpy.env.scratchFolder + "\\" + raster, polygon_output, "NO_SIMPLIFY", "VALUE")
            outExtractByMask = ExtractByMask(arcpy.env.workspace + "\\cells", polygon_output, "INSIDE")
            # Save the output 
            outExtractByMask.save(arcpy.env.workspace + "\\cell_" + os.path.splitext(raster)[0])
    return
if __name__ == "__main__":
    param0 = "a"
    param1 = "b"
    script_tool(param0, param1)
    arcpy.SetParameterAsText(0, True)
