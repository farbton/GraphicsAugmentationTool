# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:56:18 2023

@author: Kirko
"""

import os, io
from PyQt5 import QtCore
from PIL import Image, ImageEnhance
import skimage as ski
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel 
from PyQt5.QtCore import QBuffer
# from wand.image import Image
import qimage2ndarray

class Noise(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, comboBox_noise):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        # self.le_steps = le_steps
        self.comboBox_noise = comboBox_noise
        print(self.comboBox_noise.currentText())
        
    def preview_noise_oneImage(self):
        ski_imagelist_noise = []
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        pil_image = Image.open(item_path, mode='r')
        img_noise = self.change_noise_oneImage(pil_image)
        ski_imagelist_noise.append([img_noise,
                                    item_name.text(),
                                    self.comboBox_noise.currentText(),
                                    None]) #Placeholder for Counter

        return ski_imagelist_noise
            
    def change_noise_oneImage(self, pil_image):
       
        array = np.asarray(pil_image)
        array_noise = ski.util.random_noise(array, mode = self.comboBox_noise.currentText())       
        qimage = qimage2ndarray.array2qimage(array_noise, normalize=True)      
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        qimage.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        
        return pil_im
        

    def change_noise_allImages(self, txt_list, mode, writer):
        pil_imagelist_noise_allImages = []
        for index in range(len(self.lw_sourcefolder)):

            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())
            
            with Image.open(item_path, mode='r') as pil_image:
                img_noise = self.change_noise_oneImage(pil_image)
                pil_imagelist_noise_allImages.append([img_noise,
                                                      item_name.text(),
                                                      self.comboBox_noise.currentText(),
                                                      None]) # None = Placeholder for Counter
                writer.write_noised_files_oneImage(pil_imagelist_noise_allImages,
                                           txt_list,
                                           mode)
                pil_imagelist_noise_allImages.pop()