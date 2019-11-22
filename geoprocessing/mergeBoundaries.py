#this script merges all of the individual state boundaries into one single US census boundary file per year. 
from qgis.core import *
import os
import sys
 
yearInput='2012_'
typeInput="cousub" # change input based on which boundary type you are using. 
# Set the directory where the input files are stored
if typeInput == 'cousub':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/subcounties/"
elif typeInput == 'cts':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/tracts/"

 
# Get the list of input files
fileList = os.listdir(directory)
 
# Copy the features from all the files in a new list
feats = []
for file in fileList:
    if file.endswith('.shp'):
        if str(yearInput) in file:
            layer = QgsVectorLayer(directory + file, file, 'ogr')
            for feat in layer.getFeatures():
                geom = feat.geometry()
                attrs = feat.attributes()
                feature = QgsFeature()
                feature.setGeometry(geom)
                feature.setAttributes(attrs)
                feats.append(feature)
 
# Get the Coordinate Reference System and the list of fields from the last input file
crs = layer.crs().toWkt()
field_list = layer.dataProvider().fields().toList()
 
v_layer = QgsVectorLayer('Polygon?crs=' + crs, 'Merged', "memory")
 
# Add the features to the merged layer
prov = v_layer.dataProvider()
prov.addAttributes(field_list)
v_layer.updateFields()
v_layer.startEditing()
prov.addFeatures(feats)
v_layer.commitChanges()
 

filePathFinal = directory + yearInput +"US"+typeInput+".shp"

QgsVectorFileWriter.writeAsVectorFormat(v_layer,filePathFinal,'utf-8',driverName='ESRI Shapefile')

iface.addVectorLayer(filePathFinal,yearInput +"US", "ogr")

# https://howtoinqgis.wordpress.com/2016/11/01/how-to-merge-multiple-vector-layers-in-qgis-from-a-folder-using-python/