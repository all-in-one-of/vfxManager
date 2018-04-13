from btpPySide import *
import btpGrabImageBoard
import UploadPanelUI
class BaseUploadPanel(QDialog):
    def __init__(self,dataList,parent=None):
        QDialog.__init__(self,parent)
        self.ui=UploadPanelUI.Ui_Form()
        self.ui.setupUi(self)

        self.ui.progressBar_taskFiles.reset()
        self.ui.progressBar_texFiles.reset()

        self.ui.pushButton_upload.clicked.connect(self.upload)

        self.ui.label_Project.setText(dataList[0])
        self.ui.label_task.setText(dataList[1])
        self.ui.label_taskFile.setText(dataList[2])

        self.rootNode=dataList[3]
        self.imagePathName=dataList[4]

        btpGrabImageBoard.SetLabelImage(self.ui.label_image,dataList[4])

        self.ui.spinBox_startFrame.setValue(dataList[5])
        self.ui.spinBox_endFrame.setValue(dataList[6])

        