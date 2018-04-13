import hou
import btpVfxManager

def main():
    mainWidget=hou.ui.mainQtWindow()
    panel=btpVfxManager.btpVfxManager(mainWidget,"Hou")
    panel.show()