# -*- coding: utf-8 -*-
"""
We are creating a DEM contour of 25m from a provided file.
The folder paths have been change to empty quotes for privacy and flexibility. 

@author: dknight2
"""

# Importing the proper modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Allow overwriting the output for convenience.
arcpy.env.overwriteOutput = True

# Set the workspace environment
env.workspace = r""

# Set the variables for the Contour tool

inRaster = ""
outContours = r""
contourInterval = 25
baseContour = 0

# Set up the Try/Except method to handle errors
try:
    #Check out the Spatial Analyst Extension
    arcpy.CheckOutExtension("Spatial_Analyst")
    
    # Run the Contour tool
    Contour(inRaster, outContours, contourInterval, baseContour)
    
    # Check in the Spatial Analyst Extension
    arcpy.CheckInExtension("Spatial_Analyst")
    
    # Report completion message
    print ("Contour complete!")
    
except:
    # Report the error message
    print ("Could not complete the Contour. Please adjust inputs and try again")
    
    # Get any messages that the contour tool generated
    arcpy.AddMessage(arcpy.GetMessages())
    
    