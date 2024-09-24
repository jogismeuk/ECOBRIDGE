"""
Trainer.py

Description:
    This script automates the process of training deep learning models for spatial analysis. 
    It leverages the arcpy module to export training data from specified raster inputs and then trains a
    deep learning model using this data.

Requirements:
    - ArcGIS Pro with the Image Analyst extension licensed and enabled.
    - Python 3.x environment configured with ArcGIS Pro.

Inputs:
    - in_raster: The input raster from which training samples are to be exported.
    - in_class_data: The input raster or feature class that contains the class labels for training data.

Outputs:
    - Training samples exported to the specified output folder.
    - A trained deep learning model saved in the specified model directory.

Author:
    Josep Serra Gallego
Date:
    2024-1-1
Version:
    1.0
ArcGIS Version:
    Compatible with ArcGIS Pro 3.2
Python Version:
    3.x
"""

import arcpy
import os
import shutil

def script_tool(param0, param1):
    # Export training samples

    arcpy.ia.ExportTrainingDataForDeepLearning(
        in_raster= arcpy.env.workspace + "\CL3",
        out_folder=r"C:\ECOBRIDGE\SAMPLES",
        in_class_data=arcpy.env.workspace + "\RasterT_CL41",
        image_chip_format="TIFF",
        tile_size_x=256,
        tile_size_y=256,
        stride_x=128,
        stride_y=128,
        output_nofeature_tiles="ONLY_TILES_WITH_FEATURES",
        metadata_format="Classified_Tiles",
        start_index=0,
        class_value_field="gridcode",
        buffer_radius=0,
        in_mask_polygons=None,
        rotation_angle=0,
        reference_system="MAP_SPACE",
        processing_mode="PROCESS_AS_MOSAICKED_IMAGE",
        blacken_around_feature="NO_BLACKEN",
        crop_mode="FIXED_SIZE",
        in_raster2=None,
        in_instance_data=None,
        instance_class_value_field=None,
        min_polygon_overlap_ratio=0
    )

    # Train deep learning model
    arcpy.ia.TrainDeepLearningModel(
            in_folder=r"C:\ECOBRIDGE\SAMPLES",
            out_folder=r"C:\ECOBRIDGE\MODEL",
            max_epochs=2,
            model_type="UNET",
            batch_size=8,
            arguments="class_balancing False;mixup False;focal_loss False;ignore_classes 0",
            learning_rate=None,
            backbone_model="RESNET34",
            pretrained_model=None,
            validation_percentage=10,
            stop_training="STOP_TRAINING",
            freeze="FREEZE_MODEL",
            augmentation="DEFAULT",
            augmentation_parameters=None,
            chip_size=224,
            resize_to="",
            weight_init_scheme="",
            monitor="VALID_LOSS"
        )
    return
if __name__ == "__main__":
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)

    samples_dir = r"C:\ECOBRIDGE\SAMPLES"
    model_dir = r"C:\ECOBRIDGE\MODEL"

    # Check if the SAMPLES directory exists and remove it if it does
    if os.path.exists(samples_dir):
        shutil.rmtree(samples_dir)

    # Check if the MODEL directory exists and remove it if it does
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)
    
    # Export Samples and Train Model
    script_tool(param0, param1)
    arcpy.SetParameterAsText(2, "Result")
