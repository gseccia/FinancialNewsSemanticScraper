# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './resources/gui/client_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_finNSEMA(object):
    def setupUi(self, finNSEMA):
        finNSEMA.setObjectName("finNSEMA")
        finNSEMA.setEnabled(True)
        finNSEMA.resize(650, 549)
        finNSEMA.setFixedSize(650, 549)
        finNSEMA.setWindowIcon(QtGui.QIcon("../../resources/gui/icon.png"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(finNSEMA.sizePolicy().hasHeightForWidth())
        finNSEMA.setSizePolicy(sizePolicy)
        self.bg_image_label = QtWidgets.QLabel(finNSEMA)
        self.bg_image_label.setGeometry(QtCore.QRect(-90, -40, 931, 611))
        self.bg_image_label.setText("")
        self.bg_image_label.setPixmap(QtGui.QPixmap("../../resources/gui/big_data_fintech_globe_thinkstock_826139768-100749747-large.jpg"))
        self.bg_image_label.setScaledContents(False)
        self.bg_image_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bg_image_label.setWordWrap(False)
        self.bg_image_label.setIndent(3)
        self.bg_image_label.setObjectName("bg_image_label")
        self.launch_button = QtWidgets.QPushButton(finNSEMA)
        self.launch_button.setGeometry(QtCore.QRect(230, 220, 72, 72))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.launch_button.setFont(font)
        self.launch_button.setAutoFillBackground(False)
        self.launch_button.setStyleSheet("border: 0px;\n"
"background: transparent;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.launch_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../resources/gui/off_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.launch_button.setIcon(icon)
        self.launch_button.setIconSize(QtCore.QSize(64, 64))
        self.launch_button.setDefault(False)
        self.launch_button.setFlat(False)
        self.launch_button.setObjectName("launch_button")
        self.vis_button = QtWidgets.QPushButton(finNSEMA)
        self.vis_button.setGeometry(QtCore.QRect(450, 220, 72, 72))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.vis_button.setFont(font)
        self.vis_button.setAutoFillBackground(False)
        self.vis_button.setStyleSheet("border: 0px;\n"
"background: transparent;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.vis_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../resources/gui/visualize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.vis_button.setIcon(icon1)
        self.vis_button.setIconSize(QtCore.QSize(64, 64))
        self.vis_button.setDefault(False)
        self.vis_button.setFlat(False)
        self.vis_button.setObjectName("vis_button")
        self.log_label = QtWidgets.QLabel(finNSEMA)
        self.log_label.setGeometry(QtCore.QRect(60, 320, 121, 20))
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
        self.label.setPixmap(QtGui.QPixmap("../../resources/gui/logo_stroke.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.conf_button = QtWidgets.QPushButton(finNSEMA)
        self.conf_button.setGeometry(QtCore.QRect(120, 220, 72, 72))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.conf_button.setFont(font)
        self.conf_button.setAutoFillBackground(False)
        self.conf_button.setStyleSheet("border: 0px;\n"
"background: transparent;\n"
"background-color: rgba(255, 255, 255, 0);\n"
"")
        self.conf_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../resources/gui/Settings_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.conf_button.setIcon(icon2)
        self.conf_button.setIconSize(QtCore.QSize(64, 64))
        self.conf_button.setDefault(False)
        self.conf_button.setFlat(False)
        self.conf_button.setObjectName("conf_button")
        self.news_counter_label = QtWidgets.QLabel(finNSEMA)
        self.news_counter_label.setGeometry(QtCore.QRect(230, 500, 231, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.news_counter_label.setFont(font)
        self.news_counter_label.setStyleSheet("color: rgb(0, 2, 37);")
        self.news_counter_label.setObjectName("news_counter_label")
        self.query_button = QtWidgets.QPushButton(finNSEMA)
        self.query_button.setGeometry(QtCore.QRect(340, 220, 72, 72))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.query_button.setFont(font)
        self.query_button.setAutoFillBackground(False)
        self.query_button.setStyleSheet("border: 0px;\n"
"background: transparent;\n"
"background-color: rgba(255, 255, 255, 0);\n"
"")
        self.query_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../resources/gui/query_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.query_button.setIcon(icon3)
        self.query_button.setIconSize(QtCore.QSize(64, 64))
        self.query_button.setDefault(False)
        self.query_button.setFlat(False)
        self.query_button.setObjectName("query_button")
        self.log_area = QtWidgets.QTextEdit(finNSEMA)
        self.log_area.setGeometry(QtCore.QRect(60, 340, 521, 141))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.log_area.setFont(font)
        self.log_area.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.log_area.setReadOnly(True)
        self.log_area.setObjectName("log_area")
        self.bg_image_label.raise_()
        self.stripe_label.raise_()
        self.label.raise_()
        self.launch_button.raise_()
        self.vis_button.raise_()
        self.conf_button.raise_()
        self.motto1.raise_()
        self.motto2.raise_()
        self.news_counter_label.raise_()
        self.query_button.raise_()
        self.log_label.raise_()
        self.log_area.raise_()

        self.retranslateUi(finNSEMA)
        QtCore.QMetaObject.connectSlotsByName(finNSEMA)

    def retranslateUi(self, finNSEMA):
        _translate = QtCore.QCoreApplication.translate
        finNSEMA.setWindowTitle(_translate("finNSEMA", "finNSEMA"))
        self.launch_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Launch the application</p></body></html>"))
        self.vis_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Visualize Data</p></body></html>"))
        self.log_label.setText(_translate("finNSEMA", "Logging Info"))
        self.motto1.setText(_translate("finNSEMA", "Bring your financial business to a higher level"))
        self.motto2.setText(_translate("finNSEMA", "embracing the power of semantic analysis"))
        self.conf_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Set configuration file</p></body></html>"))
        self.news_counter_label.setText(_translate("finNSEMA", "News processed up to now: 0"))
        self.query_button.setToolTip(_translate("finNSEMA", "<html><head/><body><p>Interactive query compilation</p></body></html>"))
