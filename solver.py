# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:50:20 2020

@author: Thomas
"""

"""
So, what does this do ?

This is the live solver. It opens a page to a captcha, and then proceeds to solve it live. Headless mode can be disabled to see it in action.

"""

import model
import time
import shutil
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox");
chrome_options.add_argument("--incognito");
chrome_options.add_argument("--disable-gpu");
chrome_options.add_argument("--user-agent="+user_agent)


if(sys.argv[1] != "none"):
    chrome_options.add_argument("--proxy-server=%s" % sys.argv[1]);

chrome_driver = "chromedriver.exe"

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

def solveChallenge(apikey):

    
    if(apikey == "none"):
        apikey = "9F35E182-C93C-EBCC-A31D-CF8ED317B996"

    driver.get("https://funcaptcha.com/fc/api/nojs/?pkey="+apikey)
    driver.save_screenshot("screenshot.png")
    start_button = driver.find_element_by_id("verify_btn")
    start_button.click()
    count = 0
    while(len(driver.find_elements_by_id("victoryScreen")) == 0):
        driver.save_screenshot("hey"+str(count)+".png")
        count += 1
        rot40 = Image.open(BytesIO(requests.get(driver.find_element_by_class_name("rot-40").get_attribute("src")).content))
        rot40 = rot40.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot80 = rot40.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot120 = rot80.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot160 = rot120.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot200 = rot160.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot240 = rot200.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot280 = rot240.rotate(360-40,expand=False,resample=Image.BICUBIC)
        rot320 = rot280.rotate(360-40,expand=False,resample=Image.BICUBIC)


        indicator = False
        while(1==1):
            rot40Test = another_proto.getResult(rot40) 
            if(rot40Test):
                driver.find_element_by_class_name("rot-40").click()
                break
            rot80Test = another_proto.getResult(rot80)
            if(rot80Test):
                driver.find_element_by_class_name("rot-80").click()
                break
            rot120Test = another_proto.getResult(rot120)
            if(rot120Test):
                driver.find_element_by_class_name("rot-120").click()
                break
            rot160Test = another_proto.getResult(rot160)
            if(rot160Test):
                driver.find_element_by_class_name("rot-160").click()
                break
            rot200Test = another_proto.getResult(rot200)
            if(rot200Test):
                driver.find_element_by_class_name("rot-200").click()
                break
            rot240Test = another_proto.getResult(rot240)
            if(rot240Test):
                driver.find_element_by_class_name("rot-240").click()
                break
            rot280Test = another_proto.getResult(rot280)
            if(rot280Test):
                driver.find_element_by_class_name("rot-280").click()
                break
            rot320Test = another_proto.getResult(rot320)
            if(rot320Test):
                driver.find_element_by_class_name("rot-320").click()
                break
            indicator = True
            break
        if(indicator):
            break
    return driver.find_element_by_id("verification-code").get_attribute("value")
token = ""
tries = 0
while(len(token) == 0 and tries < 100):
    try:
        token = solveChallenge(sys.argv[2])
    except:
        print()
    tries += 1
if len(token) == 0:
    token = "Timeout"
print(token)
driver.close()
driver.quit()
