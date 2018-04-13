import os,time,re
import shutil,glob
import maya.cmds as cmds

def copyFile(srcFile,tarFile):
    if os.path.isfile(srcFile):
        shutil.copy(srcFile,tarFile)

def CopyMultiUVFiles(method):
    def copymultiuvfiles_func(*argv):
        targetPath=argv[1]
        filteredFileName=method(*argv)
        print filteredFileName
        fileList=glob.glob(filteredFileName)
        if fileList:
            for curFile in fileList:
                print curFile,targetPath
                copyFile(curFile,targetPath)
    return copymultiuvfiles_func

@CopyMultiUVFiles
def CopyUdimTexFiles(srcImagePathName,targetPath):
    return re.sub("\d{4}","????",srcImagePathName)

@CopyMultiUVFiles
def Copy1BasedTexFiles(srcImagePathName,targetPath):
    return re.sub("\d{1}","?",srcImagePathName)

def FilePathFromName(filePathName):
    return re.sub("/[^////]+$","",filePathName)

def FileExists(filePathName):
    return os.path.isfile(filePathName)

def MakeSureDirExists(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)

def RepathTextureFiles(targetDir):
    fileNodeAttrList=cmds.filePathEditor(query=True, listFiles="", attributeOnly=True)
    if fileNodeAttrList:
        validTexFileNodeAttrList=[]
        for curAttr in fileNodeAttrList:
            if re.search("\.",curAttr):
                fileNode=re.sub("\.[^.]+$","",curAttr)
                if not cmds.referenceQuery(fileNode,isNodeReferenced=True) and cmds.objectType(fileNode) in mlNodeDef.textureNode:
                    validTexFileNodeAttrList.append(curAttr)

        if len(validTexFileNodeAttrList) > 0:
            cmds.filePathEditor(validTexFileNodeAttrList,repath=targetDir,force=True)

def CopyAndRepathTextureFiles(targetDir,progressBar):
    MakeSureDirExists(targetDir)
    fileNodeAttrList=cmds.filePathEditor(query=True, listFiles="", attributeOnly=True)
    if fileNodeAttrList:
        perStepValue=100/len(fileNodeAttrList)
        for curAttr in fileNodeAttrList:
            if re.search("\.",curAttr):
                fileNode=re.sub("\.[^.]+$","",curAttr)
                if ObjExists(fileNode):
                    if not cmds.referenceQuery(fileNode,isNodeReferenced=True) and cmds.objectType(fileNode) in mlNodeDef.textureNode:
                        srcImagePathName=cmds.getAttr(curAttr)
                        if FileExists(srcImagePathName):
                            imageFilePath=FilePathFromName(srcImagePathName)
                            print imageFilePath,targetDir
                            if imageFilePath != targetDir:
                                if cmds.attributeQuery('uvTilingMode',node=fileNode,exists=True):
                                    uvTilingModeAttr="%s.uvTilingMode"%fileNode
                                    uvTilingMode=cmds.getAttr(uvTilingModeAttr)
                                    if uvTilingMode == 3:
                                        CopyUdimTexFiles(srcImagePathName,targetDir)
                                    elif uvTilingMode == 2:
                                        Copy1BasedTexFiles(srcImagePathName,targetDir)
                                    else:
                                        copyFile(srcImagePathName,targetDir)
                                else:
                                    copyFile(srcImagePathName,targetDir)

            progressBar.setValue(progressBar.value()+perStepValue)
    progressBar.setValue(100)
    RepathTextureFiles(targetDir)