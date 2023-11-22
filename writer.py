# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:15:35 2022

@author: Admin
"""
import os

class Writer():
    def __init__(self, mainwindow, source_folder_path, destination_folder_path):
        self.mainwindow = mainwindow
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path
        
    
    def write_files_to_disk(self, pil_imagelist, txtlist, mode):
        # print(pil_imagelist_bright)
        # print(txtlist)
        # file_ext  = ".jpg"
        for (image, fullname, value) in pil_imagelist:
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(value) + "_" + str(mode)[0:2] + tail
            new_file_path = self.destination_folder_path + "\\" + new_file_name
            image.save(new_file_path)
            self.write_txtfile_to_disk(fullname, value, mode)
    
    def write_txtfile_to_disk(self, fullname, value, mode):
        if not os.path.exists(self.destination_folder_path):
            os.makedirs(self.destination_folder_path)
            self.mainwindow.lb_console.setText("destination folder created")
            
        if not os.access(self.destination_folder_path, os.W_OK):
            print("%s folder is not writeable.")

        head, tail = os.path.splitext(fullname)
        new_filename = head + "_" + str(value) + "_" + str(mode)[0:2] + ".txt"
        new_file_path = self.destination_folder_path + "\\" + new_filename
        with open(self.source_folder_path + "/"+  head + ".txt", "r") as txtfile:
            # print(txtfile)
            with open(new_file_path, "w") as new_txtfile:
                new_txtfile.writelines(str(line) for line in txtfile)
                
    def write_rotated_files_oneImage(self, pil_imagellist, txt_list, mode):
        
        # print(pil_imagellist)
        # print(txt_list)
        for number in range(len(pil_imagellist)):
            
            img_name_mode_list = pil_imagellist[number]
            bbox_list = txt_list[number]
            image, fullname, angle = img_name_mode_list
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(angle) + "_" + str(mode)[0:2] + tail
            new_file_path = self.destination_folder_path + "\\" + new_file_name
            image.save(new_file_path)
            self.write_rotate_bbox_list(bbox_list, fullname, angle, mode)
    
    def write_rotated_files_allImages(self, pil_imagelist_rotation_allImages,
                                      txt_filelist_rotation_all,
                                      mode):
        
        # print(len(pil_imagelist_rotation_allImages))
        # print(len(txt_filelist_rotation_all))
        for number in range(len(pil_imagelist_rotation_allImages)):
            img = pil_imagelist_rotation_allImages[number]
            bbox_list = txt_filelist_rotation_all[number]
            # print(bbox_list)
            self.write_rotated_files_oneImage([img], [bbox_list], mode)
        
        
        
        
    def write_rotate_bbox_list(self, bbox_list, fullname, angle, mode):
        # print("fullnmae: ", fullname)
        head, tail = os.path.splitext(fullname)
        # print("tail: " , tail)
        new_file_name = head + "_" +  str(angle) + "_" + str(mode)[0:2] + ".txt"
        new_file_path = self.destination_folder_path + "\\" + new_file_name
        new_file = open(new_file_path, "w")
        new_file.writelines(str(bbox) for bbox in bbox_list)
        new_file.close()
      
    