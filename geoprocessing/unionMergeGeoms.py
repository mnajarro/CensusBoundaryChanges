# This script does a second check on tiger files to assess area changes of individual boundary files that have
# have the same GEOIDs overtime.
# Please Note that you will need an advanced license of ArcGIS Desktop to run this script.
# Creator Mayro Najarro

import os
import sys
from collections import OrderedDict
import arcpy
import os.path
from os import path

tigerTypeFolder=['UScousub','county','UScts','zcta']

for typeInput in tigerTypeFolder:
    print(typeInput+' shapefiles:')
    joinField = 'GEOID'
    #Set the directory where the input files are stored
    if typeInput == 'UScousub':
        #directory = "C:/Users/maynajar/Projects/Boundaries/comparison/subcounties/"
        directory= "C:/work/tigerfiles/subcounties/"
    elif typeInput == 'county':
        #directory = "C:/Users/maynajar/Projects/Boundaries/comparison/counties/"
        directory= "C:/work/tigerfiles/counties/"
    elif typeInput == 'UScts':
        #directory = "C:/Users/maynajar/Projects/Boundaries/comparison/tracts/"
        directory = "C:/work/tigerfiles/tracts/"
    elif typeInput =='zcta':
        #directory = "C:/Users/maynajar/Projects/Boundaries/comparison/zctas/"
        directory = "C:/work/tigerfiles/zctas/"
        joinField = 'GEOID10'
    else:
        print('not needed')

    #shapefiles with the original projection
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = directory
    featureclasses = arcpy.ListFeatureClasses()
    geomShps = []
    for shp in featureclasses:
        #print(shp)
        if '_geomChg' in str(shp):
            print(shp)
            geomShps.append(shp)

    # Use Merge tool to move features into single dataset
    mergedGeomsChg = directory+"geomChg12_17_"+typeInput+".shp"
    arcpy.Merge_management(geomShps, mergedGeomsChg)

    # create new field with rounded ratio
    arcpy.AddField_management(mergedGeomsChg, 'ratio_rnd', "DOUBLE")
    arcpy.CalculateField_management(mergedGeomsChg, 'ratio_rnd', 'round(!area_ratio!,3)', 'PYTHON')
    # Remove duplicates based on ratio_rnd and GEOID fields
    arcpy.DeleteIdentical_management(mergedGeomsChg, [joinField, "ratio_rnd"])

    # Make a copy and remove duplicates only by GEOID
    layerName = mergedGeomsChg[:-4] + '_unique.shp'
    arcpy.CopyFeatures_management(mergedGeomsChg, layerName)
    arcpy.DeleteIdentical_management(layerName, [joinField])



print('done!')

