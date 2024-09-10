# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:56:18 2023

@author: Kirko
"""

import os
from PyQt5 import QtCore
from PIL import Image, ImageEnhance


class Brightness(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps

        
    def preview_brightness_oneImage(self):
        pil_imagelist_brightness = []
        steps = int(self.le_steps.text())
        factor = round((2 / steps), 2)
        value  = factor
        current_index = self.lw_sourcefolder.currentRow()
        # print(self.lw_sourcefolder)
        # for item in range(0, self.lw_sourcefolder.count()):
        # self.lb_console.setText(str(current_index))
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        pil_image = Image.open(item_path, mode='r')
        for j in range(steps):
            img_bright = self.change_brightness_oneImage(pil_image, value)
            pil_imagelist_brightness.append([img_bright,
                                             item_name.text(),
                                             value,
                                             None]) # None = Placeholder for Counter
            value = round(value + factor, 2)
            
        return pil_imagelist_brightness
            
    def change_brightness_oneImage(self, pil_image, factor):
        img_ieb    = ImageEnhance.Brightness(pil_image)
        img_bright = img_ieb.enhance(factor)
        return img_bright
    
    def change_brightness_allImages(self, txt_list, mode, writer):
        pil_imagelist_brightness_allImages = []
        for index in range(len(self.lw_sourcefolder)):
            steps = int(self.le_steps.text())
            factor = round((2 / steps), 2)
            value  = factor
            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())

            with Image.open(item_path, mode='r') as pil_image:

                for j in range(steps):
                    img_bright = self.change_brightness_oneImage(pil_image, value)
                    pil_imagelist_brightness_allImages.append([img_bright,
                                                               item_name.text(),
                                                               value,
                                                               None]) # None = Placeholder for Counter
                    value = round(value + factor, 2)
                    writer.write_files_to_disk(pil_imagelist_brightness_allImages,
                                               txt_list,
                                               mode)
                    pil_imagelist_brightness_allImages.pop()
    
    
    
  