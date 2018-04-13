from pyside2uic import compileUi
import py_compile,glob,os,re

uiPath=os.curdir
print uiPath
preIndex=len(uiPath)+1
uiFiles=glob.glob("%s/ui/*.ui"%uiPath)
print uiFiles
for uiFile in uiFiles:
    print uiFile
    fileBaseName=re.search("[^\\\\]+.ui$",uiFile).group(0)
    fileBaseName=re.search("^[^.]+",fileBaseName).group(0)
    pyFile="%s/%sUI.py"%(uiPath,fileBaseName)
    print uiFile,pyFile
    pyFileP = open(pyFile, 'w')
    compileUi(uiFile, pyFileP, False, 4, False)
    pyFileP.close()