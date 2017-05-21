# -*- coding: utf-8 -*-
# Extracting and Parsing Web Site Data (Python)

# prepare for Python version 3x features and functions
from __future__ import division, print_function
from bs4 import BeautifulSoup  # DOM html manipulation
from selenium import webdriver
from lxml import html  # functions for parsing HTML

from future_builtins import ascii, filter, hex, map, oct, zip

import nltk  # draw on the Python natural language toolkit
from nltk.corpus import PlaintextCorpusReader

# import packages for web scraping/parsing
import requests  # functions for interacting with web pages
import time 
import os
import json
import re
import pandas as pd
import numpy as np
import csv

def get_BaseProject_Path():
    ### NOTE: Set the directory to the actual folder of this file or Change to Editor Directory in Canopy 

    fp = os.getcwd()
    fp1=os.path.dirname(fp)
    fp2=os.path.dirname(fp1)
    return(fp2)
    

base_dir = get_BaseProject_Path()
print(base_dir)
data_path = base_dir + "\\data\\"
config_data_path = base_dir + "\\src\\sentiment\\config-files\\"
print(data_path)
print(config_data_path)


twtr_data_path = base_dir + "\\data\\twitter\\"
fb_data_path = base_dir + "\\data\\facebook\\"
cnet_data_path = base_dir + "\\data\\cnet\\"
sentiment_out_path = base_dir + "\\output\\"
################################################
# import codebook and stoplists
################################################
stoplist = []
with open(config_data_path+'stoplist.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        stoplist.append(row)
stoplist
    
codebook=[]
with open(config_data_path+'codebook.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #skip header
    next(reader)
    for row in reader:
        codebook.append(row)
print(codebook)

#codebook.sort(reverse=True)    
# define list of codes to be dropped from document
# carriage-returns, line-feeds, tabs
codelist = ['\r', '\n', '\t']    

################################################
## web page parsing function for creating text document 
################################################

def page_parse(string):
    # replace non-alphanumeric with space 
    temp_string = re.sub('[^a-zA-Z]', '  ', string)    
    # replace codes with space
    for i in range(len(codelist)):
        stopstring = ' ' + str(codelist[i]) + '  '
        temp_string = re.sub(stopstring, '  ', temp_string)      
    # replace single-character words with space
    temp_string = re.sub('\s.\s', ' ', temp_string)   
    # convert uppercase to lowercase
    temp_string = temp_string.lower()    
    # replace selected character strings/stop-words with space
    for i in range(len(stoplist)):
        stopstring = ' ' + str(stoplist[i][0]) + ' '
        temp_string = re.sub(stopstring, ' ', temp_string)        
    # replace selected character strings/codebooks with alternate words
    for i in range(len(codebook)):
        cb_orig_string = ' ' +str(codebook[i][0])+ ' '
        cb_repl_string = ' ' +str(codebook[i][1])+ ' '
        temp_string = re.sub(cb_orig_string, cb_repl_string, temp_string)        
    # replace multiple blank characters with one blank character
    temp_string = re.sub('\s+', ' ', temp_string)    
    return(temp_string)    

#temp_string= 'ab amazon is out best they js amazon echo  echo home google home alexa'
#for i in range(len(codebook)):
#    temp_string = re.sub(' '+codebook[i][0]+' ', ' '+codebook[i][1]+' ', temp_string)  
#    print(codebook[i][0] + ": "+temp_string) 
#ret_val = page_parse('ab amazon is out best they js amazon echo ')
#print(ret_val)

#temp_string = re.sub('amazon echo', 'amazonecho', 'ab amazon is out best they js amazon echo ')  
#print(temp_string)       
################################################
##  Quarters Lookup data
################################################
def load_quarters():
    
    quarters_df = pd.read_csv(config_data_path+'calendar_by_quarters.csv', index_col=None, parse_dates=True)
    print(quarters_df)
    quarters_df['start_date'] = pd.to_datetime(quarters_df.start_date)
    quarters_df['end_date'] = pd.to_datetime(quarters_df.end_date)
    quarters_df['start_date'] = quarters_df['start_date'].dt.strftime('%Y-%m-%d')
    quarters_df['end_date'] = quarters_df['end_date'].dt.strftime('%Y-%m-%d')
    return(quarters_df)

    
################################################
##  Join Quarters for a Date in another dataframe
################################################
def assign_calendar(qtrs_df, content_df):
    content_df['quarter'] = np.nan
    for index, ser in qtrs_df.iterrows():
        in_interval = (content_df['date'] >= ser['start_date']) & \
                      (content_df['date'] <= ser['end_date'])
        content_df['quarter'][in_interval] = ser['quarter']

    result = content_df.merge(qtrs_df, how='inner').sort_values(by='date').reset_index(drop=True)
    return ( result)




################################################
##  Convert a single column List to two column 
##  data frame: Date, Content
################################################
def text_to_dataframe(web_page_content):
    import datetime
    import time
    from datetime import date
    web_page_content[0] = web_page_content[0].strip()
    dt=[]
    comments=[]
    r = 0
    val= ''
    #dtr = ''
    i = 0
    print(len(web_page_content))
    for row in web_page_content:
        try:
            i = i + 1
            print("row " + str(len(row))+ "> " + str(i) + ": " +row.strip(' \t\n\r'))
            dtr = datetime.datetime.strptime(row.strip(' \t\n\r') , "%B %d, %Y").date() 
            print(dtr)
            #print(datetime.datetime.strptime("September 28, 2016", "%B %d, %Y").date())
            dt.append(dtr)
            #dtr=''
            if(r >0 ): 
                comments.append(val)
                val = ''
                print("text")
                print(val)
            r = r+1
        except ValueError, e:
            val = val + ' ' + row
            #print(dtr)
            if(i == len(web_page_content) ): 
                comments.append(val)
                val = ''
            continue    
    
    print("Date Length: "+str(len(dt)))
    print("Comments Length: " + str(len(comments)))
    print("Comments Text: " + comments[0])
    print(dt)
    import pandas as pd
    #Combine the stories into a Data Frame and remove any that argen't target stories
    results = pd.DataFrame({'date':dt, 'content': comments}, dtype='str')
    
    ##Create Date
    results['date'] = results['date'].astype('str')
    #results['date'] = results['date'].str[2:13]
    results['date'] = pd.to_datetime(results['date'])
    
    #Fix content problems
    results['content'] = results['content'].astype('str')
    #results['content'] = results['content'].apply(text_parse)
    print("data frame")
    print(results['date'])
    print(results['content'])
    
    
#    print(results['date'][len(results['date'])-1])  
#    print(results['content'][len(results['content'])-1])  
#    print(len(dt))
#    print(len(comments))
    
    return(results)
##############

################################################
##  Load CNET data
################################################
def load_cnet_data():
    
    text_file = open(os.path.join(cnet_data_path, 'Amazon_Echo_Editor_Review.txt'), "r")
    lines = text_file.readlines()
#    print (text_file)
#    print (len(lines))
    text_file.close()
    cnet_amzn_editor_df = text_to_dataframe(lines)           
#    print(type(cnet_amzn_editor_df))
#    print(cnet_amzn_editor_df)

    text_file = open(os.path.join(cnet_data_path, 'Amazon_Echo_User_Reviews.txt'), "r")
    lines = text_file.readlines()
#    print (text_file)
#    print (len(lines))
    text_file.close()
    cnet_amzn_user_df = text_to_dataframe(lines)           
#    print(type(cnet_amzn_user_df))
#    print(cnet_amzn_user_df)

    cnet_amzn_df = pd.concat([cnet_amzn_user_df,cnet_amzn_editor_df])
#    print(cnet_amzn_df)

    cnet_amzn_df['date'] = pd.to_datetime(cnet_amzn_df['date'])
    cnet_amzn_df = cnet_amzn_df.dropna()
    cnet_amzn_df['date'] = cnet_amzn_df['date'].dt.strftime('%Y-%m-%d')    
    cnet_amzn_df = cnet_amzn_df.sort_values(by='date').reset_index(drop=True)
    cnet_amzn_df['source'] = "CNET"
    cnet_amzn_df['dataset'] = "Amazon"
        
    text_file = open(os.path.join(cnet_data_path, 'Google_Home_Editor_Review.txt'), "r")
    lines = text_file.readlines()
#    print (text_file)
#    print (len(lines))
    text_file.close()
    cnet_goog_editor_df = text_to_dataframe(lines)           
#    print(type(cnet_goog_editor_df))
#    print(cnet_goog_editor_df)

    text_file = open(os.path.join(cnet_data_path, 'Google_Home_User_Reviews.txt'), "r")
    lines = text_file.readlines()
#    print (text_file)
#    print (len(lines))
    text_file.close()
    cnet_goog_user_df = text_to_dataframe(lines)           
#    print(type(cnet_goog_user_df))
#    print(cnet_goog_user_df)

#        df = pd.append(my_df, ignore_index=True)
    cnet_goog_df = pd.concat([cnet_goog_user_df,cnet_goog_editor_df])
#    print(cnet_goog_df)

    cnet_goog_df['date'] = pd.to_datetime(cnet_goog_df['date'])
    cnet_goog_df = cnet_goog_df.dropna()
    cnet_goog_df['date'] = cnet_goog_df['date'].dt.strftime('%Y-%m-%d')    
    cnet_goog_df = cnet_goog_df.sort_values(by='date').reset_index(drop=True)
    cnet_goog_df['source'] = "CNET"
    cnet_goog_df['dataset'] = "Google"

    return(cnet_amzn_df,cnet_goog_df)
    


################################################
##  Load TWITTER data
################################################
def load_twitter_data():
    twtr_amzn_df = pd.read_csv(twtr_data_path+'amazonecho_tweet_date_text_file.txt', delimiter = '\t',index_col=None, header=None, parse_dates=True)
    twtr_amzn_df.columns=['content', 'date']
    twtr_amzn_df['date'] = pd.to_datetime(twtr_amzn_df['date'])
    twtr_amzn_df = twtr_amzn_df.dropna()
    twtr_amzn_df['date'] = twtr_amzn_df['date'].dt.strftime('%Y-%m-%d')    
    twtr_amzn_df = twtr_amzn_df.sort_values(by='date').reset_index(drop=True)
    twtr_amzn_df['source'] = "Twitter"
    twtr_amzn_df['dataset'] = "Amazon"
    
#    print(twtr_amzn_df)
#    print(type(twtr_amzn_df['date']))

    twtr_goog_df = pd.read_csv(twtr_data_path+'googlehome_tweet_date_text_file.txt', delimiter = '\t',index_col=None, header=None, parse_dates=True)
    twtr_goog_df.columns=['content', 'date']
    twtr_goog_df['date'] = pd.to_datetime(twtr_goog_df['date'])    
    twtr_goog_df = twtr_goog_df.dropna()
    twtr_goog_df['date'] = twtr_goog_df['date'].dt.strftime('%Y-%m-%d')    
    twtr_goog_df = twtr_goog_df.sort_values(by='date').reset_index(drop=True)
    twtr_goog_df['source'] = "Twitter"
    twtr_goog_df['dataset'] = "Google"
#    print(twtr_goog_df)
#    print(type(twtr_goog_df['date']))

    return(twtr_amzn_df, twtr_goog_df)

  

################################################
##  Load FACEBOOK data
################################################
def load_facebook_data():

    fb_amzn_df = pd.read_csv(twtr_data_path+'amazonecho_tweet_date_text_file.txt', delimiter = '\t',index_col=None, header=None, parse_dates=True)
    fb_amzn_df.columns=['content', 'date']
    fb_amzn_df['date'] = pd.to_datetime(fb_amzn_df['date'])    
    fb_amzn_df = fb_amzn_df.dropna()
    fb_amzn_df['date'] = fb_amzn_df['date'].dt.strftime('%Y-%m-%d')    
    fb_amzn_df = fb_amzn_df.sort_values(by='date').reset_index(drop=True)
    fb_amzn_df['source'] = "Facebook"
    fb_amzn_df['dataset'] = "Amazon"

    fb_goog_df = pd.read_csv(twtr_data_path+'amazonecho_tweet_date_text_file.txt', delimiter = '\t',index_col=None, header=None, parse_dates=True)
    fb_goog_df.columns=['content', 'date']
    fb_goog_df['date'] = pd.to_datetime(fb_goog_df['date'])    
    fb_goog_df = fb_goog_df.dropna()
    fb_goog_df['date'] = fb_goog_df['date'].dt.strftime('%Y-%m-%d')    
    fb_goog_df = fb_goog_df.sort_values(by='date').reset_index(drop=True)
    fb_goog_df['source'] = "Facebook"
    fb_goog_df['dataset'] = "Google"
    
    return(fb_amzn_df, fb_goog_df)

################################################
##  Load scoring dictionary
################################################
def generate_scoring_dictionary():
    # create lists of positive and negative words using Hu and Liu (2004) lists
    positive_list = PlaintextCorpusReader(config_data_path, 'Hu_Liu_positive_word_list.txt', encoding = 'latin-1')
    negative_list = PlaintextCorpusReader(config_data_path, 'Hu_Liu_negative_word_list.txt', encoding = 'latin-1')
    positive_words = positive_list.words()
    negative_words = negative_list.words()
    
    # define bag-of words dictionaries
    positive_scoring = dict([(positive_words, 1) for positive_words in positive_words])
    negative_scoring = dict([(negative_words, -1) for negative_words in negative_words])
    scoring_dictionary = dict(positive_scoring.items() + negative_scoring.items())
    
    return(scoring_dictionary)

################################################
##  Sentiment Scoring - By search term and corpus
################################################
def compute_sentiment_score(search_word, blogstring, scoring_dictionary):    
    # Because our interest is sentiment about Google Analytics,
    # let's see how often the search_word appears in the corpus.
    blogstring.count(search_word)  
    print(type(blogstring))    
    cnt = blogstring.count(search_word)  
    print(cnt)
    blogcorpus = blogstring.split()
    print(type(blogcorpus))    
    # see how many words are in the corpus 
    # subtracting the number of textdivider words 
    len(blogcorpus) - blogstring.count('xxxxxxxx')

        
    # list for assigning a score to every word in the blogcorpus
    # scores are -1 if in negative word list, +1 if in positive word list
    # and zero otherwise. We use a dictionary for scoring.
    blogscore = [0] * len(blogcorpus)  # initialize scoring list
    
    for iword in range(len(blogcorpus)):
        if blogcorpus[iword] in scoring_dictionary:
            blogscore[iword] = scoring_dictionary[blogcorpus[iword]]
            
    # report the norm sentiment score for the words in the corpus
    print('Corpus Average Sentiment Score:')
    corpus_SSA = round(sum(blogscore) / (len(blogcorpus) - blogstring.count('xxxxxxxx')), 3)
    print(corpus_SSA)        
    
    # Read the blogcorpus from beginning to end
    # identifying all the places where the search_word occurs.
    # We arbitrarily identify search-string-relevant words
    # to be those within three words of the search string.
    blogrelevant = [0] * len(blogcorpus)  # initialize blog-relevnat indicator
    blogrelevantgroup = [0] * len(blogcorpus)
    groupcount = 0  
    
    srch_str_relevant_word_count = 15
    
    for iword in range(len(blogcorpus)):
        if blogcorpus[iword] == search_word:
            groupcount = groupcount + 1
            for index in range(max(0,(iword - srch_str_relevant_word_count)),min((iword + srch_str_relevant_word_count+1), len(blogcorpus))):
                blogrelevant[index] = 1
                blogrelevantgroup[index] = groupcount
    
    # Compute the average sentiment score for the words nearby the search term.
    print('Average Sentiment Score Around Search Term:', search_word)
    search_term_SSA = round(sum((np.array(blogrelevant) * np.array(blogscore))) / sum(np.array(blogrelevant)),3)
    print(search_term_SSA)
    cnt = blogstring.count(search_word)  
    print(cnt)


    return(search_term_SSA, corpus_SSA)


# Step 1: Load Quarters
qtrs_df = load_quarters()
print(qtrs_df)

# Step 2: Load data from CNET
cnet_amzn_dfx, cnet_goog_dfx = load_cnet_data()      
print(cnet_amzn_dfx)

# Step 3: Load data from Twitter
twtr_amzn_dfx, twtr_goog_dfx = load_twitter_data()      
print(twtr_goog_dfx)

# Step 4: Load data from Facebook
fb_amzn_dfx, fb_goog_dfx = load_facebook_data()      
print(fb_goog_dfx)

# Step 5: Assign Quarters to CNET, Twitter & Facebook Data
# CNET
cnet_amzn_dfx = assign_calendar(qtrs_df, cnet_amzn_dfx)
print(cnet_amzn_dfx)

cnet_goog_dfx = assign_calendar(qtrs_df, cnet_goog_dfx)
print(cnet_goog_dfx)

# Twitter
twtr_amzn_dfx = assign_calendar(qtrs_df, twtr_amzn_dfx)
print(twtr_amzn_dfx)

twtr_goog_dfx = assign_calendar(qtrs_df, twtr_goog_dfx)
print(twtr_goog_dfx)

# Facebook
fb_amzn_dfx = assign_calendar(qtrs_df, fb_amzn_dfx)
print(fb_amzn_dfx)

fb_goog_dfx = assign_calendar(qtrs_df, fb_goog_dfx)
print(fb_goog_dfx)

# Step 6: Combine Amazon Data across CNET, Twitter & Facebook in one dataframe
#         Combine Google Data across CNET, Twitter & Facebook in one dataframe
amazon_dfx = pd.concat([cnet_amzn_dfx,twtr_amzn_dfx, fb_amzn_dfx])

google_dfx = pd.concat([cnet_goog_dfx,twtr_goog_dfx, fb_goog_dfx])

print(amazon_dfx)
print(google_dfx)

# Step 7: Combine 
# combine content based on quarters
amazon_df = amazon_dfx.groupby(['end_date'])['content'].apply(lambda x: 'xxxxxxxx ' .join(x)).reset_index()
#res1 = amazon_dfx.groupby(['quarter', 'source', 'dataset'])['content'].apply(lambda x: 'XXXXXX'.join(x)).reset_index()
print(amazon_df)

google_df = google_dfx.groupby(['end_date'])['content'].apply(lambda x: 'xxxxxxxx ' .join(x)).reset_index()
#res1 = amazon_dfx.groupby(['quarter', 'source', 'dataset'])['content'].apply(lambda x: 'XXXXXX'.join(x)).reset_index()
print(google_df)

# Step 8:
# Amazon Dataframe 
amazon_df['content1'] = ' '
amazon_df['search_term_score']=0.000
amazon_df['corpus_score']=0.000
for i,r in amazon_df.iterrows():
    str_val = r['content']
    ret_val = page_parse(str_val)
    amazon_df['content1'][i]=ret_val
    print('strval: '+ str(len(str_val)), 'retval: '+ str(len(ret_val)))
print(amazon_df)

# Google Dataframe 
google_df['content1'] = ' '
google_df['search_term_score']=0.000
google_df['corpus_score']=0.000
for i,r in google_df.iterrows():
    str_val = r['content']
    ret_val = page_parse(str_val)
    google_df['content1'][i]=ret_val
    print('strval: '+ str(len(str_val)), 'retval: '+ str(len(ret_val)))
print(google_df)

# Step 9: Loading scoring dictionary / bag of +ve and -ve words        
scoring_dict = generate_scoring_dictionary()

# Step 10: Compute Sentiment Scores (Corpus & Search word
search_word = 'amazonecho'            

for i,r in amazon_df.iterrows():
    str_val = r['content1']
    srch_score, corpus_score = compute_sentiment_score(search_word, str_val, scoring_dict)
    amazon_df['search_term_score'][i]=srch_score
    amazon_df['corpus_score'][i]=corpus_score
    
print(amazon_df)

search_word = 'googlehome'            

for i,r in google_df.iterrows():
    str_val = r['content1']
    srch_score, corpus_score = compute_sentiment_score(search_word, str_val, scoring_dict)
    google_df['search_term_score'][i]=srch_score
    google_df['corpus_score'][i]=corpus_score
    
print(google_df)


# Amazon Sentiments
import numpy as np
import matplotlib.pyplot as plt
dt = pd.to_datetime(amazon_df['end_date'])
sta = amazon_df['search_term_score']
cpa = amazon_df['corpus_score']
plt.plot(dt, sta, label='Search Term')
plt.plot(dt, cpa, label='Corpus')
plt.ylabel('Score')
plt.xlabel('Quarter End Date')
plt.title("Amazon Echo User Sentiment Score")
plt.grid(True)
plt.legend(loc='upper center', shadow=True)
plt.xticks(rotation = 90)
plt.show()
plt.savefig(sentiment_out_path+ 'amazon_user_sentiment.pdf')
plt.close()

# Google Sentiments
dt = pd.to_datetime(google_df['end_date'])
stg = google_df['search_term_score']
cpg = google_df['corpus_score']
plt.plot(dt, stg, label='Search Term')
plt.plot(dt, cpg, label='Corpus')
plt.ylabel('Score')
plt.xlabel('Quarter End Date')
plt.title("Google Home User Sentiment Score")
plt.grid(True)
plt.legend(loc='upper center', shadow=True)
plt.xticks(rotation = 90)
plt.show()
plt.savefig(sentiment_out_path+ 'google_user_sentiment.pdf')
plt.close()

# Google vs Amazon Sentiments
dt = pd.to_datetime(amazon_df['end_date'])
dtg = pd.to_datetime(google_df['end_date'])
sta = amazon_df['search_term_score']
stg = google_df['search_term_score']
plt.plot(dt, sta, label='Amazon - Search Term')
plt.plot(dtg, stg, label='Google - Search Term')
plt.ylabel('Score')
plt.xlabel('Quarter End Date')
plt.title("Amazon Echo & Google Home User Sentiment Score")
plt.legend(loc='upper center', shadow=True)
plt.grid(True)
plt.xticks(rotation = 90)
plt.show()
plt.savefig(sentiment_out_path+ 'amzon_google_sentiment.pdf')
plt.close()




################################################################################
# define counts of positive, negative, and total words in text document 
def count_words(text, word):    
    positive = [w for w in text.split() if w in word]
    return(len(positive))




