# -*- coding: utf-8 -*-
"""
Its intended purpose is to split a single database into many databases,
according to AOI boundaries. For this project, I created a simple 4-Grid 
group with point, line, and polygon data in each AOI. The desired
output should be a unique geodatabase named according to the AOI name, with only
features from that AOI available.

NOTE: This is one of two scripts that does the same function. This was written with 
      hard-coded file paths for variables and is intended to be run in an IDE.

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""

import arcpy
import os

arcpy.env.workspace = r""
arcpy.env.overwriteOutput = True

# Establish the variables
aoiBoundaries = "aoiBoundaries.shp"                     # AOI Boundary shapefile
fcList = arcpy.ListFeatureClasses()                     # Original feature classes
cellNameField = "Name"                                  # field used to select AOI
cellList = []                                           # list of AOI names
outputFolder = r""                                      # Output Folder path

# Search through each AOI and get the name
# Because the data is stored as a tuple, some manipulation has to take place
# before it can be added to the list and used later on.
with arcpy.da.SearchCursor(aoiBoundaries, 'Name') as cursor:
    for row in cursor:
        item = str(row).strip("('").strip("',)")
        cellList.append(item)

# Select the feature classes that intersect with each 
for cell in cellList:
    # Create a query for the cell name
    cellQuery = cellNameField + " = '" + cell + "'"
    cellName = cell + ".gdb"
    # Create a unique gdb for each cell name, which is the identifier for the gdb
    arcpy.CreateFileGDB_management(outputFolder, cellName)
    
    # Loop through each fc in the fc list
    for fc in fcList:
        outFeatureClass = os.path.join(outputFolder + "\\" + cellName, fc)
        arcpy.CopyFeatures_management(fc, outFeatureClass)

    # Set each new gdb as a temporary environment
    with arcpy.EnvManager(workspace = outputFolder + "\\" + cellName):
        # Create a new list with the feature classes from each gdb
        fcList2 = arcpy.ListFeatureClasses()
        # Loop through the list
        for fcs in fcList2:
            # Create a temporary aoi layer that will be used in the selection.
            tempAoiLayer = arcpy.MakeFeatureLayer_management(aoiBoundaries, "TempAoi", cellQuery)
            # Create a features layer that inverts the selection; i.e. everything outside the aoi
            features = arcpy.SelectLayerByLocation_management(fcs, "INTERSECT", tempAoiLayer, '', '',"INVERT")
            # Delete these selected features
            arcpy.DeleteFeatures_management(features)
            # Delete the temporary aoi layer
            arcpy.Delete_management(tempAoiLayer)
