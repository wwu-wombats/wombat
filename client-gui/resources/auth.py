# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auth.ui'
#
# Created: Sat Feb  1 17:37:19 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_authForm(object):
    def setupUi(self, authForm):
        authForm.setObjectName(_fromUtf8("authForm"))
        authForm.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("wombat.gif")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        authForm.setWindowIcon(icon)
        self.label = QtGui.QLabel(authForm)
        self.label.setGeometry(QtCore.QRect(71, 10, 240, 38))
        self.label.setObjectName(_fromUtf8("label"))
        self.username = QtGui.QLineEdit(authForm)
        self.username.setGeometry(QtCore.QRect(71, 110, 241, 25))
        self.username.setObjectName(_fromUtf8("username"))
        self.password = QtGui.QLineEdit(authForm)
        self.password.setGeometry(QtCore.QRect(70, 150, 240, 25))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.loginButton = QtGui.QPushButton(authForm)
        self.loginButton.setGeometry(QtCore.QRect(200, 190, 111, 27))
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.label_2 = QtGui.QLabel(authForm)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 401, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(authForm)
        QtCore.QMetaObject.connectSlotsByName(authForm)

    def retranslateUi(self, authForm):
        authForm.setWindowTitle(QtGui.QApplication.translate("authForm", "Wombat v.1 | SetUp", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("authForm", "<html><head/><body><p><span style=\" font-size:24pt; color:#06ccde;\">Wombat SetUp</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.username.setPlaceholderText(QtGui.QApplication.translate("authForm", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.password.setPlaceholderText(QtGui.QApplication.translate("authForm", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("authForm", "Log In", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("authForm", "<html><head/><body><p><span style=\" font-size:11pt; text-decoration: underline; color:#0563de;\">Log in to your wombat account to get started now!</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

