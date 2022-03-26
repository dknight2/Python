# -*- coding: utf-8 -*-
"""
The goal of this script is to 
display a new shapefile for every position in a position list 
on a hockey team in a selected country, while also changing the players'
measureables from the imperial system to the metric system.

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""
# Import arcpy, workplace, and ensure files will be overwritten when run multiple times.
# To adopt the script to your own machine, you should only need to change the workspace path
# And have the associated shapefiles.
import arcpy
arcpy.env.workspace = r""
arcpy.env.overwriteOutput = True

# Establish all variables
countryBoundariesFC = "Countries_WGS84.shp"     # Shapefile has all countries in the world
playersFC = "nhlrosters.shp"                    # Shapefile with all players in the nhl
countryIDField = "CNTRY_NAME"                   # Field name for countries in the countries shapefile
countryOfChoice = "Sweden"                      # Choose the country here. Sweden is selected
positionID = "position"                         # Field name for position players play
positionList = ["LW", "RW", "C"]                # List with the positions in it
oldHeightField = "height"                       # Field name of the imperial height
oldWeightField = "weight"                       # Field name of the imperial weight
newHeightField = "height_cm"                    # New field name for metric height in cm
newWeightField = "weight_kg"                    # New field name for metric weight in kg

# Create a query to access just the country of your choice
countryQuery = countryIDField + " = '" + countryOfChoice + "'"

# Create for loop to run through each item in the position list
for position in positionList:
    print ("Processing players who play the " + position + " position...")
    
    # Create a position query that makes the code as flexible as the list 
    positionQuery = positionID + " = '" + position + "'"
    
    # Create a layer query for each position, adding the Fc to the end
    # of the name, and making the position lower-case.
    layerQuery = position + 'fc'
    
    try:
        # Create a temporary feature layer that only has sweden selected
        tempCountryLayer = arcpy.MakeFeatureLayer_management(countryBoundariesFC, "tempCountry", countryQuery)
        # Create a temporary feature layer that only selects players in desired positions.
        tempPlayerLayer = arcpy.MakeFeatureLayer_management(playersFC, "tempPlayers", positionQuery)
        # Select all players that fall within the country's borders
        swedishPlayers = arcpy.SelectLayerByLocation_management(tempPlayerLayer, "CONTAINED_BY", tempCountryLayer)
        # Save a feature class with the selected players, naming it after the position they play.
        arcpy.CopyFeatures_management(tempPlayerLayer, layerQuery)
        
        # Create a call for feature class variable that coordinates with the layer query
        # and adds the .shp file extension on the end of it.
        fc = layerQuery + ".shp"
        
        # Add new fields for height and weight
        arcpy.AddField_management(fc, newHeightField, "FLOAT", 6, 2)
        arcpy.AddField_management(fc, newWeightField, "FLOAT", 6, 2)
        
        #Update the Height field, accounting for the quotation marks and eliminating them.
        with arcpy.da.UpdateCursor(fc, (oldHeightField, newHeightField)) as heightCursor:
            for row in heightCursor:
                height = row[0]
                heightFeet = (float(height[0]) * 12) * 2.54
                heightReplace = height.replace('"', "")
                heightInches = float(heightReplace[-2:]) * 2.54
                row[1] = heightFeet + heightInches
                heightCursor.updateRow(row)
        
        # Update the Weight field.        
        with arcpy.da.UpdateCursor(fc, (oldWeightField, newWeightField)) as weightCursor:
            for row in weightCursor:
                oldWeight = weightCursor[0]
                newWeight = float(oldWeight * 0.453592)
                row[1] = newWeight
                weightCursor.updateRow(row)
    
    except:
        # Print any error that would be generated from errors in the script.
        print (arcpy.GetMessages())

    finally:
        # Delete the cursors and temporary layers.
        arcpy.Delete_management(tempCountryLayer)
        arcpy.Delete_management(tempPlayerLayer)
        del heightCursor, weightCursor

print ("Processing complete! Please find your results in your workspace folder.")