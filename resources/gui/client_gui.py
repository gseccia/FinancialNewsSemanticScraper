# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\gui\client_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_finNSEMA(object):
    def setupUi(self, finNSEMA):
        finNSEMA.setObjectName("finNSEMA")
        finNSEMA.resize(651, 549)
        self.bg_image_label = QtWidgets.QLabel(finNSEMA)
        self.bg_image_label.setGeometry(QtCore.QRect(-90, -40, 931, 611))
        self.bg_image_label.setText("")
        self.bg_image_label.setPixmap(QtGui.QPixmap("resources\\gui\\big_data_fintech_globe_thinkstock_826139768-100749747-large.jpg"))
        self.bg_image_label.setScaledContents(False)
        self.bg_image_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bg_image_label.setWordWrap(False)
        self.bg_image_label.setIndent(3)
        self.bg_image_label.setObjectName("bg_image_label")
        self.launch_button = QtWidgets.QPushButton(finNSEMA)
        self.launch_button.setGeometry(QtCore.QRect(240, 230, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.launch_button.setFont(font)
        self.launch_button.setAutoFillBackground(False)
        self.launch_button.setStyleSheet("background-color: rgb(1, 65, 92);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 155, 183);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"")
        self.launch_button.setDefault(False)
        self.launch_button.setFlat(False)
        self.launch_button.setObjectName("launch_button")
        self.vis_button = QtWidgets.QPushButton(finNSEMA)
        self.vis_button.setGeometry(QtCore.QRect(60, 230, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.vis_button.setFont(font)
        self.vis_button.setAutoFillBackground(False)
        self.vis_button.setStyleSheet("background-color: rgb(1, 65, 92);\n"
"color: rgb(255, 255, 255);\n"
"gridline-color: rgb(255, 0, 127);\n"
"border-top-color: rgb(255, 0, 0);\n"
"border-color: rgb(255, 155, 183);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"")
        self.vis_button.setDefault(False)
        self.vis_button.setFlat(False)
        self.vis_button.setObjectName("vis_button")
        self.scroll_area_log = QtWidgets.QScrollArea(finNSEMA)
        self.scroll_area_log.setGeometry(QtCore.QRect(60, 320, 531, 151))
        self.scroll_area_log.setStyleSheet("background-color: rgb(1, 65, 92);\n"
"gridline-color: rgb(255, 0, 127);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(244, 68, 79);")
        self.scroll_area_log.setWidgetResizable(True)
        self.scroll_area_log.setObjectName("scroll_area_log")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 149))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll_area_log.setWidget(self.scrollAreaWidgetContents)
        self.log_label = QtWidgets.QLabel(finNSEMA)
        self.log_label.setGeometry(QtCore.QRect(60, 300, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.log_label.setFont(font)
        self.log_label.setStyleSheet("color: rgb(248, 72, 49);\n"
"color: rgb(5, 26, 60);")
        self.log_label.setObjectName("log_label")
        self.motto1 = QtWidgets.QLabel(finNSEMA)
        self.motto1.setGeometry(QtCore.QRect(160, 150, 331, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.motto1.setFont(font)
        self.motto1.setStyleSheet("color: rgb(243, 17, 28);\n"
"color: rgb(255, 255, 255);")
        self.motto1.setObjectName("motto1")
        self.motto2 = QtWidgets.QLabel(finNSEMA)
        self.motto2.setGeometry(QtCore.QRect(170, 170, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.motto2.setFont(font)
        self.motto2.setStyleSheet("color: rgb(243, 17, 28);\n"
"color: rgb(255, 255, 255);")
        self.motto2.setObjectName("motto2")
        self.stripe_label = QtWidgets.QLabel(finNSEMA)
        self.stripe_label.setGeometry(QtCore.QRect(0, 150, 651, 51))
        self.stripe_label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));")
        self.stripe_label.setText("")
        self.stripe_label.setObjectName("stripe_label")
        self.label = QtWidgets.QLabel(finNSEMA)
        self.label.setGeometry(QtCore.QRect(-100, -120, 801, 451))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources\\gui\\logo_stroke.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.conf_button = QtWidgets.QPushButton(finNSEMA)
        self.conf_button.setGeometry(QtCore.QRect(420, 230, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.conf_button.setFont(font)
        self.conf_button.setAutoFillBackground(False)
        self.conf_button.setStyleSheet("background-color: rgb(1, 65, 92);\n"
"color: rgb(255, 255, 255);\n"
"gridline-color: rgb(255, 0, 127);\n"
"border-top-color: rgb(255, 0, 0);\n"
"border-color: rgb(255, 155, 183);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"")
        self.conf_button.setDefault(False)
        self.conf_button.setFlat(False)
        self.conf_button.setObjectName("conf_button")
        self.news_counter_label = QtWidgets.QLabel(finNSEMA)
        self.news_counter_label.setGeometry(QtCore.QRect(230, 480, 231, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.news_counter_label.setFont(font)
        self.news_counter_label.setStyleSheet("color: rgb(0, 2, 37);")
        self.news_counter_label.setObjectName("news_counter_label")
        self.bg_image_label.raise_()
        self.scroll_area_log.raise_()
        self.log_label.raise_()
        self.stripe_label.raise_()
        self.label.raise_()
        self.launch_button.raise_()
        self.vis_button.raise_()
        self.conf_button.raise_()
        self.motto1.raise_()
        self.motto2.raise_()
        self.news_counter_label.raise_()

        self.retranslateUi(finNSEMA)
        QtCore.QMetaObject.connectSlotsByName(finNSEMA)

    def retranslateUi(self, finNSEMA):
        _translate = QtCore.QCoreApplication.translate
        finNSEMA.setWindowTitle(_translate("finNSEMA", "finSEMA"))
        self.launch_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Launch the application</p></body></html>"))
        self.launch_button.setText(_translate("finNSEMA", "Launch Engine"))
        self.vis_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Visualize Data</p></body></html>"))
        self.vis_button.setText(_translate("finNSEMA", "Visualize Data"))
        self.log_label.setText(_translate("finNSEMA", "Logging Info"))
        self.motto1.setText(_translate("finNSEMA", "Bring your financial business to a higher level"))
        self.motto2.setText(_translate("finNSEMA", "embracing the power of semantic analysis"))
        self.conf_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Visualize Data</p></body></html>"))
        self.conf_button.setText(_translate("finNSEMA", "Configure"))
        self.news_counter_label.setText(_translate("finNSEMA", "News processed up to now:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    finNSEMA = QtWidgets.QDialog()
    ui = Ui_finNSEMA()
    ui.setupUi(finNSEMA)
    finNSEMA.show()
    sys.exit(app.exec_())
