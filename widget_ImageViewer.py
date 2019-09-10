import sys
import os
import io
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import Thread 
from collections import deque,OrderedDict
import threading
import time
from PIL import Image
import gphoto2 as gp
from imageButton import ImageButton

class ImageViewerWidget(QWidget):



    def __init__(self,parent):
        super(ImageViewerWidget, self).__init__(parent)
        self.parent=parent
        self.capture_image=None
        self.iscapture_image=False
        self.camera_fps= 0.5
        self.fittowindow= False
        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.isplay= False
        self.ispreview=False
        self.isexit=False
        

        self.scaleFactor = 1.0
        self.imageLabel = QLabel(self)
        
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.scrollArea.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff ) 
        
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)

        self.layout_widget= QWidget(self)
        

        self.zoom_in= ImageButton(self.parent.zoom_in2,self.parent.zoom_in1,self.parent.zoom_in2,40,30,self.layout_widget)
        self.zoom_in.setText("")
        self.zoom_in.clicked.connect(self.zoomIn)
        self.zoom_in.setGeometry(QtCore.QRect(0, 0, 40, 30))


        self.zoom_out= ImageButton(self.parent.zoom_out2,self.parent.zoom_out1,self.parent.zoom_out2,40,30,self.layout_widget)
        self.zoom_out.setText("")
        self.zoom_out.clicked.connect(self.zoomOut)
        self.zoom_out.setGeometry(QtCore.QRect(42, 0, 40, 30))

        self.btn_play_pause= ImageButton(self.parent.play2,self.parent.play1,self.parent.play2,40,30,self.layout_widget)
        self.btn_play_pause.setText("")
        self.btn_play_pause.clicked.connect(self.play_pause)
        self.btn_play_pause.setGeometry(QtCore.QRect(84, 0, 40, 30))

        self.btn_capture= ImageButton(self.parent.foto_capture2,self.parent.foto_capture1,self.parent.foto_capture2,40,30,self.layout_widget)
        self.btn_capture.setText("")
        self.btn_capture.clicked.connect(self.start_capture)
        self.btn_capture.setGeometry(QtCore.QRect(126, 0, 40, 30))

        # self.galery_btn= ImageButton(self.parent.galery_btn2,self.parent.galery_btn1,self.parent.galery_btn2,40,30,self.layout_widget)
        # self.galery_btn.setText("")
        # self.galery_btn.clicked.connect(self.open_galery)
        # self.galery_btn.setGeometry(QtCore.QRect(170, 0, 40, 30))


        camreaspeed_LayoutWidget = QtGui.QWidget(self)
        camreaspeed_LayoutWidget.setGeometry(QtCore.QRect(4, 4, 170, 40))
        

        self.fps_comboBox = QtGui.QComboBox(camreaspeed_LayoutWidget)
        self.fps_comboBox.setGeometry(QtCore.QRect(4, 1, 80, 30))
        self.fps_comboBox.setObjectName("fps_comboBox")
        self.fps_comboBox.setStyleSheet("""QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px; text-align: center;}
                        #fps_comboBox{color:#FFFFFF; padding:2px; border: 1px solid #FFFFFF;border-radius: 10px;background-color:#424242;}""")
        self.fps_comboBox.setEditable(True)
        self.fps_comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.fps_comboBox.lineEdit().setReadOnly(True)
        self.fps_comboBox.addItem("2 fps")
        self.fps_comboBox.addItem("4 fps")
        self.fps_comboBox.addItem("8 fps")
        self.fps_comboBox.addItem("12 fps")
        self.fps_comboBox.addItem("16 fps")
        # self.fps_comboBox.addItem("20 fps")
        self.fps_comboBox.currentIndexChanged.connect(self.setcamera_fps)



        self.pixmap = QtGui.QPixmap()
        self.img = QImage()
        # self.start()
        self.connect(self, QtCore.SIGNAL("show_preview()"), self.show_preview)
        threading.Timer(self.camera_fps, self.signalemit).start()
 

    def open_galery(self):
        self.parent.galery.setVisible(True)
        self.parent.galery.galeri_start_emit()
    def open_setings(self):
        self.parent.settings_menu.setVisible(True)
    def signalemit(self):
        if not self.isexit :
            self.emit(QtCore.SIGNAL("show_preview()"))
            threading.Timer(self.camera_fps, self.signalemit).start()

    def show_preview(self):
        
        if(self.parent.canonCemara.isconnec):
            if self.isplay:
                if not self.ispreview :
                    self.ispreview=True
                    try:
                        camera_file = gp.check_result(gp.gp_camera_capture_preview(self.parent.canonCemara.camera))
                        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
                        image = Image.open(io.BytesIO(file_data))
                        self.pixmap=self.PILimageToQImage(image)
                        self.imageLabel.setPixmap(self.pixmap)
                    except Exception as e:
                        print("Frame Read error")
                    self.ispreview=False
            elif self.iscapture_image:
                self.iscapture_image=False
                self.pixmap=self.PILimageToQImage(self.capture_image)
                self.imageLabel.setPixmap(self.pixmap)


    def addFrame(self,image):
        self.pause_()
        self.pixmap=image
        self.imageLabel.setPixmap(self.pixmap)

    def start_capture(self):
        self.pause_()
        time.sleep(self.camera_fps)
        OK,path=self.parent.canonCemara.capture_image()
        if OK :
            self.capture_image = Image.open(path)
            self.iscapture_image=True
        else :
            self.parent.showMesage("Capture Fail..","..")
    
    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def play_pause(self):
        if self.isplay :
            self.pause_()
        else:
            self.play_()

    def play_(self):
        self.isplay=True
        self.btn_play_pause.setBackground(self.parent.pause2,self.parent.pause1,self.parent.pause2)
    def pause_(self):
        self.isplay=False
        self.btn_play_pause.setBackground(self.parent.play2,self.parent.play1,self.parent.play2)

    def fitToWindow(self):
        # fitToWindow = self.fitToWindowAct.isChecked()
        if self.fittowindow :
            self.fittowindow=False
        else:
            self.fittowindow = True
        self.scrollArea.setWidgetResizable(self.fittowindow)
        # if not fitToWindow:
        #     self.normalSize()
 
    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)


    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))


    def setcamera_fps(self,index):
        if index == 0:
            self.camera_fps=0.5
        elif index==1:
            self.camera_fps=0.25
        elif index==2:
            self.camera_fps=0.12
        elif index == 3:
            self.camera_fps==0.08
        elif index == 4:
            self.camera_fps=0.06
        elif index==5:
            self.camera_fps=0.05

    def setframespeed_dec(self):
        self.parent.framespeed += 0.05
        if self.parent.framespeed >= 0.5:
            self.parent.framespeed = 0.5

        self.framespeed.setText(str(self.parent.framespeed))
    def setframespeed_inc(self):
        self.parent.framespeed -= 0.05
        if(self.parent.framespeed <= 0) :
            self.parent.framespeed = 0

        self.framespeed.setText(str(self.parent.framespeed))
    def PILimageToQImage(self,im):
        im2 = im.convert("RGB")
        data = im2.tobytes("raw", "RGB")
        qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGB888)
        # qim.save('hehe.png')
        pixmap = QtGui.QPixmap.fromImage(qim)
        return pixmap
    def PILimageToQImage2(self,im):
        im2 = im.convert("RGB")
        data = im2.tobytes("raw", "RGB")
        qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGB888)
        return qim
    def setImagePath(self,path):
        self.path=path
        image = QImage(self.path)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
    def exit(self):
        self.isexit=True
        self.iscapture360=False
        self.iscapture360_start=False
    def setSize(self,x,y,w,h):
        self.setGeometry(QtCore.QRect(x, y, w, h))
        self.imageLabel.setGeometry(QtCore.QRect(0, 0, w, h))
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, w, h))
        self.layout_widget.setGeometry(QtCore.QRect((w-250)/2, 4, 250, 40))