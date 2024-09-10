# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp_sensor_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 550))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btnParameters = QtWidgets.QPushButton(self.centralwidget)
        self.btnParameters.setObjectName("btnParameters")
        self.gridLayout.addWidget(self.btnParameters, 0, 0, 1, 1)
        self.btnStartDetection = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartDetection.setObjectName("btnStartDetection")
        self.gridLayout.addWidget(self.btnStartDetection, 0, 1, 1, 1)
        self.btnStopDetection = QtWidgets.QPushButton(self.centralwidget)
        self.btnStopDetection.setObjectName("btnStopDetection")
        self.gridLayout.addWidget(self.btnStopDetection, 0, 2, 1, 1)
        self.messageDisplay = QtWidgets.QTextEdit(self.centralwidget)
        self.messageDisplay.setObjectName("messageDisplay")
        self.gridLayout.addWidget(self.messageDisplay, 3, 0, 1, 1)
        self.dataDisplay = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.dataDisplay.sizePolicy().hasHeightForWidth())
        self.dataDisplay.setSizePolicy(sizePolicy)
        self.dataDisplay.setReadOnly(True)
        self.dataDisplay.setObjectName("dataDisplay")
        self.gridLayout.addWidget(self.dataDisplay, 4, 0, 3, 1)
        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 6, 1, 1, 1)
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setObjectName("btnClear")
        self.gridLayout.addWidget(self.btnClear, 6, 2, 1, 1)
        self.btnMoveLeft = QtWidgets.QPushButton(self.centralwidget)
        self.btnMoveLeft.setObjectName("btnMoveLeft")
        self.gridLayout.addWidget(self.btnMoveLeft, 5, 1, 1, 1)
        self.btnMoveRight = QtWidgets.QPushButton(self.centralwidget)
        self.btnMoveRight.setObjectName("btnMoveRight")
        self.gridLayout.addWidget(self.btnMoveRight, 5, 2, 1, 1)
        self.plotWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setObjectName("plotWidget")
        self.gridLayout.addWidget(self.plotWidget, 3, 1, 2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnParameters.setText(_translate("MainWindow", "Parameters"))
        self.btnStartDetection.setText(_translate("MainWindow", "Start"))
        self.btnStopDetection.setText(_translate("MainWindow", "Stop"))
        self.btnSave.setText(_translate("MainWindow", "Save"))
        self.btnClear.setText(_translate("MainWindow", "Clear"))
        self.btnMoveLeft.setText(_translate("MainWindow", "<"))
        self.btnMoveRight.setText(_translate("MainWindow", ">"))
