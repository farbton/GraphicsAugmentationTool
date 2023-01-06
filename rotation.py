# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 13:37:43 2023

@author: Admin
"""

import os
from PyQt5 import QtCore
from PIL import Image, ImageEnhance

class Rotation(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        # self.le_steps = le_steps
        
    def preview_rotation_oneImage(self):
        pil_imagelist_rotation = []
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = self.source_folder_path + "/" + item_name.text()
        pil_image = Image.open(item_path)
        
        angle = 30
        
        
        for j in range(4):
            img_rot = self.change_rotation_oneImage(pil_image, angle)
            pil_imagelist_rotation.append([img_rot,
                                           item_name.text(),
                                           angle])
            # value = round(value + factor, 1)
          
        return pil_imagelist_rotation
    
    def change_rotation_oneImage(self, pil_image, angle):
        # img_ier    = ImageEnhance.Rotation(pil_image)
        img_rot = pil_image.rotate(angle, resample=Image.Resampling.BICUBIC)
        return img_rot