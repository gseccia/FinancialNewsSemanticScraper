# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\resources\gui\gen_query.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(580, 451)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 581, 451))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../resources/gui/big_data_fintech_globe_thinkstock_826139768-100749747-large.jpg"))
        self.label.setObjectName("label")
        self.queryTextArea = QtWidgets.QTextEdit(Dialog)
        self.queryTextArea.setGeometry(QtCore.QRect(50, 200, 481, 191))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(10)
        self.queryTextArea.setFont(font)
        self.queryTextArea.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.queryTextArea.setObjectName("queryTextArea")
        self.generateButton = QtWidgets.QPushButton(Dialog)
        self.generateButton.setGeometry(QtCore.QRect(260, 120, 72, 72))
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
        self.label_2.setGeometry(QtCore.QRect(170, 390, 221, 31))
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
        self.subgroup_label.setGeometry(QtCore.QRect(180, 30, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subgroup_label.setFont(font)
        self.subgroup_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.subgroup_label.setObjectName("subgroup_label")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(370, 30, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(460, 30, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
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
        self.subgroup_list.setGeometry(QtCore.QRect(180, 60, 161, 41))
        self.subgroup_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.subgroup_list.setObjectName("subgroup_list")
        self.order_list = QtWidgets.QListWidget(Dialog)
        self.order_list.setGeometry(QtCore.QRect(370, 60, 61, 41))
        self.order_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.order_list.setObjectName("order_list")
        item = QtWidgets.QListWidgetItem()
        self.order_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.order_list.addItem(item)
        self.limit_list = QtWidgets.QListWidget(Dialog)
        self.limit_list.setGeometry(QtCore.QRect(460, 60, 61, 41))
        self.limit_list.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 7, 42, 255), stop:1 rgba(34, 139, 169, 255));\n"
"color: rgb(255, 255, 255);")
        self.limit_list.setObjectName("limit_list")
        item = QtWidgets.QListWidgetItem()
        self.limit_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.limit_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.limit_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.limit_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.limit_list.addItem(item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Query generation panel"))
        self.queryTextArea.setToolTip(_translate("Dialog", "<html><head/><body><p>>Generated query</p></body></html>"))
        self.generateButton.setToolTip(_translate("Dialog", "<html><head/><body><p>Generate a query with the specified parameters</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Copy this query to Tarsier interface"))
        self.group_label.setText(_translate("Dialog", "Group"))
        self.subgroup_label.setText(_translate("Dialog", "Subgroup"))
        self.label_5.setText(_translate("Dialog", "Order"))
        self.label_6.setText(_translate("Dialog", "Limit"))
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
        __sortingEnabled = self.order_list.isSortingEnabled()
        self.order_list.setSortingEnabled(False)
        item = self.order_list.item(0)
        item.setText(_translate("Dialog", "ASC"))
        item = self.order_list.item(1)
        item.setText(_translate("Dialog", "DESC"))
        self.order_list.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.limit_list.isSortingEnabled()
        self.limit_list.setSortingEnabled(False)
        item = self.limit_list.item(0)
        item.setText(_translate("Dialog", "5"))
        item = self.limit_list.item(1)
        item.setText(_translate("Dialog", "10"))
        item = self.limit_list.item(2)
        item.setText(_translate("Dialog", "15"))
        item = self.limit_list.item(3)
        item.setText(_translate("Dialog", "20"))
        item = self.limit_list.item(4)
        item.setText(_translate("Dialog", "25"))
        self.limit_list.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())