# This script takes in tiger files and geocomponent files to output subsets of both based on tiger file intersections
# and adding fields to geocomponents. this script generate centroids based off of us county or subcounty boundaries then uses 
# it to do a spatial join on geocomponents
# Ultimate this preps the data for the geocomponents.html application. 

import sys

from qgis.core import *
import os
sys.path.append('C:\\OSGeo4W64\\apps\\qgis\\python\\plugins')
import processing
# Get input files

usCountiesTiger = r'C:\Users\maynajar\Projects\Boundaries\comparison\counties\tl_2018_us_county.shp'
us2018Countytiger = QgsVectorLayer(usCountiesTiger, "", 'ogr')

usCountySubTiger = r'C:\Users\maynajar\Projects\Boundaries\comparison\subcounties\2018UScousub.shp'
us2018CountySubtiger = QgsVectorLayer(usCountySubTiger, "", 'ogr')

geocomponentLoc = r'C:\Users\maynajar\Projects\Boundaries\comparison\SDMSgeocomponents\SDMSGeocomponents.shp'
geocomponentMCDLayer = QgsVectorLayer(geocomponentLoc, "", 'ogr')
geocomponentCountyLayer = QgsVectorLayer(geocomponentLoc, "", 'ogr')

crs = geocomponentMCDLayer.crs().toWkt()

# Filter down geocomponents
geocomponentMCDLayer.setSubsetString("GeoUnitTyp = 'MCD' AND (StatusDesc = 'Designated' OR StatusDesc = 'Proposed For Withdrawal')")
geocomponentCountyLayer.setSubsetString("GeoUnitTyp = 'COUNTY' AND (StatusDesc = 'Designated' OR StatusDesc = 'Proposed For Withdrawal')")

# Add fields to geocomponents
dpCounty = geocomponentCountyLayer.dataProvider() # need to create a data provider
fieldstoAdd = ['GEOID','NAME','STATEFIP']
for field in fieldstoAdd:
    if field not in geocomponentCountyLayer.fields().names():
        #print(field)
        dpCounty.addAttributes([QgsField(field,  QVariant.String)])
        geocomponentCountyLayer.updateFields()
#dpCounty.deleteAttributes([27]) for deletin extras
#geocomponentCountyLayer.updateFields()


# Run intersect on county and subcounties
countyIntersect = []
for feature in us2018Countytiger.getFeatures():
    tigerGeom = feature.geometry()
    for features in geocomponentCountyLayer.getFeatures():
        gcGeom = features.geometry()
        if tigerGeom.intersects(gcGeom):
            if feature not in countyIntersect:
#                print(feature['NAMELSAD'])
                countyIntersect.append(feature)

print(len(countyIntersect))

countySubIntersect = []
for feat in us2018CountySubtiger.getFeatures():
    tigerSubGeom = feat.geometry()
    for feats in geocomponentMCDLayer.getFeatures():
        gcSubGeom = feats.geometry()
        if tigerSubGeom.intersects(gcSubGeom):
            if feat not in countySubIntersect:
                #print(feat['NAMELSAD'])
                countySubIntersect.append(feat)


def getCentroids(fieldLayer, featureList):
    field_list = fieldLayer.dataProvider().fields().toList()
     
    v_layer = QgsVectorLayer('Polygon?crs=' + crs, 'Merged', "memory")
     
    # Add the features to the merged layer
    prov = v_layer.dataProvider()
    prov.addAttributes(field_list)
    v_layer.updateFields()
    v_layer.startEditing()
    prov.addFeatures(featureList)
    v_layer.commitChanges()
    output = processing.run("native:centroids", {'INPUT':v_layer,'ALL_PARTS':True,'OUTPUT':'memory:'}) 
    return output['OUTPUT']

countyCentroids = getCentroids(us2018Countytiger,countyIntersect)
mcdCentroids = getCentroids(us2018CountySubtiger,countySubIntersect)
#
## Join attributes from tiger boundaries to geocomponents using contains operation of tiger centroids
## MCDs
geocomponentMCDLayer.startEditing()
for features in geocomponentMCDLayer.getFeatures():
    gcGeom = features.geometry()
    for feature in mcdCentroids.getFeatures():
        mcdGeom = feature.geometry()
#        centroid = mcdGeom.centroid()
        if gcGeom.contains(mcdGeom): # ALL PARTS doesn't seem to be working. May need to debug
            features['GEOID'] = feature['GEOID']
            features['NAME'] = feature['NAME']
            features['STATEFIP'] = feature['STATEFP']
            geocomponentMCDLayer.updateFeature(features)
            #print(features['GEOID'])
            
geocomponentMCDLayer.commitChanges()


# Counties
geocomponentCountyLayer.startEditing()
for features in geocomponentCountyLayer.getFeatures():
    gcGeom = features.geometry()
    for feature in countyCentroids.getFeatures():
        countyGeom = feature.geometry()
#        centroid = countyGeom.centroid()
        if gcGeom.contains(countyGeom):
            features['GEOID'] = feature['GEOID']
            features['NAME'] = feature['NAME']
            features['STATEFIP'] = feature['STATEFP']
            geocomponentCountyLayer.updateFeature(features)
            
geocomponentCountyLayer.commitChanges()
    

# Save Outputs
def mergeWrite(featureList, tlayer, name):
    field_list = tlayer.dataProvider().fields().toList()
     
    v_layer = QgsVectorLayer('Polygon?crs=' + crs, 'Merged', "memory")
     
    # Add the features to the merged layer
    prov = v_layer.dataProvider()
    prov.addAttributes(field_list)
    v_layer.updateFields()
    v_layer.startEditing()
    prov.addFeatures(featureList)
    v_layer.commitChanges()
    fileName = name+'.geojson' 
    QgsVectorFileWriter.writeAsVectorFormat(v_layer, fileName, 'utf-8', driverName='GeoJSON', onlySelected=False)
    iface.addVectorLayer(fileName,'', "ogr")

directory = 'C:/Users/maynajar/Projects/Boundaries/CensusBoundaryChanges/data/'    
mergeWrite(countySubIntersect,us2018CountySubtiger,directory+'mcdTiger2018')
mergeWrite(countyIntersect,us2018Countytiger,directory+'countyTiger2018')
QgsVectorFileWriter.writeAsVectorFormat(geocomponentMCDLayer, directory+'mcdGeocomponents.geojson', 'utf-8', driverName='GeoJSON', onlySelected=False)
iface.addVectorLayer(directory+'mcdGeocomponents.geojson','', "ogr")
QgsVectorFileWriter.writeAsVectorFormat(geocomponentCountyLayer, directory+'countyGeocomponents.geojson', 'utf-8', driverName='GeoJSON', onlySelected=False)
iface.addVectorLayer(directory+'countyGeocomponents.geojson','', "ogr")

print('done!')


