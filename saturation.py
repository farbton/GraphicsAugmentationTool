# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 09:44:06 2023

@author: Admin
"""

import os
from PyQt5 import QtCore
from PIL import Image, ImageEnhance


class Saturation(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps
        
    def preview_saturation_oneImage(self):
        pil_imagelist_saturation = []
        steps = int(self.le_steps.text())
        factor = round((2 / steps), 1)
        value  = factor
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = self.source_folder_path + "/" + item_name.text()
        pil_image = Image.open(item_path)
        # print("test")
        for j in range(steps):
            img_sat = self.change_saturation_oneImage(pil_image, value)
            pil_imagelist_saturation.append([img_sat,
                                             item_name.text(),
                                             value])
            value = round(value + factor, 1)

        return pil_imagelist_saturation
        
        
    def change_saturation_oneImage(self, pil_image, value):
         img_iec    = ImageEnhance.Color(pil_image)
         img_sat    = img_iec.enhance(value)
         return img_sat
     
    def change_saturation_allImages(self):
        pil_imagelist_saturation_allImages = []
        for index in range(len(self.lw_sourcefolder)):
            steps = int(self.le_steps.text())
            factor = round((2 / steps), 1)
            value  = factor
            # print(factor)
            item_name = self.lw_sourcefolder.item(index)
            item_path = self.source_folder_path + "/" + item_name.text()
            pil_image = Image.open(item_path)

            for j in range(steps):
                img_sat = self.change_saturation_oneImage(pil_image, value)
                pil_imagelist_saturation_allImages.append([img_sat,
                                                           item_name.text(),
                                                           value])
                value = round(value + factor, 1)
                
        return pil_imagelist_saturation_allImages
    
    
    
    
    
    
    
    