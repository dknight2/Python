# -*- coding: utf-8 -*-
"""
This is the main function that is imported into PyProj_7_main.

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""
import arcpy
arcpy.env.overwriteOutput= True

# This code uses the following variables:
# polygonFile: input polygon file (e.g. file with countries)
# polygonField: name of field of the input polygon file to query on (e.g. 'NAME')
# polygonValue: value to query polygonField for (e.g. 'El Salvador')
# pointFile: input point file (e.g. file with points of interest)
# pointField: name of field of the input point file to query on (e.g. 'shop')
# pointValue: value to query pointField for (e.g. 'supermarket'); if this variable has the value None, all features with something in pointField will be included
# outputFile: name of the output shapefile to produce

def  mainFunction(polygonFile, polygonField, polygonValue, pointFile, pointField, pointValue, outputFile): 
    # select target polygon from polygon file
    polygonQuery = '"{0}" = \'{1}\''.format(polygonField, polygonValue)          # query string
    arcpy.MakeFeatureLayer_management(polygonFile,"polygonLayer", polygonQuery)  # produce layer based on query string
 
    # select target points from point file
    if pointValue:   # not None, so the query string needs to use pointValue
        pointQuery = '"{0}" = \'{1}\''.format(pointField, pointValue)
    else:            # pointValue is None, so the query string aks for entries that are not NULL and not the empty string
        pointQuery = '"{0}" IS NOT NULL AND "{0}" <> \'\''.format(pointField) 
    arcpy.MakeFeatureLayer_management(pointFile,"pointLayer", pointQuery)        # produce layer based on query string
 
    # select only points of interest in point layer that are within the target polygon    
    arcpy.SelectLayerByLocation_management("pointLayer", "WITHIN", "polygonLayer")
 
    # write selection to output file
    arcpy.CopyFeatures_management("pointLayer", outputFile)
 
    # clean up layers    
    arcpy.Delete_management("polygonLayer")
    arcpy.Delete_management("pointLayer")