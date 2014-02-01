from PyQt4 import QtGui, QtCore
import sys, signal
from test import Ui_Form

class wombatClient(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.ui = Ui_Form()
		self.ui.setupUi(self)


def main():
	app = QtGui.QApplication(sys.argv)
	window = wombatClient()
	window.show()
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
