# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:56:09 2023

@author: Admin
"""

import os
import numpy as np
from PyQt5 import QtCore
from PIL import Image, ImageOps

class Flip(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path

        
    def preview_flip_oneImage(self):
        pil_imagelist_flip = []
        txt_filelist_flip  = []
        current_index = self.lw_sourcefolder.currentRow()
        # print(self.lw_sourcefolder)
        # for item in range(0, self.lw_sourcefolder.count()):
        # self.lb_console.setText(str(current_index))
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = self.source_folder_path + "/" + item_name.text()
        head, tail = os.path.splitext(str(item_name.text()))
        pil_image = Image.open(item_path)
        
        img_flip = self.flip_oneImage(pil_image)
        txt_flip = self.change_txt(head, "flip")
        pil_imagelist_flip.append([img_flip, item_name.text(), "flip"])
        txt_filelist_flip.append(txt_flip)
        
        img_mirror = self.mirror_oneImage(pil_image)
        txt_mirror = self.change_txt(head, "mirror")       
        pil_imagelist_flip.append([img_mirror, item_name.text(), "mirror"])
        txt_filelist_flip.append(txt_mirror)
        
        # print("flip.preview_pil",pil_imagelist_flip) 
        # print("flip.preview_txt",txt_filelist_flip) 
        
        return pil_imagelist_flip, txt_filelist_flip
            
    def flip_oneImage(self, pil_image):
        img_flip = ImageOps.flip(pil_image)
        return img_flip
    
    def mirror_oneImage(self, pil_image):
        img_mir = ImageOps.mirror(pil_image) 
        return img_mir
    
    def change_txt(self, head, string):        
            bbox_list = self.get_bbox_list(head)
            bbox_list_flip = self.flip_bbox_list(bbox_list, string)
            return bbox_list_flip
        
    def get_bbox_list(self,head):
      bbox_list = []
      with open(self.source_folder_path + "/" + head + ".txt", "r") as txt_file:
          bbox_list = txt_file.readlines()
      return bbox_list
  
    def flip_bbox_list(self,bbox_list, string):
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
            y_center = 1-float(y_center)
            bbox_flip = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname),\
                                                          float(x_center),\
                                                          float(y_center),\
                                                          float(width),\
                                                          float(height))       
            bbox_flip_mirror = bbox_flip.replace(',', '')
        
        if string == "mirror":
            x_center = 1-float(x_center)
            bbox_mirror = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname),\
                                                             float(x_center),\
                                                             float(y_center),\
                                                             float(width),\
                                                             float(height))
            bbox_flip_mirror = bbox_mirror.replace(',', '')
            
            
        return bbox_flip_mirror
    
    def flip_allImages(self):
        pil_imagelist_flip_mirror_allImages = []
        txt_filelist_flip_mirror_allImages  = []
        
        for index in range(len(self.lw_sourcefolder)):
            
            item_name = self.lw_sourcefolder.item(index)
            item_path = self.source_folder_path + "/" + item_name.text()
            pil_image = Image.open(item_path)

            img_flip = self.flip_oneImage(pil_image)
            img_mirror = self.mirror_oneImage(pil_image)
            pil_imagelist_flip_mirror_allImages.append([img_flip,\
                                                        item_name.text(),\
                                                            "fl"])
            pil_imagelist_flip_mirror_allImages.append([img_mirror,\
                                                        item_name.text(),\
                                                            "mi"])
            
            
            

            item_name = self.lw_sourcefolder.item(index)
            item_path = self.source_folder_path + "/" + item_name.text()
            head, tail = os.path.splitext(str(item_name.text()))            
            txt_flip = self.change_txt(head, "flip")
            txt_filelist_flip_mirror_allImages.append(txt_flip)
            txt_mirror = self.change_txt(head, "mirror") 
            txt_filelist_flip_mirror_allImages.append(txt_mirror)
                
        return pil_imagelist_flip_mirror_allImages,\
               txt_filelist_flip_mirror_allImages
    
    
    
    
    