import tkinter as tk
from tkinter import filedialog
from PIL import Image
from math import sqrt
import cv2
import argparse
from os import listdir
from os.path import isfile, join



class sharpening(object):
    def __init__(self, path):
        self.path = path
      
    def calculate (self, pathToFile):
        img = Image.open(self.path+'/'+pathToFile)
        bright = []
        pix = img.load()
        width = img.size[0]
        height = img.size[1]
        print (width, " ", height)
        for i in range(0, width):
            temp = []
            for j in range(0, height):
                temp.append(pix[(i, j)][0]*0.2126 + pix[(i, j)][1]*0.5786 + pix[(i, j)][2]*0.0072)
            bright.append(temp)

        #Расчет коэффициента резкости
        RQ = 0.0
        K = 255.0
        for i in range (1, width):
            for j in range(1, height):
                r = (abs(bright[i][j]-bright[i-1][j]) + abs(bright[i][j]-bright[i][j-1]))
                RQ += ( r*r/((width - 1)*(height-1)*K))
        print(RQ)
        return RQ
    def solve(self):
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        maxI = 0
        maxRQ = self.calculate(onlyfiles[0])
        for i in range(1, len(onlyfiles)):
            k = self.calculate(onlyfiles[i])
            if k > maxRQ:
                maxRQ = k
                maxI = i
        return onlyfiles[maxI]
          


#открытие фотографии (test)
"""
maxI = 0

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
maxRQ = calculate(onlyfiles[0])
print (onlyfiles)



def calcAll(onlyfiles):
    for i in range(1, len(onlyfiles)):
        k = calculate(onlyfiles[i])
        if k > maxRQ:
            maxRQ = k
            maxI = i
    return onlyfiles[i]
"""


root = tk.Tk()
root.withdraw()

yoooo = filedialog.askdirectory()


obj = sharpening(yoooo)
print (obj.solve())