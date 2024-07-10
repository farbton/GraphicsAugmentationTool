# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:23:50 2022

@author: Kirko
"""
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog,\
    QGraphicsPixmapItem, QGridLayout, QLabel, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QPen, QFont, QImage
from PIL import Image, ImageEnhance , ImageQt, ImageShow
import reader, writer, brightness, saturation, contrast, sharpness,\
    rotation, flip, translation, scale
import os, numpy as np
import time
import io
testwert = 0

class Window(QMainWindow):
    
    def __init__(self, app):       
        super(Window, self).__init__()       
        uic.loadUi("AugmentationTool_GUI_test.ui", self)
        self.source_folder_path = "source/"
        self.destination_folder_path = "destination/"
        self.setWindowTitle("Augmentation Tool for Images")
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
        
    def print_info_text_in_gv(self):
        self.scene.addText("Drücken Sie den Button <Sourcefolder> um das Quellverzeichnis auszuwählen \n \
                            oder drücken Sie einen Button zur Bildmanipulation",
                            font=QFont("Times", 14))
        # size = self.gv_preview.size()
        # print(size.height())
        
        # text_item = QGraphicsTextItem("HHHHHHHHHHHHHHH")
        # self.scene.addItem(text_item)
        self.gv_preview.setScene(self.scene)
        # self.gv_preview.centerOn(text_item)
        
    def print_info2_text_in_gv(self):
        self.scene.clear()
        self.scene.addText("Wählen Sie jetzt ein Button für die Bildmanipulation aus", 
                           font=QFont("Times", 14))
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
        self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
        self.list_filenames = self.reader.read_sourcefolder(self.source_folder_path)
        self.show_filenames_in_listwidget_sourcefolder()
        # self.print_info2_text_in_gv()
        self.print_sourcefolder_path()
        self.print_imagecounter()
        
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
            self.list_filenames = self.reader.read_sourcefolder(self.source_folder_path)
            self.show_filenames_in_listwidget_sourcefolder()
            self.print_info2_text_in_gv()
            self.print_sourcefolder_path()
            self.print_imagecounter()
     
    def print_sourcefolder_path(self):
        self.lb_sourcefolder_path.setText(self.source_folder_path[:10] + "..." + self.source_folder_path[-30:])
     
    def print_destinationfolder_path(self):
        self.lb_destinationfolder_path.setText("..." + self.destination_folder_path[-30:])
        
    def open_destinationfolder(self):
        self.destination_folder_path = QFileDialog.getExistingDirectory()
        if self.destination_folder_path:
            self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
            self.print_destinationfolder_path()
            #print(self.destination_folder_path)
               
    def show_filenames_in_listwidget_sourcefolder(self):
        self.lw_sourcefolder.clear()
        for name in self.list_filenames:
            if name.endswith(('.jpg', '.png')):
                self.lw_sourcefolder.addItem(str(name))
            if name.endswith('.txt'):
                self.txt_list.append(name)
        self.lw_sourcefolder.setCurrentRow(0)
        self.determine_finished_images()
        
    def show_filenames_in_listwidget_destinationfolder(self):
        # self.destination_folder_path = os.getcwd() + "/" + self.destination_folder_path
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
            
            
        row = 0
        col = 0
        # print("mainwindow.show_pil...()",imagelist)
        for i, (image, ___ , ___) in enumerate(imagelist):
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
        
        pics_per_row = gv_width // 300
        
        
        
        for i, (image, ___, ___) in enumerate(imagelist):
            
            aspect_ratio = image.width / image.height
            # print("aspect_ratio: ", aspect_ratio)
            
            if image.mode == "RGB":
                imageformat = QImage.Format_RGB888
            if image.mode == "RGBA":
                imageformat = QImage.Format_RGBA8888
            if image.mode == "L":
                imageformat = QImage.Format_Grayscale8
                
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
     
            pixmap = QPixmap.fromImage(qimage)  
            
            if pm_width_new <= pm_height_new:
                pixmap_item = self.scene.addPixmap(pixmap.scaled(int(300 * aspect_ratio), 300))
            else:     
                pixmap_item = self.scene.addPixmap(pixmap.scaled(300, int(300 / aspect_ratio)))
                
            
            pixmap_item.setPos(col*(300 + 10),row * (300 + 10))
            self.gv_preview.setScene(self.scene)
            col += 1                               

    def brightness(self):
        # print("funktion: brightness")
        self.mode = "brightness"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.brightness = brightness.Brightness(self.lw_sourcefolder,
                                                self.source_folder_path, 
                                                self.le_steps)
        
        self.pil_imagelist_brightness = self.brightness.preview_brightness_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()
        
        
    def saturation(self):
        self.mode = "saturation"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.saturation = saturation.Saturation(self.lw_sourcefolder,
                                                self.source_folder_path,
                                                self.le_steps)
        
        self.pil_imagelist_saturation = self.saturation.preview_saturation_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()
        

    def contrast(self):
        self.mode = "contrast"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.contrast = contrast.Contrast(self.lw_sourcefolder,
                                          self.source_folder_path,
                                          self.le_steps)
        
        self.pil_imagelist_contrast = self.contrast.preview_contrast_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()
        

    def sharpness(self):
        self.mode = "sharpness"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.sharpness = sharpness.Sharpness(self.lw_sourcefolder,
                                             self.source_folder_path,
                                             self.le_steps)
        
        self.pil_imagelist_sharpness = self.sharpness.preview_sharpness_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()
        
        
    def rotation(self):
        self.mode = "rotation"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.rotation = rotation.Rotation(self.lw_sourcefolder,
                                          self.source_folder_path,
                                          self.le_steps)
        
        self.pil_imagelist_rotation, self.txt_filelist_rotation = \
            self.rotation.preview_rotation_oneImage()
        self.show_pil_imagelist_rotation_in_gv()
        self.determine_finished_images()
        
    def translation(self):
        self.mode = "translation"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.translation = translation.Translation(self.lw_sourcefolder,
                                                   self.source_folder_path,
                                                   self.le_steps)
        
        self.pil_imagelist_translation, self.txt_filelist_translation =\
            self.translation.preview_translation_oneImage()        
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()
        
        
        
    def flip(self):
        self.mode = "flip"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.flip = flip.Flip(self.lw_sourcefolder, self.source_folder_path)
        self.pil_imagelist_flip, self.txt_filelist_flip =\
            self.flip.preview_flip_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()
        
    def noise(self):
        self.mode = "noise"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()   
        
        
    def scale(self):
        self.mode = "scale"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.scale = scale.Scale(self.lw_sourcefolder, 
                                 self.source_folder_path,
                                 self.le_steps)
        self.pil_imagelist_scale, self.txt_filelist_scale =\
            self.scale.preview_scale_oneImage()
        self.show_pil_imagelist_in_gv()
        self.determine_finished_images()

    def print_mode_in_console(self):
        self.lb_console.setText("Mode: " + str(self.mode))
                
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
            self.writer.write_scaled_files_oneImage(self.pil_imagelist_scale,
                                                    self.txt_filelist_scale,
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
                
        self.show_filenames_in_listwidget_destinationfolder()
    
    def determine_finished_images(self):    
        count_listwidget = len(self.lw_sourcefolder)
        summe = count_listwidget * int(self.le_steps.text())
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
            self.determine_finished_images()
            self.pil_imagelist_brightness = \
                self.brightness.preview_brightness_oneImage()
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
            
        else:
            self.lb_console.setText("Mode: " + str(self.mode))












