# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:32:28 2024

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:56:18 2023

@author: Kirko
"""

import os
from PyQt5 import QtCore
from PIL import Image, ImageEnhance, ImageOps
import numpy as np




class Scale(QtCore.QObject):
    def __init__(self, main_window, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
        self.main_window = main_window
        self.lw_sourcefolder = lw_sourcefolder
        self.source_folder_path = source_folder_path
        self.le_steps = le_steps

    def preview_scale_oneImage(self):
        pil_imagelist_scale = []
        txt_filelist_scale  = []
        steps = int(self.le_steps.text())
        factor = round((2 / steps), 2)
        value  = factor
        current_index = self.lw_sourcefolder.currentRow()
        item_name = self.lw_sourcefolder.item(current_index)
        item_path = os.path.join(self.source_folder_path, item_name.text())
        head, tail = os.path.splitext(str(item_name.text()))
        pil_image = Image.open(item_path, mode='r')
        
        for j in range(steps):
            # img_scale als Liste implementieren 
            img_scaled_list = self.change_scale_oneImage(pil_image, value)
            
            for img_scale, counter, border in img_scaled_list:
                pil_imagelist_scale.append([img_scale,
                                            item_name.text(),
                                            value, float(counter)])
                
                txt_scale = self.change_txt(head, value, pil_image.size,
                                            img_scale.size, border)
                
                txt_filelist_scale.append([txt_scale, counter])
                
            value = round(value + factor, 2)
            
        return pil_imagelist_scale, txt_filelist_scale
    
    def change_scale_allImages(self, txt_list, mode, writer):
        pil_imagelist_scale_allImages = []
        txt_filelist_scale_all = []
        self.main_window.progressBar.reset()
        self.main_window.progressBar.setRange(0, len(self.lw_sourcefolder))
        
        for index in range(len(self.lw_sourcefolder)):
            item_name = self.lw_sourcefolder.item(index)
            item_path = os.path.join(self.source_folder_path, item_name.text())
            head, tail = os.path.splitext(str(item_name.text()))
            steps = int(self.le_steps.text())
            factor = round((2 / steps), 2)
            value  = factor
            self.main_window.progressBar.setValue(index+1)
            
            with Image.open(item_path, mode='r') as pil_image:
                counter = 0
                for j in range(steps):
                    img_scaled_list = self.change_scale_oneImage(pil_image, value)
                    
                    for img_scale, counter, border in img_scaled_list:
                        pil_imagelist_scale_allImages.append([img_scale,
                                                              item_name.text(),
                                                              value, 
                                                              float(counter)])
            
                        txt_scale = self.change_txt(head, 
                                                    value, 
                                                    pil_image.size, 
                                                    img_scale.size, 
                                                    border)
                    
                        txt_filelist_scale_all.append([txt_scale, counter])
                    
                    
                    value = round(value + factor, 2)
                    counter += 1
            
                writer.write_scaled_files_allImages(pil_imagelist_scale_allImages,
                                                    txt_filelist_scale_all,
                                                    mode)
                
                del pil_imagelist_scale_allImages[-counter:]
                del txt_filelist_scale_all[-counter:]
                
    def change_txt(self, head, value, pil_image_size, img_scale_size, border):        
            bbox_list = self.get_bbox_list(head)
            bbox_list_scaled = self.scale_bbox_list(bbox_list,
                                                    value,
                                                    pil_image_size,
                                                    img_scale_size,
                                                    border)
            return bbox_list_scaled
    
    def get_bbox_list(self,head):
      bbox_list = []
      with open(self.source_folder_path + "/" + head + ".txt", "r") as txt_file:
          bbox_list = txt_file.readlines()
      return bbox_list               
    
    def scale_bbox_list(self,bbox_list, value, pil_image_size, img_scale_size, border):
        bbox_list_scaled = []
        for bbox in bbox_list:
            bbox_scaled = self.calculate_points(bbox, value, pil_image_size, img_scale_size, border)
            bbox_list_scaled.append(bbox_scaled)
            bbox_list_scaled.append('\n')
            
        bbox_list_scaled = filter( None, bbox_list_scaled)
        
        list_scaled = []
        for l in bbox_list_scaled:
            if l != "\n":
                list_scaled.append(l+"\n")            
        
        # print(list_scaled)
        return list_scaled
    
    def calculate_points(self, bbox, value, pil_image_size, img_scale_size, border):
        classname, x_center, y_center, width_old, height_old = bbox.split() 
        x_begin_border, x_end_border, y_begin_border, y_end_border = border
        # print(border)
        x_center_new = 0
        y_center_new = 0
        width_new    = 0
        height_new   = 0
        bbox_scaled  = None
        
        # bottom_left  = np.array([
        #     (float(x_center)-(float(width_old)/2)) * pil_image_size[0],\
        #     (float(y_center)+(float(height_old)/2))* pil_image_size[1]])
            
        # bottom_right = np.array([
        #     (float(x_center)+(float(width_old)/2)) * pil_image_size[0],\
        #     (float(y_center)+(float(height_old)/2))* pil_image_size[1]])
            
        # top_left     = np.array([
        #     (float(x_center)-(float(width_old)/2)) * pil_image_size[0],\
        #     (float(y_center)-(float(height_old)/2))* pil_image_size[1]])
            
        # top_right    = np.array([
        #     (float(x_center)+(float(width_old)/2)) * pil_image_size[0],\
        #     (float(y_center)-(float(height_old)/2))* pil_image_size[1]])
        
        
        # print(x_center, y_center, width_old, height_old, value)
        # print(top_left[0], top_right[0], bottom_left[1], bottom_right[1]) 
        
        x      = float(x_center)   * value
        y      = float(y_center)   * value
        width  = float(width_old)  * value
        height = float(height_old) * value
        
        bottom_left_scaled =np.array([(x-width/2) * img_scale_size[0],\
                                      (y+height/2) * img_scale_size[1]])
        
        bottom_right_scaled =np.array([(x+width/2) * img_scale_size[0],\
                                       (y+height/2) * img_scale_size[1]])
        
        top_left_scaled =np.array([(x-width/2) * img_scale_size[0],\
                                   (y-height/2) * img_scale_size[1]])
            
        top_right_scaled =np.array([(x+width/2) * img_scale_size[0],\
                                    (y-height/2) * img_scale_size[1]])
        
        
        
        if x_begin_border < top_left_scaled[0]     < x_end_border and \
           x_begin_border < top_right_scaled[0]    < x_end_border and \
           x_begin_border < bottom_left_scaled[0]  < x_end_border and \
           x_begin_border < bottom_right_scaled[0] < x_end_border and \
           y_begin_border < top_left_scaled[1]     < y_end_border and \
           y_begin_border < top_right_scaled[1]    < y_end_border and \
           y_begin_border < bottom_left_scaled[1]  < y_end_border and \
           y_begin_border < bottom_right_scaled[1] < y_end_border:
               
               if  x < 1 and y < 1:
                   x_center_new = x
                   y_center_new = y
                   width_new    = width
                   height_new   = height
                   # print(x_center_new, y_center_new, width_new, height_new)
                   bbox_scaled = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                                     float(x_center_new), 
                                                                     float(y_center_new), 
                                                                     float(width_new), 
                                                                     float(height_new))
                   bbox_scaled = bbox_scaled.replace(',', '')
        
               elif x > 1 and y < 1:             
                    x_center_new = x-1
                    y_center_new = y
                    width_new    = width
                    height_new   = height
                    bbox_scaled = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                                  float(x_center_new), 
                                                                  float(y_center_new), 
                                                                  float(width_new), 
                                                                  float(height_new))
                    bbox_scaled = bbox_scaled.replace(',', '')
            
        
               elif x < 1.0 and y > 1.0 :
                    x_center_new = x
                    y_center_new = y-1
                    width_new    = width
                    height_new   = height
                    bbox_scaled = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                                      float(x_center_new), 
                                                                      float(y_center_new), 
                                                                      float(width_new), 
                                                                      float(height_new))
                    bbox_scaled = bbox_scaled.replace(',', '')
        
               elif x > 1.0 and y > 1.0 :
                    x_center_new = x-1
                    y_center_new = y-1
                    width_new    = width
                    height_new   = height
                    bbox_scaled = "{}, {:f}, {:f}, {:f}, {:f}".format(int(classname), 
                                                                      float(x_center_new), 
                                                                      float(y_center_new), 
                                                                      float(width_new), 
                                                                      float(height_new))
                    bbox_scaled = bbox_scaled.replace(',', '')
                
               # center_new       = self.make_points_decimal((x,y), img_scale_size)        
 
        return bbox_scaled  
    
    def change_scale_oneImage(self, pil_image, value):
        w, h = pil_image.size
        # print(w, h)
        img_scale = ImageOps.scale(pil_image, value)
        img = Image.new(mode="RGB", size=pil_image.size)
        img_scaled_list = []
        w_new, h_new = img_scale.size
        horizontal = w_new - w
        vertical   = h_new - h
        end = 0
        counter = 1
        # print("value: ", value)
        if w_new > w:
            ''' 
            img_scale is bigger then pil_image
            '''
            col = 0
            row = 0
            
            while end != 1: 
                
                number = img_scale.size[0] / pil_image.size[0]

                array = np.zeros((pil_image.size[1], pil_image.size[0], 3))
                array_pil   = np.array(img_scale)
         
                if col * pil_image.size[0] + pil_image.size[0] <= \
                                             img_scale.size[0] and\
                   row * pil_image.size[1] + pil_image.size[1] <= \
                                             img_scale.size[1]:                                         
                   
                       array[:, :, 0] = array_pil[row * pil_image.size[1] : \
                                                  row * pil_image.size[1] + \
                                                        pil_image.size[1],          
                                                  col * pil_image.size[0] : \
                                                  col * pil_image.size[0] + \
                                                        pil_image.size[0], 0]
                   
                       array[:, :, 1] = array_pil[row * pil_image.size[1] : \
                                                  row * pil_image.size[1] + \
                                                        pil_image.size[1],          
                                                  col * pil_image.size[0] : \
                                                  col * pil_image.size[0] + \
                                                        pil_image.size[0], 1]
                   
                       array[:, :, 2] = array_pil[row * pil_image.size[1] : \
                                                  row * pil_image.size[1] + \
                                                        pil_image.size[1],          
                                                  col * pil_image.size[0] : \
                                                  col * pil_image.size[0] + \
                                                        pil_image.size[0], 2]
                           
                       x_begin_border = col * pil_image.size[0]
                       x_end_border   = x_begin_border + pil_image.size[0]
                       y_begin_border = row * pil_image.size[1]
                       y_end_border   = y_begin_border + pil_image.size[1]
                       border = [x_begin_border,x_end_border,y_begin_border,y_end_border]
                       col += 1
                       img = Image.fromarray(np.uint8(array))
                       obj = [img, counter, border]
                       img_scaled_list.append(obj)
                       # print("bigger_1", counter)
                       counter += 1
                   
                elif col * pil_image.size[0] + pil_image.size[0] >  \
                                               img_scale.size[0] and \
                     row * pil_image.size[1] + pil_image.size[1] <= \
                                               img_scale.size[1]:
                       
                       end_col = img_scale.size[0] - \
                           ((col-1) * pil_image.size[0] + pil_image.size[0])
                       
                       # print("end:col: ", end_col)
                       
                       if end_col != 0: 
                       
                           array[:, :end_col, 0] = \
                               array_pil[row * pil_image.size[1] : \
                                         row * pil_image.size[1] + \
                                               pil_image.size[1],          
                                         col * pil_image.size[0] : \
                                         col * pil_image.size[0] + end_col, 0]
                          
                           array[:, :end_col, 1] = \
                               array_pil[row * pil_image.size[1] : \
                                         row * pil_image.size[1] + \
                                               pil_image.size[1],          
                                         col * pil_image.size[0] : \
                                         col * pil_image.size[0] + end_col, 1]
                          
                           array[:, :end_col, 2] = \
                               array_pil[row * pil_image.size[1] : \
                                         row * pil_image.size[1] + \
                                               pil_image.size[1],          
                                         col * pil_image.size[0] : \
                                         col * pil_image.size[0] + end_col, 2]
                           
                           x_begin_border = col * pil_image.size[0]
                           x_end_border   = x_begin_border + pil_image.size[0]
                           y_begin_border = row * pil_image.size[1]
                           y_end_border   = y_begin_border + pil_image.size[1]
                           border = [x_begin_border,x_end_border,y_begin_border,y_end_border]
                           img = Image.fromarray(np.uint8(array))
                           obj = [img, counter, border]
                           img_scaled_list.append(obj)
                           # print("bigger_2", counter)
                           counter += 1
                       col  = 0
                       row += 1
                       

                elif col * pil_image.size[0] + pil_image.size[0] <= \
                                               img_scale.size[0] and\
                     row * pil_image.size[1] + pil_image.size[1] >  \
                                               img_scale.size[1]:                       
                       
                       end_row = img_scale.size[1] - \
                           ((row-1) * pil_image.size[1] + pil_image.size[1])

                       if end_col != 0:
                           array[:end_row, :, 0] = \
                               array_pil[row * pil_image.size[1] : \
                                         row * pil_image.size[1] + end_row,          
                                         col * pil_image.size[0] : \
                                         col * pil_image.size[0] + \
                                               pil_image.size[0], 0]
                          
                           array[:end_row, :, 1] = \
                               array_pil[row * pil_image.size[1] : \
                                         row * pil_image.size[1] + end_row,          
                                         col * pil_image.size[0] : \
                                         col * pil_image.size[0] + \
                                               pil_image.size[0], 1]
                          
                           array[:end_row, :, 2] = \
                               array_pil[row * pil_image.size[1] : \
                                         row * pil_image.size[1] + end_row,          
                                         col * pil_image.size[0] : \
                                         col * pil_image.size[0] + \
                                               pil_image.size[0], 2]
                       
                           x_begin_border = col * pil_image.size[0]
                           x_end_border   = x_begin_border + pil_image.size[0]
                           y_begin_border = row * pil_image.size[1]
                           y_end_border   = y_begin_border + pil_image.size[1]
                           border = [x_begin_border,x_end_border,y_begin_border,y_end_border]
                           img = Image.fromarray(np.uint8(array))
                           obj = [img, counter, border]
                           img_scaled_list.append(obj)
                       col += 1
                       # print("bigger_3" , counter)
                       counter += 1
                       
                
                
                elif col * pil_image.size[0] + pil_image.size[0] > \
                                               img_scale.size[0] and\
                     row * pil_image.size[1] + pil_image.size[1] > \
                                               img_scale.size[1]:
                         
                         end_row = img_scale.size[1] - ((row-1) * \
                                   pil_image.size[1] + pil_image.size[1])
                         end_col = img_scale.size[0] - ((col-1) * \
                                   pil_image.size[0] + pil_image.size[0])

                         if end_col or end_row != 0:
                             array[:end_row, :end_col, 0] = \
                                 array_pil[row * pil_image.size[1] : \
                                           row * pil_image.size[1] + end_row,          
                                           col * pil_image.size[0] : \
                                           col * pil_image.size[0] + end_col, 0]
                          
                             array[:end_row, :end_col, 1] = \
                                 array_pil[row * pil_image.size[1] : \
                                           row * pil_image.size[1] + end_row,          
                                           col * pil_image.size[0] : \
                                           col * pil_image.size[0] + end_col, 1]
                          
                             array[:end_row, :end_col, 2] = \
                                 array_pil[row * pil_image.size[1] : \
                                           row * pil_image.size[1] + end_row,          
                                           col * pil_image.size[0] : \
                                           col * pil_image.size[0] + end_col, 2]
                             
                             x_begin_border = col * pil_image.size[0]
                             x_end_border   = x_begin_border + pil_image.size[0]
                             y_begin_border = row * pil_image.size[1]
                             y_end_border   = y_begin_border + pil_image.size[1]
                             border = [x_begin_border,x_end_border,y_begin_border,y_end_border]                          
                             img = Image.fromarray(np.uint8(array))
                             obj = [img, counter, border]
                             img_scaled_list.append(obj)
                             # print("bigger_4", counter)
                         end = 1
                         counter = 1

        else:
            ''' 
            img_scale is smaller then pil_image
            '''
            array = np.zeros((pil_image.size[1], pil_image.size[0], 3))
            array_pil   = np.array(img_scale)
            row = 0
            col = 0
            counter = 1
                       
            while end != 1:
                
                # print("col: ", col , "row: ", row)
                
                if col * img_scale.size[0] + img_scale.size[0] <= \
                                             pil_image.size[0] and\
                   row * img_scale.size[1] + img_scale.size[1] <= \
                                             pil_image.size[1]: 

                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + img_scale.size[0], 0] =\
                                                        array_pil[:,:,0]
                   
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + img_scale.size[0], 1] =\
                                                        array_pil[:,:,1]
                    
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + img_scale.size[0], 2] =\
                                                        array_pil[:,:,2]
                    
                   # print("smaller_1", "row: ", row, "col: ", col)
                   col += 1
                
                elif col * img_scale.size[0] + img_scale.size[0] >  \
                                               pil_image.size[0] and\
                     row * img_scale.size[1] + img_scale.size[1] <= \
                                               pil_image.size[1]:
                                                
                                          
                    end_col = pil_image.size[0] - \
                        ((col-1) * img_scale.size[0] + img_scale.size[0])
                   
                    array[row * img_scale.size[1] : \
                          row * img_scale.size[1] + img_scale.size[1],
                          col * img_scale.size[0] : \
                          col * img_scale.size[0] + end_col, 0] = \
                                      array_pil[:, 0:end_col, 0]
                    
                    array[row * img_scale.size[1] : \
                          row * img_scale.size[1] + img_scale.size[1],
                          col * img_scale.size[0] : \
                          col * img_scale.size[0] + end_col, 1] = \
                                      array_pil[:, 0:end_col, 1]
                    
                    array[row * img_scale.size[1] : \
                          row * img_scale.size[1] + img_scale.size[1],
                          col * img_scale.size[0] : \
                          col * img_scale.size[0] + end_col, 2] = \
                                      array_pil[:, 0:end_col, 2]
            
                    # print("smaller_2","row: ", row, "col: ", col)
                    row += 1
                    col  = 0
                    
                elif col * img_scale.size[0] + img_scale.size[0] <= \
                                               pil_image.size[0] and\
                     row * img_scale.size[1] + img_scale.size[1] > \
                                               pil_image.size[1]:
                   
                   end_row = pil_image.size[1] - \
                       ((row-1) * img_scale.size[1] + img_scale.size[1])
                   
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + img_scale.size[0], 0] =\
                                                array_pil[0:end_row,:,0]
                   
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + img_scale.size[0], 1] =\
                                                array_pil[0:end_row,:,1]
                    
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + img_scale.size[0], 2] =\
                                                array_pil[0:end_row,:,2]

                   col += 1
                   # print("smaller_3", "row: ", row, "col: ", col)

                elif col * img_scale.size[0] + img_scale.size[0] > \
                                               pil_image.size[0] and\
                     row * img_scale.size[1] + img_scale.size[1] > \
                                               pil_image.size[1]:
                  
                   end_col = pil_image.size[0] - \
                       ((col-1) * img_scale.size[0] + img_scale.size[0])
                   end_row = pil_image.size[1] - \
                       ((row-1) * img_scale.size[1] + img_scale.size[1])
                   
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + end_col, 0] =\
                              array_pil[0:end_row,0:end_col,0]
                   
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + end_col, 1] =\
                              array_pil[0:end_row,0:end_col,1]
                    
                   array[row * img_scale.size[1] : \
                         row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : \
                         col * img_scale.size[0] + end_col, 2] =\
                              array_pil[0:end_row,0:end_col,2]
                   
                   end = 1
                   # print("smaller_4", "row: ", row, "col: ", col)
            
            x_begin_border = 0
            x_end_border   = x_begin_border + pil_image.size[0]
            y_begin_border = 0
            y_end_border   = y_begin_border + pil_image.size[1]
            border = [x_begin_border,x_end_border,y_begin_border,y_end_border]     
            img = Image.fromarray(np.uint8(array))
            obj = [img, counter, border]
            img_scaled_list.append(obj)
        # print(img_scaled_list)
        return img_scaled_list
    