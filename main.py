# coding=utf-8
import os,sys, stat
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
from camera_gp import CanonCamera
from collections import deque,OrderedDict
import json, codecs

from widget_ImageViewer import ImageViewerWidget


class Ui_MainWindow(QMainWindow):
    
    def setupUi(self):
        self.resize(800, 480)
        
        

        self.zoom_in = QPixmap("Resources/zoom-in.png")
        self.zoom_out = QPixmap("Resources/zoom-out.png")

        self.zoom_in1 = QPixmap("Resources/zoom-in1.png")
        self.zoom_in2 = QPixmap("Resources/zoom-in2.png")
        self.zoom_out1 = QPixmap("Resources/zoom-out1.png")
        self.zoom_out2 = QPixmap("Resources/zoom-out2.png")

        self.play1 = QPixmap("Resources/buton_play1.png")
        self.play2 = QPixmap("Resources/buton_play2.png")

        self.pause1 = QPixmap("Resources/buton_pause1.png")
        self.pause2 = QPixmap("Resources/buton_pause2.png")

        self.foto_capture1 = QPixmap("Resources/foto_capture1.png")
        self.foto_capture2 = QPixmap("Resources/foto_capture2.png")



        self.canonCemara= CanonCamera(self)

        self.imageviewer= ImageViewerWidget(self)
        # self.imageviewer.setImagePath("Resources/background.png")
        self.imageviewer.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.imageviewer.setSize(0, 0,800, 480)
    
    def showMesage(self,message1,message2):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message1) 
        msg.setInformativeText(message2)
        msg.setWindowTitle("Warning !")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    
    def closeEvent(self,event):
        
        self.canonCemara.exit_camera()
        self.imageviewer.exit()

    def close_app(self):
        # self.canonCemara.exit()
        self.canonCemara.exit_camera()
        self.imageviewer.exit()
        
        exit()

        
    
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    mainwindow1 = Ui_MainWindow()
    mainwindow1.setupUi()
    mainwindow1.show()
    sys.exit(app.exec_())
    