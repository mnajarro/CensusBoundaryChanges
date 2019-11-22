#This script calculates the geometric difference between each census boundary shapefile by year. 
from qgis.core import *
import os
import sys


typeInput="UScousub" # change input based on which boundary type you are using. 
# Set the directory where the input files are stored
if typeInput == 'UScousub':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/subcounties/"
elif typeInput == 'county':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/counties/"
elif typeInput == 'UScts':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/tracts/"
else:
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/zctas/"

fileList = os.listdir(directory)
layerList = []
layer2018 = ''
feats = []
crs = ''
field_list=[]
def extractYear(name):
    years = ['2012', '2013', '2014', '2015', '2016', '2017']
    for year in years:
        if year in name:
            return year

for file in fileList:
    if file.endswith('.shp'):
        if str(typeInput) in file:
            layer = QgsVectorLayer(directory + file, "", 'ogr')
            if '2018' in file:
                layer2018 = layer
            else:
                layerList.append(layer)

difflayer = QgsVectorLayer('Polygon?crs=' + crs, 'Merged', "memory")
#here we want to iterate through each layer and do a difference with the 2018 layer
for layer in layerList:
    outgoingFeatureList = []
    fields = layer.fields()
    #print(layer)
    for f in layer.getFeatures():
        compFeature = QgsGeometry()
        localFeature = QgsGeometry()
        outgoingFeature = QgsFeature()
        localFeature = f.geometry()
        for h in layer2018.getFeatures():
            compFeature = h.geometry()
            if localFeature.intersects(compFeature):
                localFeature = localFeature.difference(compFeature)
        outgoingFeature.setFields(fields)
        outgoingFeature.setGeometry(localFeature)
        outgoingFeature['GEOID'] = f['GEOID']
        outgoingFeatureList.append(outgoingFeature)
    difflayer.dataProvider().addFeatures(outgoingFeatureList)
    difflayer.commitChanges()
    break
iface.addVectorLayer(difflayer,"", "ogr")
print('done!')