# coding=utf-8
import re
from btpPySide import *
from btpDebugInfo import *
import vfxMayaOp
import CopyMayaTex
import btpVfxProject
import btpGrabImageBoard
import BaseUploadPanel
import mayaMakePreview

class UploadPanel(BaseUploadPanel.BaseUploadPanel):
    def __init__(self,dataList,parent=None):
        BaseUploadPanel.BaseUploadPanel.__init__(self,dataList,parent)

    def upload(self):
        btpVfxProject.SetProjName(self.ui.label_Project.text())
        versionStr=btpVfxProject.TimeMark()
        vfxMayaOp.UnlockNode(self.rootNode)
        vfxMayaOp.UnlockAttr(self.rootNode,"version")
        vfxMayaOp.SetAttr_Str(self.rootNode,"version",versionStr)
        vfxMayaOp.LockAttr(self.rootNode,"version")
        vfxMayaOp.LockNode(self.rootNode)
        globalTaskPath=btpVfxProject.AttachRootPath(self.ui.label_Project.text(),self.ui.label_task.text())
        CopyMayaTex.CopyAndRepathTextureFiles("%s/texture"%globalTaskPath,self.ui.progressBar_texFiles)
        maFile="%s/%s"%(globalTaskPath,self.ui.label_taskFile.text())
        vfxMayaOp.SaveMaFile(maFile)
        self.ui.progressBar_taskFiles.setValue(10)
        projInfo=btpVfxProject.ProjInfo()
        previewFile="%s/%s_preview.mov"%(globalTaskPath,self.rootNode)
        mayaMakePreview.makePreview(previewFile,"%s_Cam"%self.rootNode,True,100,100,1,100,(projInfo["resW"],projInfo["resH"]),1)
        self.ui.progressBar_taskFiles.setValue(20)
        btpVfxProject.SaveVersion(  projName=self.ui.label_Project.text(),
                                    taskPath=self.ui.label_task.text(),
                                    files=[maFile,self.imagePathName,previewFile],
                                    comment=self.ui.textEdit_comment.toHtml(),
                                    timeMark=versionStr,
                                    progressBar=self.ui.progressBar_taskFiles )
        self.accept()

class mayaOp(object):
    def InitTask(self,taskPathName,projData):
        vfxMayaOp.SetProjConfig(projData)
        taskGrpName=re.sub("/","_",taskPathName)
        vfxMayaOp.CreateTaskGrp(taskGrpName,btpVfxProject.ProjName(),taskPathName)
        vfxMayaOp.LockNode(taskGrpName)

        cameraNode="%s_Cam"%taskGrpName
        vfxMayaOp.CreateCameraByFilmGate(cameraNode,"35mm 1.85 Projection")
        if not vfxMayaOp.IsParent(cameraNode,taskGrpName):
            vfxMayaOp.SetParent(cameraNode,taskGrpName)

    def OpenTaskFile(self,fileName):
        vfxMayaOp.OpenMaFile(fileName)

    def LoadFileSeq(self,fileName):
        pass

    def UploadTask(self):
        if vfxMayaOp.IsTaskScene():
            imagePathName=""
            taskNodeName=vfxMayaOp.FindTaskNode("(efx|render)")
            projName,taskPathName=vfxMayaOp.FindProjAndTaskPathName("(efx|render)")
            globalTaskPath=btpVfxProject.AttachRootPath(projName,taskPathName)
            imageBoard=btpGrabImageBoard.GrabImageBoard(globalTaskPath)
            if imageBoard.exec_()  == QDialog.Accepted:
                imageFileName=re.sub("/","_",taskPathName)
                imagePathName="%s/%s.jpg"%(globalTaskPath,imageFileName)
                imageBoard.SaveImage(imagePathName)
            startFrame,endFrame=vfxMayaOp.FrameRange()
            uploadPanel=UploadPanel([projName,taskPathName,vfxMayaOp.MayaFileByTaskNode(taskNodeName),taskNodeName,imagePathName,startFrame,endFrame])
            uploadPanel.exec_()
        else:
            Warning_No_Task_Node()