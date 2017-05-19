# -*- coding: utf-8 -*-
# Extracting and Parsing Web Site Data (Python)

# prepare for Python version 3x features and functions
from __future__ import division, print_function
from bs4 import BeautifulSoup  # DOM html manipulation
from selenium import webdriver
from lxml import html  # functions for parsing HTML

# import packages for web scraping/parsing
import requests  # functions for interacting with web pages
import time 
import os
import json


""" NOTE: Set the directory to the actual folder of this file or Change to Editor Directory in Canopy 
"""

def get_File_Path():
    fp = os.getcwd()
    return(fp)
    
def get_OutputFile_Path(current_dir,out_folder):    
    #os.chdir(os.path.dirname(current_dir))
    fp=os.path.dirname(current_dir)
    #os.chdir(fp+"\\"+out_folder)
    fp=fp+"\\"+out_folder #os.getcwd()
    print(fp)
    return(fp)

out_folder = "3. Outputs"
current_dir = get_File_Path()
save_to_path = get_OutputFile_Path(current_dir,out_folder)


def get_html_stream(url):
    """ gets html stream for given URL
    """
    driver = webdriver.Chrome(executable_path="C:\\Chrome\\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    time.sleep(15)
    #WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "the-element-id"))) # waits till the element with the specific id appears
    soup = BeautifulSoup(driver.page_source)
    driver.quit()
    return (soup)

def get_CNET_User_Reviews(url, fname):
    soup = get_html_stream(url )

    g_data  = soup.findAll(True, {"class":["fyre-comment-date", "fyre-review-title", "fyre-comment-username",  "fyre-review-subpart","fyre-comment", "fyre-reviews-rated", "fyre-reviews-helpful" ]})  #"fyre-review-subpart",

    thefile = open(save_to_path+"\\"+ fname, "w")

    for item in g_data:
        thefile.write("%s\n" % item)
    thefile.close()

    return(g_data)

# Amazon Echo - CNET review
strm = get_CNET_User_Reviews('https://www.cnet.com/products/amazon-echo/user-reviews/', 'Amazon_Echo_User_Reviews.txt')
print(strm)

# Google Home - CNET review
strm = get_CNET_User_Reviews('https://www.cnet.com/products/google-home/user-reviews/', 'Google_Home_User_Reviews.txt')
print(strm)


def get_CNET_Product_Review(url, fname):
    soup = get_html_stream(url )

    g_data  = soup.findAll(True, {"class":["stars-rating", "theGood", "theBad", "theBottomLine", "description"]})
    thefile = open(save_to_path+"\\"+ fname, "w")

    for item in g_data:
        thefile.write("%s\n" % item)
    thefile.close()

    return(g_data)

# Amazon Echo - CNET review
strm = get_CNET_Product_Review('https://www.cnet.com/products/amazon-echo-review/', 'Amazon_Echo_Editor_Review.txt')
print(strm)

# Google Home - CNET review
strm = get_CNET_Product_Review('https://www.cnet.com/products/google-home/review/', 'Google_Home_Editor_Review.txt')
print(strm)

