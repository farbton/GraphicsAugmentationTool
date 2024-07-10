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
        factor = round((2 / steps), 2)
        value  = factor
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        pil_image = Image.open(item_path)
        for j in range(steps):
            img_sharp = self.change_sharpness_oneImage(pil_image, value)
            pil_imagelist_sharpness.append([img_sharp,
                                            item_name.text(),
                                            value])
            value = round(value + factor, 2)
          
        return pil_imagelist_sharpness
            
    def change_sharpness_oneImage(self, pil_image, factor):
        img_ies    = ImageEnhance.Sharpness(pil_image)
        img_sharp = img_ies.enhance(factor)
        return img_sharp
    
    def change_sharpness_allImages(self, txt_list, mode, writer):
        pil_imagelist_sharpness_allImages = []
        for index in range(len(self.lw_sourcefolder)):
            steps = int(self.le_steps.text())
            factor = round((2 / steps), 2)
            value  = factor
            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())
            
            with Image.open(item_path, mode='r') as pil_image:

                for j in range(steps):
                    img_sharp = self.change_sharpness_oneImage(pil_image, value)
                    pil_imagelist_sharpness_allImages.append([img_sharp,
                                                              item_name.text(),
                                                              value])
                    value = round(value + factor, 2)
                    writer.write_files_to_disk(pil_imagelist_sharpness_allImages,
                                               txt_list,
                                               mode)
                    pil_imagelist_sharpness_allImages.pop()
    
    
    
    
    
    
    
    
    