# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/gui/gen_query.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(680, 450)
        Dialog.setFixedSize(680, 450)
        Dialog.setWindowIcon(QtGui.QIcon("../../resources/gui/icon.png"))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-50, -10, 891, 531))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../resources/gui/big_data_fintech_globe_thinkstock_826139768-100749747-large.jpg"))
        self.label.setObjectName("label")
        self.queryTextArea = QtWidgets.QTextEdit(Dialog)
        self.queryTextArea.setGeometry(QtCore.QRect(40, 200, 600, 190))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.queryTextArea.setFont(font)
        self.queryTextArea.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.queryTextArea.setObjectName("queryTextArea")
        self.generateButton = QtWidgets.QPushButton(Dialog)
        self.generateButton.setGeometry(QtCore.QRect(304, 120, 72, 72))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.generateButton.setFont(font)
        self.generateButton.setStyleSheet("border: 0px;\n"
"background: transparent;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.generateButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../resources/gui/gen_query_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.generateButton.setIcon(icon)
        self.generateButton.setIconSize(QtCore.QSize(64, 64))
        self.generateButton.setObjectName("generateButton")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(229, 390, 222, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 9, 44);")
        self.label_2.setObjectName("label_2")
        self.group_label = QtWidgets.QLabel(Dialog)
        self.group_label.setGeometry(QtCore.QRect(50, 30, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.group_label.setFont(font)
        self.group_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.group_label.setObjectName("group_label")
        self.subgroup_label = QtWidgets.QLabel(Dialog)
        self.subgroup_label.setGeometry(QtCore.QRect(170, 30, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subgroup_label.setFont(font)
        self.subgroup_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.subgroup_label.setObjectName("subgroup_label")
        self.positiveness_label = QtWidgets.QLabel(Dialog)
        self.positiveness_label.setGeometry(QtCore.QRect(350, 30, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.positiveness_label.setFont(font)
        self.positiveness_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.positiveness_label.setObjectName("positiveness_label")
        self.threshold_label = QtWidgets.QLabel(Dialog)
        self.threshold_label.setGeometry(QtCore.QRect(420, 30, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.threshold_label.setFont(font)
        self.threshold_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.threshold_label.setObjectName("threshold_label")
        self.group_list = QtWidgets.QListWidget(Dialog)
        self.group_list.setGeometry(QtCore.QRect(50, 60, 101, 41))
        self.group_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.group_list.setObjectName("group_list")
        item = QtWidgets.QListWidgetItem()
        self.group_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.group_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.group_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.group_list.addItem(item)
        self.subgroup_list = QtWidgets.QListWidget(Dialog)
        self.subgroup_list.setGeometry(QtCore.QRect(170, 60, 161, 41))
        self.subgroup_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.subgroup_list.setObjectName("subgroup_list")
        self.positiveness_list = QtWidgets.QListWidget(Dialog)
        self.positiveness_list.setGeometry(QtCore.QRect(350, 60, 51, 41))
        self.positiveness_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.positiveness_list.setObjectName("positiveness_list")
        item = QtWidgets.QListWidgetItem()
        self.positiveness_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.positiveness_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.positiveness_list.addItem(item)
        self.threshold_list = QtWidgets.QListWidget(Dialog)
        self.threshold_list.setGeometry(QtCore.QRect(420, 60, 61, 41))
        self.threshold_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.threshold_list.setObjectName("threshold_list")
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.threshold_list.addItem(item)
        self.topic_label = QtWidgets.QLabel(Dialog)
        self.topic_label.setGeometry(QtCore.QRect(500, 30, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.topic_label.setFont(font)
        self.topic_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.topic_label.setObjectName("topic_label")
        self.topic_list = QtWidgets.QListWidget(Dialog)
        self.topic_list.setGeometry(QtCore.QRect(500, 60, 141, 41))
        self.topic_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.topic_list.setObjectName("topic_list")
        item = QtWidgets.QListWidgetItem()
        self.topic_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.topic_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.topic_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.topic_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.topic_list.addItem(item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Query generation panel"))
        self.queryTextArea.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">Generated query</span></p></body></html>"))
        self.generateButton.setToolTip(_translate("Dialog", "<html><head/><body><p>Generate a query with the specified parameters</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Copy this query to Tarsier interface"))
        self.group_label.setText(_translate("Dialog", "Group"))
        self.subgroup_label.setText(_translate("Dialog", "Subgroup"))
        self.positiveness_label.setText(_translate("Dialog", "Sign"))
        self.threshold_label.setText(_translate("Dialog", "Threshold"))
        __sortingEnabled = self.group_list.isSortingEnabled()
        self.group_list.setSortingEnabled(False)
        item = self.group_list.item(0)
        item.setText(_translate("Dialog", "Person"))
        item = self.group_list.item(1)
        item.setText(_translate("Dialog", "Stock"))
        item = self.group_list.item(2)
        item.setText(_translate("Dialog", "Company"))
        item = self.group_list.item(3)
        item.setText(_translate("Dialog", "Country"))
        self.group_list.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.positiveness_list.isSortingEnabled()
        self.positiveness_list.setSortingEnabled(False)
        item = self.positiveness_list.item(0)
        item.setText(_translate("Dialog", "No"))
        item = self.positiveness_list.item(1)
        item.setText(_translate("Dialog", ">"))
        item = self.positiveness_list.item(2)
        item.setText(_translate("Dialog", "<"))
        self.positiveness_list.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.threshold_list.isSortingEnabled()
        self.threshold_list.setSortingEnabled(False)
        item = self.threshold_list.item(0)
        item.setText(_translate("Dialog", "0.75"))
        item = self.threshold_list.item(1)
        item.setText(_translate("Dialog", "0.50"))
        item = self.threshold_list.item(2)
        item.setText(_translate("Dialog", "0.25"))
        item = self.threshold_list.item(3)
        item.setText(_translate("Dialog", "0"))
        item = self.threshold_list.item(4)
        item.setText(_translate("Dialog", "-0.25"))
        item = self.threshold_list.item(5)
        item.setText(_translate("Dialog", "-0.50"))
        item = self.threshold_list.item(6)
        item.setText(_translate("Dialog", "-0.75"))
        self.threshold_list.setSortingEnabled(__sortingEnabled)
        self.topic_label.setText(_translate("Dialog", "News Topic"))
        __sortingEnabled = self.topic_list.isSortingEnabled()
        self.topic_list.setSortingEnabled(False)
        item = self.topic_list.item(0)
        item.setText(_translate("Dialog", "No topic"))
        item = self.topic_list.item(1)
        item.setText(_translate("Dialog", "CompaniesEconomy"))
        item = self.topic_list.item(2)
        item.setText(_translate("Dialog", "Markets&Goods"))
        item = self.topic_list.item(3)
        item.setText(_translate("Dialog", "NationalEconomy"))
        item = self.topic_list.item(4)
        item.setText(_translate("Dialog", "OtherTopic"))
        self.topic_list.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
