from btpPySide import *

import glob,os

def SetLabelImage(label,filePathName):
    label.clear()
    label.setText("No Image")
    if filePathName is not None and os.path.isfile(filePathName):
        pixmap=QPixmap()
        pixmap.load(filePathName)
        label.setScaledContents(True)
        label.setPixmap(pixmap)

class GrabImageBoard(QDialog):
    def __init__(self,imageSavedPath,parent=None):
        QDialog.__init__(self,parent)
        self.path=imageSavedPath
        self.fullPix=QPixmap.grabWindow(QApplication.desktop().winId())
        pixSize=self.fullPix.size()
        
        self.fullPixmapLabel=QLabel(self)
        self.fullPixmapLabel.setPixmap(self.fullPix)
        self.resize(pixSize)
        
        self.btn_ok = QPushButton(self)
        self.btn_ok.setText("OK")
        self.btn_ok.setGeometry(QRect(110, 100, 100, 32))
        self.btn_ok.clicked.connect(self.accept)
        
        self.x=0
        self.y=0
        self.endX=0
        self.endY=0
        self.width=0
        self.height=0
        
    def SaveLatestImage(self):
        cropedImage=self.fullPix.copy(self.x,self.y,self.width,self.height)
        showBoardFiles=glob.glob("%s/showBoard_????.jpg"%self.path)
        lastNum=1
        if len(showBoardFiles)>0:
            showBoardFiles.sort()
            lastNum=int(showBoardFiles[-1][-8:-4]) + 1
            
        imagePathName="%s/showBoard_%04d.jpg"%(self.path,lastNum)
        cropedImage.save(imagePathName)

    def SaveImage(self,imagePathName):
        cropedImage=self.fullPix.copy(self.x,self.y,self.width,self.height)
        cropedImage.save(imagePathName)
        
    def DrawBound(self):
        pen=QPen()
        pen.setWidth(2)
        pen.setColor(QColor.fromRgb(255,200,100))
        painter=QPainter()
        
        painter.begin(self.fullPixmapLabel.pixmap())
        painter.setPen(pen)
        painter.drawRect(self.x,self.y,self.width,self.height)
        painter.end()
    
    def paintEvent(self,event):
        self.fullPixmapLabel.setPixmap(self.fullPix)
        self.DrawBound()
        
        btn_width=100
        btn_height=32
        self.btn_ok.setGeometry(QRect(self.endX-btn_width, self.endY, btn_width, btn_height))
        
    def mousePressEvent(self,event):
        if event.button() == Qt.RightButton:
            self.accept()
            
        self.x=event.x()
        self.y=event.y()
        
    def mouseMoveEvent(self,event):
        self.endX=event.x()
        self.width=self.endX-self.x

        self.height=self.width*0.75
        self.endY=self.y+self.height