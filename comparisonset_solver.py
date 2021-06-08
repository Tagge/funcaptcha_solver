# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:32:50 2020

@author: Admin_TG
"""

"""
So, what does this do ?

It just sends a challenge to 2Captcha to have it solved. It returns the correct orientation as an angle in degrees.
"""

import requests
import time
from PIL import Image

api_key = "9e431e5aac38391dde4356b1ecca9e1e"

def sendChallenge(image):
    global api_key
    print("Sending image to 2captcha")
    payload = {"key":api_key, "method":"rotatecaptcha"}
    image.save("tmp_im.png", "PNG")
    image = {'file_1': ("tmp_im.png", open("tmp_im.png", "rb"), 'image/png')}
    endpoint = "https://2captcha.com/in.php"
    response = requests.post(endpoint, data=payload, files=image)
    return response.text

def getOrientation(scanId):
    global api_key
    response = requests.get("https://2captcha.com/res.php?key="+api_key+"&action=get&id="+scanId)
    return response.text

def processChallenge(image):
    solveId = sendChallenge(image).replace("OK|", "")
    if(solveId.startswith("ERROR") == True):
        return "FAILED"
    time.sleep(5)
    orientation = getOrientation(solveId)
    if(orientation.startswith("ERROR") == True):
        return "FAILED"
    tries = 0
    while(orientation == "CAPCHA_NOT_READY" and tries < 10):
        time.sleep(5)
        orientation = getOrientation(solveId)
        tries = tries + 1 
    if(orientation.startswith("ERROR") == True):
        return "FAILED"
    if(orientation == "CAPCHA_NOT_READY"):
        return "FAILED"
    orientation = orientation.split("|")[1]
    return orientation
    
    
    
