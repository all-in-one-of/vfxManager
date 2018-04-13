import SwingMenu

def CreateUI():
    SwingMenu.Swing_CreateUI(["VFX Manager","Upload"],["import mayaVfxManager\nmayaVfxManager.main()","import btpVfxManager\nbtpVfxManager.UploadTask(\"Maya\")"])