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

import model
import numpy as np
import cv2
import json
import pickle
from os import listdir

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True)

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
