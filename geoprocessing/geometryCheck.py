# This script does a second check on tiger files to assess area changes of individual boundary files.

import os
import sys
from collections import OrderedDict
import arcpy
import os.path
from os import path

def get2018shp(featureclasses):
    for files in featureclasses:
        if '2018' in files:
            if 'proj' in files:
                print(files)
                return files
# tigerType = ['']
# tigerTypeFolder=['UScousub','county','UScts','zctas'] # change based on where tiger files are saved
tigerTypeFolder=['zcta']
#typeInput = input()
for typeInput in tigerTypeFolder:
    print(typeInput)
    joinField = 'GEOID'
    # Set the directory where the input files are stored
    # if typeInput == 'UScousub':
    #     directory = "C:/work/tigerfiles/subcounties/"
    # elif typeInput == 'county':
    #     directory = "C:/work/tigerfiles/counties/"
    if typeInput == 'UScts':
        directory = "C:/work/tigerfiles/tracts/"
    elif typeInput =='zcta':
        directory = "C:/work/tigerfiles/zctas/"
        joinField = 'GEOID10'
    else:
        print('not needed')

    #shapefiles with the original projection
    print(directory)
    arcpy.env.workspace = directory
    featureclasses = arcpy.ListFeatureClasses()

    for shp in featureclasses:
        if str(typeInput) in str(shp):
            if '_proj' not in shp:
                print(shp[:-4])
                shpName = shp[:-4]
#     #if shp == file18:
                dsc = arcpy.Describe(shp)
                print(dsc.spatialReference.Name)
                if dsc.spatialReference.Name == "Unknown":
                    print('skipped this fc due to undefined coordinate system: ' + shp)
                else:
                    # Determine the new output feature class path and name
                    outShp= os.path.join(directory, shpName+'_proj.shp')

                    # Set output coordinate system
                    outCS = arcpy.SpatialReference(102003)
                    if path.exists(outShp):
                        print('already reprojected')
                    else:
                        # run project tool
                        arcpy.Project_management(shp, outShp, outCS)
                        arcpy.AddGeometryAttributes_management(outShp, "AREA", "METERS")
                        # check messages
                        print(arcpy.GetMessages())
#
# # Add new column with area
# arcpy.AddGeometryAttributes_management("2018_UScousub_proj.shp", "AREA", "METERS")
# arcpy.AddGeometryAttributes_management("2012_UScousub_proj.shp", "AREA", "METERS")
#

# # Join 201X to 2018
    for shp in featureclasses:
        if 'proj.shp' in shp:
            if '2018' not in shp:
                print(shp)
                shpName = shp[:-4]
                shp2018 = get2018shp(featureclasses)
                print(shp2018)
                arcpy.JoinField_management(shp, joinField, shp2018, joinField,
                                           [joinField, "NAME", "POLY_AREA"])
                arcpy.AddField_management(shp, "area_diff", "DOUBLE")
                arcpy.CalculateField_management(shp, "area_diff",
                                                "!POLY_AREA! - !POLY_ARE_1!", "PYTHON", "")
                arcpy.AddField_management(shp, "area_ratio", "DOUBLE")
                arcpy.CalculateField_management(shp, "area_ratio",
                                                "!POLY_ARE_1! / !POLY_AREA!", "PYTHON", "")
                arcpy.MakeFeatureLayer_management(shp, shpName+"lyr")
                arcpy.SelectLayerByAttribute_management(shpName+"lyr", "NEW_SELECTION",
                                                        '(area_ratio < 0.98999999999999998 And area_ratio <> 0) Or area_ratio >= 1.01')

                # Write the selected features to a new featureclass
                arcpy.CopyFeatures_management(shpName+"lyr", shpName+'_geomChg.shp')

# arcpy.JoinField_management("2012_UScousub_proj.shp", "GEOID", "2018_UScousub_proj.shp","GEOID",["GEOID", "NAME", "POLY_AREA"])
# arcpy.JoinField_management("2018_UScousub_proj.shp", "GEOID", "2012_UScousub_proj.shp","GEOID",["GEOID", "NAME", "POLY_AREA"])
#
# arcpy.AddField_management("2012_UScousub_proj.shp", "area_diff", "DOUBLE")
# arcpy.CalculateField_management("2012_UScousub_proj.shp", "area_diff",
#                                 "!POLY_AREA! - !POLY_ARE_1!","PYTHON","")
# arcpy.AddField_management("2012_UScousub_proj.shp", "area_ratio", "DOUBLE")
# arcpy.CalculateField_management("2012_UScousub_proj.shp", "area_ratio",
#                                 "!POLY_ARE_1! / !POLY_AREA!","PYTHON","")

# arcpy.AddField_management("2018_UScousub_proj.shp", "area_diff", "DOUBLE")
# arcpy.CalculateField_management("2018_UScousub_proj.shp", "area_diff",
#                                 "!POLY_AREA! - !POLY_ARE_1!","PYTHON","")
# arcpy.AddField_management("2018_UScousub_proj.shp", "area_ratio", "DOUBLE")
# arcpy.CalculateField_management("2018_UScousub_proj.shp", "area_ratio",
#                                 "!POLY_ARE_1! / !POLY_AREA!","PYTHON","")
# Need to add all Fields into new file


## Need to filter features by area diff or area ratio depending on threshold
# select only features that have an area ratio that is less than 0.97 and is not 0 or if the area ratio is greater than 1.01
#arcpy.SelectLayerByAttribute_management("2018_UScousub_proj.shp", "NEW_SELECTION", '(area_ratio < 0.98999999999999998 And area_ratio <> 0) Or area_ratio >= 1.01')
# arcpy.MakeFeatureLayer_management("2012_UScousub_proj.shp","2012_UScousub_proj_lyr")
# arcpy.SelectLayerByAttribute_management("2012_UScousub_proj_lyr", "NEW_SELECTION", '(area_ratio < 0.98999999999999998 And area_ratio <> 0) Or area_ratio >= 1.01')
#
#
# # Write the selected features to a new featureclass
# arcpy.CopyFeatures_management("2012_UScousub_proj_lyr", 'geom2012Change.shp')

# make script configurable to work on all geography levels

print('done!')

