# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:40:41 2023

@author: Admin
"""
import os
from PyQt5 import QtCore
from PIL import Image, ImageEnhance

class Contrast(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps
        
    def preview_contrast_oneImage(self):
        pil_imagelist_contrast = []
        steps = int(self.le_steps.text())
        factor = round((2 / steps), 1)
        value  = factor
        current_index = self.lw_sourcefolder.currentRow()
        # print(self.lw_sourcefolder)
        # for item in range(0, self.lw_sourcefolder.count()):
        # self.lb_console.setText(str(current_index))
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = self.source_folder_path + "/" + item_name.text()
        # print(item_path)
        pil_image = Image.open(item_path)
        for j in range(steps):
            img_cont = self.change_contrast_oneImage(pil_image, value)
            pil_imagelist_contrast.append([img_cont,
                                           item_name.text(),
                                           value])
            value = round(value + factor, 1)
            
        return pil_imagelist_contrast
            
    def change_contrast_oneImage(self, pil_image, factor):
        img_iec    = ImageEnhance.Contrast(pil_image)
        img_cont = img_iec.enhance(factor)
        return img_cont
    
    def change_contrast_allImages(self):
        pil_imagelist_contrast_allImages = []
        for index in range(len(self.lw_sourcefolder)):
            steps = int(self.le_steps.text())
            factor = round((2 / steps), 1)
            value  = factor
            # print(factor)
            item_name = self.lw_sourcefolder.item(index)
            item_path = self.source_folder_path + "/" + item_name.text()
            pil_image = Image.open(item_path)

            for j in range(steps):
                img_cont = self.change_contrast_oneImage(pil_image, value)
                pil_imagelist_contrast_allImages.append([img_cont,
                                                         item_name.text(),
                                                         value])
                value = round(value + factor, 1)
                
        return pil_imagelist_contrast_allImages
    
    
    
    
    
    
    
    
    
    
    