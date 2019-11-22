# Census Boundary Change Analysis


# Web Application
This web map displays the changes in county and count subdivision features from 2012 to 2018. It also displays a summary table of 
the number of features that have changed by census boundary type. The layers on the map can be turned off and on

# GeoProcessing Scripts and Process
A lot of geoprocessing was required to extract, merge and assess changes in census boundary features. Features in this assessment are referring to the individual row in for example a county shapefile of the US. 
So feature in this case refers to each individual county in the united states.

## Extracting and Merging Census Boundary Shapefile
ran extract.py script to download and extract all census tracts and county subdivisions from the us census tiger boundary files site
across 2012 to 2018 years

merged all cts and subcounties for each year so that there is a single country file for boundaries. I
ended up scripting the merging in mergeBoundaries.py

## Running Feature Changes Analysis
Also need to run analysis on record count an missing features. This analysis was run through changeAnalysis.py script.
The script bascially join each census boundary shapefile by year (oging back to 2012) to the 2018 census boundary. this join is based on the geoid
It outputs a shapfile of each feature join mismatch.

## Geometry Change Analysis *THis is a work in progress.
Then ran a batch operation of the difference tool in qgis to compare changes from each year to 2018.

Then reprojected change files to North_America_Albers_Equal_Area_Conic and caculated the area in QGIS manually

Initial difference run for counties
I ran a visual analysis in QGIS to see if there were any glaring differences

I also checked against BAS county changes table and verified changes. 
*** UPDATE this operation was too heavy to run on my computer.

** Note Most of the geoprocessing scripts require QGIS and pyqgis library for python in order to run them. 






