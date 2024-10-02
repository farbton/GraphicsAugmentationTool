# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:56:09 2023

@author: Kirko
"""

import os
import numpy as np
from PyQt5 import QtCore
from PIL import Image, ImageOps

class Flip(QtCore.QObject):
    def __init__(self, main_window, lw_sourcefolder, source_folder_path):
        QtCore.QObject.__init__(self)
        self.main_window = main_window
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path

        
    def preview_flip_oneImage(self):
        pil_imagelist_flip = []
        txt_filelist_flip  = []
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        head, tail = os.path.splitext(str(item_name.text()))
        pil_image = Image.open(item_path, mode='r')
        
        img_flip = self.flip_oneImage(pil_image)
        txt_flip = self.change_txt(head, "flip")
        pil_imagelist_flip.append([img_flip, item_name.text(), "fl", None]) # None = Placeholder for Counter
        txt_filelist_flip.append(txt_flip)
        
        img_mirror = self.mirror_oneImage(pil_image)
        txt_mirror = self.change_txt(head, "mirror")       
        pil_imagelist_flip.append([img_mirror, item_name.text(), "mi", None]) # None = Placeholder for Counter
        txt_filelist_flip.append(txt_mirror)
       
        return pil_imagelist_flip, txt_filelist_flip
            
    def flip_oneImage(self, pil_image):
        # print("flip_one_image")
        img_flip = ImageOps.flip(pil_image)
        return img_flip
    
    def mirror_oneImage(self, pil_image):
        # print("mirror_one_image")
        img_mir = ImageOps.mirror(pil_image) 
        return img_mir
    
    def change_txt(self, head, string):   
        # print("change_txt...")
        bbox_list = self.get_bbox_list(head)
        bbox_list_flip = self.flip_bbox_list(bbox_list, string)
        return bbox_list_flip
        
    def get_bbox_list(self,head):
      bbox_list = []
      with open(self.source_folder_path + "/" + head + ".txt", "r") as txt_file:
          bbox_list = txt_file.readlines()
      return bbox_list
  
    def flip_bbox_list(self,bbox_list, string):
        # print("flip_bbox_list")
        bbox_list_flip = []
        for bbox in bbox_list:
            bbox_flip = self.calculate_points(bbox, string)
            bbox_list_flip.append(bbox_flip)
            bbox_list_flip.append('\n')
        return bbox_list_flip
    
    def calculate_points(self, bbox, string):
        classname, x_center, y_center, width, height = bbox.split()
        # v = np.array([float(x_center),float(y_center)])
        
        if string == "flip":
            # print("calculate_point_flip")
            # print("y-alt: ", y_center)
            y_center = 1-float(y_center)
            # print("y-neu: ", y_center)
            bbox_flip = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname),\
                                                          float(x_center),\
                                                          float(y_center),\
                                                          float(width),\
                                                          float(height))       
            bbox_flip_mirror = bbox_flip.replace(',', '')
        
        if string == "mirror":
            # print("calculate_point_mirror")
            x_center = 1-float(x_center)
            bbox_mirror = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname),\
                                                             float(x_center),\
                                                             float(y_center),\
                                                             float(width),\
                                                             float(height))
            bbox_flip_mirror = bbox_mirror.replace(',', '')
            
            
        return bbox_flip_mirror
    
    def flip_allImages(self, txt_list, mode, writer):
        pil_imagelist_flip_mirror_allImages = []
        txt_filelist_flip_mirror_allImages  = []
        self.main_window.progressBar.reset()
        self.main_window.progressBar.setRange(0, len(self.lw_sourcefolder))
        
        for index in range(len(self.lw_sourcefolder)):
            # print(index)
            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())
            head, tail = os.path.splitext(str(item_name.text()))  
            self.main_window.progressBar.setValue(index+1)
            
            with Image.open(item_path, mode='r') as pil_image:

                img_flip = self.flip_oneImage(pil_image)
                pil_imagelist_flip_mirror_allImages.append([img_flip,\
                                                            item_name.text(),\
                                                                "fl", None]) # None = Placeholder for Counter
                txt_flip = self.change_txt(head, "flip")
                txt_filelist_flip_mirror_allImages.append(txt_flip)
 
                img_mirror = self.mirror_oneImage(pil_image)
                pil_imagelist_flip_mirror_allImages.append([img_mirror,\
                                                            item_name.text(),\
                                                                "mi", None]) # None = Placeholder for Counter
                txt_mirror = self.change_txt(head, "mirror") 
                txt_filelist_flip_mirror_allImages.append(txt_mirror)
                    
                writer.write_fliped_files_allImages(pil_imagelist_flip_mirror_allImages,
                                           txt_filelist_flip_mirror_allImages,
                                           mode)
                
                pil_imagelist_flip_mirror_allImages.pop()
                txt_filelist_flip_mirror_allImages.pop()
                pil_imagelist_flip_mirror_allImages.pop()
                txt_filelist_flip_mirror_allImages.pop()
    
    
    
    
    