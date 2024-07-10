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
    def __init__(self, lw_sourcefolder, source_folder_path, le_steps):
        QtCore.QObject.__init__(self)
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
        pil_image = Image.open(item_path, mode='r')
        
        for j in range(steps):
            # img_scale als Liste implementieren 
            img_scaled_list = self.change_scale_oneImage(pil_image, value)
            
            for img_scale, counter in img_scaled_list:
                pil_imagelist_scale.append([img_scale,
                                            item_name.text(),
                                            value+float(counter)])
            
            value = round(value + factor, 2)
            
        return pil_imagelist_scale, txt_filelist_scale
    
    def change_scale_oneImage(self, pil_image, value):
        w, h = pil_image.size
        # print(w, h)
        img_scale = ImageOps.scale(pil_image, value)
        img = Image.new(mode="RGB", size=pil_image.size)
        img_scaled_list = []
        w_new, h_new = img_scale.size
        horizontal = w_new - w
        vertical   = h_new - h
        # print(img_scale.size, horizontal, vertical, value)
        
        if w_new > w:
            ''' 
            img_scale is bigger then pil_image
            '''
            print("if")
            # img = img_scale.crop((horizontal // 2  , vertical // 2,
            #                      (horizontal // 2) + w, (vertical // 2) + h))
            counter = 0
            col = 0
            row = 0
            print("vor while________________")
            while counter < 10:
                
                number = img_scale.size[0] / pil_image.size[0]
                # print("number: ", number) 
                array = np.zeros((pil_image.size[1], pil_image.size[0], 3))
                array_pil   = np.array(img_scale)
                print(pil_image.size, img_scale.size, array.shape)
               
              
               
                if col * pil_image.size[0] + pil_image.size[0] < img_scale.size[0] and\
                   row * pil_image.size[1] + pil_image.size[1] < img_scale.size[1]:
                   
                    # print("col: ", col, "counter: ", counter)
                    print("1. col< & row<")
                   
                    # end = 
                   
                    array[:, :, 0] = array_pil[row * pil_image.size[1] : row * pil_image.size[1] + pil_image.size[1],          
                                              col * pil_image.size[0] : col * pil_image.size[0] + pil_image.size[0],
                                              0]
                   
                    array[:, :, 1] = array_pil[row * pil_image.size[1] : row * pil_image.size[1] + pil_image.size[1],          
                                              col * pil_image.size[0] : col * pil_image.size[0] + pil_image.size[0],
                                              1]
                   
                    array[:, :, 2] = array_pil[row * pil_image.size[1] : row * pil_image.size[1] + pil_image.size[1],          
                                              col * pil_image.size[0] : col * pil_image.size[0] + pil_image.size[0],
                                              2]

                    # col += 1
                   
                   
                counter += 1
            
               
            img = Image.fromarray(np.uint8(array))
            obj = [img, counter]
            img_scaled_list.append(obj)







        else:
            ''' 
            img_scale is smaller then pil_image
            '''
            array = np.zeros((pil_image.size[1], pil_image.size[0], 3))
            array_pil   = np.array(img_scale)
            # print(pil_image.size, img_scale.size, array.shape)
            print("else")
            row = 0
            col = 0
            counter = 0
            
            
            while counter != "end":
                
                # print("col: ", col , "row: ", row)
                
                if col * img_scale.size[0] + img_scale.size[0] <= pil_image.size[0] and\
                   row * img_scale.size[1] + img_scale.size[1] <= pil_image.size[1]: 
                   
                   # print("1. col< & row<")
                       
                   array[row * img_scale.size[1] : row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : col * img_scale.size[0] + img_scale.size[0], 0] =\
                       array_pil[:,:,0]
                   
                   array[row * img_scale.size[1] : row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : col * img_scale.size[0] + img_scale.size[0], 1] =\
                       array_pil[:,:,1]
                    
                   array[row * img_scale.size[1] : row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : col * img_scale.size[0] + img_scale.size[0], 2] =\
                       array_pil[:,:,2]
                    
                   col += 1
                
                elif col * img_scale.size[0] + img_scale.size[0] >  pil_image.size[0] and\
                     row * img_scale.size[1] + img_scale.size[1] <= pil_image.size[1]:
                    
                   # print("2. col> & row<")   
                    
                   end_col = pil_image.size[0] - ((col-1) * img_scale.size[0] + img_scale.size[0])
                   # print("end_col: ", end_col, "col: ", col)
                                    
                   # print(col * img_scale.size[0],col * img_scale.size[0] + end)
                   # print(col*img_scale.size[0]+end_col)
                   
                   array[row * img_scale.size[1] : row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : col * img_scale.size[0] + end_col, 0] = array_pil[:,0:end_col,0]
                    
                   array[row * img_scale.size[1] : row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : col * img_scale.size[0] + end_col, 1] = array_pil[:,0:end_col,1]
                    
                   array[row * img_scale.size[1] : row * img_scale.size[1] + img_scale.size[1],
                         col * img_scale.size[0] : col * img_scale.size[0] + end_col, 2] = array_pil[:,0:end_col,2]
            
                   row += 1
                   col  = 0
                    
                elif col * img_scale.size[0] + img_scale.size[0] <= pil_image.size[0] and\
                     row * img_scale.size[1] + img_scale.size[1] > pil_image.size[1]:
                   
                   # print("3. col< & row>")    
                   
                   end_row = pil_image.size[1] - ((row-1) * img_scale.size[1] + img_scale.size[1])
                   
                   # print("end_row: ", end_row)
                   
                   array[row * img_scale.size[1] : row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : col * img_scale.size[0] + img_scale.size[0], 0] =\
                       array_pil[0:end_row,:,0]
                   
                   array[row * img_scale.size[1] : row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : col * img_scale.size[0] + img_scale.size[0], 1] =\
                       array_pil[0:end_row,:,1]
                    
                   array[row * img_scale.size[1] : row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : col * img_scale.size[0] + img_scale.size[0], 2] =\
                       array_pil[0:end_row,:,2]

                   col += 1

                elif col * img_scale.size[0] + img_scale.size[0] > pil_image.size[0] and\
                     row * img_scale.size[1] + img_scale.size[1] > pil_image.size[1]:
                      
                   # print("4. col> & row>") 
                   
                   end_col = pil_image.size[0] - ((col-1) * img_scale.size[0] + img_scale.size[0])
                   end_row = pil_image.size[1] - ((row-1) * img_scale.size[1] + img_scale.size[1])
                   
                   # print(end_col, end_row)
                   
                   array[row * img_scale.size[1] : row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : col * img_scale.size[0] + end_col, 0] =\
                       array_pil[0:end_row,0:end_col,0]
                   
                   array[row * img_scale.size[1] : row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : col * img_scale.size[0] + end_col, 1] =\
                       array_pil[0:end_row,0:end_col,1]
                    
                   array[row * img_scale.size[1] : row * img_scale.size[1] + end_row,
                         col * img_scale.size[0] : col * img_scale.size[0] + end_col, 2] =\
                       array_pil[0:end_row,0:end_col,2]
                   
                   counter = "end"
                   
                # counter += 1
                
            img = Image.fromarray(np.uint8(array))
            obj = [img, 0]
            img_scaled_list.append(obj)
            
           
        
        return img_scaled_list
    