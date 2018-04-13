# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui\vfxTaskPanel.ui'
#
# Created: Wed Apr 11 18:14:16 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(812, 907)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(360, 25, 441, 271))
        self.groupBox.setObjectName("groupBox")
        self.listWidget_Version = QtWidgets.QListWidget(self.groupBox)
        self.listWidget_Version.setGeometry(QtCore.QRect(250, 50, 181, 211))
        self.listWidget_Version.setObjectName("listWidget_Version")
        self.btn_Revert = QtWidgets.QPushButton(self.groupBox)
        self.btn_Revert.setGeometry(QtCore.QRect(296, 20, 91, 23))
        self.btn_Revert.setObjectName("btn_Revert")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(11, 25, 54, 12))
        self.label.setObjectName("label")
        self.textEdit_Comment = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_Comment.setGeometry(QtCore.QRect(10, 50, 231, 211))
        self.textEdit_Comment.setObjectName("textEdit_Comment")
        self.btn_Show = QtWidgets.QPushButton(self.groupBox)
        self.btn_Show.setGeometry(QtCore.QRect(120, 20, 75, 23))
        self.btn_Show.setObjectName("btn_Show")
        self.label_TitleImage = QtWidgets.QLabel(Form)
        self.label_TitleImage.setGeometry(QtCore.QRect(10, 45, 331, 241))
        self.label_TitleImage.setText("")
        self.label_TitleImage.setObjectName("label_TitleImage")
        self.btn_Init = QtWidgets.QPushButton(Form)
        self.btn_Init.setGeometry(QtCore.QRect(654, 310, 91, 23))
        self.btn_Init.setObjectName("btn_Init")
        self.label_Title = QtWidgets.QLabel(Form)
        self.label_Title.setGeometry(QtCore.QRect(10, 10, 341, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_Title.setFont(font)
        self.label_Title.setObjectName("label_Title")
        self.btn_GoFolder = QtWidgets.QPushButton(Form)
        self.btn_GoFolder.setGeometry(QtCore.QRect(655, 350, 91, 23))
        self.btn_GoFolder.setObjectName("btn_GoFolder")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Form", "版本", None, -1))
        self.btn_Revert.setText(QtWidgets.QApplication.translate("Form", "恢复", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "注释", None, -1))
        self.btn_Show.setText(QtWidgets.QApplication.translate("Form", "Show", None, -1))
        self.btn_Init.setText(QtWidgets.QApplication.translate("Form", "初始化", None, -1))
        self.label_Title.setText(QtWidgets.QApplication.translate("Form", "Title", None, -1))
        self.btn_GoFolder.setText(QtWidgets.QApplication.translate("Form", "去目录", None, -1))

