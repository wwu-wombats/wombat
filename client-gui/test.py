# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created: Fri Jan 31 20:44:02 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 30, 131, 61))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(110, 110, 171, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 150, 171, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.logInButton = QtGui.QPushButton(Form)
        self.logInButton.setGeometry(QtCore.QRect(115, 223, 161, 31))
        self.logInButton.setStyleSheet(_fromUtf8("color:rgb(8, 243, 255);\n"
"font-size: 24px;"))
        self.logInButton.setObjectName(_fromUtf8("logInButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:24pt; color:#00fefe;\">Log In</span></p></body></html>", None))
        self.lineEdit.setPlaceholderText(_translate("Form", "Username", None))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password", None))
        self.logInButton.setText(_translate("Form", "LOG IN", None))

