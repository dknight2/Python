# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L4_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(513, 160)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.jsonTB = QtWidgets.QToolButton(self.centralwidget)
        self.jsonTB.setObjectName("jsonTB")
        self.gridLayout.addWidget(self.jsonTB, 0, 3, 1, 1)
        self.linearOutLE = QtWidgets.QLineEdit(self.centralwidget)
        self.linearOutLE.setObjectName("linearOutLE")
        self.gridLayout.addWidget(self.linearOutLE, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.jsonLE = QtWidgets.QLineEdit(self.centralwidget)
        self.jsonLE.setObjectName("jsonLE")
        self.gridLayout.addWidget(self.jsonLE, 0, 2, 1, 1)
        self.arealOutTB = QtWidgets.QToolButton(self.centralwidget)
        self.arealOutTB.setObjectName("arealOutTB")
        self.gridLayout.addWidget(self.arealOutTB, 3, 3, 1, 1)
        self.arealOutLE = QtWidgets.QLineEdit(self.centralwidget)
        self.arealOutLE.setObjectName("arealOutLE")
        self.gridLayout.addWidget(self.arealOutLE, 3, 2, 1, 1)
        self.linearOutTB = QtWidgets.QToolButton(self.centralwidget)
        self.linearOutTB.setObjectName("linearOutTB")
        self.gridLayout.addWidget(self.linearOutTB, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.StartPB = QtWidgets.QPushButton(self.centralwidget)
        self.StartPB.setObjectName("StartPB")
        self.gridLayout.addWidget(self.StartPB, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Areal output name:"))
        self.jsonTB.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Linear output name:"))
        self.arealOutTB.setText(_translate("MainWindow", "..."))
        self.linearOutTB.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Input JSON file:"))
        self.StartPB.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

