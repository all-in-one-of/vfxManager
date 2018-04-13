import vfxMayaOp
import btpVfxManager

def main():
    panel=btpVfxManager.btpVfxManager(vfxMayaOp.MayaMainWindow(),"Maya")
    panel.show()