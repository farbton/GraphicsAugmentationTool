# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:23:50 2022

@author: Kirko
"""
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog,\
    QGraphicsPixmapItem, QGridLayout, QLabel, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QPen, QFont, QImage, QColor, QImageReader
from PIL import Image, ImageEnhance , ImageQt, ImageShow
import reader, writer, brightness, saturation, contrast, sharpness, \
    rotation, flip, translation, scale, noise
import os, numpy as np
import time
import io
testwert = 0
import matplotlib.pyplot as plt

class Window(QMainWindow):
    
    def __init__(self, app):       
        super(Window, self).__init__()       
        uic.loadUi("AugmentationTool_GUI.ui", self)
        self.source_folder_path = "source/"
        self.destination_folder_path = "destination/"
        # self.source_folder_path = "C:/Users/Admin/Nextcloud/Gemeinsame Dateien/Fg-Medientechnik_Lehrstuhl/3_Projekte/KI@MINT/HariboAufnahmen/Haribo_Orginalaufnahmen_2.Versuch/40cm/"
        # self.destination_folder_path = "C:/KI_MINT/Haribo_Bilder_ohne_Cloud/"
        self.setWindowTitle("Image Augmentation Tool")
        self.screen = app.primaryScreen()
        self.width  = int(self.screen.size().width()/2)
        self.height = int(self.screen.size().height()/2)
        self.left   = int(self.screen.size().width()/2 - self.width/2)
        self.top    = int(self.screen.size().height()/2 - self.height/2)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.lw_sourcefolder.resize(50,50)
        self.reader = reader.Reader()       
        self.scene = QGraphicsScene(self)
        self.info_text  = True
        self.info2_text = False
        self.pil_imagelist = []
        self.pil_imagelist_rotation = []
        self.txt_list = []
        self.pil_imagelist_brightness = []
        self.pil_imagelist_brightness_allImages = []
        self.pil_imagelist_flip = []
        self.pil_imagelist_translation = []
        self.mode = None
        self.init_source_path()
        self.print_destinationfolder_path()
        self.show_filenames_in_listwidget_destinationfolder()
        self.comboBox_noise.addItems(["gaussian","localvar","poisson", "s&p", "speckle"])
        
    def print_info_text_in_gv(self):
        text_item = QGraphicsTextItem()
        text_item.setHtml("<html> <body> <h1 style=color:red;> \
            1. Press the &lt;Source&gt; button to select the source folder or \
            press a button to manipulate the image in the default sourcefolder. <br> \
            2. Press the &lt;Destination&gt; button to select the destination folder or use the default folder <br> \
            3. Each image manipulation has a field for values. Change the values if required <br> \
            4. You can edit .jpg and .png files. <br> \
            </h1></body></html>")
        self.scene.addItem(text_item)
        self.gv_preview.setScene(self.scene)
        
    def print_info2_text_in_gv(self):
        self.scene.clear()
        text_item = QGraphicsTextItem()
        text_item.setHtml("<html> <body> <h1 style=color:red;> \
            Now select a button for image manipulation<br> \
            </h1></body></html>")
        self.scene.addItem(text_item)
        self.gv_preview.setScene(self.scene)
        
    def start(self):
        self.pb_sourcefolder.clicked.connect(self.open_sourcefolder)
        self.pb_brightness.clicked.connect(self.brightness)
        self.pb_convert_and_save_one_image.clicked.connect(self.save_one_file)
        self.pb_convert_and_save_all_images.clicked.connect(self.save_all_files)
        self.lw_sourcefolder.itemClicked.connect(self.preview_item)
        self.pb_destinationfolder.clicked.connect(self.open_destinationfolder)
        self.pb_saturation.clicked.connect(self.saturation)
        self.pb_contrast.clicked.connect(self.contrast)
        self.pb_sharpness.clicked.connect(self.sharpness)
        self.pb_rotation.clicked.connect(self.rotation)
        self.pb_translation.clicked.connect(self.translation)
        self.pb_flip.clicked.connect(self.flip)
        self.pb_noise.clicked.connect(self.noise)
        self.pb_scale.clicked.connect(self.scale)
     
    def init_source_path(self):
        self.source_folder_path = os.getcwd() + "/" + self.source_folder_path
        # print("init_source_path: ", self.source_folder_path, "\n")
        self.destination_folder_path = os.getcwd() + "/" + self.destination_folder_path
        # print("init_source_path: ", self.destination_folder_path, "\n")
        self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
        self.list_filenames = self.reader.read_sourcefolder(self.source_folder_path)
        self.show_filenames_in_listwidget_sourcefolder()
        # self.print_info2_text_in_gv()
        self.print_sourcefolder_path()
        self.print_imagecounter()
        self.print_text_in_console("source folder path: " + self.source_folder_path)
        self.print_text_in_console("destination folder path: " + self.destination_folder_path)
        
    def print_imagecounter(self):
        counter = 0
        counter = self.lw_sourcefolder.count()
        self.lb_imagecounter.setText(str(counter))
        
    def open_sourcefolder(self):
        
        dir = QFileDialog.getExistingDirectory()
        
        if dir:
            self.source_folder_path = dir

        if self.source_folder_path:
            self.info_text  = False
            self.info2_text = True
            self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
            # print("open_sourcefolder: ", self.source_folder_path, "\n")
            self.list_filenames = self.reader.read_sourcefolder(self.source_folder_path)
            self.show_filenames_in_listwidget_sourcefolder()
            self.print_info2_text_in_gv()
            self.print_sourcefolder_path()
            self.print_imagecounter()
            self.print_text_in_console("source folder path: " + self.source_folder_path)
     
    def print_sourcefolder_path(self):
        self.lb_sourcefolder_path.setText(self.source_folder_path[:60] + "..." + self.source_folder_path[-60:])
        # self.lb_sourcefolder_path.setText(self.source_folder_path)
     
    def print_destinationfolder_path(self):
        self.lb_destinationfolder_path.setText(self.destination_folder_path[:60] + "..." + self.destination_folder_path[-60:])
        # self.lb_destinationfolder_path.setText(self.destination_folder_path)
        
    def open_destinationfolder(self):
        self.destination_folder_path = QFileDialog.getExistingDirectory()
        if self.destination_folder_path:
            self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
            self.print_destinationfolder_path()
            self.print_text_in_console("destination folder path: " + self.destination_folder_path)
               
    def show_filenames_in_listwidget_sourcefolder(self):
        self.lw_sourcefolder.clear()
        for name in self.list_filenames:
            if name.endswith(('.jpg', '.png')):
                self.lw_sourcefolder.addItem(str(name))
            if name.endswith('.txt'):
                self.txt_list.append(name)
        self.lw_sourcefolder.setCurrentRow(0)
        # self.determine_finished_images()
        
    def show_filenames_in_listwidget_destinationfolder(self):
        # self.destination_folder_path = os.getcwd() + "/" + self.destination_folder_path
        # print("show_filenames_in_listwidget_destinationfolder: ",self.destination_folder_path, "\n")
        list_filenames = self.reader.read_sourcefolder(self.destination_folder_path)
        self.lw_destinationfolder.clear()
        for name in list_filenames:
            if name.endswith(('.jpg', '.png')):
                self.lw_destinationfolder.addItem(str(name))
            
        # self.lw_sourcefolder.setCurrentRow(0)
        # self.determine_finished_images()
           
    def get_gv_height_and_width(self):
        return  self.gv_preview.width(), self.gv_preview.height()

    def show_pil_imagelist_in_gv(self):
        # print("Funktion: show_pil_imagelist_in_gv")
        self.scene.clear()
        gv_width, gv_height = self.get_gv_height_and_width()
        imagelist = []
        
        if self.mode == "brightness":
            imagelist = self.pil_imagelist_brightness
            # print(len(imagelist))
            
        if self.mode == "saturation":
            imagelist = self.pil_imagelist_saturation
        if self.mode == "contrast":
            imagelist = self.pil_imagelist_contrast
        if self.mode == "sharpness":
            imagelist = self.pil_imagelist_sharpness
        if self.mode == "flip":
            imagelist = self.pil_imagelist_flip
        if self.mode == "translation":
            imagelist = self.pil_imagelist_translation
        if self.mode == "scale":
            imagelist = self.pil_imagelist_scale
        if self.mode == "noise":
            imagelist = self.pil_imagelist_noise
            
            
        row = 0
        col = 0
        # print("mainwindow.show_pil...()",imagelist)
        for i, (image, name, value, counter) in enumerate(imagelist):
            # print(image.mode)
            # image.show()
            if image.mode == "RGB":
                imageformat = QImage.Format_RGB888
            if image.mode == "RGBA":
                imageformat = QImage.Format_RGBA8888
            if image.mode == "L":
                imageformat = QImage.Format_Grayscale8
          
            if (i % 5  == 0) and (i > 0):
                row += 1
                col  = 0
                
            # os.system("pause")
            pm_width_new = int((gv_width - 70)//5)  # 70 = offset Zwischenraum zwischen den Bildern
            # print("width: ", pm_width_new)
            aspect_ratio = image.width / image.height # Seitenverhältnis
            images_per_col = gv_height / (pm_width_new  / aspect_ratio) 
            pm_height_new = int(gv_height / images_per_col)

            qimage = QImage(image.tobytes(), image.width, image.height, imageformat)#Format_RGB888
            # qimage = qimage.convertToFormat(QImage.Format_ARGB32)
            # print(qimage.format())
            # print("__", qimage.isNull())
            # time.sleep(.5)
            # plt.imshow(qimage)
            pixmap = QPixmap.fromImage(qimage)
            pixmap_item = self.scene.addPixmap(pixmap.scaled(pm_width_new, pm_height_new ))
            pixmap_item.setPos(col*(pm_width_new+10),row * (pm_height_new + 10))
            # pixmap_item.setFlag(QGraphicsItem.ItemIsMovable)
            self.gv_preview.setScene(self.scene)
            # print(col)
            col += 1
            
    def show_pil_imagelist_rotation_in_gv(self):
        self.scene.clear()
        gv_width, gv_height = self.get_gv_height_and_width()
        imagelist = [] 
        imagelist = self.pil_imagelist_rotation
        row = 0
        col = 0
        # print("gv_width:" , gv_width, "gv_height: ", gv_height) 
        
        # pm_width_new  = 300
        # pm_height_new = 300
        img_width = imagelist[0][0].width // 3
        # print(img_width)
        pics_per_row = gv_width // img_width
        
        
        
        for i, (image, ___, ___, ___) in enumerate(imagelist):
            
            aspect_ratio = image.width / image.height
            # print("aspect_ratio: ", aspect_ratio)
            
            # if image.mode == "RGB":
            #     imageformat = QImage.Format_RGB888
            # if image.mode == "RGBA":
            #     imageformat = QImage.Format_RGBA8888
            # if image.mode == "L":
            #     imageformat = QImage.Format_Grayscale8
                
            if (i % pics_per_row  == 0) and (i > 0) :
                row += 1
                col  = 0
                
               
            pm_width_new = int((gv_width - 70)//5)  # 70 = offset Zwischenraum zwischen den Bildern
            # print("pm_width_new: ", pm_width_new)
            images_per_col = gv_height / (pm_width_new / aspect_ratio)
            pm_height_new = int(gv_height / images_per_col)            
            image = image.convert("RGBA")            
            qimage = QImage(image.tobytes("raw", "BGRA"),
                            image.width,
                            image.height,
                            QImage.Format_ARGB32)
     
            # print(qimage.format())
            pixmap = QPixmap.fromImage(qimage)  
            if pm_width_new <= pm_height_new:
                pixmap_item = self.scene.addPixmap(pixmap.scaled(int(img_width * aspect_ratio), img_width))
            else:     
                pixmap_item = self.scene.addPixmap(pixmap.scaled(img_width, int(img_width / aspect_ratio)))
                
            
            pixmap_item.setPos(col*(img_width + 10),row * (img_width + 10))
            self.gv_preview.setScene(self.scene)
            col += 1                               

    def brightness(self):
        # print("funktion: brightness")
        self.mode = "brightness"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.brightness = brightness.Brightness(self,
                                                self.lw_sourcefolder,
                                                self.source_folder_path, 
                                                self.le_brightness)
        
        self.pil_imagelist_brightness = self.brightness.preview_brightness_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(self.le_brightness.text())
        
        
    def saturation(self):
        self.mode = "saturation"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.saturation = saturation.Saturation(self,
                                                self.lw_sourcefolder,
                                                self.source_folder_path,
                                                self.le_saturation)
        
        self.pil_imagelist_saturation = self.saturation.preview_saturation_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(self.le_saturation.text())
        

    def contrast(self):
        self.mode = "contrast"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.contrast = contrast.Contrast(self, 
                                          self.lw_sourcefolder,
                                          self.source_folder_path,
                                          self.le_contrast)
        
        self.pil_imagelist_contrast = self.contrast.preview_contrast_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(self.le_contrast.text())
        

    def sharpness(self):
        self.mode = "sharpness"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.sharpness = sharpness.Sharpness(self, 
                                             self.lw_sourcefolder,
                                             self.source_folder_path,
                                             self.le_sharpness)
        
        self.pil_imagelist_sharpness = self.sharpness.preview_sharpness_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(self.le_sharpness.text())
        
        
    def rotation(self):
        self.mode = "rotation"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.rotation = rotation.Rotation(self, 
                                          self.lw_sourcefolder,
                                          self.source_folder_path,
                                          self.le_rotation)
        
        self.pil_imagelist_rotation, self.txt_filelist_rotation = \
            self.rotation.preview_rotation_oneImage()
        self.show_pil_imagelist_rotation_in_gv()
        self.determine_finished_images(self.le_rotation.text())
        
    def translation(self):
        self.mode = "translation"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.translation = translation.Translation(self, 
                                                   self.lw_sourcefolder,
                                                   self.source_folder_path,
                                                   self.le_translation)
        
        self.pil_imagelist_translation, self.txt_filelist_translation =\
            self.translation.preview_translation_oneImage()        
        self.show_pil_imagelist_in_gv()
        img_width = self.pil_imagelist_translation[0][0].width
        self.determine_finished_images(img_width / int(self.le_translation.text()))
        
    def flip(self):
        self.mode = "flip"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.flip = flip.Flip(self, self.lw_sourcefolder, self.source_folder_path)
        self.pil_imagelist_flip, self.txt_filelist_flip =\
            self.flip.preview_flip_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(2)
        
    def noise(self):
        self.mode = "noise"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)   
        self.noise = noise.Noise(self, 
                                 self.lw_sourcefolder, 
                                 self.source_folder_path,
                                 self.comboBox_noise)
        
        self.pil_imagelist_noise = self.noise.preview_noise_oneImage()
        # print(len(self.pil_imagelist_noise))
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(1)
        
    def scale(self):
        self.mode = "scale"
        self.info_text = False
        self.info2_text = False
        self.print_text_in_console("mode: " + self.mode)
        self.scale = scale.Scale(self, 
                                 self.lw_sourcefolder, 
                                 self.source_folder_path,
                                 self.le_scale)
        self.pil_imagelist_scale, self.txt_filelist_scale =\
            self.scale.preview_scale_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images(self.le_scale.text())
    
    def print_text_in_console(self, text):
        self.lb_console.setText(self.lb_console.text() + "\n" + text)
        # scrollBar = self.scrollArea.verticalScrollBar()
        # scrollBar.setValue(scrollBar.maximum()+1)
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        
    def save_one_file(self):
        if self.mode == "brightness":
            self.writer.write_files_to_disk(self.pil_imagelist_brightness,
                                            self.txt_list,
                                            self.mode)
        if self.mode == "saturation":
            self.writer.write_files_to_disk(self.pil_imagelist_saturation,
                                            self.txt_list,
                                            self.mode)
        if self.mode == "contrast":
            self.writer.write_files_to_disk(self.pil_imagelist_contrast,
                                            self.txt_list,
                                            self.mode)
        if self.mode == "sharpness":
            self.writer.write_files_to_disk(self.pil_imagelist_sharpness,
                                            self.txt_list,
                                            self.mode)
        if self.mode == "rotation":            
            self.writer.write_rotated_files_oneImage(
                self.pil_imagelist_rotation, 
                self.txt_filelist_rotation,
                self.mode)
            
        if self.mode == "translation":            
            self.writer.write_translated_file_oneImage(
                self.pil_imagelist_translation,
                self.txt_filelist_translation,
                self.mode)
            
        if self.mode == "flip":            
            self.writer.write_fliped_files_oneImage(
                self.pil_imagelist_flip, 
                self.txt_filelist_flip,
                self.mode)
            
        if self.mode == "scale":
            # print(len(self.pil_imagelist_scale))
            self.writer.write_scaled_files_oneImage(self.pil_imagelist_scale,
                                                    self.txt_filelist_scale,
                                                    self.mode)
        if self.mode == "noise":
            # print(len(self.pil_imagelist_noise))
            self.writer.write_noised_files_oneImage(self.pil_imagelist_noise,
                                                    self.txt_list,
                                                    self.mode)
            
            
        self.show_filenames_in_listwidget_destinationfolder()    
                    
    def save_all_files(self):
        if self.mode == "brightness":
            self.brightness.change_brightness_allImages(self.txt_list, 
                                                        self.mode, 
                                                        self.writer)
            
        if self.mode == "saturation":
            self.saturation.change_saturation_allImages(self.txt_list, 
                                                        self.mode, 
                                                        self.writer)
              
        if self.mode == "contrast":
            self.contrast.change_contrast_allImages(self.txt_list, 
                                                    self.mode, 
                                                    self.writer)
            
        if self.mode == "sharpness":
            self.sharpness.change_sharpness_allImages(self.txt_list, 
                                                      self.mode, 
                                                      self.writer)
                        
        if self.mode == "rotation":
            self.rotation.change_rotation_allImages(self.txt_list, 
                                                    self.mode, 
                                                    self.writer)
                
        if self.mode == "flip":
            self.flip.flip_allImages(self.txt_list, 
                                     self.mode, 
                                     self.writer)     
            
        if self.mode == "translation":
            self.translation.change_translation_allImages(self.txt_list, 
                                                          self.mode, 
                                                          self.writer)
            
        if self.mode == "scale":
            self.scale.change_scale_allImages(self.txt_list, 
                                              self.mode, 
                                              self.writer)
            
        if self.mode == "noise":
            self.noise.change_noise_allImages(self.txt_list, 
                                              self.mode, 
                                              self.writer)
                
        self.show_filenames_in_listwidget_destinationfolder()
    
    def determine_finished_images(self, number):    
        count_listwidget = len(self.lw_sourcefolder)
        summe = count_listwidget * int(number)
        self.lb_sum_of_images_2.setText(str(summe))

    # def mousePressEvent(self, event):
    #     pos = event.localPos()
    #     # print("event.pos(): " , pos)

    def resizeEvent(self, event):       
        
        if self.mode == "rotation":
            self.show_pil_imagelist_rotation_in_gv()
        else:
            self.show_pil_imagelist_in_gv()
             
        if self.info_text == True:
            self.print_info_text_in_gv()
            
        if self.info2_text == True:
            self.print_info2_text_in_gv()
            
        self.show_filenames_in_listwidget_destinationfolder()
            
        
    def preview_item(self):
        # print("Funktion: preview_item")
        if self.mode == "brightness":
            # self.determine_finished_images()
            self.pil_imagelist_brightness = \
                self.brightness.preview_brightness_oneImage()
            # print("preview_item brightness")
            # time.sleep(1)
            self.show_pil_imagelist_in_gv()
            
        if self.mode == "saturation":
            self.pil_imagelist_saturation = \
                self.saturation.preview_saturation_oneImage()
            self.show_pil_imagelist_in_gv()
            
        if self.mode == "contrast":
            self.pil_imagelist_contrast = \
                self.contrast.preview_contrast_oneImage()
            self.show_pil_imagelist_in_gv()

        if self.mode == "sharpness":
            self.pil_imagelist_sharpness = \
                self.sharpness.preview_sharpness_oneImage()
            self.show_pil_imagelist_in_gv()

        if self.mode == "rotation":
            self.pil_imagelist_rotation, self.txt_filelist_rotation = \
                self.rotation.preview_rotation_oneImage()
            self.show_pil_imagelist_rotation_in_gv()
            
        if self.mode == "flip":
            self.pil_imagelist_flip, self.txt_filelist_flip = \
                self.flip.preview_flip_oneImage()
            # print("mainwindow.preview()_pil:", self.pil_imagelist_flip)
            # print("mainwindow.preview()_txt:", self.txt_filelist_flip)
            self.show_pil_imagelist_in_gv()
            
        # else:
        #     self.lb_console.setText("Mode: " + str(self.mode))












