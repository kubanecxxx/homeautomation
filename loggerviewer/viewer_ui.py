# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(666, 601)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonOpen = QtGui.QPushButton(self.groupBox)
        self.buttonOpen.setObjectName(_fromUtf8("buttonOpen"))
        self.horizontalLayout.addWidget(self.buttonOpen)
        self.buttonClose = QtGui.QPushButton(self.groupBox)
        self.buttonClose.setObjectName(_fromUtf8("buttonClose"))
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.spinControl = QtGui.QSpinBox(self.groupBox)
        self.spinControl.setMaximum(10000)
        self.spinControl.setProperty("value", 5559)
        self.spinControl.setObjectName(_fromUtf8("spinControl"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinControl)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.editIP = QtGui.QLineEdit(self.groupBox)
        self.editIP.setObjectName(_fromUtf8("editIP"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.editIP)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinPort = QtGui.QSpinBox(self.groupBox)
        self.spinPort.setMinimum(5000)
        self.spinPort.setMaximum(10000)
        self.spinPort.setProperty("value", 5550)
        self.spinPort.setObjectName(_fromUtf8("spinPort"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.spinPort)
        self.buttonStart = QtGui.QPushButton(self.groupBox)
        self.buttonStart.setObjectName(_fromUtf8("buttonStart"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.buttonStart)
        self.buttonStop = QtGui.QPushButton(self.groupBox)
        self.buttonStop.setObjectName(_fromUtf8("buttonStop"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.buttonStop)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.groupBox_2 = QtGui.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.plainReturn = QtGui.QPlainTextEdit(self.groupBox_2)
        self.plainReturn.setReadOnly(True)
        self.plainReturn.setObjectName(_fromUtf8("plainReturn"))
        self.verticalLayout_3.addWidget(self.plainReturn)
        self.editShell = QtGui.QLineEdit(self.groupBox_2)
        self.editShell.setObjectName(_fromUtf8("editShell"))
        self.verticalLayout_3.addWidget(self.editShell)
        self.groupBox_3 = QtGui.QGroupBox(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.plainOutput = QtGui.QPlainTextEdit(self.groupBox_3)
        self.plainOutput.setReadOnly(True)
        self.plainOutput.setObjectName(_fromUtf8("plainOutput"))
        self.verticalLayout_4.addWidget(self.plainOutput)
        self.editFilter = QtGui.QLineEdit(self.groupBox_3)
        self.editFilter.setObjectName(_fromUtf8("editFilter"))
        self.verticalLayout_4.addWidget(self.editFilter)
        self.verticalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Home automation logging", None))
        self.groupBox.setTitle(_translate("MainWindow", "Control", None))
        self.buttonOpen.setText(_translate("MainWindow", "Open TCP", None))
        self.buttonClose.setText(_translate("MainWindow", "Close TCP", None))
        self.label_4.setText(_translate("MainWindow", "Control port", None))
        self.label_5.setText(_translate("MainWindow", "IP address", None))
        self.editIP.setText(_translate("MainWindow", "10.0.2.15", None))
        self.label_2.setText(_translate("MainWindow", "Logging port", None))
        self.buttonStart.setText(_translate("MainWindow", "Start", None))
        self.buttonStop.setText(_translate("MainWindow", "Stop", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Shell", None))
        self.editShell.setPlaceholderText(_translate("MainWindow", "Shell", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Log output", None))
        self.editFilter.setPlaceholderText(_translate("MainWindow", "Filter", None))

