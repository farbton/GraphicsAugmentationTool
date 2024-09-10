# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 11:05:59 2024

@author: Admin
"""

import os
import numpy as np
from PyQt5 import QtCore
from PIL import Image, ImageChops
import time

class Translation(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps
        
    def preview_translation_oneImage(self):
        pil_imagelist_translation = []
        txt_filelist_translation  = []
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        head, tail = os.path.splitext(str(item_name.text()))
        pil_image = Image.open(item_path)
        offset = int(self.le_steps.text())
        value  = offset
        steps  = round(pil_image.size[0] // offset)

        for j in range(steps):
        
            img_translate = self.change_translation_oneImage(pil_image, offset)
            txt_translate = self.change_txt(head, 
                                            offset,  
                                            img_translate.size)
            
            pil_imagelist_translation.append([img_translate,
                                              item_name.text(),
                                              offset,
                                              None]) # None = Placeholder for Counter
             
            txt_filelist_translation.append(txt_translate)
            
            offset = offset + value

        return pil_imagelist_translation, txt_filelist_translation
    
    def change_translation_allImages(self, txt_list, mode, writer):
        pil_imagelist_translation_allImages = []
        txt_filelist_translation_all  = []

        for index in range(len(self.lw_sourcefolder)):
            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())
            head, tail = os.path.splitext(str(item_name.text()))
            offset       = int(self.le_steps.text())
            value  = offset
            
            with Image.open(item_path, mode='r') as pil_image:
                
                steps  = pil_image.size[0] // offset
                counter = 0 
                for j in range(steps):
                    img_translation = self.change_translation_oneImage(
                        pil_image, 
                        offset)
                    txt_translation = self.change_txt(head, 
                                                      offset, 
                                                      pil_image.size)
                    
                    pil_imagelist_translation_allImages.append([img_translation,
                                                              item_name.text(),
                                                              offset,
                                                              None]) # None = Placeholder for Counter

                    txt_filelist_translation_all.append(txt_translation)
                    offset += value
                    counter += 1
                    
                writer.write_translated_files_allImages(
                    pil_imagelist_translation_allImages,
                    txt_filelist_translation_all,
                    mode)
                
                del pil_imagelist_translation_allImages[-counter:]
                del txt_filelist_translation_all[-counter:]
    
    def change_translation_oneImage(self, pil_image, offset):
        img_trans = ImageChops.offset(pil_image, offset, 0)
        # img_trans.show()
        return img_trans
    
    def change_txt(self, head, offset, img_size):
        bbox_list = self.get_bbox_list(head)
        bbox_list_rotate = self.translate_bbox_list(bbox_list,
                                                    offset,
                                                    img_size)
        return bbox_list_rotate
    
    def get_bbox_list(self,head):
      bbox_list = []
      with open(self.source_folder_path + "/" + head + ".txt", "r") as txt_file:
          bbox_list = txt_file.readlines()
      return bbox_list 
    
    def translate_bbox_list(self, bbox_list, offset, img_size):
        bbox_list_translate = []
        for bbox in bbox_list:
            bbox_translate = self.calculate_points(bbox, offset, img_size)
            if bbox_translate:
                bbox_list_translate.append(bbox_translate)
                bbox_list_translate.append('\n')
        return bbox_list_translate
        
    def calculate_points(self, bbox, offset, img_size):
        classname, x_center, y_center, width, height = bbox.split()
        
        bottom_left  = np.array([(float(x_center)-(float(width)/2)) * 
                                 img_size[0],\
                                 (float(y_center)+(float(height)/2))* 
                                 img_size[1]])
            
        bottom_right = np.array([(float(x_center)+(float(width)/2)) * 
                                 img_size[0],\
                                 (float(y_center)+(float(height)/2))* 
                                 img_size[1]])
            
        top_left     = np.array([(float(x_center)-(float(width)/2)) * 
                                 img_size[0],\
                                 (float(y_center)-(float(height)/2))* 
                                 img_size[1]])
            
        top_right    = np.array([(float(x_center)+(float(width)/2)) * 
                                 img_size[0],\
                                 (float(y_center)-(float(height)/2))* 
                                 img_size[1]])
            
        center       = np.array([float(x_center) * img_size[0],\
                                 float(y_center) * img_size[1]])
        
        # print(bbox)
        bbox_translate = self.translate_bbox_in_x_direction(img_size, 
                                                            offset,
                                                            classname,
                                                            center,
                                                            bottom_right, 
                                                            bottom_left,
                                                            width,
                                                            height)
        
        return bbox_translate
        
    def translate_bbox_in_x_direction(self, img_size, offset, classname, 
                                      center, bottom_right, bottom_left,
                                      width, height):
        bbox_translate = []
        bottom_left_new_x = bottom_left[0] + offset
        center_new_x = center[0] + offset
        bottom_right_new_x = bottom_right[0] + offset

        if bottom_left_new_x >= img_size[0]:  
            x = center_new_x - img_size[0]
            point = [x, center[1]]
            center_new = self.make_points_decimal(point, img_size)
            bbox_translate = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                              float(center_new[0]), 
                                                              float(center_new[1]), 
                                                              float(width), 
                                                              float(height))       
            bbox_translate = bbox_translate.replace(',', '')
            
        
        
        elif bottom_right_new_x < img_size[0]:
            point = [center_new_x, center[1]]
            center = self.make_points_decimal(point, img_size)
            bbox_translate =  "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                              float(center[0]), 
                                                              float(center[1]), 
                                                              float(width), 
                                                              float(height))       
            bbox_translate = bbox_translate.replace(',', '')   
    
        return bbox_translate
        
    def make_points_decimal(self, point, img_rot_size):
        point[0] = point[0] / img_rot_size[0]
        point[1] = point[1] / img_rot_size[1]
        return point    
        
        
        
        
        
        
        
        
        
        
        
        