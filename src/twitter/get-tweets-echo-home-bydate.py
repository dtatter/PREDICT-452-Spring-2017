# Python code that uses selenium to scrape Twitter advanced search tweets 
#for tweets containing #AmazonEcho #GoogleHome at specific dates in each yearly Quarter

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome('/Users/jnakfour/Downloads/chromedriver')



# Function the executes the url in the browser
# simulates a page down
# captures data in files
def twitter_search_loop(product, url, searchYear):
    browser.get(url)
    time.sleep(1)

    body=browser.find_element_by_tag_name('body')


    #pushing page down 100 times
    for _ in range(100):
        print("Down")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    # Get all the text and save in a *.txt file for later sentiment processing. 
    # This will be just a plain text file with all the tweet text bodies
    # a new line between tweets
    # Populate another file with date,text of tweet
    # data file location ../../data/twitter/
    fulltext_filename = product + '_tweet_text_file.txt'
    datetext_filename = product + '_tweet_date_text_file.txt'
    path='../../data/twitter/'
    tweets_body = browser.find_elements_by_class_name('js-stream-tweet')
    fulltext_fileIO = open(path+fulltext_filename, "a")
    datetext_fileIO = open(path+datetext_filename, "a")
    for tweet in tweets_body:
        tweets_text = tweet.find_elements_by_class_name('tweet-text')
        tweets_date = tweet.find_elements_by_class_name('_timestamp')
        print(tweets_text[0].text.encode('utf-8'))
        print(tweets_date[0].text.encode('utf-8'))
        
        fulltext_fileIO.write("%s " % tweets_text[0].text.encode('utf-8'))
        if searchYear is None:
            datetext_fileIO.write('%s\t%s\n' % (tweets_text[0].text.encode('utf-8'), tweets_date[0].text.encode('utf-8')))
        else:
            print(searchYear.encode('utf-8'))
            datetext_fileIO.write('%s\t%s %s\n' % (tweets_text[0].text.encode('utf-8'), tweets_date[0].text.encode('utf-8'),searchYear.encode('utf-8')))
    fulltext_fileIO.close()
    datetext_fileIO.close()
  
################################ 2017 ###############################
################################ Q2 #############################
# 2017 Second Quarter Amazon Echo
# Twitter Advanced Search fields
# These hashtags: #amazonecho
# Written in : English
# From this date: 2017-05-15 to 2017-05-18
url='https://twitter.com/search?l=en&q=%23amazonecho%20since%3A2017-05-15%20until%3A2017-05-18&src=typd&lang=en'
twitter_search_loop("amazonecho",url,"2017")

# 2017 Second Quarter Google Home
# Twitter Advanced Search fields
# These hashtags: #googlehome
# Written in : English
# From this date: 2017-05-15 to 2017-05-18
url="https://twitter.com/search?l=en&q=%23googlehome%20since%3A2017-05-15%20until%3A2017-05-18&src=typd&lang=en"
twitter_search_loop("googlehome",url,"2017")

################################ Q1 #############################
# 2017 First Quarter Amazon Echo
# Twitter Advanced Search fields
# These hashtags: #amazonecho
# Written in : English
# From this date: 2017-03-06 to 2017-03-17
url='https://twitter.com/search?l=en&q=%23amazonecho%20since%3A2017-03-06%20until%3A2017-03-17&src=typd&lang=en'
twitter_search_loop("amazonecho",url,"2017")

# 2017 First Quarter Google Home
# Twitter Advanced Search fields
# These hashtags: #googlehome
# Written in : English
# From this date: 2017-03-06 to 2017-03-17
url='https://twitter.com/search?l=en&q=%23googlehome%20since%3A2017-03-06%20until%3A2017-03-17&src=typd&lang=en'
twitter_search_loop("googlehome",url,"2017")

################################ 2016 ###############################
################################ Q4 #############################
# 2016 forth Quarter Amazon Echo
# Twitter Advanced Search fields
# These hashtags: #amazonecho
# Written in : English
# From this date: 2016-11-07 to 2016-11-19
url='https://twitter.com/search?l=en&q=%23amazonecho%20since%3A2016-11-07%20until%3A2016-11-19&src=typd&lang=en'
twitter_search_loop("amazonecho",url,None)

# 2016 forth Quarter Google Home
# Twitter Advanced Search fields
# These hashtags: #googlehome
# Written in : English
# From this date: 2016-11-07 to 2016-11-19
url='https://twitter.com/search?l=en&q=%23googlehome%20since%3A2016-11-07%20until%3A2016-11-19&src=typd&lang=en'
twitter_search_loop("googlehome",url,None)

################################ Q3 #############################
# 2016 third Quarter Amazon Echo
# Twitter Advanced Search fields
# These hashtags: #amazonecho
# Written in : English
# From this date: 2016-08-15 to 2016-08-27
url='https://twitter.com/search?l=en&q=%23amazonecho%20since%3A2016-08-15%20until%3A2016-08-27&src=typd&lang=en'
twitter_search_loop("amazonecho",url,None)

# 2016 third Quarter Google Home
# Twitter Advanced Search fields
# These hashtags: #googlehome
# Written in : English
# From this date: 2016-08-15 to 2016-08-27
url='https://twitter.com/search?l=en&q=%23googlehome%20since%3A2016-08-15%20until%3A2016-08-27&src=typd&lang=en'
twitter_search_loop("googlehome",url,None)

################################ Q2 #############################
# 2016 second Quarter Amazon Echo
# Twitter Advanced Search fields
# These hashtags: #amazonecho
# Written in : English
# From this date: 2016-05-09 to 2016-05-21
url='https://twitter.com/search?l=en&q=%23amazonecho%20since%3A2016-05-09%20until%3A2016-05-21&src=typd&lang=en'
twitter_search_loop("amazonecho",url,None)

# 2016 second Quarter Google Home
# Twitter Advanced Search fields
# These hashtags: #googlehome
# Written in : English
# From this date: 2016-05-09 to 2016-05-21
url='https://twitter.com/search?l=en&q=%23googlehome%20since%3A2016-05-09%20until%3A2016-05-21&src=typd&lang=en'
twitter_search_loop("googlehome",url,None)

################################ Q1 #############################
# 2016 first Quarter Amazon Echo
# Twitter Advanced Search fields
# These hashtags: #amazonecho
# Written in : English
# From this date: 2016-03-06 to 2016-03-17
url='https://twitter.com/search?l=en&q=%23amazonecho%20since%3A2016-03-06%20until%3A2016-03-17&src=typd&lang=en'
twitter_search_loop("amazonecho",url,None)

# 2016 first Quarter Google Home
# Twitter Advanced Search fields
# These hashtags: #googlehome
# Written in : English
# From this date: 2016-03-06 to 2016-03-17
url='https://twitter.com/search?l=en&q=%23googlehome%20since%3A2016-03-06%20until%3A2016-03-17&src=typd&lang=en'
twitter_search_loop("googlehome",url,None)
