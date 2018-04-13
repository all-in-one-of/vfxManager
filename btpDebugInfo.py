from btpPySide import *

errorWindow=None
def displayInfo(msgMethod):
    def displayFunc(*msg):
        global errorWindow
        errorWindow = QErrorMessage()
        errorWindow.showMessage(msgMethod(*msg))
    return displayFunc

@displayInfo
def Warnning_Exists(directory):
    return "%s already exists!"%directory

@displayInfo
def Warnning_NotEmpty(directory):
    return "%s is not empty!"%directory    

@displayInfo
def Warning_No_Task_Node():
    return "No task node in scene. Initialize the scene before upload."

@displayInfo
def Warnning_Name_Format():
    return "The name that includes SPACE or existent NAME would not be accepted."

@displayInfo
def Warnning_Func_Absent(funcName):
    return "Function %s does not exist."%funcName

@displayInfo
def Error_Dir_Absent(dirName):
    return "The directory %s does not exist."%dirName

@displayInfo
def Warnning_TaskUser_Not_Match(taskPath,userName):
    return "%s does not belong to this task:%s"%(userName,taskPath)

@displayInfo
def Warnning_TaskNode_Absent():
    return "Task node does not exist."

@displayInfo
def Warning_Select_Object_First(type):
    return "Select %s at first."%type

@displayInfo
def Warning_Task_Absent(taskName):
    return "The task,%s,does not exist."%taskName

@displayInfo
def Warning_Task_File_Absent(taskFileName):
    return "The task file,%s,does not exist."%taskFileName