# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\config_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import json

CONFIG_FILE_PATH = "../configuration.config"
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 60, 371, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tarsier_path = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.tarsier_path.setObjectName("tarsier_path")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tarsier_path)
        self.fuseki_path = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.fuseki_path.setObjectName("fuseki_path")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.fuseki_path)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.news_update = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.news_update.setObjectName("news_update")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.news_update)

        self.show_field()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Tarsier Path"))
        self.label.setText(_translate("Dialog", "News Update period (s)"))
        self.label_3.setText(_translate("Dialog", "Fuseki Path"))

    def show_field(self):
        with open(CONFIG_FILE_PATH, "r") as f:
            config_file=json.load(f)
            f.close()
        self.tarsier_path.setText(config_file["tarsier_path"])
        self.fuseki_path.setText(config_file["fuseki_path"])
        self.news_update.setText(str(config_file["news_update"]))

    def save_field(self):
        config_file["tarsier_path"] = self.tarsier_path.get
        self.fuseki_path.setText(config_file["fuseki_path"])
        self.news_update.setText(str(config_file["news_update"]))
        with open(CONFIG_FILE_PATH, "w") as f:
            f.write(json.dumps(config_file))
            f.close()