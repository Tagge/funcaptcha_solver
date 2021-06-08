# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:35:47 2020

@author: Thomas
"""

"""
So, what does this do ?

Same file as db_maker.py, except that creating a db is now a function.
Why did I do that ? Laziness.
"""

import numpy as np
import cv2
import json
import pickle
from os import listdir

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True)


def getCenterOfGravity(cloud):
   xMean = 0
   yMean = 0
   for point in range(0,len(cloud)):
       xMean += cloud[point][0][0]
       yMean += cloud[point][0][1]
   xMean = xMean / len(cloud)
   yMean = yMean / len(cloud)
   return (xMean,yMean) 

def processImage(imagePath):
    img = cv2.imread(imagePath)
    imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgg = cv2.GaussianBlur(imgg,(5,5),cv2.BORDER_DEFAULT)
    imgg = cv2.threshold(imgg, 252, 255, cv2.THRESH_BINARY_INV)[1]
    contours, hierarchy = cv2.findContours(imgg, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea)
    return c

def adjustCloud(cloud):
    centerOfGravity = getCenterOfGravity(cloud)
    for point in range(0, len(cloud)):
        cloud[point][0][0] -= centerOfGravity[0]
        cloud[point][0][1] -= centerOfGravity[1]

def processAndSave(fileName, data):
    #with open('image.p', 'rb') as infile:
    #    imageArray = pickle.load(infile)
    imageArray = data
    img = cv2.imread("all/bad/"+fileName)
    imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgg = cv2.GaussianBlur(imgg,(5,5),cv2.BORDER_DEFAULT)
    imgg = cv2.threshold(imgg, 252, 255, cv2.THRESH_BINARY_INV)[1]
    imageArray[fileName] = imgg
    return imageArray

def createDb():   
    allPics = listdir("all/bad")
    data = {}
    for picture in allPics:
        data = processAndSave(picture, data)
    with open('image.p', 'wb') as outfile:
        pickle.dump(data, outfile, protocol=pickle.HIGHEST_PROTOCOL)
