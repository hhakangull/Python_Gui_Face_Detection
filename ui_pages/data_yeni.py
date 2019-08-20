# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(781, 504)
        Frame.setFixedSize(781,504)
        self.tableWidget = QtWidgets.QTableWidget(Frame)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 703, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.btnDownload = QtWidgets.QPushButton(Frame)
        self.btnDownload.setGeometry(QtCore.QRect(710, 3, 61, 51))
        self.btnDownload.setText("")
        self.btnDownload.setIconSize(QtCore.QSize(80, 80))
        self.btnDownload.setObjectName("btnDownload")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Frame", "Ad"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Frame", "Soyad"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Frame", "ID"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Frame", "Durum"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Frame", "Kurum"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Frame", "Kimlik"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Frame", "Alan1"))




