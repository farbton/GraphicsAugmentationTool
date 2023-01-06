# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:23:50 2022

@author: Kirko
"""
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QGraphicsPixmapItem, QGridLayout, QLabel, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QPen, QFont
from PIL import Image, ImageEnhance, ImageQt
import reader, writer, brightness, saturation, contrast, sharpness, rotation
import os


class Window(QMainWindow):
    
    def __init__(self, app):       
        super(Window, self).__init__()       
        uic.loadUi("AugmentationTool_GUI.ui", self)
        self.source_folder_path = "source/"
        self.destination_folder_path = "destination/"
        self.setWindowTitle("Augmentation Tool for Images")
        self.screen = app.primaryScreen()
        self.width  = self.screen.size().width()/2
        self.height = self.screen.size().height()/2
        self.left   = self.screen.size().width()/2 - self.width/2
        self.top    = self.screen.size().height()/2 - self.height/2
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.lw_sourcefolder.resize(50,50)
        self.reader = reader.Reader()       
        self.scene = QGraphicsScene(self)
        self.info_text  = True
        self.info2_text = False
        self.pil_imagelist = []
        self.txt_list = []
        self.pil_imagelist_brightness = []
        self.pil_imagelist_brightness_allImages = []
        self.mode = None
        self.init_source_path()
        self.print_destinationfolder_path()
        
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
        self.pb_blur.clicked.connect(self.sharpness)
        self.pb_rotation.clicked.connect(self.rotation)
     
    def init_source_path(self):
        self.source_folder_path = os.getcwd() + "/" + self.source_folder_path
        self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
        self.list_filenames = self.reader.read_sourcefolder(self.source_folder_path)
        self.show_filenames_in_listwidget_sourcefolder()
        # self.print_info2_text_in_gv()
        self.print_sourcefolder_path()
        
     
    def open_sourcefolder(self):
        self.source_folder_path = QFileDialog.getExistingDirectory()
        if self.source_folder_path:
            self.info_text  = False
            self.info2_text = True
            self.writer = writer.Writer(self, self.source_folder_path, self.destination_folder_path)
            self.list_filenames = self.reader.read_sourcefolder(self.source_folder_path)
            self.show_filenames_in_listwidget_sourcefolder()
            self.print_info2_text_in_gv()
            self.print_sourcefolder_path()
     
    def print_sourcefolder_path(self):
        self.lb_sourcefolder_path.setText(self.source_folder_path[:10] + "..." + self.source_folder_path[-30:])
     
    def print_destinationfolder_path(self):
        self.lb_destinationfolder_path.setText("..." + self.destination_folder_path[-30:])
        
    def open_destinationfolder(self):
        self.destination_folder_path = QFileDialog.getExistingDirectory()
        if self.destination_folder_path:
            print(self.destination_folder_path)
               
    def show_filenames_in_listwidget_sourcefolder(self):
        self.lw_sourcefolder.clear()
        for name in self.list_filenames:
            if name.endswith(('.jpg', '.png')):
                self.lw_sourcefolder.addItem(str(name))
            if name.endswith('.txt'):
                self.txt_list.append(name)
        self.lw_sourcefolder.setCurrentRow(0)
        self.determine_finished_images()
           
    def get_gv_height_and_width(self):
        return  self.gv_preview.width(), self.gv_preview.height()

    def show_pil_imagelist_in_gv(self):
        self.scene.clear()
        gv_width, gv_height = self.get_gv_height_and_width()
        imagelist = []
        
        if self.mode == "brightness":
            imagelist = self.pil_imagelist_brightness
        if self.mode == "saturation":
            imagelist = self.pil_imagelist_saturation
        if self.mode == "contrast":
            imagelist = self.pil_imagelist_contrast
        if self.mode == "sharpness":
            imagelist = self.pil_imagelist_sharpness
        if self.mode == "rotation":
            imagelist = self.pil_imagelist_rotation
            
        row = 0
        col = 0
        for i, (image, name, value) in enumerate(imagelist):
            if i % 5 == 0 :
                row += 1
                col  = 0
                
            pm_width_new = (gv_width - 50)//5  # 50 = offset Zwischenraum zwischen den Bildern
            images_per_col = gv_height / (pm_width_new / (16/9))
            pm_height_new = gv_height / images_per_col
            qimage = ImageQt.ImageQt(image)
            pixmap = QPixmap.fromImage(qimage)
            pixmap_item = self.scene.addPixmap(pixmap.scaled(pm_width_new, pm_height_new ))
            pixmap_item.setPos(col*(pm_width_new+10),row * (pm_height_new + 10))
            pixmap_item.setFlag(QGraphicsItem.ItemIsMovable)
            self.gv_preview.setScene(self.scene)
            col += 1

    def brightness(self):
        self.mode = "brightness"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.brightness = brightness.Brightness(self.lw_sourcefolder,
                                                self.source_folder_path, 
                                                self.le_steps)
        
        self.pil_imagelist_brightness = self.brightness.preview_brightness_oneImage()
        self.show_pil_imagelist_in_gv()
        
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
        
    def rotation(self):
        self.mode = "rotation"
        self.info_text = False
        self.info2_text = False
        self.print_mode_in_console()
        self.rotation = rotation.Rotation(self.lw_sourcefolder,
                                             self.source_folder_path)
        
        self.pil_imagelist_rotation = self.rotation.preview_rotation_oneImage()
        self.show_pil_imagelist_in_gv()

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
                    
    def save_all_files(self):
        if self.mode == "brightness":
            self.pil_imagelist_brightness_allImages = self.brightness.change_brightness_allImages()
            self.writer.write_files_to_disk(self.pil_imagelist_brightness_allImages,
                                            self.txt_list,
                                            self.mode)
        if self.mode == "saturation":
            self.pil_imagelist_saturation_allImages = self.saturation.change_saturation_allImages()
            self.writer.write_files_to_disk(self.pil_imagelist_saturation_allImages,
                                            self.txt_list,
                                            self.mode)   
        if self.mode == "contrast":
            self.pil_imagelist_contrast_allImages = self.contrast.change_contrast_allImages()
            self.writer.write_files_to_disk(self.pil_imagelist_contrast_allImages,
                                            self.txt_list,
                                            self.mode)
        if self.mode == "sharpness":
            self.pil_imagelist_sharpness_allImages = self.sharpness.change_sharpness_allImages()
            self.writer.write_files_to_disk(self.pil_imagelist_sharpness_allImages,
                                            self.txt_list,
                                            self.mode)
    
    def determine_finished_images(self):    
        count_listwidget = len(self.lw_sourcefolder)
        summe = count_listwidget * int(self.le_steps.text())
        self.lb_sum_of_images_2.setText(str(summe))

    def mousePressEvent(self, event):
        pos = event.localPos()
        print("event.pos(): " , pos)

    def resizeEvent(self, event):       
        
        self.show_pil_imagelist_in_gv()
        
        if self.info_text == True:
            self.print_info_text_in_gv()
            
        if self.info2_text == True:
            self.print_info2_text_in_gv()
            
        
    def preview_item(self):
        if self.mode == "brightness":
            self.pil_imagelist_brightness =  self.brightness.preview_brightness_oneImage()
            self.show_pil_imagelist_in_gv()
            
        if self.mode == "saturation":
            self.pil_imagelist_saturation = self.saturation.preview_saturation_oneImage()
            self.show_pil_imagelist_in_gv()
            
        if self.mode == "contrast":
            self.pil_imagelist_contrast = self.contrast.preview_contrast_oneImage()
            self.show_pil_imagelist_in_gv()

        if self.mode == "sharpness":
            self.pil_imagelist_sharpness = self.sharpness.preview_sharpness_oneImage()
            self.show_pil_imagelist_in_gv()

        if self.mode == "rotation":
            self.pil_imagelist_rotation = self.rotation.preview_rotation_oneImage()
            self.show_pil_imagelist_in_gv()












