import sys
from PyQt5 import QtWidgets, QtCore
from gui.client_gui_specialized import ClientGUI


class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ClientGUI()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.isInitialized = False

    def closeEvent(self, event):
        # NB if main loop is kept opened it may take a while to be closed...
        result = QtWidgets.QMessageBox.question(
            self, 'Confirm Close', 'Are you sure you want to close?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            self.ui.shutdown_finNSEMA()
            event.accept()
        else:
            event.ignore()

    def showEvent(self, event):
        if not self.isInitialized:
            self.ui.update_log("Welcome in finSEMA, system loading hold on...")
            t = QtCore.QTimer()
            t.singleShot(100, self.ui.startup_finNSEMA_daemons)
            self.ui.setupEvent()
            self.isInitialized = True

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                print('changeEvent: Minimised')
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                print('changeEvent: Maximised/FullScreen')


def run_finSEMA():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_finSEMA()