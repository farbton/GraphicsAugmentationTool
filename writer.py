# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:15:35 2022

@author: Admin
"""
import os

class Writer():
    def __init__(self, mainwindow, destination_folder_path):
        self.mainwindow = mainwindow
        self.destination_folder_path = destination_folder_path
    
    def write_files_to_disk(self, imagelist, txtlist):
        file_name = "test"
        file_ext  = ".jpg"
        for (image, value) in imagelist:
            new_file_name = file_name + "_" + str(value) + file_ext
            new_file_path = self.destination_folder_path + "\\" + new_file_name
            image.save(new_file_path)
            # with open("")  
    
    def write_txtfile_to_disk(self, txtlist):
        if not os.path.exists(self.destination_folder_path):
            os.makedirs(self.destination_folder_path)
            self.mainwindow.lb_console.setText("destination folder created")
            
        if not os.access(self.destination_folder_path, os.W_OK):
            print("%s folder is not writeable.")

        