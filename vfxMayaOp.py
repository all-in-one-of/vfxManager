import re
import maya.cmds as cmds
import maya.mel as mel
from btpPySide import *
from btpDebugInfo import *

try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance 

from maya import OpenMayaUI as omui
def MayaMainWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QWidget)
    return mayaMainWindow


def SetAttrGeneral(method):
    def SetAttrFunc(*arg):
        nodeAttr="%s.%s"%(arg[0],arg[1])
        if cmds.lockNode(arg[0],q=True):
            UnlockNode(arg[0])
            if cmds.getAttr(nodeAttr,l=True):
                cmds.setAttr(nodeAttr,l=False)
                method(*arg)
                cmds.setAttr(nodeAttr,l=True)
            LockNode(arg[0])
        else:
            method(*arg)
    return SetAttrFunc

@SetAttrGeneral
def SetAttr_Str(node,attr,value):
    cmds.setAttr("%s.%s"%(node,attr),value,type="string")

@SetAttrGeneral
def SetAttr_Long(node,attr,value):
    cmds.setAttr("%s.%s"%(node,attr),value)

def LockNode(node):
    cmds.lockNode(node,l=True)

def UnlockNode(node):
    cmds.lockNode(node,l=False)

def UnlockAttr(node,attr):
    UnlockNode(node)
    cmds.setAttr("%s.%s"%(node,attr),l=False)
    LockNode(node)

def LockAttr(node,attr):
    UnlockNode(node)
    cmds.setAttr("%s.%s"%(node,attr),l=True)
    LockNode(node)

def CreateGroup(grpName):
    cmds.CreateEmptyGroup()
    cmds.rename(grpName)

def AddAttr_Str(node,name,value):
    if not cmds.attributeQuery(name,node=node,exists=True):
        cmds.addAttr(node,ln=name,dt="string")

    attr="%s.%s"%(node,name)
    cmds.setAttr(attr,l=False)
    cmds.setAttr(attr,value,type="string")
    cmds.setAttr(attr,l=True)

def CreateTaskGrp(grpName,projName,taskPath):
    if not cmds.objExists(grpName):
        CreateGroup(grpName)
        AddAttr_Str(grpName,"taskPath",taskPath)
        AddAttr_Str(grpName,"version","0")
        AddAttr_Str(grpName,"projName",projName)
    else:
        Warnning_Exists(grpName)

def SetProjConfig(projData):
    cmds.currentUnit( time=projData['fps'] )
    cmds.setAttr("defaultResolution.width",projData['resW'])
    cmds.setAttr("defaultResolution.height",projData['resH'])
    cmds.setAttr("defaultResolution.pixelAspect",1)

def OpenMaFile(maFile):
    cmds.file(maFile,open=True,f=True,ignoreVersion=True)

def SaveMaFile(maFile):
    cmds.file(rename=maFile)
    cmds.file(save=True)

def SetParent(child,parent):
    if cmds.lockNode(parent,q=True):
        cmds.lockNode(parent,l=False)
        cmds.parent(child,parent)
        cmds.lockNode(parent,l=True)
    else:
        cmds.parent(child,parent)

def IsParent(child,parent):
    parentList=cmds.listRelatives(child,parent=True)
    if parentList:
        return parentList[0] == parent
    return False

def SetFilmGate_s16mm(camera):
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,0.493)
    cmds.setAttr("%s.verticalFilmAperture"%camera,0.292)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=True)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=True)

def SetFilmGate_35mm(camera):
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,0.825)
    cmds.setAttr("%s.verticalFilmAperture"%camera,0.446)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=True)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=True)

def SetFilmGate_70mm(camera):
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,2.772)
    cmds.setAttr("%s.verticalFilmAperture"%camera,2.072)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=True)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=True)

def SetFilmGate_35mm_User(camera):
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=False)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,1.417)
    cmds.setAttr("%s.verticalFilmAperture"%camera,0.945)
    cmds.setAttr("%s.horizontalFilmAperture"%camera,l=True)
    cmds.setAttr("%s.verticalFilmAperture"%camera,l=True)

def CreateCameraByFilmGate(cameraName,filmGate):
    if not cmds.objExists(cameraName):
        camNewName=cmds.camera(n=cameraName)
        cmds.rename(camNewName[0],cameraName)
        shapeList=cmds.listRelatives(cameraName)
        cmds.setAttr("%s.renderable"%shapeList[0],True)

    if filmGate == "35mm Default":
        SetFilmGate_35mm_User(cameraName)
    elif filmGate == "35mm 1.85 Projection":
        SetFilmGate_35mm(cameraName)
    elif filmGate == "70mm IMAX":
        SetFilmGate_70mm(cameraName)
    else:
        SetFilmGate_s16mm(cameraName)

def IsTaskScene():
    transList=cmds.ls(lockedNodes=True)
    return len(transList)>0

def FileType():
    return cmds.file(q=True,type=True)

def MayaFileByTaskNode(taskNode):
    if FileType() == "mayaAscii":
        return "%s.ma"%taskNode
    return "%s.mb"%taskNode

def FindTaskNode(taskType):
    transList=cmds.ls(lockedNodes=True)
    return [curNode for curNode in transList if re.search(taskType,curNode) and cmds.attributeQuery("taskPath",node=curNode,exists=True)][0]

def FindProjAndTaskPathName(taskType):
    taskNode=FindTaskNode(taskType)
    return cmds.getAttr("%s.projName"%taskNode),cmds.getAttr("%s.taskPath"%taskNode)

def FrameRange():
    return cmds.playbackOptions(animationStartTime=True,q=True),cmds.playbackOptions(animationEndTime=True,q=True)

