# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:50:20 2020

@author: Thomas
"""

"""
This file records new challenges that can then be sorted to create a comparison set.
It can be run multiple times. It checks for challenges that would have already been solvable and doesn't save them if that's the case.
"""

import model
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox");
chrome_options.add_argument("--incognito");
chrome_options.add_argument("--disable-gpu");
chrome_options.add_argument("--user-agent="+user_agent)

chrome_driver = os.getcwd() + "/chromedriver.exe"

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

def recordChallenge(fileName):
    
    driver.get("https://funcaptcha.com/fc/api/nojs/?pkey=9F35E182-C93C-EBCC-A31D-CF8ED317B996")
    start_button = driver.find_element_by_id("verify_btn")
    start_button.click()
    
    rot40 = Image.open(BytesIO(requests.get(driver.find_element_by_class_name("rot-40").get_attribute("src")).content))
    os.mkdir(os.getcwd()+"/"+fileName)
    
    rot40 = rot40.rotate(40,expand=False,resample=Image.BICUBIC)
    rot80 = rot40.rotate(40,expand=False,resample=Image.BICUBIC)
    rot120 = rot80.rotate(40,expand=False,resample=Image.BICUBIC)
    rot160 = rot120.rotate(40,expand=False,resample=Image.BICUBIC)
    rot200 = rot160.rotate(40,expand=False,resample=Image.BICUBIC)
    rot240 = rot200.rotate(40,expand=False,resample=Image.BICUBIC)
    rot280 = rot240.rotate(40,expand=False,resample=Image.BICUBIC)
    rot320 = rot280.rotate(40,expand=False,resample=Image.BICUBIC)
  
    rot40.save(fileName+"/40"+fileName+".png", "PNG")
    rot80.save(fileName+"/80"+fileName+".png", "PNG")
    rot120.save(fileName+"/120"+fileName+".png", "PNG")
    rot160.save(fileName+"/160"+fileName+".png", "PNG")
    rot200.save(fileName+"/200"+fileName+".png", "PNG")
    rot240.save(fileName+"/240"+fileName+".png", "PNG")
    rot280.save(fileName+"/280"+fileName+".png", "PNG")
    rot320.save(fileName+"/320"+fileName+".png", "PNG")
    
    driver.get_screenshot_as_file(fileName+"/full.png")
    rot40Test = model.getResult(rot40)
    if(rot40Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot40.save("positive/"+fileName+".png", "PNG")
        return
    rot80Test = model.getResult(rot80)
    if(rot80Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot80.save("positive/"+fileName+".png", "PNG")
        return
    rot120Test = model.getResult(rot120)
    if(rot120Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot120.save("positive/"+fileName+".png", "PNG")
        return
    rot160Test = model.getResult(rot160)
    if(rot160Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot160.save("positive/"+fileName+".png", "PNG")
        return
    rot200Test = model.getResult(rot200)
    if(rot200Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot200.save("positive/"+fileName+".png", "PNG")
        return
    rot240Test = model.getResult(rot240)
    if(rot240Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot240.save("positive/"+fileName+".png", "PNG")
        return
    rot280Test = model.getResult(rot280)
    if(rot280Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot280.save("positive/"+fileName+".png", "PNG")
        return
    rot320Test = model.getResult(rot320)
    if(rot320Test):
        print("A positive match has been registered. Deleting folder now and saving the match ...")
        rot320.save("positive/"+fileName+".png", "PNG")
        return
    


for i in range(0,100):
    recordChallenge(str(i))
