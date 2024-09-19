"""
Classifier.py

Description:
    This script performs a raster reclassification based on specific class transitions defined in a CSV file.
    It requires arcpy and the Spatial Analyst extension for raster operations. 
    The script reads a list of raster files following a naming convention that indicates class transitions,
    filters these based on the transitions defined in the CSV file, and performs reclassification where necessary. 
    The reclassified rasters are then saved to a specified location.

Requirements:
    - ArcGIS Desktop or ArcGIS Pro with the Spatial Analyst extension licensed and enabled.
    - Python 3.2 or higher installed and configured with ArcGIS.
    - Pandas and NumPy libraries installed in the Python environment used by ArcGIS.

Inputs:
    - param0: Placeholder parameter (not used in the current implementation).
    - param1: Path to the CSV file containing downscale information for raster reclassification.

Outputs:
    - Reclassified raster files saved in the ArcGIS scratch folder. The naming convention for output files includes the initial and new class transitions, both for the tile and cell levels.

Usage:
    The script is intended to be used as a Script Tool within an ArcGIS toolbox. 
    It requires setting up a tool interface with the appropriate parameters (param0 and param1) and configuring
    the environment settings, including the scratch folder location.

Example:
    To run this script as a Script Tool in ArcGIS, create a new tool in a custom toolbox and set the script file as the source. Define two parameters:
    - Parameter 0: Unused (can be set as a dummy parameter).
    - Parameter 1: A file parameter allowing the user to specify the path to the CSV file with downscale information.

    Ensure that the Spatial Analyst extension is enabled before running the tool.

Notes:
    - The script assumes that raster files follow a specific naming pattern ('cell_t_*') to identify relevant files for processing.
    - The CSV file should contain columns for 'initial_tile_class', 'new_tile_class', 'initial_cell_class', and 'new_cell_class' to define the reclassification rules.
    - The script logs messages to the ArcGIS tool interface, including the start and end of the reclassification process and details about each reclassification performed.

Author:
    Jo Serra
Date:
    2024-01-01
Version:
    1.0
ArcGIS Version:
    Tested on ArcGIS 3.2
Python Version:
    3.x
"""

import sys, os, arcpy
import arcgis
import arcpy
import pandas as pd
import numpy as np
from arcpy.sa import * # Import spatial analyst tools for raster operations

def ScriptTool(param0, param1):
    # Retrieve the path parameter as text
    path = r'' + arcpy.GetParameterAsText(1)
    # Initialize a variable to track if any reclassification has occurred
    changed = False
    # Log start of the reclassification process
    arcpy.AddMessage('Starting reclassification module')
    # Create a Dataframe from the list of raster files with a specific naming pattern
    df_list_cell = pd.DataFrame(arcpy.ListRasters('cell_t_*'))
    # Read the csv file containing downscale information into a Dataframe
    df_downscale = pd.read_csv(path)
    # Iterate over each raster file identified
    for row in df_list_cell.iterrows():
        # Split the raster fine name to extract class transition information
        cell = pd.Series(row[1][0]).str.split('_')
        initial_tile_class = int(cell[0][2])
        new_tile_class = int(cell[0][3])
        # Filter the downscale Dataframe for the carrent transition
        df_cell_transition = df_downscale.loc[(df_downscale['initial_tile_class'] == int(initial_tile_class)) & (df_downscale['new_tile_class'] == int(new_tile_class))]
        # Select only the columns related to cell class transitions
        df_cell_transition = df_cell_transition[['initial_cell_class','new_cell_class']]
        # Initialise variable to hold the current raster being processed
        reclassed_cell = row[1][0]
        # Iterate over each transition in the filtered Dataframe
        for transition in df_cell_transition.iterrows():
            initial_cell_class = int(transition[1][0])
            new_cell_class = int(transition[1][1])
            # Check if reclassification is needed
            if initial_cell_class != new_cell_class:
                changed = True
                # Log the reclassification action
                arcpy.AddMessage("Reclassifying low resolution areas under baseline transition " + str(initial_tile_class) + " -> " + str(new_tile_class) + " with downscaled high resolution transition " + str(initial_cell_class) + "  ->  " + str(new_cell_class))
                # Perform the reclassification
                reclassed_cell = arcpy.sa.Reclassify(reclassed_cell, 'value', RemapValue([[initial_cell_class,new_cell_class]]))
        # If a change has occurred, save the reclassified raster
        if changed == True:
            destination = arcpy.env.scratchFolder + '\\rec_cell_' + str(initial_tile_class) + "_" + str(new_tile_class) + "_" + str(initial_cell_class) + "_" + str(new_cell_class) + '.tif'
            arcpy.management.CopyRaster(reclassed_cell, destination, '', None, "255", "NONE", "NONE", "8_BIT_UNSIGNED", "NONE", "NONE", "TIFF", "NONE", "CURRENT_SLICE", "NO_TRANSPOSE")
            changed = False
    # Log the exit from the reclassification module
    arcpy.AddMessage('Exiting reclassification module')
    # Begin process to delete initial transition frames
    arcpy.AddMessage('Deleting initial transition frames')
    try:
        # Set the workspace to the scratch folder
        arcpy.env.workspace = arcpy.env.scratchFolder
        # List and delete raster files with a specific naming pattern
        df_list_frames = pd.Series(arcpy.ListRasters("t_*"))
        for row in df_list_frames.items():
            arcpy.management.Delete(row[1])
    finally:
        # Log completion of deletion process
        arcpy.AddMessage('Finished deleting transition frames')
    return
if __name__ == "__main__":
    ScriptTool("a", "b")
    arcpy.SetParameter(0, True)
