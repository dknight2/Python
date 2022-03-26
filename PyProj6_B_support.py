"""
This is the support script for the PyProj6_B_main. Here, we practice defining a function 
and importing it into another module. 

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""

import os, sys
import arcpy

# overwrites the output from previous runs
arcpy.env.overwriteOutput = True
 
def worker(clipper, tobeclipped, field, oid, outputFolder): 
    """  
       This is the function that gets called and does the work of clipping the input feature class to one of the polygons from the clipper feature class. 
       Note that this function does not try to write to arcpy.AddMessage() as nothing is ever displayed.  If the clip succeeds then it returns TRUE else FALSE.  
    """
    try:
        fc = os.path.basename(os.path.splitext(tobeclipped)[0])
        # Create a layer with only the polygon with ID oid. Each clipper layer needs a unique name, so we include oid in the layer name.
        query = '"' + field +'" = ' + str(oid)
        arcpy.MakeFeatureLayer_management(clipper, "clipper_" + str(oid) + "_" + fc, query) 
        
        # Do the clip. We include the oid in the name of the output feature class. 
        outFC = outputFolder + "\clip_" + str(oid) + "_" + fc + ".shp"
        arcpy.Clip_analysis(tobeclipped, "clipper_" + str(oid) + "_" + fc, outFC) 
         
        print("finished clipping:", str(oid)) 
        return True # everything went well so we return True
    except: 
        # Some error occurred so return False 
        print("error condition") 
        return False
    
