# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameters_dialog_box.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setMinimumSize(QtCore.QSize(400, 300))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_measureInterval = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_measureInterval.setObjectName("lineEdit_measureInterval")
        self.gridLayout.addWidget(self.lineEdit_measureInterval, 3, 1, 1, 1)
        self.label_serialPort = QtWidgets.QLabel(Dialog)
        self.label_serialPort.setObjectName("label_serialPort")
        self.gridLayout.addWidget(self.label_serialPort, 0, 0, 1, 1)
        self.label_SimulationMode = QtWidgets.QLabel(Dialog)
        self.label_SimulationMode.setObjectName("label_SimulationMode")
        self.gridLayout.addWidget(self.label_SimulationMode, 4, 0, 1, 1)
        self.lineEdit_baudRate = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_baudRate.setObjectName("lineEdit_baudRate")
        self.gridLayout.addWidget(self.lineEdit_baudRate, 1, 1, 1, 1)
        self.lineEdit_Dt = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Dt.setText("")
        self.lineEdit_Dt.setObjectName("lineEdit_Dt")
        self.gridLayout.addWidget(self.lineEdit_Dt, 2, 1, 1, 1)
        self.label_secs1 = QtWidgets.QLabel(Dialog)
        self.label_secs1.setObjectName("label_secs1")
        self.gridLayout.addWidget(self.label_secs1, 2, 2, 1, 1)
        self.btnSave = QtWidgets.QPushButton(Dialog)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 8, 1, 1, 1)
        self.radioButton_simOn = QtWidgets.QRadioButton(Dialog)
        self.radioButton_simOn.setAutoExclusive(True)
        self.radioButton_simOn.setObjectName("radioButton_simOn")
        self.gridLayout.addWidget(self.radioButton_simOn, 4, 1, 1, 1)
        self.label_baudRate = QtWidgets.QLabel(Dialog)
        self.label_baudRate.setObjectName("label_baudRate")
        self.gridLayout.addWidget(self.label_baudRate, 1, 0, 1, 1)
        self.label_Dt = QtWidgets.QLabel(Dialog)
        self.label_Dt.setObjectName("label_Dt")
        self.gridLayout.addWidget(self.label_Dt, 2, 0, 1, 1)
        self.label_measureInterval = QtWidgets.QLabel(Dialog)
        self.label_measureInterval.setObjectName("label_measureInterval")
        self.gridLayout.addWidget(self.label_measureInterval, 3, 0, 1, 1)
        self.btnCancel = QtWidgets.QPushButton(Dialog)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout.addWidget(self.btnCancel, 8, 0, 1, 1)
        self.lineEdit_serialPort = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_serialPort.setObjectName("lineEdit_serialPort")
        self.gridLayout.addWidget(self.lineEdit_serialPort, 0, 1, 1, 1)
        self.label_secs2 = QtWidgets.QLabel(Dialog)
        self.label_secs2.setObjectName("label_secs2")
        self.gridLayout.addWidget(self.label_secs2, 3, 2, 1, 1)
        self.radioButton_simOff = QtWidgets.QRadioButton(Dialog)
        self.radioButton_simOff.setChecked(True)
        self.radioButton_simOff.setAutoExclusive(True)
        self.radioButton_simOff.setObjectName("radioButton_simOff")
        self.gridLayout.addWidget(self.radioButton_simOff, 5, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_serialPort.setText(_translate("Dialog", "Serial port:"))
        self.label_SimulationMode.setText(_translate("Dialog", "Simulation mode:"))
        self.lineEdit_baudRate.setText(_translate("Dialog", "9600"))
        self.label_secs1.setText(_translate("Dialog", "s"))
        self.btnSave.setText(_translate("Dialog", "Save"))
        self.radioButton_simOn.setText(_translate("Dialog", "On"))
        self.label_baudRate.setText(_translate("Dialog", "Baud rate:"))
        self.label_Dt.setText(_translate("Dialog", "Time window:"))
        self.label_measureInterval.setText(_translate("Dialog", "Measure interval:"))
        self.btnCancel.setText(_translate("Dialog", "Cancel"))
        self.lineEdit_serialPort.setText(_translate("Dialog", "COM3"))
        self.label_secs2.setText(_translate("Dialog", "s"))
        self.radioButton_simOff.setText(_translate("Dialog", "Off"))
