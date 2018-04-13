# coding=utf-8
import os,sys,re,glob,time,shutil
from jsonIO import *
from btpDebugInfo import *

pyPath="D:/asunlab/github/vfxManager"
vfxConfigFile="%s/vfxConfig.ini"%pyPath

projName=None

def ReadConfigFile():
    if os.path.isfile(vfxConfigFile):
        file=open(vfxConfigFile,"r")
        fileContent=file.read().split("\n")
        file.close()
        return fileContent

def RootPath():
    fileContent=ReadConfigFile()
    if fileContent:
        return UnifyPathName(fileContent[1].strip())

def NukeCmd():
    fileContent=ReadConfigFile()
    if fileContent:
        return fileContent[3].strip()

def WriteRootPath(rootPath):
    fileContent=ReadConfigFile()
    if fileContent:
        fileContent[1]=rootPath
        file=open(vfxConfigFile,"w")
        file.writelines(["%s\n"%curLine for curLine in fileContent])
        file.close()

def WriteNukeCmd(nukeCmd):
    fileContent=ReadConfigFile()
    if fileContent:
        fileContent[3]=nukeCmd
        file=open(vfxConfigFile,"w")
        file.writelines(["%s\n"%curLine for curLine in fileContent])
        file.close()

def SetProjName(_projName):
    global projName
    projName=_projName

def ProjName():
    return projName

def ProjPath():
    return "%s/%s"%(RootPath(),projName)

def ValidRootPath():
    return os.path.isdir(RootPath())

def AttachProjPath(pathName):
    return "%s/%s"%(ProjPath(),pathName)

def AttachRootPath(projName,taskPathName):
    return "%s/%s/%s"%(RootPath(),projName,taskPathName)

def NewProjDirTree():
    fileContent=ReadConfigFile()
    if fileContent:
        gProjPath="%s/%s"%(RootPath(),projName)
        os.makedirs(gProjPath)
        index=fileContent.index("[proj struct]")+1
        lIndex=fileContent.index("[vfx struct]")
        for curDir in fileContent[index:lIndex]:
            gCurDir="%s/%s"%(gProjPath,curDir)
            os.makedirs(gCurDir)

def TimeMark():
    return time.strftime('%Y%b%d_%a_h%Hm%Ms%S',time.localtime(time.time()))

def NewVfxDirTree(taskPathName):
    fileContent=ReadConfigFile()
    index=fileContent.index("[vfx struct]")+1
    rootPath=RootPath()
    if fileContent:
        for curDir in fileContent[index:]:
            gCurDir="%s/%s"%(taskPathName,curDir)
            os.makedirs(gCurDir)

def UnifyPathName(pathName):
    return re.sub("\\\\","/",pathName)

def TaskNodeNameByTaskPathName(taskPathName):
    return re.sub("/","_",UnifyPathName(taskPathName))

def IconFilePathName(taskPathName):
    return "%s/%s/%s.jpg"%(ProjPath(),taskPathName,TaskNodeNameByTaskPathName(taskPathName))

def ProjInfoFile():
    return "%s/proj.json"%ProjPath()

def ProjInfo():
    return LoadJson(ProjInfoFile())

def MakeSureDirExists(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)

def copyFile(srcFile,tarFile):
    if os.path.isfile(srcFile):
        print "copy %s %s"%(srcFile,tarFile)
        shutil.copy(srcFile,tarFile)

def TaskVersionPath(taskPathName,curVer):
    projTaskPathName=AttachProjPath(taskPathName)
    return "%s/Versions/%s"%(projTaskPathName,curVer)

def RevertVersionFiles(taskPathName,curVer):
    projTaskPathName=AttachProjPath(taskPathName)
    for curFile in glob.glob("%s/*.*"%TaskVersionPath(taskPathName,curVer)):
        copyFile(curFile,projTaskPathName)

def VersionShowFile(taskPathName,curVer):
    verShowFile="%s/%s_preview.mov"%(TaskVersionPath(taskPathName,curVer),TaskNodeNameByTaskPathName(taskPathName))
    if os.path.isfile(verShowFile):
        return verShowFile
    else:
        Warning_Task_File_Absent(verShowFile)

def SaveVersion(projName,taskPath,files,comment,timeMark,progressBar):
    taskVersionPath="%s/%s/%s/Versions"%(RootPath(),projName,taskPath)
    curVersionPath="%s/%s"%(taskVersionPath,timeMark)
    print curVersionPath
    MakeSureDirExists(curVersionPath)
    perStepValue=(progressBar.value()-progressBar.minimum())/len(files)
    for curFile in files:
        copyFile(curFile,curVersionPath)
        progressBar.setValue(progressBar.value()+perStepValue)

    progressBar.setValue(100)
    UpdateVersionFile(projName,taskPath,comment,timeMark)

def VersionFileName(taskPath):
    return "%s/%s/version.json"%(ProjPath(),taskPath)

def ReadVersionFile(taskPath):
    return LoadJson(VersionFileName(taskPath))

def UpdateVersionFile(projName,taskPath,comment,timeMark):
    versionFile="%s/%s/%s/version.json"%(RootPath(),projName,taskPath)
    versionData=[]
    if os.path.isfile(versionFile):
        versionData=LoadJson(versionFile)
    versionData.append({'timeMark':timeMark,'comment':comment})
    DumpJson(versionFile,versionData)

import subprocess
def JpgToMov(jpgSeq,movFile,frameRange,artist,task,ver):
    cmd="%s -t %s/convertJpgToMov.py \"%s %s %i %i %s %s %s %s\" %i,%i"%(NukeCmd(),pyPath,jpgSeq,movFile,frameRange[0],frameRange[1],ProjName(),artist,task,ver,frameRange[0],frameRange[1])
    subprocess.call(cmd)

def DeleteFiles(fileFilter):
    for curFile in glob.glob(fileFilter):
        os.remove(curFile)