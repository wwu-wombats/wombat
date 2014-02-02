# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dirs.ui'
#
# Created: Sat Feb  1 16:51:03 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dirForm(object):
    def setupUi(self, dirForm):
        dirForm.setObjectName(_fromUtf8("dirForm"))
        dirForm.resize(400, 300)
        dirForm.setAutoFillBackground(False)
        self.label = QtGui.QLabel(dirForm)
        self.label.setGeometry(QtCore.QRect(40, 20, 311, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.addDir = QtGui.QPushButton(dirForm)
        self.addDir.setGeometry(QtCore.QRect(320, 75, 30, 21))
        self.addDir.setStyleSheet(_fromUtf8("font-size:24px;\n"
"font-weight:bold;\n"
"color: rgb(92, 208, 38);"))
        self.addDir.setObjectName(_fromUtf8("addDir"))
        self.finButton = QtGui.QPushButton(dirForm)
        self.finButton.setGeometry(QtCore.QRect(250, 250, 100, 27))
        self.finButton.setObjectName(_fromUtf8("finButton"))
        self.dirList = QtGui.QPlainTextEdit(dirForm)
        self.dirList.setGeometry(QtCore.QRect(30, 100, 320, 141))
        self.dirList.setObjectName(_fromUtf8("dirList"))

        self.retranslateUi(dirForm)
        QtCore.QMetaObject.connectSlotsByName(dirForm)

    def retranslateUi(self, dirForm):
        dirForm.setWindowTitle(QtGui.QApplication.translate("dirForm", "Wombat v.1", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dirForm", "Please select the directories to monitor.", None, QtGui.QApplication.UnicodeUTF8))
        self.addDir.setText(QtGui.QApplication.translate("dirForm", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.finButton.setText(QtGui.QApplication.translate("dirForm", "Finish!", None, QtGui.QApplication.UnicodeUTF8))

