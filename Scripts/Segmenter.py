"""
Segmenter_ECB.py

Description:
    This script is designed to segment raster data based on transitions defined in a CSV file.
    It operates within the ArcGIS environment, utilizing arcpy and the Spatial Analyst extension for raster operations.
    The script reads a CSV file containing transition information, performs raster segmentation for each unique transition
    by subtracting scenario raster data from baseline raster data, and saves the resulting raster segments to a temporary database if they contain data.

Requirements:
    - ArcGIS Desktop or ArcGIS Pro with the Spatial Analyst extension licensed and enabled.
    - Python 3.x installed and configured with ArcGIS.
    - Pandas and NumPy libraries installed in the Python environment used by ArcGIS.

Inputs:
    - downscale: A CSV file containing transition table data.
    - path and db path: File system path and database path where the rasters and CSV file are located.

Outputs:
    - Rasters for each unique transition saved in a temporary database, provided they contain data.

Functions:
    - script_tool(para0): The main function that orchestrates the reading of the CSV file, performs raster segmentation for each transition, and saves the resulting rasters.

Usage:
    The script is intended to be used as a Script Tool within an ArcGIS toolbox. It requires setting up a tool interface with the appropriate parameters and configuring the environment settings,
    including the scratch folder location.

Example:
    To run this script as a Script Tool in ArcGIS, create a new tool in a custom toolbox and set the script file as the source.
    Define the necessary parameters for the CSV file path and the database path. Ensure that the Spatial Analyst extension is enabled before running the tool.

Notes:
    - The script assumes that the input rasters ('baseline' and 'scenario') are correctly formatted and located within the specified database path.
    - The output rasters are named using a convention that includes the transition identifiers and are saved in the ArcGIS scratch folder.

Author:
    Jo Serra
Date:
    04/09/2023
Version:
    1.0
ArcGIS Version:
    Compatible with ArcGIS Pro 3.2
Python Version:
    3.x
"""

import arcpy
# Esri start of added imports
# Esri end of added imports
from arcpy.sa import *
import arcgis
import pandas as pd
import numpy as np
import os
from pathlib import Path
def script_tool(para0):
    # Get the path parameter as text
    path = r'' + arcpy.GetParameterAsText(1)
    # Read the CSV file into a pandas DataFrame
    df_model = pd.read_csv(path)
    # Select only the first two columns and remove duplicates
    df_tile_change = df_model.iloc[:,[0,1]]
    df_tile_change = df_tile_change.drop_duplicates()
    # Log the start of the process
    arcpy.AddMessage("Starting low-resolution segmentation")
    for i, rows in df_tile_change.iterrows():
        # For each unique transition, perform raster operations
        baseline_tile = ExtractByAttributes("baseline", "Value = " + str(rows[0]))
        scenario_tile = ExtractByAttributes("scenario", "Value = " + str(rows[1]))
        # Subtract the scenario raster from the baseline raster to identify changes
        substracted_tile = baseline_tile - scenario_tile
        # Check if the resulting raster is entirely NoData; if so, skip saving
        nodataresult = arcpy.management.GetRasterProperties(substracted_tile,"ALLNODATA")
        if (nodataresult.getOutput(0) == "1"):
            arcpy.AddMessage("Omitting transition " + str(rows[0]) + " -> " + str(rows[1]) + "...")
        else:
            # Save the raster representing the transition
            substracted_tile.save(arcpy.env.scratchFolder + "\\t_" + str(rows[0]) + "_" + str(rows[1]) + ".tif")
            arcpy.AddMessage("Segmenting " + str(rows[0]) + "  -> " + str(rows[1]))
    # Log  the end of the process
    arcpy.AddMessage("End of low-resolution segmentation.")
    return
if __name__ == "__main__":
    # Call the script_tool function with a placeholder parameter
    script_tool("a")
    # Set the script tool's output parameter to True, indicating success
    arcpy.SetParameter(0, True)
