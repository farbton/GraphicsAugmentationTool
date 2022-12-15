# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:23:50 2022

@author: Kirko
"""
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QGraphicsPixmapItem, QGridLayout, QLabel, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPen
from PIL import Image, ImageEnhance, ImageQt
import reader, writer

destination_folder_path = "destination/"
class Window(QMainWindow):
    
    def __init__(self, app):       
        super(Window, self).__init__()       
        uic.loadUi("AugmentationTool_GUI.ui", self)
        self.setWindowTitle("Augmentation Tool for Images")
        self.screen = app.primaryScreen()
        self.width = self.screen.size().width()/2
        self.height = self.screen.size().height()/2
        self.left = self.screen.size().width()/2 - self.width/2
        self.top  = self.screen.size().height()/2 - self.height/2
        self.setGeometry(self.left, self.top, self.width, self.height)
        print(self.size())
        self.lw_sourcefolder.resize(50,50)
        print(self.lw_sourcefolder.size())
        self.reader = reader.Reader()
        self.writer = writer.Writer(self, destination_folder_path)
        self.scene = QGraphicsScene(self)
        self.pil_imagelist = []
        self.txt_list = []
        self.pil_imagelist_bright = []
        self.steps = 10
        # self.setMouseTracking(True)
        # self.lw_sourcefolder.setMouseTracking(True)
        # self.grid_layout = QGridLayout()
        
        
    def start(self):
        self.pb_sourcefolder.clicked.connect(self.open_sourcefolder)
        self.pb_brightness.clicked.connect(self.preview_brighness)
        self.pb_convert_and_save_all_images.clicked.connect(self.save_all_files)
        self.lw_sourcefolder.itemClicked.connect(self.preview_item)
        
    def open_sourcefolder(self):
        self.source_path = QFileDialog.getExistingDirectory()
        if self.source_path:
            self.list_filenames = self.reader.read_sourcefolder(self.source_path)
            self.write_filenames_in_listwidget()
               
    def write_filenames_in_listwidget(self):
        self.lw_sourcefolder.clear()
        for name in self.list_filenames:
            if name.endswith(('.jpg', '.png')):
                self.lw_sourcefolder.addItem(str(name))
            if name.endswith('.txt'):
                self.txt_list.append(name)
        self.lw_sourcefolder.setCurrentRow(0)
        
    def preview_brighness(self):
        self.pil_imagelist_bright = []
        factor = round((2 / self.steps), 1)
        value  = factor
        current_index = self.lw_sourcefolder.currentRow()
        # print(self.lw_sourcefolder)
        # for item in range(0, self.lw_sourcefolder.count()):
        # self.lb_console.setText(str(current_index))
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = self.source_path + "/" + item_name.text()
        pil_image = Image.open(item_path)
        for j in range(self.steps):
            img_bright = self.change_brighness(pil_image, value)
            self.pil_imagelist_bright.append([img_bright, value])
            value += round(factor,1)
            print(value)
            
        # pixmap_item = QGraphicsPixmapItem(img_pixmap)
        # self.gv_pil_imagelist.append(pil_image)
        # current_index += 1
        self.show_pil_imagelist_bright_in_gv()

    def change_brighness(self, pil_image, factor):
        img_ieb    = ImageEnhance.Brightness(pil_image)
        img_bright = img_ieb.enhance(factor)
        return img_bright
    
    def get_gv_height_and_width(self):
        return  self.gv_preview.width(), self.gv_preview.height()

    def show_pil_imagelist_bright_in_gv(self):
        self.scene.clear()
        print("len(pil_imagelist_bright): " , len(self.pil_imagelist_bright))
        print("len(txt_list): " , len(self.txt_list))
        gv_width, gv_height = self.get_gv_height_and_width()
        
        row = 0
        col = 0
        for i, (image, value) in enumerate(self.pil_imagelist_bright):
            if i % 5 == 0 :
                row += 1
                col  = 0
                
            # print("col: ", col , "row: " , row)
            # pm_height = image.height
            # pm_width  = image.width
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

    def save_all_files(self):
        self.writer.write_files_to_disk(self.pil_imagelist_bright, self.txt_list)

    def mousePressEvent(self, event):
        pos = event.localPos()
        print("event.pos(): " , pos)

    def resizeEvent(self, event):
        self.show_pil_imagelist_bright_in_gv()
        
    def preview_item(self):
        self.preview_brighness()

















