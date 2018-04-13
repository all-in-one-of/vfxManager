# coding=utf-8
import re
from btpPySide import *
from btpDebugInfo import *

import hou
import toolutils
import btpVfxProject
import BaseUploadPanel
import btpGrabImageBoard

class UploadPanel(BaseUploadPanel.BaseUploadPanel):
    def __init__(self,dataList,parent=None):
        BaseUploadPanel.BaseUploadPanel.__init__(self,dataList,parent)

    def upload(self):
    	btpVfxProject.SetProjName(self.ui.label_Project.text())
        versionStr=btpVfxProject.TimeMark()
        taskNode=hou.node("/obj/%s"%self.rootNode)
        taskNode.setParms({"version":versionStr})
        globalTaskPath=btpVfxProject.AttachRootPath(self.ui.label_Project.text(),self.ui.label_task.text())
        hipFile="%s/%s"%(globalTaskPath,self.ui.label_taskFile.text())
        hou.hipFile.save(hipFile)
        self.ui.progressBar_taskFiles.setValue(10)

        projInfo=btpVfxProject.ProjInfo()
        globalTaskPreviewName="%s/%s_preview"%(globalTaskPath,self.rootNode)
        previewFile="%s.$F4.jpg"%globalTaskPreviewName
        scene=toolutils.sceneViewer()
        flipbook_options=scene.flipbookSettings().stash()

       	frameRange=( self.ui.spinBox_startFrame.value(), self.ui.spinBox_endFrame.value() )
       	flipbook_options.useResolution(True)
       	flipbook_options.resolution((projInfo["resW"],projInfo["resH"]))
        flipbook_options.frameRange( frameRange )
        flipbook_options.output(previewFile)
        viewport=scene.curViewport()
        viewport.setCamera(hou.node("/obj/%s_Cam"%self.rootNode))
        scene.flipbook(viewport,flipbook_options)
        previewFile_jpgSeq="%s.####.jpg"%globalTaskPreviewName
        previewFile_mov="%s.mov"%globalTaskPreviewName
        btpVfxProject.JpgToMov(previewFile_jpgSeq,previewFile_mov,frameRange,"Nobody",self.ui.label_task.text(),versionStr)
        btpVfxProject.DeleteFiles("%s.????.jpg"%globalTaskPreviewName)
        self.ui.progressBar_taskFiles.setValue(20)

        btpVfxProject.SaveVersion(  projName=self.ui.label_Project.text(),
                                    taskPath=self.ui.label_task.text(),
                                    files=[hipFile,self.imagePathName,previewFile_mov],
                                    comment=self.ui.textEdit_comment.toHtml(),
                                    timeMark=versionStr,
                                    progressBar=self.ui.progressBar_taskFiles )
        self.accept()


class houOp(object):
    def InitTask(self,taskPathName,projData):
        obj=hou.node("/obj")
        taskGrpName=btpVfxProject.TaskNodeNameByTaskPathName(taskPathName)
        taskNode=obj.createNode("geo",node_name=taskGrpName)
        fileObj=hou.node("/obj/%s/file1"%taskGrpName)
        fileObj.destroy()
        taskNode.addSpareParmTuple(hou.StringParmTemplate("taskPath","taskPath",1))
        taskNode.addSpareParmTuple(hou.StringParmTemplate("version","version",1))
        taskNode.addSpareParmTuple(hou.StringParmTemplate("projName","projName",1))
        taskNode.setParms({"taskPath":taskPathName,"projName":btpVfxProject.ProjName(),"version":"0"})
        projInfo=btpVfxProject.ProjInfo()
        hou.setFps({"film":24,"ntsc":30,"pal":25}[projInfo["fps"]])
        taskCamNode=obj.createNode("cam",node_name="%s_Cam"%taskGrpName)
        taskCamNode.setParms({"resx":float(projInfo["resW"]),"resy":float(projInfo["resH"])})

    def OpenTaskFile(self,fileName):
        hou.hipFile.load(fileName)

    def LoadFileSeq(self,fileName):
        pass

    def UploadTask(self):
        taskPathAndProjName=self.FindTaskNode()
        print taskPathAndProjName
        if taskPathAndProjName:
            imagePathName=""
            taskNodeName=taskPathAndProjName[0]
            taskPathName=taskPathAndProjName[1]
            projName=taskPathAndProjName[2]
            globalTaskPath=btpVfxProject.AttachRootPath(projName,taskPathName)
            imageBoard=btpGrabImageBoard.GrabImageBoard(globalTaskPath)
            if imageBoard.exec_()  == QDialog.Accepted:
                imageFileName=re.sub("/","_",taskPathName)
                imagePathName="%s/%s.jpg"%(globalTaskPath,imageFileName)
                imageBoard.SaveImage(imagePathName)
            startFrame,endFrame=hou.playbar.playbackRange()
            uploadPanel=UploadPanel([projName,taskPathName,"%s.hip"%taskNodeName,taskNodeName,imagePathName,startFrame,endFrame])
            uploadPanel.exec_()
        else:
            Warning_No_Task_Node()

    def FindTaskNode(self):
        for curNode in hou.node("/obj").children():
            print [curParm.name() for curParm in curNode.parms()]
            if "taskPath" in [curParm.name() for curParm in curNode.parms()]:
                return (curNode.name(),curNode.parm("taskPath").evalAsString(),curNode.parm("projName").evalAsString())
