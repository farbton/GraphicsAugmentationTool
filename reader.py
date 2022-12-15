# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 10:28:43 2022

@author: Admin
"""
import os
from PyQt5 import QtCore

# txt_filenames = ""
# jpg_filenames = ""

class Reader(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.list_filenames = []
                
    def read_sourcefolder(self, path):
        self.get_list_of_filenames(path)
        return self.list_filenames
    
    def get_list_of_filenames(self, path):
        self.list_filenames = []
        for filename in os.listdir(path):
            self.list_filenames.append(filename)
