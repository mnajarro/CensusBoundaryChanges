# THis script merges all of the change boundary outputs into one file per census boundary type. 
from qgis.core import *
import os
import sys


typeInput="county"
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
layerList = {}
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
        if 'chg18_' in file:
            layer = QgsVectorLayer(directory + file, "", 'ogr')
            (myDirectory,nameFile) = os.path.split(layer.source())
            currentYear = extractYear(nameFile)
            print(currentYear)
            yearField = QgsField(name='year',type=QVariant.Int,typeName='int', len=10, prec=1)
            layer.startEditing()
            layer.addAttribute(yearField)
            layer.commitChanges()
            for feature in layer.getFeatures():
                layer.startEditing()
                layer.changeAttributeValue(feature.id(),feature.fieldNameIndex('year'),int(currentYear))
                layer.commitChanges()
                layer.updateFields()
                #print(feature['year'])
                # now merge all of the chg files into one chg file.
                geom = feature.geometry()
                attrs = feature.attributes()
                features = QgsFeature()
                features.setGeometry(geom)
                features.setAttributes(attrs)
                feats.append(features)
                
            layer.updateFields()
            layer.commitChanges()
            crs = layer.crs().toWkt()
            field_list = layer.dataProvider().fields().toList()
#            for field in layer.fields():
#                print(field.name(), field.typeName())
#            for feature in layer.getFeatures():
#                print(feature['year'])


 
v_layer = QgsVectorLayer('Polygon?crs=' + crs, 'Merged', "memory")
 
# Add the features to the merged layer
prov = v_layer.dataProvider()
prov.addAttributes(field_list)
v_layer.updateFields()
v_layer.startEditing()
prov.addFeatures(feats)
v_layer.commitChanges()
 
filePathFinal = directory + "chg_12_18.shp"
QgsVectorFileWriter.writeAsVectorFormat(v_layer,filePathFinal,'utf-8',driverName='ESRI Shapefile')
iface.addVectorLayer(filePathFinal,'', "ogr")            
            
print('done!')
            