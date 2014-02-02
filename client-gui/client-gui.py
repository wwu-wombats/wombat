from PyQt4 import QtGui, QtCore
import sys, signal
from resources.auth import Ui_authForm
from resources.dirs import Ui_dirForm


class authClient(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.auth = Ui_authForm()
        self.auth.setupUi(self)

        self.auth.loginButton.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.auth.username.text().toAscii()
        password = self.auth.password.text().toAscii()

        print username + " " + password
        self.showDirWidget()

    def showDirWidget(self):
        window.hide()
        global window
        window = dirSelector()
        window.show()


class dirSelector(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.dirSelection = Ui_dirForm()
        self.dirSelection.setupUi(self)

        self.dirSelection.addDir.clicked.connect(self.chooseDir)

    def chooseDir(self):
        selection = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.updateDirList(selection)

    def updateDirList(self, selection):
        self.dirSelection.dirList.insertPlainText(selection + '\n')

def main():
    global window
    app = QtGui.QApplication(sys.argv)
    window = authClient()
    window.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())

if __name__ == '__main__':
	main()
