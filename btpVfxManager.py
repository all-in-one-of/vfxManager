# coding=utf-8
import sys,re,glob
from btpPySide import *
from jsonIO import *
from fileOp import *
from letUI import *

import dcc
import btpVfxProject
import btpDebugInfo
import vfxProjectUI
import vfxTaskPanelUI
import ProjManagerConfigUI
import NewProjectUI
import OpenProjectUI


def SetLabelImage(iconLabel,iconPathName,width,height):
    iconLabel.setScaledContents(True)
    pixmap=QPixmap(width, height)
    if os.path.isfile(iconPathName):
        pixmap.load(iconPathName)
    else:
        pixmap.fill(Qt.black)

    iconLabel.setPixmap(pixmap)

def ThumbnailWidget(parent,taskPath):
    iconWidget=QWidget(parent)
    iconLabel=QLabel(iconWidget)
    iconLabel.setGeometry(QRect(0, 0, 60, 40))
    iconPathName=btpVfxProject.IconFilePathName(taskPath)
    SetLabelImage(iconLabel,iconPathName,60,40)
    return iconWidget

def SetThumbnailWidget(treeWidget,item,curPathName):
    itemText=str(item.text(0)).strip()
    item.setSizeHint(0,QSize(100,42))
    treeWidget.setItemWidget(item,0,ThumbnailWidget(treeWidget,curPathName[1:]))
    item.setText(0,"\t%s"%itemText)

class btpConfigDial(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.ui=ProjManagerConfigUI.Ui_Dialog()
        self.ui.setupUi(self)

    def ProjPath(self):
        return self.ui.lineEdit.text()

    def NukeCmd(self):
        return self.ui.lineEdit_NukeCmd.text()        

    def SetProjPath(self,projPath):
        self.ui.lineEdit.setText(projPath)

    def SetNukeCmd(self,nukeCmd):
        self.ui.lineEdit_NukeCmd.setText(nukeCmd)

class btpNewProjectDial(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.ui=NewProjectUI.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.lineEdit_ProjName.setText("untitled")

    def ProjName(self):
        return self.ui.lineEdit_ProjName.text()

    def FPS(self):
        return self.ui.comboBox_FPS.currentText()

    def ResW(self):
        return self.ui.spinBox_W.value()

    def ResH(self):
        return self.ui.spinBox_H.value()

    def NewProj(self,projPath):
        name=self.ProjName()
        btpVfxProject.SetProjName(name)
        projPathName=btpVfxProject.ProjPath()
        projJsonFile="%s/proj.json"%projPathName
        if os.path.isdir(projPathName):
            btpDebugInfo.Warnning_Exists(projPathName)
            return

        btpVfxProject.NewProjDirTree()

        if not os.path.isfile(projJsonFile):
            data={"name":name,"fps":self.FPS(),"resW":self.ResW(),"resH":self.ResH()}
            DumpJson(projJsonFile,data)

class btpOpenProjectDial(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.ui=OpenProjectUI.Ui_Dialog()
        self.ui.setupUi(self)

    def ListProj(self,projPath):
        self.ui.listWidget.addItems([curDir for curDir in os.listdir(projPath) if os.path.isdir("%s/%s"%(projPath,curDir))])

    def CurrentProj(self):
        return self.ui.listWidget.currentItem().text()

class TaskPanelFileWidget(QTreeWidget):
    def __init__(self,groupBox_DataTree,dccType):
        QTreeWidget.__init__(self,groupBox_DataTree)
        self.setGeometry(QRect(10, 310, 591, 581))
        self.setObjectName("treeWidget_Files")
        self.headerItem().setText(0, "Files")
        self.taskFileExt={"Maya":".m?$","Hou":".hip$","Nk":".nk$","StandAlone":".xx"}[dccType]
        self.panelWidget=groupBox_DataTree
        self.dccType=dccType
        self.RemoveMarkItem()

    def RemoveMarkItem(self):
        self.markedItem=None

    def mousePressEvent(self, event):
        if QApplication.mouseButtons() == Qt.LeftButton:
            QTreeWidget.mousePressEvent(self,event)
        if QApplication.mouseButtons() == Qt.RightButton:
            if not self.markedItem:
                self.markedItem=self.itemAt(event.pos())
                if self.markedItem:
                    menu=None
                    if re.search(".mov$",self.markedItem.text(0)):
                        menu=FloatMenu([["Open",self.OpenCommonFile]])
                    elif re.search(self.taskFileExt,self.markedItem.text(0)):
                        menu=FloatMenu([["Open",self.OpenFile]])

                    if menu:
                        menu.exec_(event.globalPos())
                self.RemoveMarkItem()

    def MarkedFile(self):
        return "%s/%s"%(self.panelWidget.GlobalTaskPath(),self.markedItem.text(0))

    def OpenFile(self):
        dccOp=dcc.CreateDccOp(self.dccType)
        dccOp.OpenTaskFile(self.MarkedFile())

    def OpenCommonFile(self):
        os.startfile(self.MarkedFile())

class btpTaskPanelWidget(QWidget):
    def __init__(self,parent,dccType):
        QWidget.__init__(self,parent)
        self.ui=vfxTaskPanelUI.Ui_Form()
        self.ui.setupUi(self)

        self.dccOp=dcc.CreateDccOp(dccType)

        self.ui.treeWidget_Files=TaskPanelFileWidget(self,dccType)

        self.ui.btn_Init.clicked.connect(self.InitTask)
        self.ui.btn_GoFolder.clicked.connect(self.GoFolder)
        self.ui.btn_Revert.clicked.connect(self.Revert)
        self.ui.btn_Show.clicked.connect(self.Show)
        self.ui.listWidget_Version.currentItemChanged.connect(self.SelectVersion)

    def Clear(self):
        self.ui.treeWidget_Files.clear()
        self.ui.listWidget_Version.clear()

    def Revert(self):
        curVer=self.ui.listWidget_Version.currentItem().text()
        btpVfxProject.RevertVersionFiles(self.taskPathName,curVer)

    def Show(self):
        curVer=self.ui.listWidget_Version.currentItem().text()
        showFile=btpVfxProject.VersionShowFile(self.taskPathName,curVer)
        if showFile:
            os.startfile(showFile)

    def SetTask(self,taskPathName):
        self.taskPathName=taskPathName
        self.Clear()
        if re.search("(render|efx|comp)$",taskPathName):
            self.ui.label_Title.setText(taskPathName)

            self.setHidden(False)
            folderDict={}
            gTaskPathName=self.GlobalTaskPath()
            for a in os.walk(gTaskPathName):
                parentFolder=a[0][len(gTaskPathName):]
                if parentFolder != "":
                    parentFolder=re.search("[^\\\\\\\\]+$",parentFolder).group(0)

                for curFolder in a[1]:
                    curPath='%s\\%s'%(a[0],curFolder)

                    parentItem=self.ui.treeWidget_Files
                    if parentFolder != "":
                        if a[0] in folderDict:
                            parentItem=folderDict[a[0]]
                        else:
                            continue

                    if not re.search("Versions",curPath):
                        folderDict[curPath]=QTreeWidgetItem(parentItem,[curFolder])

                for curFile in a[2]:
                    curPath='%s\\%s'%(a[0],curFile)

                    parentItem=self.ui.treeWidget_Files
                    if parentFolder != "":
                        if a[0] in folderDict:
                            parentItem=folderDict[a[0]]
                        else:
                            continue

                    if not re.search("(Versions|version.json|.jpg)",curPath):
                        folderDict[curPath]=QTreeWidgetItem(parentItem,[curFile])

            iconPathName=btpVfxProject.IconFilePathName(taskPathName)
            self.UpdateVersion()
            SetLabelImage(self.ui.label_TitleImage,iconPathName,330,240)
        else:
            self.setHidden(True)

    def UpdateVersion(self):
        versionList=btpVfxProject.ReadVersionFile(self.taskPathName)
        if versionList:
            self.ui.listWidget_Version.clear()
            for curVer in versionList:
                self.ui.listWidget_Version.addItem(curVer["timeMark"])
            self.ui.listWidget_Version.sortItems(Qt.DescendingOrder)
            self.ui.listWidget_Version.setCurrentRow(0)

    def SelectVersion(self):
        versionList=btpVfxProject.ReadVersionFile(self.taskPathName)
        curItem=self.ui.listWidget_Version.currentItem()
        if curItem:
            curVer=curItem.text()
            for curVerInfo in versionList:
                if curVerInfo["timeMark"] == curVer:
                    self.ui.textEdit_Comment.setText(curVerInfo['comment'])
                    verPicName="%s/Versions/%s/%s.jpg"%(self.GlobalTaskPath(),curVer,btpVfxProject.TaskNodeNameByTaskPathName(self.taskPathName))
                    SetLabelImage(self.ui.label_TitleImage,verPicName,330,240)
                    break

    def InitTask(self):
        self.dccOp.InitTask(self.taskPathName,btpVfxProject.ProjInfo())

    def GoFolder(self):
        os.startfile(self.GlobalTaskPath())

    def GlobalTaskPath(self):
        return btpVfxProject.AttachProjPath(self.taskPathName)


class btpNewNameEdit(QLineEdit):
    def __init__(self,treeWidget):
        QLineEdit.__init__(self)
        self.treeWidget=treeWidget

    def setItem(self,item,typeName,num):
        newNameDict={'plays':'chapter','chapter':'shot',"shot":"efx","lookdev":"efx"}
        self.item=item
        self.itemType=None
        if typeName in newNameDict:
            self.itemType=newNameDict[typeName]
            self.setText("%s%03dA"%(self.itemType,num))
        else:
            self.setText("New_Name")

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            name=self.text().strip()
            if not re.search(" ",name):
                self.treeWidget.removeItemWidget(self.item,0)
                self.item.setText(0,name)
                taskPathName=self.treeWidget.TreeItemPathName(self.item)
                os.makedirs(taskPathName)
                if self.itemType=="efx":
                    btpVfxProject.NewVfxDirTree(taskPathName)
                    item=QTreeWidgetItem(self.item,["efx"])
                    SetThumbnailWidget(self.treeWidget,item,self.treeWidget.LocalTreeItemPathName(item))

                    item=QTreeWidgetItem(self.item,["render"])
                    SetThumbnailWidget(self.treeWidget,item,self.treeWidget.LocalTreeItemPathName(item))

                    item=QTreeWidgetItem(self.item,["comp"])
                    SetThumbnailWidget(self.treeWidget,item,self.treeWidget.LocalTreeItemPathName(item))
                    
                self.treeWidget.RemoveMarkItem()
            else:
                btpDebugInfo.Warnning_Name_Format()
        else:
            QLineEdit.keyPressEvent(self,event)

class btpDataTreeWidget(QTreeWidget):
    def __init__(self,groupBox_DataTree,dccType):
        QTreeWidget.__init__(self,groupBox_DataTree)
        self.setGeometry(QRect(10, 20, 480, 835))
        self.setObjectName("treeWidget_DataTree")

        self.headerItem().setText(0, "Project")
        self.setColumnWidth(0,540)

        self.RemoveMarkItem()

        self.currentItemChanged.connect(self.selItem)

        self.taskTypeFilters={  "Maya":"(\\\\efx\\\\|\\\\render\\\\|\\\\comp)",
                                "Hou":"(\\\\efx\\\\|\\\\render\\\\|\\\\comp)",
                                "Nk":"(\\\\efx|\\\\render|\\\\comp\\\\)",
                                "StandAlone":"(\\\\efx\\\\|\\\\render\\\\|\\\\comp\\\\)" }[dccType]

    def RemoveMarkItem(self):
        self.markedItem=None

    def LocalTreeItemPathName(self,item):
        curItem=item.parent()
        pathName=item.text(0).strip()
        while(curItem):
            pathName="%s/%s"%(curItem.text(0),pathName)
            curItem=curItem.parent()

        return pathName

    def TreeItemPathName(self,item):
        pathName="%s/%s"%(btpVfxProject.ProjPath(),self.LocalTreeItemPathName(item))
        return pathName

    def Update(self):
        self.clear()
        folderDict={}
        projPathName=btpVfxProject.ProjPath()
        for a in os.walk(projPathName):
            parentFolder=a[0][len(projPathName):]
            if parentFolder != "":
                parentFolder=re.search("[^\\\\\\\\]+$",parentFolder).group(0)

            for curFolder in a[1]:
                curPath='%s\\%s'%(a[0],curFolder)

                parentItem=self
                if parentFolder != "":
                    if a[0] in folderDict:
                        parentItem=folderDict[a[0]]
                    else:
                        continue

                if re.search("(lookdev|plays)",curPath):
                    if not re.search(self.taskTypeFilters,curPath):
                        folderDict[curPath]=QTreeWidgetItem(parentItem,[curFolder])

        def walkLevelItem(item,curPath):
            item.setExpanded(True)
            itemText=str(item.text(0)).strip()
            curPathName="%s/%s"%(curPath,itemText)
            if item.childCount() == 0:
                if re.search("(efx|render|comp)$",itemText):
                    SetThumbnailWidget(self,item,curPathName)
            else:
                for i in range(item.childCount()):
                    walkLevelItem(item.child(i),curPathName)

        for i in range(self.topLevelItemCount()):
            item=self.topLevelItem(i)
            walkLevelItem(item,"")


    def Create(self):
        curItem=QTreeWidgetItem(self.markedItem)
        self.lineEdit=btpNewNameEdit(self)
        self.lineEdit.setItem(curItem,self.matchedCreateType,self.markedItem.childCount())
        self.setItemWidget(curItem,0,self.lineEdit)
        self.markedItem.setExpanded(True)

    def MatchCreateType(self):
        parentItem=self.markedItem.parent()
        if parentItem:
            name=parentItem.text(0)
            if name == "plays":
                return "chapter"

            gradParentItem=parentItem.parent()
            if gradParentItem:
                name=gradParentItem.text(0)
                if name == "plays":
                    return "shot"


        name=self.markedItem.text(0)
        if name == "plays":
            return "plays"

        return name

    def mousePressEvent(self, event):
        if QApplication.mouseButtons() == Qt.LeftButton:
            QTreeWidget.mousePressEvent(self,event)
        if QApplication.mouseButtons() == Qt.RightButton:
            if not self.markedItem:
                self.markedItem=self.itemAt(event.pos())
                if self.markedItem:
                    self.matchedCreateType=self.MatchCreateType()
                    if self.matchedCreateType:
                        menu=None
                        if self.matchedCreateType in ("plays","chapter","shot","lookdev"):
                            menu=FloatMenu([["Create",self.Create]])
                        elif self.matchedCreateType not in ("efx","render","comp") and self.IsEmptyItemDir(self.markedItem):
                            menu=FloatMenu([["CreateTask",self.Create]])

                        if menu:
                            menu.exec_(event.globalPos())
                self.RemoveMarkItem()

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Delete:
            curItem=self.currentItem()
            dirPathName=self.TreeItemPathName(curItem)
            if IsEmptyDir(dirPathName):
                DeleteDir(dirPathName)
                dbWraper.DelTask(self.LocalTreeItemPathName(curItem))
                curItem.parent().removeChild(curItem)
            else:
                btpDebugInfo.Warnning_NotEmpty(dirPathName)

    def selItem(self):
        curItem=self.currentItem()
        if curItem:
            self.taskPanel.setHidden(False)
            subTaskPath=self.LocalTreeItemPathName(self.currentItem())
            self.taskPanel.SetTask(subTaskPath)
        else:
            self.taskPanel.setHidden(True)

    def SetTaskPanel(self,taskPanel):
        self.taskPanel=taskPanel

    def IsEmptyItemDir(self,item):
        return IsEmptyDir(btpVfxProject.AttachProjPath(self.LocalTreeItemPathName(item)))

class btpVfxManager(QMainWindow):
    def __init__(self,parent,dccType):
        QMainWindow.__init__(self,parent)
        self.ui=vfxProjectUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_New.triggered.connect(self.NewProj)
        self.ui.action_Setting.triggered.connect(self.Config)
        self.ui.action_Open.triggered.connect(self.OpenProj)
        self.ui.action_Fresh.triggered.connect(self.Fresh)

        self.ui.taskPanel=btpTaskPanelWidget(self.ui.frame_TaskPanel,dccType)
        self.ui.taskPanel.setHidden(True)

        self.ui.dataTreeWidget=btpDataTreeWidget(self.ui.groupBox_DataTree,dccType)
        self.ui.dataTreeWidget.SetTaskPanel(self.ui.taskPanel)

    def NewProj(self):
        dial=btpNewProjectDial()
        if dial.exec_():
            dial.NewProj(btpVfxProject.RootPath())
            self.UpdateProj()

    def Config(self):
    	dial=btpConfigDial()
    	dial.SetProjPath(btpVfxProject.RootPath())
        dial.SetNukeCmd(btpVfxProject.NukeCmd())
        if dial.exec_():
            btpVfxProject.WriteRootPath(dial.ProjPath())
            btpVfxProject.WriteNukeCmd(dial.NukeCmd())

    def OpenProj(self):
    	dial=btpOpenProjectDial()
        rootPath=btpVfxProject.RootPath()
        dial.ListProj(rootPath)
        if dial.exec_():
            btpVfxProject.SetProjName(dial.CurrentProj())
            self.ui.dataTreeWidget.Update()
            projInfo=btpVfxProject.ProjInfo()
            self.ui.label_resX.setText(str(projInfo["resW"]))
            self.ui.label_resY.setText(str(projInfo["resH"]))
            self.ui.label_fps.setText(projInfo["fps"])

    def Fresh(self):
        self.ui.dataTreeWidget.Update()

def UploadTask(dccType):
    dccOp=dcc.CreateDccOp(dccType)
    dccOp.UploadTask()

if __name__ == '__main__':
    app = QApplication.instance()
    if app==None:
        app=QApplication(sys.argv)

    mainWin=btpVfxManager(None,"StandAlone")
    mainWin.show()
        
    app.exec_()
    sys.exit()