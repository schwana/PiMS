# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'displaysrs.ui'
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

class Ui_displaySRS(object):
    def setupUi(self, displaySRS):
        displaySRS.setObjectName(_fromUtf8("displaySRS"))
        displaySRS.resize(400, 300)
        self.centralWidget = QtGui.QWidget(displaySRS)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 190, 80, 22))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lcdTime = QtGui.QLCDNumber(self.centralWidget)
        self.lcdTime.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.lcdTime.setDigitCount(8)
        self.lcdTime.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdTime.setObjectName(_fromUtf8("lcdTime"))
        displaySRS.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(displaySRS)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 19))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        displaySRS.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(displaySRS)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        displaySRS.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(displaySRS)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        displaySRS.setStatusBar(self.statusBar)

        self.retranslateUi(displaySRS)
        QtCore.QMetaObject.connectSlotsByName(displaySRS)

    def retranslateUi(self, displaySRS):
        displaySRS.setWindowTitle(_translate("displaySRS", "displaySRS", None))
        self.pushButton.setText(_translate("displaySRS", "Test", None))

