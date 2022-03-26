"""
This script reads data from a csv file and creates a shapefile detailing each lap it iterates through.
After creating the shapefile, an attribute was created to describe the lap.
The csv file has not been provided for further use.

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2 
"""
import csv
import arcpy

arcpy.env.workspace = r""
arcpy.env.overwriteOutput = True
sr = arcpy.SpatialReference(4326)

# Create feature classes for the laps
lapFc = "LapFc.shp"
arcpy.CreateFeatureclass_management(arcpy.env.workspace, lapFc, "POLYLINE", spatial_reference=sr)
spatialRef = arcpy.Describe(lapFc).spatialReference
arcpy.AddField_management(lapFc, "Lap", field_type = "TEXT")

# Open the input file
gpsTracker =  open(arcpy.env.workspace + "\_", "r") # csv filepath goes in the first set of quotes
dataList = []

# Set up the CSV reader and process the header    
csvReader = csv.reader(gpsTracker)

# send each line from the reader into a list; I was told this is good practice
# so the code doesn't have to read from the file every time in future functions
for line in csvReader:
    dataList.append(line)

# Create an array and a dictionary to store data values in
vertices = arcpy.Array()
coordDict = {}

# run through the data list, skipping the first line (header), and the lines
# that indicate new laps/session end
for row in dataList[1:]:   
    if len(row) > 1:
        lap = row[1]
        lat = row[5]
        lon = row[6]
        
        # add coordinates to an array, key the laps to each array
        coord = arcpy.Point(lon, lat)
        vertices.append(coord)
        coordDict[lap] = vertices

# Use an insert cursor to add each lap to the feature class
with arcpy.da.InsertCursor(lapFc, ("SHAPE@","Lap")) as cursor:
    for key in coordDict:
        polyline = arcpy.Polyline(coordDict[key], spatialRef)
        lap = key
        cursor.insertRow((polyline,lap))
del cursor
