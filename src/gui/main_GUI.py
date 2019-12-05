import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from gui.client_gui_specialized import ClientGUI
from gui.SemantiCat import SemantiCat
import numpy as np


class MainWindow(QtWidgets.QGraphicsView, QtWidgets.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ClientGUI()
        self.ui.setupUi(self)
        self.isInitialized = False
        self.initAnimation()


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

    ### Animation methods

    def initAnimation(self):
        self.semanticat = SemantiCat()
        self.anim = QtCore.QPropertyAnimation(self.semanticat.l, b'pos')
        self.anim.setDuration(12000)

        # Animation
        self.anim.setStartValue(QtCore.QPointF(0, 150-0.1*self.semanticat.icon_size))
        self.anim.setKeyValueAt(0.25, QtCore.QPointF(144, 150-0.1*self.semanticat.icon_size))
        self.anim.setKeyValueAt(0.5, QtCore.QPointF(288, 150-0.1*self.semanticat.icon_size))
        self.anim.setKeyValueAt(0.75, QtCore.QPointF(432, 150-0.1*self.semanticat.icon_size))
        self.anim.setEndValue(QtCore.QPointF(651 - self.semanticat.icon_size, 150-0.1*self.semanticat.icon_size))

        self.scene = QtWidgets.QGraphicsScene(self)
        self.semanticat.l.setParent(self)

        self.setScene(self.scene)

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.anim.valueChanged.connect(self.animated)
        self.setFixedSize(650, 549)
        QtCore.QTimer().singleShot(3000, self.anim.start)
        # self.anim.start()
        # self.show()

    def outward_animation(self):
        x_points = np.linspace(0, 651 - self.semanticat.icon_size, num=5)
        y_points = np.linspace(150, 201, num=2) -0.1*self.semanticat.icon_size
        perc = np.linspace(0, 1, num=5)
        self.anim.setStartValue(QtCore.QPointF(x_points[0], y_points[0]))
        self.anim.setKeyValueAt(perc[1], QtCore.QPointF(x_points[1], y_points[0]))
        self.anim.setKeyValueAt(perc[2], QtCore.QPointF(x_points[2], y_points[0]))
        self.anim.setKeyValueAt(perc[3], QtCore.QPointF(x_points[3], y_points[0]))
        self.anim.setEndValue(QtCore.QPointF(x_points[4], y_points[0]))
        self.anim.start()

    def backward_animation(self):
        x_points = np.linspace(0, 651 - self.semanticat.icon_size, num=5)
        y_points = np.linspace(150, 201, num=2) -0.1*self.semanticat.icon_size
        perc = np.linspace(0, 1, num=5)
        self.anim.setStartValue(QtCore.QPointF(x_points[4], y_points[0]))
        self.anim.setKeyValueAt(perc[1], QtCore.QPointF(x_points[3], y_points[0]))
        self.anim.setKeyValueAt(perc[2], QtCore.QPointF(x_points[2], y_points[0]))
        self.anim.setKeyValueAt(perc[3], QtCore.QPointF(x_points[1], y_points[0]))
        self.anim.setEndValue(QtCore.QPointF(x_points[0], y_points[0]))
        self.anim.start()

    def animated(self, value):
        if value.x() >= 651 - self.semanticat.icon_size:
            # print("Fine corsa di andata")
            self.anim.stop()
            self.anim.disconnect()
            self.backward_animation()
            self.anim.valueChanged.connect(self.animated)
        elif value.x() == 0:
            # print("Fine corsa di ritorno")
            self.anim.stop()
            self.anim.disconnect()
            self.outward_animation()
            self.anim.valueChanged.connect(self.animated)
        self.update()


def run_finSEMA():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_finSEMA()