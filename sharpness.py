# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:56:09 2023

@author: Admin
"""

import os
from PyQt5 import QtCore
from PIL import Image, ImageEnhance

class Sharpness(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps
        
    def preview_sharpness_oneImage(self):
        pil_imagelist_sharpness = []
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
            img_sharp = self.change_sharpness_oneImage(pil_image, value)
            pil_imagelist_sharpness.append([img_sharp,
                                            item_name.text(),
                                            value])
            value = round(value + factor, 1)
          
        return pil_imagelist_sharpness
            
    def change_sharpness_oneImage(self, pil_image, factor):
        img_ies    = ImageEnhance.Sharpness(pil_image)
        img_sharp = img_ies.enhance(factor)
        return img_sharp
    
    def change_sharpness_allImages(self):
        pil_imagelist_sharpness_allImages = []
        for index in range(len(self.lw_sourcefolder)):
            steps = int(self.le_steps.text())
            factor = round((2 / steps), 1)
            value  = factor
            # print(factor)
            item_name = self.lw_sourcefolder.item(index)
            item_path = self.source_folder_path + "/" + item_name.text()
            pil_image = Image.open(item_path)

            for j in range(steps):
                img_sharp = self.change_sharpness_oneImage(pil_image, value)
                pil_imagelist_sharpness_allImages.append([img_sharp,
                                                          item_name.text(),
                                                          value])
                value = round(value + factor, 1)
                
        return pil_imagelist_sharpness_allImages
    
    
    
    
    