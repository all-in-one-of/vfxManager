# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui\UploadPanel.ui'
#
# Created: Wed Apr 11 18:14:16 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(419, 581)
        self.pushButton_upload = QtWidgets.QPushButton(Form)
        self.pushButton_upload.setGeometry(QtCore.QRect(10, 540, 401, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.pushButton_upload.setFont(font)
        self.pushButton_upload.setObjectName("pushButton_upload")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 401, 521))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(80, 0))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.label_image = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_image.sizePolicy().hasHeightForWidth())
        self.label_image.setSizePolicy(sizePolicy)
        self.label_image.setMinimumSize(QtCore.QSize(212, 160))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_image.setFont(font)
        self.label_image.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_image.setText("")
        self.label_image.setScaledContents(False)
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setWordWrap(False)
        self.label_image.setObjectName("label_image")
        self.horizontalLayout.addWidget(self.label_image)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(80, 0))
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressBar_taskFiles = QtWidgets.QProgressBar(self.gridLayoutWidget_3)
        self.progressBar_taskFiles.setProperty("value", 24)
        self.progressBar_taskFiles.setTextVisible(False)
        self.progressBar_taskFiles.setObjectName("progressBar_taskFiles")
        self.gridLayout_2.addWidget(self.progressBar_taskFiles, 1, 1, 1, 1)
        self.progressBar_texFiles = QtWidgets.QProgressBar(self.gridLayoutWidget_3)
        self.progressBar_texFiles.setProperty("value", 24)
        self.progressBar_texFiles.setTextVisible(False)
        self.progressBar_texFiles.setObjectName("progressBar_texFiles")
        self.gridLayout_2.addWidget(self.progressBar_texFiles, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 8, 1, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_taskFile = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_taskFile.setMinimumSize(QtCore.QSize(200, 0))
        self.label_taskFile.setObjectName("label_taskFile")
        self.gridLayout_4.addWidget(self.label_taskFile, 0, 1, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.gridLayout_4.addWidget(self.label_1, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_startFrame = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_startFrame.setObjectName("label_startFrame")
        self.horizontalLayout_3.addWidget(self.label_startFrame)
        self.spinBox_startFrame = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBox_startFrame.setMaximum(9999)
        self.spinBox_startFrame.setProperty("value", 1)
        self.spinBox_startFrame.setObjectName("spinBox_startFrame")
        self.horizontalLayout_3.addWidget(self.spinBox_startFrame)
        self.label_endFrame = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_endFrame.setObjectName("label_endFrame")
        self.horizontalLayout_3.addWidget(self.label_endFrame)
        self.spinBox_endFrame = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBox_endFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spinBox_endFrame.setMaximum(99999)
        self.spinBox_endFrame.setProperty("value", 100)
        self.spinBox_endFrame.setObjectName("spinBox_endFrame")
        self.horizontalLayout_3.addWidget(self.spinBox_endFrame)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 4, 1, 1, 1)
        self.label_task = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_task.setFont(font)
        self.label_task.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_task.setObjectName("label_task")
        self.gridLayout_3.addWidget(self.label_task, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 6, 1, 1, 1)
        self.textEdit_comment = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        self.textEdit_comment.setObjectName("textEdit_comment")
        self.gridLayout_3.addWidget(self.textEdit_comment, 7, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_proj = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_proj.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_proj.setFont(font)
        self.label_proj.setObjectName("label_proj")
        self.horizontalLayout_4.addWidget(self.label_proj)
        self.label_Project = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_Project.setText("")
        self.label_Project.setObjectName("label_Project")
        self.horizontalLayout_4.addWidget(self.label_Project)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Upload", None, -1))
        self.pushButton_upload.setText(QtWidgets.QApplication.translate("Form", "Upload", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Texture files", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "Task files", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("Form", "Show", None, -1))
        self.label_taskFile.setText(QtWidgets.QApplication.translate("Form", "None", None, -1))
        self.label_1.setText(QtWidgets.QApplication.translate("Form", "Maya file", None, -1))
        self.label_startFrame.setText(QtWidgets.QApplication.translate("Form", "startFrame", None, -1))
        self.label_endFrame.setText(QtWidgets.QApplication.translate("Form", "endFrame", None, -1))
        self.label_task.setText(QtWidgets.QApplication.translate("Form", "task", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Comment", None, -1))
        self.label_proj.setText(QtWidgets.QApplication.translate("Form", "Project", None, -1))

