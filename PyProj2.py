# -*- coding: utf-8 -*-
"""
This script allows us to run a tool to re-project data from different 
coordinate systems into the same coordinate system. 
Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""


# Import neccesary modules
import arcpy

arcpy.env.overwriteOutput = True

# Establish variables: Get user input for file locations.
# The workspace (variable 1) is where we will be pulling feature classes from.
# Target Projection is the feature class that we want the rest of the projections
# to mimic. 
arcpy.env.workspace = arcpy.GetParameterAsText(0)
targetProjection = arcpy.GetParameterAsText(1)

# Get all of the feature classes in a list from the workspace. 
featureClassList = arcpy.ListFeatureClasses()

# Create a list to store values that qualify the if statement in line <x>
projectionList = list()

# Get the Spatial Reference of the Target Projection
refProjection = arcpy.Describe(targetProjection)
spatialRefProjection = refProjection.spatialReference

# Give arc message saying that the script is beginning to run
arcpy.AddMessage("Running script to reproject data in the folder...")
# Iterate through every feature class within the folder
for featureClass in featureClassList:    
   # Get the spatial reference of each feature class in the target folder
   refInput = arcpy.Describe(featureClass)
   spatialRefInput = refInput.spatialReference
   
    # Compare the Spatial References of each object against the target Projection 
   if spatialRefInput.Name != spatialRefProjection.Name:
       
       # Add values that fit the if statement into their own list
       projectionList.append(featureClass)
       
       # Remove the .shp from feature class names. 
       rootName = featureClass
       if rootName.endswith(".shp"):
           rootName = rootName.replace(".shp","_projected.shp")
           
       # Run the Project tool
       # ESRI's website seems to have contradicting statements for tool syntax
       # arcpy.management.Project() and arcpy.Project_management()
       arcpy.management.Project(featureClass, rootName, spatialRefProjection)
            
       print ("Projections are now the same.")
       print (" ")
       
       # I have a print statement here so that it will just ignore any actions if
       # the projections are already the same.
   elif spatialRefInput.Name == spatialRefProjection.Name:
        print("The projections are already the same.")
        
   else:
        arcpy.AddError("Something went wrong. Please try again.")
        print("There was an Error.")

test = ""
for item in projectionList:
    test += item + ", "
# Print a message saying which feature classes were projected        
arcpy.AddMessage("Projected " + str(test[:-2]))

# Print a message saying the script is complete
arcpy.AddMessage("Completed script to reproject data in the folder...")











