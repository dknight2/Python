# -*- coding: utf-8 -*-
"""
This is the main script for PyProj7. It launches a GUI that takes inputs and runs the PyProj_7_func
function from those inputs. The point of this script is to do some basic filtering
while making use of a GUI interface and creating a new output from the selected inputs. 

There is no data uploaded associated with this script, but you can still launch the 
GUI and see the interface that I created. 

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""

import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as WebMapWidget
except:
    from PyQt5.QtWebKitWidgets import QWebView as WebMapWidget
 
import PyProj7_func  
import PyProj7_gui

# ======================================= 
# GUI event handler and related functions 
# ======================================= 
    
# Combo box with country values is available here. 
def countryQuery():
    global polygonValue
    polygonValue = ui.countryQueryCB.currentText()
    return polygonValue
    
# User selects the input Countries shapefile
def selectShapefile():
    global polygonFile
    polygonFile, _= QFileDialog.getOpenFileName(mainWindow,"Select Countries shapefile", "","Shapefile (*.shp)")
    if polygonFile:
        ui.inputPolygonLE.setText(polygonFile)
        polygonFile = ui.inputPolygonLE.text()

# User selects the input Points of Interest shapefile
def selectPOI():
    global pointFile
    pointFile, _= QFileDialog.getOpenFileName(mainWindow,"Select POI shapefile", "","Shapefile (*.shp)")
    if pointFile:
        ui.inputPoiShapefileLE.setText(pointFile)
        pointFile = ui.inputPoiShapefileLE.text()

# Establishes the shop type, which is optionally used during the processing
def updateShopTypeCB(): 
    global pointValue
    x = ui.shopTypesCheckBox.isChecked()
    # If the check boc is checked, all shops will be used, else, shop of choice
    if x == True:
        pointValue = ''
    else:
        pointValue = ui.shopTypesComboBox.currentText()

# User selects the output shapefile as a new file, or overwriting an existing one.
def outputFolder():
    global outputFile
    outputFile, _= QFileDialog.getSaveFileName(mainWindow,"Enter output shapefile", "","Shapefile (*.shp)")
    if outputFile:
       ui.outputShapefileLE.setText(outputFile)
       outputFile = ui.outputShapefileLE.text()
   
# Function connected to the Start button to run the operation
def runFunction():
    try:
        PyProj7_func.mainFunction(polygonFile, polygonField, polygonValue, pointFile, pointField, pointValue, outputFile)
        ui.statusbar.showMessage('New shapefile with desired shops has been created! \nPlease add them to ArcGIS Pro to view results!')
    except Exception as e: 
        QMessageBox.information(mainWindow, 'Operation failed', 'Creating new shapefile failed with '+ str(e.__class__) + ': ' + str(e), QMessageBox.Ok )
#========================================== 
# create app and main window + dialog GUI 
# =========================================

app = QApplication(sys.argv)  

mainWindow = QMainWindow() 
ui = PyProj7_gui.Ui_MainWindow() 
ui.setupUi(mainWindow)

#========================================== 
# connect signals 
#========================================== 
ui.inputPolygonTB.clicked.connect(selectShapefile)
ui.inputPoiTB.clicked.connect(selectPOI)
ui.outputShapefileTB.clicked.connect(outputFolder)
ui.countryQueryCB.activated.connect(countryQuery)
ui.shopTypesComboBox.activated.connect(updateShopTypeCB)
ui.startPB.clicked.connect(runFunction)
#================================== 
# initialize global variables 
#================================== 
polygonField = 'NAME'
polygonValue = countryQuery()
pointField = 'shop'
pointValue = updateShopTypeCB()
#======================================= 
# run app 
#======================================= 
mainWindow.show() 
sys.exit(app.exec_()) 

