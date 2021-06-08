# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:35:47 2020

@author: Thomas
"""

"""
So, what does this do ?

This is the brain of the project. Our model computes an adjusted cloud of points for every image and matches it with an image in our comparison set of correct and incorrect images that has the least deviation.
"""

import numpy as np
import cv2
import pickle
import math
from os import listdir
from PIL import Image


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

def adjustCloud(cloud):
    centerOfGravity = getCenterOfGravity(cloud)
    imageCenter = (55,55)
    change = [0,0]
    change[0] = centerOfGravity[0] - imageCenter[0]
    change[1] = centerOfGravity[1] - imageCenter[1]
    for point in range(0, len(cloud)):
        cloud[point][0][0] -= change[0]
        cloud[point][0][1] -= change[1]
        
#Attempt at making an heuristic by calculating the inertia of our cloud of points at the center of gravity of said cloud of points
#My hope was that the inertia would be sort of unique for animals that were upright, but not so unique that it would fail to recognize animals with slight variations to their morphology
#It ended up not being differentiable enough, so not usable
def calculateInertia(cloud):
    gravCenter = getCenterOfGravity(cloud)
    inertia = 0
    for point in range(0, len(cloud)):
        distance = math.sqrt((cloud[point][0][0] - gravCenter[0])**2) + math.sqrt((cloud[point][0][1] - gravCenter[1])**2)
        inertia += distance
    inertia *= (1/len(cloud))
    return inertia

    
def getResult(pilImage):
    
    loadedImage = np.array(pilImage)
    trans_mask = loadedImage[:,:,3] == 0
    loadedImage[trans_mask] = [255, 255, 255, 255]
    loadedImage = cv2.cvtColor(loadedImage, cv2.COLOR_BGRA2BGR)
    newImage = cv2.cvtColor(loadedImage, cv2.COLOR_RGB2GRAY)
    newImage = cv2.GaussianBlur(newImage,(5,5),cv2.BORDER_DEFAULT)
    newImage = cv2.threshold(newImage, 252, 255, cv2.THRESH_BINARY_INV)[1]
    contours, hierarchy = cv2.findContours(newImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    c = max(contours, key = cv2.contourArea)
    adjustCloud(c)
    mask = np.zeros(newImage.shape, np.uint8)
    cv2.drawContours(mask, [c], -1, 255, cv2.FILLED)
    bestPercentage = 100.0
    bestPicture = ""
    goodPics = listdir("all/good")
    with open('image.p', 'rb') as infile:
        allPics = pickle.load(infile)
    
    for nb, (key, value) in enumerate(allPics.items()):
        res = cv2.absdiff(mask, value)
        res = res.astype(np.uint8)
        percentage = (np.count_nonzero(res) * 100)/res.size
        if(percentage < bestPercentage):
            bestPercentage = percentage
            bestPicture = key

    if(bestPicture in goodPics):
        return True
    else:
        return False
    
