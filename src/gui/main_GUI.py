import sys
import time
from PyQt5 import QtWidgets, QtCore
from gui.client_gui_specialized import ClientGUI


class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ClientGUI()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(
            self, 'Confirm Close', 'Are you sure you want to close?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.ui.shutdown_finNSEMA()
        else:
            event.ignore()

    def showEvent(self, event):
        self.ui.update_log("Welcome in finSEMA, system loading hold on...")
        t = QtCore.QTimer()
        t.singleShot(100, self.ui.startup_finNSEMA_daemons)


def run_finSEMA():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_finSEMA()