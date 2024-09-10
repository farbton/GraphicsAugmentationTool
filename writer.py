# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:15:35 2022

@author: Kirko
"""
import os, time

class Writer():
    def __init__(self, mainwindow, source_folder_path, destination_folder_path):
        self.mainwindow = mainwindow
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path
        self.counter = 1
        
    
    def write_files_to_disk(self, pil_imagelist, txtlist, mode):
        # print(pil_imagelist_bright)
        # print(txtlist)
        # file_ext  = ".jpg"
        # print(self.counter)
        for (image, fullname, value, counter) in pil_imagelist:
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(value) + "_" + str(mode)[0:2] + tail
            # new_file_path = self.destination_folder_path + "\\" + new_file_name
            new_file_path = os.path.join(self.destination_folder_path, new_file_name)
            image.save(new_file_path)
            self.write_txtfile_to_disk(fullname, value, mode)
            # time.sleep(0.1)
        # self.counter += 1
    
    def write_txtfile_to_disk(self, fullname, value, mode):
        if not os.path.exists(self.destination_folder_path):
            os.makedirs(self.destination_folder_path)
            self.mainwindow.lb_console.setText("destination folder created")
            
        if not os.access(self.destination_folder_path, os.W_OK):
            print("%s folder is not writeable.")

        head, tail = os.path.splitext(fullname)
        new_filename = head + "_" + str(value) + "_" + str(mode)[0:2] + ".txt"
        # new_file_path = self.destination_folder_path + "\\" + new_filename
        new_file_path = os.path.join(self.destination_folder_path, new_filename)
        with open(self.source_folder_path + "/"+  head + ".txt", "r") as txtfile:
            # print(txtfile)
            with open(new_file_path, "w") as new_txtfile:
                new_txtfile.writelines(str(line) for line in txtfile)
                
    def write_rotated_files_oneImage(self, pil_imagelist, txt_list, mode):
        
        # print(pil_imagellist)
        # print(txt_list)
        for number in range(len(pil_imagelist)):
            
            img_name_mode_list = pil_imagelist[number]
            bbox_list = txt_list[number]
            image, fullname, angle, ____ = img_name_mode_list
            # print(img_name_mode_list)
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(angle) + "_" + str(mode)[0:2] + tail
            new_file_path = os.path.join(self.destination_folder_path, new_file_name)
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
            # print(img)
            self.write_rotated_files_oneImage([img], [bbox_list], mode)
        
        
        
        
    def write_rotate_bbox_list(self, bbox_list, fullname, angle, mode):
        # print("fullnmae: ", fullname)
        head, tail = os.path.splitext(fullname)
        # print("tail: " , tail)
        new_file_name = head + "_" +  str(angle) + "_" + str(mode)[0:2] + ".txt"
        new_file_path = os.path.join(self.destination_folder_path, new_file_name)
        new_file = open(new_file_path, "w")
        new_file.writelines(str(bbox) for bbox in bbox_list)
        new_file.close()
        
    def write_fliped_files_oneImage(self, pil_imagellist, txt_list, mode):
        
        # print(pil_imagellist)
        # print(txt_list)
        for number in range(len(pil_imagellist)):
            
            img_name_mode_list = pil_imagellist[number]
            # print(img_name_mode_list)
            bbox_list = txt_list[number]
            image, fullname, string, ___ = img_name_mode_list
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + string + tail
            new_file_path = self.destination_folder_path + "\\" + new_file_name
            image.save(new_file_path)
            self.write_fliped_bbox_list(bbox_list, fullname, string) 
            
    def write_fliped_bbox_list(self, bbox_list, fullname, string):
        # print("fullnmae: ", fullname)
        head, tail = os.path.splitext(fullname)
        # print("tail: " , tail)
        new_file_name = head + "_" +  string + ".txt"
        new_file_path = self.destination_folder_path + "\\" + new_file_name
        new_file = open(new_file_path, "w")
        new_file.writelines(str(bbox) for bbox in bbox_list)
        new_file.close()
        
    def write_fliped_files_allImages(self, pil_imagelist_flip_allImages,
                                      txt_filelist_flip_all,
                                      mode):
        
        # print(len(pil_imagelist_rotation_allImages))
        # print(len(txt_filelist_rotation_all))
        for number in range(len(pil_imagelist_flip_allImages)):
            img = pil_imagelist_flip_allImages[number]
            bbox_list = txt_filelist_flip_all[number]
            # print(img)
            # print(bbox_list)
            # print(mode)
            
            self.write_fliped_files_oneImage([img], [bbox_list], mode)
            
            
    def write_translated_file_oneImage(self, pil_imagelist, txt_list, mode):
       
        for number in range(len(pil_imagelist)):
            
            img, fullname, offset, ___ = pil_imagelist[number]
            bbox_list = txt_list[number]

            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(offset) + "_" + str(mode)[0:2] + tail
            new_file_path = os.path.join(self.destination_folder_path, new_file_name)
            img.save(new_file_path)
            self.write_translated_bbox_list(bbox_list, fullname, offset, mode)        
            
            
    def write_translated_bbox_list(self, bbox_list, fullname, offset, mode):

        head, tail = os.path.splitext(fullname)
        new_file_name = head + "_" +  str(offset) + "_" + str(mode)[0:2] + ".txt"
        new_file_path = os.path.join(self.destination_folder_path, new_file_name)
        new_file = open(new_file_path, "w")
        new_file.writelines(str(bbox) for bbox in bbox_list)
        new_file.close()        
            
    def write_translated_files_allImages(self,
                                         pil_imagelist_translation_allImages,
                                         txt_filelist_translation_all,
                                         mode):
        for number in range(len(pil_imagelist_translation_allImages)):
            
            img = pil_imagelist_translation_allImages[number]
            bbox_list = txt_filelist_translation_all[number]
            self.write_translated_file_oneImage([img], [bbox_list], mode)
    
            
    def write_scaled_files_allImages(self, pil_imagelist_scale_allImages,
                                     txt_filelist_scale_all,
                                     mode):
        
        # print(len(pil_imagelist_rotation_allImages))
        # print(len(txt_filelist_rotation_all))
        for number in range(len(pil_imagelist_scale_allImages)):
            img = pil_imagelist_scale_allImages[number]
            bbox_list = txt_filelist_scale_all[number]
            # print(img)
            self.write_scaled_files_oneImage([img], [bbox_list], mode)
    
    def write_scaled_files_oneImage(self, 
                                    pil_imagelist_scale, 
                                    txt_filelist_scale, 
                                    mode):
        # print(len(pil_imagelist_scale))
        name = "XXX"
        # counter = 1
        for number in range(len(pil_imagelist_scale)):
            # print(number)
            img, fullname, offset, counter = pil_imagelist_scale[number]
            # print(fullname)
            # if name != fullname:
                # counter = 1
                # name = fullname
            # print(number, len(txt_filelist_scale))
            if number < len(txt_filelist_scale):
                bbox_list, counter = txt_filelist_scale[number]
                self.write_scaled_bbox_list(bbox_list, fullname, offset, mode, counter)
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(offset) + "_" + \
                str(mode)[0:2] + "_" + str(int(counter)) + tail
            new_file_path = os.path.join(self.destination_folder_path, new_file_name)
            img.save(new_file_path)
            # counter += 1
            
    
    def write_scaled_bbox_list(self, bbox_list, fullname, offset, mode, counter):

        head, tail = os.path.splitext(fullname)
        new_file_name = head + "_" + str(offset) + "_" + str(mode)[0:2] \
                             + "_" + str(counter) + ".txt"
        new_file_path = os.path.join(self.destination_folder_path, new_file_name)
        new_file = open(new_file_path, "w")
        new_file.writelines(str(bbox) for bbox in bbox_list)
        new_file.close()   
        
    def write_noised_files_oneImage(self, pil_imagelist_noise, txt_list, 
                                    mode):
        
        for number in range(len(pil_imagelist_noise)):
            img, fullname, noiseType, ____ = pil_imagelist_noise[number]
            bbox_list = txt_list[number]
            # print(noiseType)
            head, tail = os.path.splitext(fullname)
            new_file_name = head + "_" + str(noiseType) + "_" + str(mode)[0:2] + tail
            new_file_path = os.path.join(self.destination_folder_path, new_file_name)
            img.save(new_file_path)
            self.write_txtfile_to_disk(fullname, noiseType, mode)