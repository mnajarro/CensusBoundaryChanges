# This script checks if there are any existing boundary features that are not in the 2018 boundaries. It also creates a difference file between the different years.
from qgis.core import *
import os
import sys
from collections import OrderedDict

yearInput='2012_'
typeInput="zcta" # change input based on which boundary type you are using. 
# Set the directory where the input files are stored
if typeInput == 'UScousub':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/subcounties/"
elif typeInput == 'county':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/counties/"
elif typeInput == 'UScts':
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/tracts/"
else:
    directory = "C:/Users/maynajar/Projects/Boundaries/comparison/zctas/"

def extractYear(name):
    years = ['2012', '2013', '2014', '2015', '2016', '2017']
    for year in years:
        if year in name:
            return year

def mergeWrite(featureList, tlayer, year):
    # Get the Coordinate Reference System and the list of fields from the last input file
    crs = tlayer.crs().toWkt()
    field_list = tlayer.dataProvider().fields().toList()
     
    v_layer = QgsVectorLayer('Polygon?crs=' + crs, 'Merged', "memory")
     
    # Add the features to the merged layer
    prov = v_layer.dataProvider()
    prov.addAttributes(field_list)
    v_layer.updateFields()
    v_layer.startEditing()
    prov.addFeatures(featureList)
    v_layer.commitChanges()
    fileName = directory + 'chg18_'+year+'.shp' 
    QgsVectorFileWriter.writeAsVectorFormat(v_layer, fileName, 'utf-8', driverName='ESRI Shapefile', onlySelected=False)
    QgsVectorFileWriter.writeAsVectorFormat(v_layer, directory+'chg18_'+year+'.csv', "utf-8", driverName="CSV")
    iface.addVectorLayer(fileName,'', "ogr")
    
#check for row amount differences in each layer
def getDiffFeatures(layer1, layer2, mergeField):
    selectedBoundaries = []
    # Set up join parameters            
    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayerId(layer2.id())
    joinObject.setJoinFieldName(mergeField)
    joinObject.setTargetFieldName(mergeField)
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(layer2)
    joinObject.setPrefix('d_')
    layer1.addJoin(joinObject)

    for features in layer1.getFeatures():
        if features['d_STATEFP'] is None:
            selectedBoundaries.append(features)
    layer1.removeJoin(layer2.id())
    return selectedBoundaries


# Check differences in number of rows
# Get the list of input files and create sublist of layers
fileList = os.listdir(directory)
layerList = {}
layer2018 = {}
for file in fileList:
    if file.endswith('.shp'):
        if str(typeInput) in file:
            layer = QgsVectorLayer(directory + file, "", 'ogr')
            if '2018' in file:
                layer2018[layer]=layer.featureCount()
                print(layer.shortName())
            else:
                layerList[layer]=layer.featureCount()
            #print(layer.featureCount())
#loop through the layer list and compare to 2018 count
geoidList = []
for layer in layerList:
    latest = list(layer2018.keys())[0]
    val2018 = list(layer2018.values())[0]
    diff = val2018 - layerList[layer]
    (myDirectory,nameFile) = os.path.split(layer.source())
    if diff == 0:
        print('no features were added in '+ layer.id())
    else:
        if diff > 0:
            print( str(diff) + ' features were added in '+ layer.id())
        if diff < 0:
            print( str(diff) + ' features were removed in '+ layer.id())
        layerYear = extractYear(nameFile)
        diffLayer1 = getDiffFeatures(layer, latest, 'GEOID')
        diffLayer2 = getDiffFeatures(latest, layer, 'GEOID')
        diffList = diffLayer1 + diffLayer2
        finalList = [i for n, i in enumerate(diffList) if i not in diffList[:n]]  
        mergeWrite(finalList, layer, layerYear)
        #Get a list of geoIDs that were removed or missing for each year

print('done!')

