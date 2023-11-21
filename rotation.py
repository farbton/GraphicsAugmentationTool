# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 13:37:43 2023

@author: Admin
"""

import os
import numpy as np
from PyQt5 import QtCore
from PIL import Image

class Rotation(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        # self.le_steps = le_steps
        
    def preview_rotation_oneImage(self):
        pil_imagelist_rotation = []
        txt_filelist_rotation  = []
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = self.source_folder_path + "/" + item_name.text()
        head, tail = os.path.splitext(str(item_name.text()))
        pil_image = Image.open(item_path)
               
        angle = 90
       
        for j in range(3):
            img_rot = self.change_rotation_oneImage(pil_image, angle)
            txt_rot = self.change_txt(head, angle)
            pil_imagelist_rotation.append([img_rot,
                                           item_name.text(),
                                           angle])
            txt_filelist_rotation.append(txt_rot)
            angle += 90
          
        return pil_imagelist_rotation, txt_filelist_rotation
    
    def change_rotation_oneImage(self, pil_image, angle):
        # img_ier    = ImageEnhance.Rotation(pil_image)
        img_rot = pil_image.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        return img_rot
    
    
    def change_rotation_allImages(self):
        pil_imagelist_rotation_allImages = []
        txt_filelist_rotation_all  = []
        
        for index in range(len(self.lw_sourcefolder)):
    
            item_name = self.lw_sourcefolder.item(index)
            item_path = self.source_folder_path + "/" + item_name.text()
            head, tail = os.path.splitext(str(item_name.text()))
            pil_image = Image.open(item_path)
            angle = 90
            
            for j in range(3):
                img_rot = self.change_rotation_oneImage(pil_image, angle)
                txt_rot = self.change_txt(head, angle)
                pil_imagelist_rotation_allImages.append([img_rot,
                                                          item_name.text(),
                                                          angle])
                txt_filelist_rotation_all.append(txt_rot)
                angle += 90
                
        return pil_imagelist_rotation_allImages, txt_filelist_rotation_all
    
    def change_txt(self, head, angle):        
            bbox_list = self.get_bbox_list(head)
            bbox_list_rotate = self.rotate_bbox_list(bbox_list, angle)
            return bbox_list_rotate
        
        
    def get_bbox_list(self,head):
      bbox_list = []
      with open(self.source_folder_path + "/" + head + ".txt", "r") as txt_file:
          bbox_list = txt_file.readlines()
      return bbox_list   
        
    def rotate_bbox_list(self,bbox_list, angle):
        bbox_list_rotate = []
        for bbox in bbox_list:
            bbox_rotate = self.calculate_points(bbox, angle)
            bbox_list_rotate.append(bbox_rotate)
            bbox_list_rotate.append('\n')
        return bbox_list_rotate
        
    def calculate_points(self, bbox, angle):
        classname, x_center, y_center, width, height = bbox.split()
        v = np.array([float(x_center),float(y_center)])
        m = self.rotation_matrix(angle)
        coordinate = m @ v.T
        x_pixel, y_pixel, width_new, height_new = self.set_corr_img_pixel(coordinate, width, height, angle)
        bbox_rotate = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), float(x_pixel), float(y_pixel), float(width_new), float(height_new))       
        bbox_rotate = bbox_rotate.replace(',', '')
        return bbox_rotate   
    
    def set_corr_img_pixel(self, coordinates, width, height, angle):
        x, y = coordinates
        def set_pix_90():
            return x, y + 1, height, width
        def set_pix_180():
            return x + 1, y + 1, width, height
        def set_pix_270():
            return x + 1, y, height, width

        switch = {
            90:  set_pix_90(),
            180: set_pix_180(),
            270: set_pix_270(),                      
        }
        return switch.get(int(angle), "error in set_coor_img_pixel()")
    
    def rotation_matrix(self, angle):
        def rotationmatrix_90():
            return np.array(((0,1),
                             (-1,0)))
       
        def rotationmatrix_180():
            return np.array(((-1,0),
                             (0,-1)))
       
        def rotationmatrix_270():
            return np.array(((0,-1),
                             (1,0)))
       
        switch = {
            90:  rotationmatrix_90(),
            180: rotationmatrix_180(),
            270: rotationmatrix_270(),                      
        }
        return switch.get(int(angle), "error in rotation_matrix()")   
        
        
        
        
        
        
        
        
        
        
        
        