# -*- coding: utf-8 -*-
"""
The purpose of this script is to launch a GUI that prompts the user to select 
either an option to APPEND or SPLIT a database. The user will then be prompted
with what inputs and outputs they desire. No data has been provided for this script,
but the user can still run this script to see the user interface.

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2 
"""

import arcpy
import os, sys
import PyProj10_gui

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
#=========================================
# GUI event handler and related functions
#=========================================
def runTool():
    activeTab = ui.tabWidget.currentWidget()
    tabHandler[activeTab]()
    
def selectAppendTo(self):
    global appendTo
    appendTo = QFileDialog.getExistingDirectory(None, caption="Select database to append to:")
    if appendTo:
        ui.AppendToLE.setText(appendTo)
        appendTo = ui.AppendToLE.text()

def selectAppendFrom(self):
    global appendFrom
    appendFrom = QFileDialog.getExistingDirectory(None, caption="Select folder that databases are in:")
    if appendFrom:
        ui.AppendFromLE.setText(appendFrom)
        appendFrom = ui.AppendFromLE.text()

def selectSplitInput(self):
    global splitInput
    splitInput = QFileDialog.getExistingDirectory(None, caption="Select the database that will be split:")
    if splitInput:
        ui.InputDataLE.setText(splitInput)
        splitInput = ui.InputDataLE.text()

def selectSplitOutput(self):
    global splitOutput
    splitOutput = QFileDialog.getExistingDirectory(None, caption="Select the database that will be split:")
    if splitOutput:
        ui.OutputFolderLE.setText(splitOutput)
        splitOutput = ui.OutputFolderLE.text()
        
def runAppend():
    try:
        #This is the database everything will be appended to
        arcpy.env.workspace = appendTo

        #Name of the appended database
        folderList = os.listdir(appendFrom)

        for folder in folderList[1:]:
            with arcpy.EnvManager(workspace =  appendFrom + "\\" + folder):
                fcList3 = arcpy.ListFeatureClasses()
                for fc in fcList3:
                    arcpy.Append_management(os.path.join(appendFrom + "\\" + folder, fc), appendTo + "\\" + fc, "NO_TEST", "","","")
        QMessageBox.information(mainWindow, 'Operation Complete!', 'Appending operation has been completed!. Please close the windows to exit the program.', QMessageBox.Ok )
             
    except:
        QMessageBox.information(mainWindow, 'An Error has occurred! ', 'Appending operation has failed. Please check inputs and try again!', QMessageBox.Ok )

def runSplit():
    try:
        workspace = splitInput
        arcpy.env.workspace = workspace
        outputFolder = splitOutput
    
        aoiBoundaries = "aoiBoundaries.shp"                     #AOI Boundary layer
        fcList = arcpy.ListFeatureClasses()                     #Original feature classes
        cellNameField = "Name"                                  # field used to select AOI
        cellList = []                                           # list of AOI names
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
        QMessageBox.information(mainWindow, 'Operation Complete!', 'Splitting operation has been completed!. Please close the windows to exit the program.', QMessageBox.Ok )

    except:
        QMessageBox.information(mainWindow, 'An error has occurred!', 'Splitting operation has been completed!. Please close the windows to exit the program.', QMessageBox.Ok )

        

#=========================================
# create app and main window + dialog GUI
#=========================================
app = QApplication(sys.argv)  
mainWindow = QMainWindow() 
ui = PyProj10_gui.Ui_mainWindow() 
ui.setupUi(mainWindow)
#=========================================
# connect signals
#=========================================
ui.AppendToTB.clicked.connect(selectAppendTo)
ui.AppendFromTB.clicked.connect(selectAppendFrom)
ui.InputDataTB.clicked.connect(selectSplitInput)
ui.OutputFolderTB.clicked.connect(selectSplitOutput)
ui.RunPB.clicked.connect(runTool)
#=========================================
# initialize global variables
#=========================================
tabHandler = {ui.AppendTab: runAppend, ui.SplitTab: runSplit}

arcpy.env.overwriteOutput = True
#=========================================
# run app
#=========================================
mainWindow.show()
sys.exit(app.exec_())