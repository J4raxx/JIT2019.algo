import tkinter as tk
from tkinter import filedialog
from PIL import Image
from math import sqrt
import cv2
import argparse
from os import listdir
from os.path import isfile, join




path = ""


def calculate(pathToFile):
	global path
	img = Image.open(path+'/'+pathToFile)
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
	return RQ



#открытие фотографии (test)
"""
root = tk.Tk()
root.withdraw()

path = filedialog.askdirectory()
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
