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



def get_BaseProject_Path():
    ### NOTE: Set the directory to the actual folder of this file or Change to Editor Directory in Canopy 

    fp = os.getcwd()
    fp1=os.path.dirname(fp)
    fp2=os.path.dirname(fp1)
    return(fp2)
    

base_dir = get_BaseProject_Path()
print(base_dir)
cnet_data_path = base_dir + "\\data\\cnet\\"

#webdriver_path = "C:\\Chrome\\chromedriver_win32\chromedriver.exe"    
webdriver_path = base_dir + "\\src\\webdriver\\chromedriver_win32\\chromedriver.exe"    
print(webdriver_path)

def get_html_stream(url):
    """ gets html stream for given URL
    """
    driver = webdriver.Chrome(executable_path=webdriver_path)
    driver.get(url)
    time.sleep(15)
    #WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "the-element-id"))) # waits till the element with the specific id appears
    soup =  html.fromstring(driver.page_source)
    driver.quit()
    return (soup)

def get_CNET_User_Reviews(url, fname):
    soup = get_html_stream(url )

    web_page_content = soup.xpath('//time[@class="fyre-comment-date"]/text() | //div[@class="fyre-comment"]/p/text()') 
    print(web_page_content)
    print(len(web_page_content))
    print(type(web_page_content))

    thefile = open(cnet_data_path+"\\"+ fname, "w") #encoding="latin-1")

    for item in web_page_content:
        thefile.write("%s\n" % item.encode('utf-8'))
    thefile.close()

    return(web_page_content)

# Amazon Echo - CNET review
strm = get_CNET_User_Reviews('https://www.cnet.com/products/amazon-echo/user-reviews/', 'Amazon_Echo_User_Reviews.txt')
print(strm)

# Google Home - CNET review
strm = get_CNET_User_Reviews('https://www.cnet.com/products/google-home/user-reviews/', 'Google_Home_User_Reviews.txt')
print(strm)


def get_CNET_Product_Review(url, fname):
    soup = get_html_stream(url )
    
    #g_data  = soup.findAll(True, {"class":["stars-rating", "theGood", "theBad", "theBottomLine", "description"]})
#    web_page_content = soup.xpath('//time[@class="dtreviewed"]/text() | //time[@class="seodtreviewed"]/text() | //p[@class="theBad"]/span/text() | //p[@class="theGood"]/span/text() |  //p[@class="theBottomLine"]/span/text() | //div[@id="editorReview"]/p/text()') 
    web_page_content = soup.xpath('//time[@class="seodtreviewed"]/text() | //p[@class="theBad"]/span/text() | //p[@class="theGood"]/span/text() |  //p[@class="theBottomLine"]/span/text() | //div[@id="editorReview"]/p/text()') 
    web_page_content[0] = web_page_content[0].strip()
    print(web_page_content)
    print(len(web_page_content))
    print(type(web_page_content))

    thefile = open(cnet_data_path+"\\"+ fname, "w")

    for item in web_page_content:
        thefile.write("%s\n" % item.encode('utf-8'))
    thefile.close()

    return(web_page_content)

# Amazon Echo - CNET review
strm = get_CNET_Product_Review('https://www.cnet.com/products/amazon-echo-review/', 'Amazon_Echo_Editor_Review.txt')
print(strm)
print(len(strm))
# Google Home - CNET review
strm = get_CNET_Product_Review('https://www.cnet.com/products/google-home/review/', 'Google_Home_Editor_Review.txt')
print(strm)

