# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DicomHelper.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 686)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 240, 711, 391))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listViewundo = QtWidgets.QListView(self.horizontalLayoutWidget_2)
        self.listViewundo.setMouseTracking(True)
        self.listViewundo.setTabletTracking(True)
        self.listViewundo.setAcceptDrops(True)
        self.listViewundo.setAutoFillBackground(True)
        self.listViewundo.setTabKeyNavigation(True)
        self.listViewundo.setDragEnabled(True)
        self.listViewundo.setDragDropOverwriteMode(True)
        self.listViewundo.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listViewundo.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listViewundo.setAlternatingRowColors(True)
        self.listViewundo.setMovement(QtWidgets.QListView.Free)
        self.listViewundo.setObjectName("listViewundo")
        self.horizontalLayout_2.addWidget(self.listViewundo)
        self.listViewdone = QtWidgets.QListView(self.horizontalLayoutWidget_2)
        self.listViewdone.setMouseTracking(True)
        self.listViewdone.setTabletTracking(True)
        self.listViewdone.setAcceptDrops(True)
        self.listViewdone.setAutoFillBackground(True)
        self.listViewdone.setDragEnabled(True)
        self.listViewdone.setDragDropOverwriteMode(True)
        self.listViewdone.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listViewdone.setResizeMode(QtWidgets.QListView.Fixed)
        self.listViewdone.setObjectName("listViewdone")
        self.horizontalLayout_2.addWidget(self.listViewdone)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 60, 721, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.adddcm = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.adddcm.setObjectName("adddcm")
        self.horizontalLayout_3.addWidget(self.adddcm)
        self.deletedcm = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.deletedcm.setObjectName("deletedcm")
        self.horizontalLayout_3.addWidget(self.deletedcm)
        self.customniminghua = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.customniminghua.setObjectName("customniminghua")
        self.horizontalLayout_3.addWidget(self.customniminghua)
        self.niming = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.niming.setObjectName("niming")
        self.horizontalLayout_3.addWidget(self.niming)
        self.doneclean = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.doneclean.setObjectName("doneclean")
        self.horizontalLayout_3.addWidget(self.doneclean)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 220, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 220, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setEnabled(True)
        self.label_3.setGeometry(QtCore.QRect(210, 10, 361, 41))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 90, 731, 131))
        self.groupBox.setObjectName("groupBox")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 711, 91))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionwenjian = QtWidgets.QAction(MainWindow)
        self.actionwenjian.setObjectName("actionwenjian")
        self.actionwenjianjia = QtWidgets.QAction(MainWindow)
        self.actionwenjianjia.setObjectName("actionwenjianjia")
        self.actionniming = QtWidgets.QAction(MainWindow)
        self.actionniming.setObjectName("actionniming")
        self.actionmiyao = QtWidgets.QAction(MainWindow)
        self.actionmiyao.setObjectName("actionmiyao")
        self.actionnohandle = QtWidgets.QAction(MainWindow)
        self.actionnohandle.setCheckable(True)
        self.actionnohandle.setChecked(True)
        self.actionnohandle.setObjectName("actionnohandle")
        self.actiontianjia = QtWidgets.QAction(MainWindow)
        self.actiontianjia.setCheckable(True)
        self.actiontianjia.setChecked(False)
        self.actiontianjia.setObjectName("actiontianjia")
        self.actionsc = QtWidgets.QAction(MainWindow)
        self.actionsc.setCheckable(True)
        self.actionsc.setObjectName("actionsc")
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName("actionabout")
        self.menu.addAction(self.actionwenjian)
        self.menu.addSeparator()
        self.menu.addAction(self.actionwenjianjia)
        self.menu.addSeparator()
        self.menu.addSeparator()
        self.menu.addAction(self.actionmiyao)
        self.menu.addSeparator()
        self.menu.addSeparator()
        self.menu.addAction(self.actionabout)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.adddcm.setText(_translate("MainWindow", "添加.dcm 后缀"))
        self.deletedcm.setText(_translate("MainWindow", "撤销.dcm 后缀"))
        self.customniminghua.setText(_translate("MainWindow", "自定义匿名化"))
        self.niming.setText(_translate("MainWindow", "匿名化"))
        self.doneclean.setText(_translate("MainWindow", "清空已完成"))
        self.label.setText(_translate("MainWindow", "待处理"))
        self.label_2.setText(_translate("MainWindow", "已完成"))
        self.label_3.setText(_translate("MainWindow", "Dicom 匿名化、反匿名化工具 "))
        self.groupBox.setTitle(_translate("MainWindow", "匿名化选项"))
        self.label_4.setText(_translate("MainWindow", "主要匿名处理为患者信息，机构信息以及症状信息,具体如下:\n"
"# 机构信息:InstitutionName\n"
"# 患者信息: PatientName,PatientID,IssuerOfPatientID,PatientBirthDate,PatientSex,OtherPatientIDs,PatientAge,\n"
"PatientSize,PatientWeight,AdditionalPatientHistory\n"
"# 症状描述: ContrastBolusAgent,BodyPartExamined"))
        self.menu.setTitle(_translate("MainWindow", "功能"))
        self.actionwenjian.setText(_translate("MainWindow", "文件"))
        self.actionwenjianjia.setText(_translate("MainWindow", "文件夹"))
        self.actionniming.setText(_translate("MainWindow", "匿名选项"))
        self.actionmiyao.setText(_translate("MainWindow", "秘钥"))
        self.actionnohandle.setText(_translate("MainWindow", "不处理"))
        self.actiontianjia.setText(_translate("MainWindow", "添加"))
        self.actionsc.setText(_translate("MainWindow", "删除"))
        self.actionabout.setText(_translate("MainWindow", "关于"))
