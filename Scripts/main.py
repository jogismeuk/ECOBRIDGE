# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2024-07-02 09:10:20
"""
import arcpy
from Dwnsclratbx.dsclrIterator import dsclrIterator
from arcpy.ia import *
from sys import argv

#For inline variable substitution, parameters passed as a String are evaluated using locals(), globals() and isinstance(). To override, substitute values directly.
def Model(Input_polygons, Input_baseline_raster_low_resolution_, Input_baseline_raster_high_resolution_, Input_scenario_raster_low_resolution_, Transition_table):  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageExt")
    arcpy.CheckOutExtension("ImageAnalyst")

    arcpy.ImportToolbox(r"C:\T6DinB\SED101.atbx")
    downscaled_output_raw = arcpy.Raster(fr"{arcpy.env.workspace}\downscaled_output_raw")
    _scratchFolder_ = f"{arcpy.env.scratchFolder}"
    _workspace_ = f"{arcpy.env.workspace}"

    # Process: Copy Features (Copy Features) (management)
    parcels = fr"{arcpy.env.workspace}\parcels"
    arcpy.management.CopyFeatures(in_features=Input_polygons.__str__().format(**locals(),**globals())if isinstance(Input_polygons, str) else Input_polygons, out_feature_class=parcels)

    # Process: Copy Raster (2) (Copy Raster) (management)
    cells = fr"{arcpy.env.workspace}\cells"
    arcpy.management.CopyRaster(in_raster=Input_baseline_raster_high_resolution_.__str__().format(**locals(),**globals())if isinstance(Input_baseline_raster_high_resolution_, str) else Input_baseline_raster_high_resolution_, out_rasterdataset=cells, pixel_type="8_BIT_UNSIGNED", format="GRID")

    # Process: Copy Raster (Copy Raster) (management)
    scenario = fr"{arcpy.env.workspace}\scenario"
    arcpy.management.CopyRaster(in_raster=Input_scenario_raster_low_resolution_.__str__().format(**locals(),**globals())if isinstance(Input_scenario_raster_low_resolution_, str) else Input_scenario_raster_low_resolution_, out_rasterdataset=scenario, nodata_value="0", pixel_type="8_BIT_UNSIGNED", format="GRID", transform="NONE")

    # Process: Copy Raster (3) (Copy Raster) (management)
    baseline = fr"{arcpy.env.workspace}\baseline"
    arcpy.management.CopyRaster(in_raster=Input_baseline_raster_low_resolution_.__str__().format(**locals(),**globals())if isinstance(Input_baseline_raster_low_resolution_, str) else Input_baseline_raster_low_resolution_, out_rasterdataset=baseline, nodata_value="0", pixel_type="8_BIT_UNSIGNED", format="GRID", transform="NONE")

    # Process: Segmentation (Segmentation) (Dwnsclratbx)
    if baseline and cells and parcels and scenario:
        s2_ouput_2_ = arcpy.Dwnsclratbx.Script1(transitiontable=Transition_table.__str__().format(**locals(),**globals())if isinstance(Transition_table, str) else Transition_table)[0]

    # Process: dsclrIterator (dsclrIterator) (Dwnsclratbx)
    mask_name_ = fr"{arcpy.env.workspace}\mask_%name%"
    cell_name_ = fr"{arcpy.env.workspace}\cell_%name%"
    if baseline and cells and parcels and s2_ouput_2_ and scenario:
        dsclrIterator(mask__name_=mask_name_, cells=cells, cell__name_=cell_name_)
        cell_name_ = arcpy.Raster(cell_name_)

    # Process: Classifier (Classifier) (Dwnsclratbx)
    if baseline and cell_name_ and cells and mask_name_ and parcels and s2_ouput_2_ and scenario:
        RecClas_2_ = arcpy.Dwnsclratbx.ClasScript(transita=Transition_table.__str__().format(**locals(),**globals())if isinstance(Transition_table, str) else Transition_table)[0]

    # Process: Create Raster Dataset (Create Raster Dataset) (management)
    if RecClas_2_ and baseline and cell_name_ and cells and mask_name_ and parcels and s2_ouput_2_ and scenario:
        rec_mosaic = arcpy.management.CreateRasterDataset(out_path=_workspace_, out_name="rec_mosaic", cellsize=10, pixel_type="8_BIT_UNSIGNED", number_of_bands=1)[0]
        rec_mosaic = arcpy.Raster(rec_mosaic)

    # Process: Workspace To Raster Dataset (Workspace To Raster Dataset) (management)
    if RecClas_2_ and baseline and cell_name_ and cells and mask_name_ and parcels and s2_ouput_2_ and scenario:
        rec_mosaic_3_ = arcpy.management.WorkspaceToRasterDataset(in_workspace=_scratchFolder_, in_raster_dataset=rec_mosaic, nodata_value=0)[0]
        rec_mosaic_3_ = arcpy.Raster(rec_mosaic_3_)

    # Process: Mosaic To New Raster (Mosaic To New Raster) (management)
    if RecClas_2_ and baseline and cell_name_ and cells and mask_name_ and parcels and s2_ouput_2_ and scenario:
        downscaled_RAW = arcpy.management.MosaicToNewRaster(input_rasters=[rec_mosaic_3_, cells], output_location=_workspace_, raster_dataset_name_with_extension="downscaled_output_RAW", cellsize=10, number_of_bands=1, mosaic_method="FIRST", mosaic_colormap_mode="REJECT")[0]
        downscaled_RAW = arcpy.Raster(downscaled_RAW)

    # Process: Cleaner (2) (Cleaner) (Dwnsclratbx)
    if RecClas_2_ and baseline and cell_name_ and cells and downscaled_RAW and mask_name_ and parcels and s2_ouput_2_ and scenario:
        cleaned_3_ = arcpy.Dwnsclratbx.CleaningScript()[0]

    # Process: Zonal Statistics as Table (Zonal Statistics as Table) (ia)
    ZonalSt_parcels1 = fr"{arcpy.env.workspace}\ZonalSt_parcels1"
    majority_parcels = "majority_parcels"
    if RecClas_2_ and baseline and cell_name_ and cells and cleaned_3_ and downscaled_RAW and mask_name_ and parcels and s2_ouput_2_ and scenario:
        with arcpy.EnvManager(extent="MINOF", snapRaster="LCM2020_UK_aggregate_10m.tif"):
            arcpy.ia.ZonalStatisticsAsTable(parcels, "gid", downscaled_output_raw, ZonalSt_parcels1, "DATA", "MAJORITY", "CURRENT_SLICE", [90], "AUTO_DETECT", "ARITHMETIC", 360, majority_parcels)
            .save(Zonal_Statistics_as_Table)


    # Process: Polygon to Raster (Polygon to Raster) (conversion)
    downscaled_output_RAS = fr"{arcpy.env.workspace}\downscaled_output_RAS"
    if RecClas_2_ and baseline and cell_name_ and cells and cleaned_3_ and downscaled_RAW and mask_name_ and parcels and s2_ouput_2_ and scenario:
        with arcpy.EnvManager(cellSize="MAXOF", snapRaster="LCM2020_UK_aggregate_10m.tif"):
            arcpy.conversion.PolygonToRaster(in_features=majority_parcels, value_field="ZonalSt_parcels1.MAJORITY", out_rasterdataset=downscaled_output_RAS, cellsize="10")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(cellSize="MINOF", extent="MINOF", outputCoordinateSystem="PROJCS[\"British_National_Grid\",GEOGCS[\"GCS_OSGB_1936\",DATUM[\"D_OSGB_1936\",SPHEROID[\"Airy_1830\",6377563.396,299.3249646]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",400000.0],PARAMETER[\"False_Northing\",-100000.0],PARAMETER[\"Central_Meridian\",-2.0],PARAMETER[\"Scale_Factor\",0.9996012717],PARAMETER[\"Latitude_Of_Origin\",49.0],UNIT[\"Meter\",1.0]]", 
                          parallelProcessingFactor="100%", processorType="GPU", pyramid="NONE", 
                          scratchWorkspace="C:\\T6DinB\\Downscaler\\Downscaler.gdb", workspace="C:\\T6DinB\\Downscaler\\Downscaler.gdb"):
        Model(*argv[1:])
