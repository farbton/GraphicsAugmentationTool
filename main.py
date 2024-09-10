# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 20:20:10 2022

@author: Kirko
    br = brightness
    sa = saturation
    co = contrast
    sh = sharpness
    fl = flip
    mi = mirror
    ro = rotation
    tr = translation
    sc = scale
    no = noise
"""

import sys; print("sys.version: ", sys.version)
from PyQt5 import QtWidgets
import mainwindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # pixmap = QPixmap("C:/Insektenlaser/GIT/verteiltes_yolov3/verteiltes_yolov3/icons/LogoFinalOhneHaus.png")
    # splash = QtWidgets.QSplashScreen(pixmap.scaled(QtCore.QSize(500, 500), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
    # splash.show()
    #app.processEvents()
    mainWindow = mainwindow.Window(app)
    mainWindow.show()
    mainWindow.start()
    # splash.finish(mainWindow)
    app.exec_()
