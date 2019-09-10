from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import *

class ImageButton(QAbstractButton):
    def __init__(self,pixmap, pixmap_hover, pixmap_pressed,w,h, parent=None):
        super(ImageButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed
        self.w=w 
        self.h=h
        self.text=QLabel(self)
        self.setGeometry(0, 0,self.w,self.h)
        # layout_widget.setObjectName("layout_widget_tmp1")
        # self.setStyleSheet(" opacity:1.0; border: 1px solid #00b959;border-radius: 10px;")
        # sself.text.setStyleSheet("border-radius: 10px;")

        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setGeometry(0, 0,self.w,self.h)
        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def setBackground(self,pixmap, pixmap_hover, pixmap_pressed):
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed
    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)


    def setText(self,text,style=None):
        self.text.setText(text)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setGeometry(0, 0,self.w,self.h)
        if(style == None):
            self.text.setStyleSheet("color: white")
        else:
            self.text.setStyleSheet(style)    
    
    def setIcon(self,icon):
        self.text.setPixmap(icon)
    # def enterEvent(self, event):
    #     self.update()

    # def leaveEvent(self, event):
    #     self.update()

    def sizeHint(self):
        
        return QSize(self.w, self.h)