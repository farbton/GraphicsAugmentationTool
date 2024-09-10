# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:36:35 2024

@author: Kirko
"""

import os
import numpy as np
from PyQt5 import QtCore
from PIL import Image
import time

class Rotation(QtCore.QObject):
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps
        
    def preview_rotation_oneImage(self):
        pil_imagelist_rotation = []
        txt_filelist_rotation  = []
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        head, tail = os.path.splitext(str(item_name.text()))
        pil_image = Image.open(item_path)
        
        steps = int(self.le_steps.text())
        degrees_steps = round(360/steps)
        degrees = degrees_steps
        
        for j in range(steps):       

            img_rot = self.change_rotation_oneImage(pil_image, degrees)
            txt_rot = self.change_txt(head, degrees, 
                                      pil_image.size, 
                                      img_rot.size)
            
            pil_imagelist_rotation.append([img_rot,
                                           item_name.text(),
                                           degrees,
                                           None]) # None = Placeholder for Counter
            
            txt_filelist_rotation.append(txt_rot)
            degrees += degrees_steps 
            
            
        return pil_imagelist_rotation, txt_filelist_rotation
        
    def change_rotation_oneImage(self, pil_image, degrees):
        # img_ier    = ImageEnhance.Rotation(pil_image)
        img_rot = pil_image.rotate(degrees, expand=True)
        return img_rot
    
    def change_rotation_allImages(self, txt_list, mode, writer):
        pil_imagelist_rotation_allImages = []
        txt_filelist_rotation_all  = []
        
        for index in range(len(self.lw_sourcefolder)):
    
            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())
            head, tail = os.path.splitext(str(item_name.text()))
            steps       = int(self.le_steps.text())
            degrees_steps = round(360/steps)
            degrees = degrees_steps
            
            with Image.open(item_path, mode='r') as pil_image:
                counter = 0
                for j in range(steps):
                    img_rot = self.change_rotation_oneImage(pil_image, degrees)
                    txt_rot = self.change_txt(head, degrees, pil_image.size, img_rot.size)
                    pil_imagelist_rotation_allImages.append([img_rot,
                                                              item_name.text(),
                                                              degrees,
                                                              None]) # None = Placeholder for Counter
                    
                    txt_filelist_rotation_all.append(txt_rot)
                    degrees += degrees_steps
                    counter += 1
                    # print("länge: ", len(pil_imagelist_rotation_allImages))
                    
                writer.write_rotated_files_allImages(pil_imagelist_rotation_allImages,
                                                     txt_filelist_rotation_all,
                                                     mode)
                
                del pil_imagelist_rotation_allImages[-counter:]
                del txt_filelist_rotation_all[-counter:]
                   
    def change_txt(self, head, degrees, pil_image_size, img_rot_size):        
            bbox_list = self.get_bbox_list(head)
            bbox_list_rotate = self.rotate_bbox_list(bbox_list,
                                                     degrees,
                                                     pil_image_size,
                                                     img_rot_size)
            return bbox_list_rotate
        
    def get_bbox_list(self,head):
      bbox_list = []
      with open(self.source_folder_path + "/" + head + ".txt", "r") as txt_file:
          bbox_list = txt_file.readlines()
      return bbox_list      
        
    def rotate_bbox_list(self,bbox_list, degrees, pil_image_size, img_rot_size):
        bbox_list_rotate = []
        for bbox in bbox_list:
            bbox_rotate = self.calculate_points(bbox, degrees, pil_image_size, img_rot_size)
            bbox_list_rotate.append(bbox_rotate)
            bbox_list_rotate.append('\n')
        return bbox_list_rotate  
    
    def calculate_points(self, bbox, degrees, pil_image_size, img_rot_size):
        classname, x_center, y_center, width, height = bbox.split()        
        
        bottom_left  = np.array([(float(x_center)-(float(width)/2)) * 
                                 pil_image_size[0],\
                                 (float(y_center)+(float(height)/2))* 
                                 pil_image_size[1]])
            
        bottom_right = np.array([(float(x_center)+(float(width)/2)) * 
                                 pil_image_size[0],\
                                 (float(y_center)+(float(height)/2))* 
                                 pil_image_size[1]])
            
        top_left     = np.array([(float(x_center)-(float(width)/2)) * 
                                 pil_image_size[0],\
                                 (float(y_center)-(float(height)/2))* 
                                 pil_image_size[1]])
            
        top_right    = np.array([(float(x_center)+(float(width)/2)) * 
                                 pil_image_size[0],\
                                 (float(y_center)-(float(height)/2))* 
                                 pil_image_size[1]])
            
        center       = np.array([float(x_center) * pil_image_size[0],\
                                 float(y_center) * pil_image_size[1]])
            
        origin =[pil_image_size[0]/2, pil_image_size[1]/2]
        
        center_new       = self.rotate_point(origin, center,       
                                             degrees, img_rot_size, 
                                             pil_image_size)
        bottom_left_new  = self.rotate_point(origin, bottom_left,  
                                             degrees, img_rot_size, 
                                             pil_image_size)
        bottom_right_new = self.rotate_point(origin, bottom_right, 
                                             degrees, img_rot_size, 
                                             pil_image_size)
        top_left_new     = self.rotate_point(origin, top_left,     
                                             degrees, img_rot_size, 
                                             pil_image_size)
        top_right_new    = self.rotate_point(origin, top_right,    
                                             degrees, img_rot_size, 
                                             pil_image_size)
        
        width_new, height_new = self.calculate_new_bounding_box(
                                        center_new,
                                        bottom_left_new,
                                        bottom_right_new,
                                        top_left_new, 
                                        top_right_new,
                                        img_rot_size)
               
        center_new       = self.make_points_decimal(center_new, img_rot_size)        
        
        bbox_rotate = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                          float(center_new[0]), 
                                                          float(center_new[1]), 
                                                          float(width_new), 
                                                          float(height_new))       
        bbox_rotate = bbox_rotate.replace(',', '')
        return bbox_rotate  
    
    def make_points_decimal(self, point, img_rot_size):
        point[0] = point[0] / img_rot_size[0]
        point[1] = point[1] / img_rot_size[1]
        return point
    
    
    def rotate_point(self, origin, point, degrees, img_rot_size, pil_image_size):
        origin_x, origin_y     = origin
        px, py                 = point
        width_org              = pil_image_size[0]
        height_org             = pil_image_size[1]
        width_rot              = img_rot_size[0]
        height_rot             = img_rot_size[1]
        
        delta_width = width_rot - width_org
        delta_height = height_rot - height_org
        
        qx = origin_x + np.cos(np.deg2rad(degrees)) * (px - origin_x) +\
                        np.sin(np.deg2rad(degrees)) * (py - origin_y)
    
        qy = origin_y - np.sin(np.deg2rad(degrees)) * (px - origin_x) +\
                        np.cos(np.deg2rad(degrees)) * (py - origin_y)
        
        qx = qx + (delta_width/2)
        qy = qy + (delta_height/2)
               
        return [qx, qy]
    

    def calculate_new_bounding_box(self, center_new, bottom_left_new, bottom_right_new,\
                                    top_left_new, top_right_new, img_rot_size):

        x_min = min(bottom_left_new[0], bottom_right_new[0],\
                       top_left_new[0],    top_right_new[0])
            
        x_max = max(bottom_left_new[0], bottom_right_new[0],\
                       top_left_new[0],    top_right_new[0])
            
        y_min = min(bottom_left_new[1], bottom_right_new[1],\
                       top_left_new[1],    top_right_new[1])
            
        y_max = max(bottom_left_new[1], bottom_right_new[1],\
                       top_left_new[1],    top_right_new[1])
            
        width_new  = x_max-x_min
        height_new = y_max-y_min
        
        width_new  = width_new  / img_rot_size[0]
        height_new = height_new / img_rot_size[1]
        
        return width_new, height_new
        
        
        
        
        
        
        
        
        
        
        
        
        