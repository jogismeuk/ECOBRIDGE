"""
A simple script to delete unnecessary files and compact db for optimisation
Author: Jo Serra
Date: 04/09/2023
"""
import arcpy
from arcpy.sa import *
import arcgis
import pandas as pd
import numpy as np
import sys, os
def script_tool(param0, param1):
    arcpy.AddMessage("Start of temporary data deletion")
    df_list_cell = pd.Series(arcpy.ListRasters("cell_t_*"))
    for index, row in df_list_cell.items():
        arcpy.management.Delete(row)
        arcpy.AddMessage("Deleted intermediate cells " + str(index) + " of " + str(df_list_cell.size))
    df_list_masks = pd.Series(arcpy.ListFeatureClasses("mask_*"))
    for index, row in df_list_masks.items():
        arcpy.management.Delete(row)
        arcpy.AddMessage("Deleted intermediate masks " + str(index) + " of " + str(df_list_masks.size))
    df_list_ext = pd.Series(arcpy.ListRasters("Extr*"))
    for index, row in df_list_ext.items():
        arcpy.management.Delete(row)
        arcpy.AddMessage("Deleted intermediate extractions  " + str(index) + " of " + str(df_list_ext.size))
    for filename in os.listdir(arcpy.env.scratchFolder):
        os.remove(arcpy.env.scratchFolder + "\\" + filename)
        arcpy.AddMessage("Deleted temp file  " + filename)
    """Delete other misc files"""
    arcpy.AddMessage("End of temporary data deletion")
    arcpy.AddMessage("Compacting geodatabase starting...")
    arcpy.management.Compact(arcpy.env.workspace)
    arcpy.AddMessage("Compacting geodatabase ended")
    arcpy.AddMessage("Calculating majority pixels and rerasterising...")
    return
if __name__ == "__main__":
    param0 = "a"
    param1 = "b"
    script_tool(param0, param1)
    arcpy.SetParameterAsText(0, True)
