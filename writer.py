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
        
    
    def write_files_to_disk(self, pil_imagelist_bright, txtlist):
        print(pil_imagelist_bright)
        print(txtlist)
        # file_ext  = ".jpg"
        for (image, fullname, value) in pil_imagelist_bright:
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(value) + tail
            new_file_path = self.destination_folder_path + "\\" + new_file_name
            image.save(new_file_path)
            self.write_txtfile_to_disk(fullname, value)
            # with open(name)  
    
    def write_txtfile_to_disk(self, fullname, value):
        if not os.path.exists(self.destination_folder_path):
            os.makedirs(self.destination_folder_path)
            self.mainwindow.lb_console.setText("destination folder created")
            
        if not os.access(self.destination_folder_path, os.W_OK):
            print("%s folder is not writeable.")

        head, tail = os.path.splitext(fullname)
        new_filename = head + "_" + str(value) + ".txt"
        new_file_path = self.destination_folder_path + "\\" + new_filename
        with open(self.source_folder_path + "/"+  head + ".txt", "r") as txtfile:
            print(txtfile)
            with open(new_file_path, "w") as new_txtfile:
                new_txtfile.writelines(str(line) for line in txtfile)