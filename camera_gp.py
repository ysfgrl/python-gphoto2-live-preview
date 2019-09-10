# import piggyphoto
from threading import Thread 
import time
from datetime import datetime
import subprocess 
from collections import deque,OrderedDict
import os, shutil
from PIL import Image
import json, codecs
import io
import logging
import subprocess 
import sys
import logging
import tzlocal
import gphoto2 as gp

class CanonCamera():
    def __init__(self, parent=None):
        self.parent=parent
        self.isconnec=False
        self.cameramodel="Undefined"
        self.find_camera()

    def exit_camera(self):
        time.sleep(0.1)
        if self.isconnec:
            sonuc=gp.check_result(gp.gp_camera_exit(self.camera))
        
    def find_camera(self):
        try:
            self.camera = gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(self.camera))
            # self.config = gp.check_result(gp.gp_camera_get_config(self.camera))
            self.config = self.camera.get_config()
            
            self.cameramodel = self.getCameraModel()
            # self.parent.settings.savecameraconfig(self.camera,"temp")
            self.isconnec=True
        except  :
            self.isconnec=False
            print("Camera not connect") 
        print("-----------------------------")
        print("Model:",self.cameramodel)

    def getCameraModel(self):
        camera_config= self.config
        OK, camera_model = gp.gp_widget_get_child_by_name(camera_config, 'cameramodel')
        if OK < gp.GP_OK:
            OK, camera_model = gp.gp_widget_get_child_by_name(camera_config, 'model')
        if OK >= gp.GP_OK:
            camera_model = camera_model.get_value()
        else:
            camera_model = ''
        return camera_model
    def capture_image(self):
        print("--")
        if(self.isconnec):
            file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE))
            print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
            path="tempcapture/tempfile.jpg"
            camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
            gp.check_result(gp.gp_file_save(camera_file, path))
            time.sleep(1)
            return (True,path)
        return (False,path)