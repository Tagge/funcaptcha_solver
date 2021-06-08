# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:50:20 2020
@author: Thomas
"""

"""
So, what does this do ?
It was supposed to be an automatic trainer for when a new serie of images would appear.
Challenges are recorded using headless Chrome. We then proceed to find the image with the right orientation automatically with 2Captcha's API, saving us a lot of time spent manually training the model.
It proved inefficient because the results returned by 2Captcha were incorrect, even though it's supposed to be the work of a person ...
"""

import comparisonset_dbmaker
import comparisonset_solver
import requests
from datetime import date
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--incognito");
chrome_options.add_argument("--disable-gpu");
chrome_options.add_argument("--user-agent="+user_agent)

chrome_driver = os.getcwd() + "/chromedriver"

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

def recordChallenge(fileName):
    print("Starting a new challenge")
    driver.get("https://funcaptcha.com/fc/api/nojs/?pkey=9F35E182-C93C-EBCC-A31D-CF8ED317B996")

    try:
        start_button = driver.find_element_by_id("verify_btn")
        start_button.click()        
        rot40 = Image.open(BytesIO(requests.get(driver.find_element_by_class_name("rot-40").get_attribute("src")).content))
    except:
        return
    
    rightOrientation = startTraining_solver.processChallenge(rot40)
    if(rightOrientation == "FAILED" or int(rightOrientation) == 0):
        print("Recognition failed")
        return
    
    rightOrientationVerification = startTraining_solver.processChallenge(rot40)
    if(rightOrientationVerification == "FAILED" or int(rightOrientationVerification) == 0):
        print("Recognition failed")
        return
    
    if(rightOrientation != rightOrientationVerification):
        print("Value mismatch")
        return
    
    rightOrientation = 360 - int(rightOrientation)
    rot40 = rot40.rotate(40,expand=False,resample=Image.BICUBIC)
    rot80 = rot40.rotate(40,expand=False,resample=Image.BICUBIC)
    rot120 = rot80.rotate(40,expand=False,resample=Image.BICUBIC)
    rot160 = rot120.rotate(40,expand=False,resample=Image.BICUBIC)
    rot200 = rot160.rotate(40,expand=False,resample=Image.BICUBIC)
    rot240 = rot200.rotate(40,expand=False,resample=Image.BICUBIC)
    rot280 = rot240.rotate(40,expand=False,resample=Image.BICUBIC)
    rot320 = rot280.rotate(40,expand=False,resample=Image.BICUBIC)
  
    rot40.save("all/bad/40"+fileName+".png", "PNG")
    rot80.save("all/bad/80"+fileName+".png", "PNG")
    rot120.save("all/bad/120"+fileName+".png", "PNG")
    rot160.save("all/bad/160"+fileName+".png", "PNG")
    rot200.save("all/bad/200"+fileName+".png", "PNG")
    rot240.save("all/bad/240"+fileName+".png", "PNG")
    rot280.save("all/bad/280"+fileName+".png", "PNG")
    rot320.save("all/bad/320"+fileName+".png", "PNG")


    
    if(rightOrientation == 40):
        rot40.save("all/good/40"+fileName+".png", "PNG")
    elif(rightOrientation == 80):
        rot80.save("all/good/80"+fileName+".png", "PNG")
    elif(rightOrientation == 120):
        rot120.save("all/good/120"+fileName+".png", "PNG")
    elif(rightOrientation == 160):
        rot160.save("all/good/160"+fileName+".png", "PNG")
    elif(rightOrientation == 200):
        rot200.save("all/good/200"+fileName+".png", "PNG")
    elif(rightOrientation == 240):
        rot240.save("all/good/240"+fileName+".png", "PNG")
    elif(rightOrientation == 280):
        rot280.save("all/good/280"+fileName+".png", "PNG")
    elif(rightOrientation == 320):
        rot320.save("all/good/320"+fileName+".png", "PNG")
    else:
        print("Error. This step hasn't been saved")
    
today = date.today()
if(os.path.exists("all")):
    if(os.path.exists("all/good")):
        os.rename("all/good", "all/good"+today.strftime("%d%m%Y"))
        os.mkdir("all/good")
    else:
        os.mkdir("all/good")
    if(os.path.exists("all/bad")):
        os.rename("all/bad", "all/bad"+today.strftime("%d%m%Y"))
        os.mkdir("all/bad")
    else:
        os.mkdir("all/bad")
else:
    os.mkdir("all")
    os.mkdir("all/good")
    os.mkdir("all/bad")
i = 0
while(len(next(os.walk("all/good"))[2]) != 80):
    recordChallenge(str(i))
    i = i + 1
startTraining_dbmaker.createDb()
