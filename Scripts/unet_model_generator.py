# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2024-07-02 09:41:43
"""
import arcpy
from arcpy.sa import *
from arcpy.sa import *
from sys import argv

#For inline variable substitution, parameters passed as a String are evaluated using locals(), globals() and isinstance(). To override, substitute values directly.
def ECOTEST(Low_Resolution_Baseline="Low Resolution Baseline", Low_Resolution_Scenario="Low Resolution Scenario", High_Resolution_Baseline_2_="High Resolution Baseline", High_Resolution_Downscaled_Output="High Resolution Downscaled Output"):  # unet_model_generator

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")

    arcpy.ImportToolbox(r"C:\T6DinB\SED101.atbx")

    # Process: Copy Raster (4) (Copy Raster) (management)
    LRB = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\LRB"
    with arcpy.EnvManager(rasterStatistics="NONE"):
        arcpy.management.CopyRaster(in_raster=Low_Resolution_Baseline.__str__().format(**locals(),**globals())if isinstance(Low_Resolution_Baseline, str) else Low_Resolution_Baseline, out_rasterdataset=LRB, format="GRID")

    # Process: Copy Raster (Copy Raster) (management)
    LRS = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\LRS"
    with arcpy.EnvManager(rasterStatistics="NONE"):
        arcpy.management.CopyRaster(in_raster=Low_Resolution_Scenario.__str__().format(**locals(),**globals())if isinstance(Low_Resolution_Scenario, str) else Low_Resolution_Scenario, out_rasterdataset=LRS, format="GRID")

    # Process: Copy Raster (2) (Copy Raster) (management)
    HRB_2_ = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\HRB"
    with arcpy.EnvManager(rasterStatistics="NONE"):
        arcpy.management.CopyRaster(in_raster=High_Resolution_Baseline_2_.__str__().format(**locals(),**globals())if isinstance(High_Resolution_Baseline_2_, str) else High_Resolution_Baseline_2_, out_rasterdataset=HRB_2_, format="GRID", transform="NONE")

    # Process: Combine (2) (Combine) (sa)
    CL3 = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\CL3"
    Combine_2_ = CL3
    with arcpy.EnvManager(snapRaster="C:\\T6DinB\\Downscaler\\Downscaler.gdb\\downscaled_output_RAW"):
        CL3 = arcpy.sa.Combine([LRB, LRS, HRB_2_])
        CL3.save(Combine_2_)


    # Process: Add Fields (multiple) (2) (Add Fields (multiple)) (management)
    CL3_2_ = arcpy.management.AddFields(in_table=CL3, field_description=[["classname", "TEXT", "classname", "255", "", ""], ["classvalue", "SHORT", "classvalue", "", "", ""]])[0]

    # Process: Calculate Fields (multiple) (2) (Calculate Fields (multiple)) (management)
    CL3_4_ = arcpy.management.CalculateFields(in_table=CL3_2_, expression_type="PYTHON3", fields=[["classname", "str(!LRB!) + \"_\" + str(!LRS!) + \"_\" + str(!HRB!)", ""], ["classvalue", "!Value!", ""]])[0]

    # Process: Copy Raster (3) (Copy Raster) (management)
    HRD = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\HRD"
    with arcpy.EnvManager(rasterStatistics="NONE"):
        arcpy.management.CopyRaster(in_raster=High_Resolution_Downscaled_Output.__str__().format(**locals(),**globals())if isinstance(High_Resolution_Downscaled_Output, str) else High_Resolution_Downscaled_Output, out_rasterdataset=HRD, format="GRID")

    # Process: Combine (Combine) (sa)
    CL4 = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\CL4"
    Combine = CL4
    with arcpy.EnvManager(cellSize="MINOF", extent="MINOF", snapRaster="C:\\T6DinB\\Downscaler\\Downscaler.gdb\\downscaled_output_RAW"):
        CL4 = arcpy.sa.Combine([LRB, LRS, HRB_2_, HRD])
        CL4.save(Combine)


    # Process: Add Fields (multiple) (Add Fields (multiple)) (management)
    CL4_2_ = arcpy.management.AddFields(in_table=CL4, field_description=[["classname", "TEXT", "classname", "255", "", ""], ["classvalue", "SHORT", "classvalue", "", "", ""]])[0]

    # Process: Calculate Fields (multiple) (Calculate Fields (multiple)) (management)
    CL4_4_ = arcpy.management.CalculateFields(in_table=CL4_2_, expression_type="PYTHON3", fields=[["classname", "str(!LRB!) + \"_\" + str(!LRS!) + \"_\" + str(!HRB!) + \"_\" + str(!HRD!)", ""], ["classvalue", "!Value!", ""]])[0]

    # Process: Raster to Polygon (Raster to Polygon) (conversion)
    RasterT_CL41 = "C:\\T6DinB\\Downscaler\\Downscaler.gdb\\RasterT_CL41"
    with arcpy.EnvManager(snapRaster="C:\\T6DinB\\Downscaler\\Downscaler.gdb\\downscaled_output_RAW"):
        arcpy.conversion.RasterToPolygon(in_raster=CL4_4_, out_polygon_features=RasterT_CL41, simplify="NO_SIMPLIFY", raster_field="classvalue")

    # Process: Trainer (Trainer) (Dwnsclratbx)
    if CL3_4_ and RasterT_CL41:
        arcpy.Dwnsclratbx.Trainer()

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(cellSize="MINOF", extent="MINOF", outputCoordinateSystem="PROJCS[\"British_National_Grid\",GEOGCS[\"GCS_OSGB_1936\",DATUM[\"D_OSGB_1936\",SPHEROID[\"Airy_1830\",6377563.396,299.3249646]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",400000.0],PARAMETER[\"False_Northing\",-100000.0],PARAMETER[\"Central_Meridian\",-2.0],PARAMETER[\"Scale_Factor\",0.9996012717],PARAMETER[\"Latitude_Of_Origin\",49.0],UNIT[\"Meter\",1.0]]", 
                          parallelProcessingFactor="100%", processorType="GPU", pyramid="NONE", 
                          scratchWorkspace="C:\\T6DinB\\Downscaler\\Downscaler.gdb", workspace="C:\\T6DinB\\Downscaler\\Downscaler.gdb"):
        ECOTEST(*argv[1:])
