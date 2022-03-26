"""
This is the main script for PyProj9. As described in the func script, the purpose
is to read JSON data and categories and create geopackage (GPKG) outputs according
to the type of waterbody each node is. This script handles all GUI inputs and displaying
the GUI. The data has not been provided, but you can still launch the GUI to see
the user interface.

A main utility of this script is to break away from the arcpy library and use
open source options, like QGIS (hence geopackages), because of the proprietary
nature of ESRI and arcpy. 

NOTE: you will have to run this script in a QGIS-enabled environment. I do this via
Anaconda. 

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""
import os, sys
import json
import PyProj9_func as waterbodies
import PyProj9_gui
import qgis
import qgis.core
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as WebMapWidget
except:
    from PyQt5.QtWebKitWidgets import QWebView as WebMapWidget
 

# ======================================= 
# GUI event handler and related functions 
# ======================================= 
    
# User selects the input JSON file
def selectJson():
    global jsonFile
    jsonFile, _= QFileDialog.getOpenFileName(mainWindow,"Select JSON File", "","JSON (*.json)")
    if jsonFile:
        ui.jsonLE.setText(jsonFile)
        jsonFile = ui.jsonLE.text()

# User selects the output shapefile as a new file, or overwriting an existing one.
def linearOut():
    global linearOutput
    linearOutput, _= QFileDialog.getSaveFileName(mainWindow,"Enter linear features output name", "","Geopackage (*.gpkg)")
    if linearOutput:
       ui.linearOutLE.setText(linearOutput)
       linearOutput = ui.linearOutLE.text()

def arealOut():
    global arealOutput
    arealOutput, _= QFileDialog.getSaveFileName(mainWindow,"Enter output shapefile", "","Geopackage (*.gpkg)")
    if arealOutput:
       ui.arealOutLE.setText(arealOutput)
       arealOutput = ui.arealOutLE.text() 
    
# Function connected to the Start button to run the operation
def runFunction():
    try:    
        with open(jsonFile, encoding = "utf8") as file:
            data = json.load(file)
        
        elements = data['elements']

        for el in elements:
            if el['type'] == 'node':
                nodes[el['id']] = el
            if el['type'] == 'way':
                ways[el['id']] = el
                
        for way in ways:
            way = ways[way]
            for c in linearClasses:
                result = c.fromOSMWay(way, nodes)
                if result:
                    feat = result.toQgsFeature()
                    linesList.append(feat)
            for c in arealClasses:
                result = c.fromOSMWay(way, nodes)
                if result:
                    feat = result.toQgsFeature()
                    arealList.append(feat)

        waterbodies.LinearWaterbody.toGeoPackage(linesList, linearOutput)
        waterbodies.ArealWaterbody.toGeoPackage(arealList, arealOutput)
        QMessageBox.information(mainWindow, 'Operation Complete!', 'Creating new GeoPackage has been completed!. Please close the windows to exit the program.', QMessageBox.Ok )
    except Exception as e: 
        QMessageBox.information(mainWindow, 'An Error has occurred! ', 'Creating new GeoPackage has failed. Please check inputs and try again!', QMessageBox.Ok )
#========================================== 
# create app and main window + dialog GUI 
# =========================================
app = QApplication(sys.argv)  
mainWindow = QMainWindow() 
ui = PyProj9_gui.Ui_MainWindow() 
ui.setupUi(mainWindow)
qgis_prefix = os.getenv("QGIS_PREFIX_PATH")      
qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True) 
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()
#========================================== 
# connect signals 
#========================================== 
ui.jsonTB.clicked.connect(selectJson)
ui.linearOutTB.clicked.connect(linearOut)
ui.arealOutTB.clicked.connect(arealOut)
ui.StartPB.clicked.connect(runFunction)
#================================== 
# initialize global variables 
#==================================
linesList = []
arealList = []
linearClasses = [waterbodies.Stream, waterbodies.River, waterbodies.Canal]
arealClasses = [waterbodies.Lake, waterbodies.Pond, waterbodies.Reservoir]
nodes = {}
ways = {}
#======================================= 
# run app 
#======================================= 
mainWindow.show() 
sys.exit(app.exec_()) 