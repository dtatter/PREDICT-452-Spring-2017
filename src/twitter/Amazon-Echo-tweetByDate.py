# This file gathers tweets for Amazon Echo and Google home
# This file plots tweets with # for either by date
# This file also saves tweets with in files
# Twitter Social Media Data Collection (Python)

# prepare for Python version 3x features and functions
from __future__ import division, print_function 

import twitter  # work with Twitter APIs
import json  # methods for working with JSON data
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np


windows_system = False  # set to True if this is a Windows computer
if windows_system:
    line_termination = '\r\n' # Windows line termination
if (windows_system == False):
    line_termination = '\n' # Unix/Linus/Mac line termination

# See Russell (2014) and Twitter site for documentation
# https://dev.twitter.com/rest/public
# Go to http://twitter.com/apps/new to provide an application name
# to Twitter and to obtain OAuth credentials to obtain API data

# -------------------------------------
# Twitter authorization a la Russell (2014) section 9.1
# Insert credentials in place of the "blah blah blah" strings 
# Sample usage of oauth() function
# twitter_api = oauth_login()    
def oauth_login():

    #JUANA TO-DO Clear keys before submitting
    CONSUMER_KEY = 'VWhYhxYNEI7HrU5LaekMa84gf'
    CONSUMER_SECRET = 'LoIydX5EQh5YbmPjVc2sbDjmJabyPw7VjaWdfk0JkYmr46bvtE'
    OAUTH_TOKEN = '778609197046964224-97OkSNtf4j90ViY3Y2IEYH21Nx5afmy'
    OAUTH_TOKEN_SECRET = 'UWN02HNs9ZqyJ6ZnlywzDMjf2LTqGyGATj0E43XkujPaS'
    
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

# -------------------------------------
# searching the REST API a la Russell (2014) section 9.4
#https://dev.twitter.com/rest/reference/get/search/tweets
#count cannot be more than a 100 tweets per call
#function that gets 100 tweets at a time and reads/requests next id
def twitter_search_loop(twitter_api, q, requested_max_results, **kw):
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and 
    # https://dev.twitter.com/docs/using-search for details on advanced 
    # search criteria that may be useful for keyword arguments
    
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets    
    #search_results = twitter_api.search.tweets(q=q, count=max_results, **kw)
    search_results = twitter_api.search.tweets(q=q,**kw)
    
    statuses = search_results['statuses']
    
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
   
    # Enforce a reasonable limit
    # Bumped up limit to 2000
    # Since there are many tweets, it only spans a couple of days
    max_results = min(2000, requested_max_results)
    print("Number of target tweets")
    print(max_results)
    
    for _ in range(20): # 20*100 = 2000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            print(e)
            break
         
       
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        #there is a bug, it is escaped twice
        #kwargs
        #{u'q': u'%2523MotivationMonday', u'count': u'100', u'include_entities': u'1', u'max_id': u'853990597971005439'}
        
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        #make sure we have the right search param
        #There is a bug in next_result, q is escaped twice, once for #, and another for %
        #kwargs
        #{u'q': u'%2523MotivationMonday', u'count': u'100', u'include_entities': u'1', u'max_id': u'853990597971005439'}
        # enforcing search term with out the double escape
        kwargs["q"] = q
        search_results = twitter_api.search.tweets(**kwargs)
        
        statuses += search_results['statuses']
        print("Number of tweets gathered")
        print(len(statuses))

        if len(statuses) > max_results: 
            print("Reached Max")
            break
    
         
    return statuses

def plotTweetByDate(tweetResults,fileName):
    # examining the results object... should be list of dictionary objects
    print('\n\ntype of results:', type(tweetResults)) 
    print('\nnumber of results:', len(tweetResults)) 
    print('\ntype of results elements:', type(tweetResults[0]))

    #--------------------------------------
    ## Read the list and save as a dictionary of json
    jsonTwitterList = []
    for tweet in tweetResults:
        jsonTwitterList.append(json.loads(json.dumps(tweet)))
    print(jsonTwitterList[0])
    
    # Create the dataframe we will use
    # Here we are gathering more information than needed
    # We plan to use this in other projects
    # For now we are only interesed in "created_at"
    tweets = pd.DataFrame()
    # We want to know when a tweet was sent
    tweets['created_at'] = map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), jsonTwitterList)
    # Who is the tweet owner
    tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], jsonTwitterList)
    # How many follower this user has
    tweets['user_followers_count'] = map(lambda tweet: tweet['user']['followers_count'], jsonTwitterList)
    # What is the tweet's content
    tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), jsonTwitterList)
    # If available what is the language the tweet is written in
    tweets['lang'] = map(lambda tweet: tweet['lang'], jsonTwitterList)
    # If available, where was the tweet sent from ?
    tweets['Location'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, jsonTwitterList)
    # How many times this tweet was retweeted and favorited
    tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], jsonTwitterList)
    tweets['favorite_count'] = map(lambda tweet: tweet['favorite_count'], jsonTwitterList)            
 


    ############## Creating the Table
    #Changing Date format
    #Creating Table with data as index, number of tweets as column
    dataFrm = pd.DataFrame(data=tweets['created_at'].value_counts())
    dataFrm.columns = ['number_tweets']

    #Adding a column for date
    dataFrm['date'] = dataFrm.index
     
       
    ########## Converting Dates to Days since it has the time
    #Extract the days
    days = [item.split(" ")[0] for item in dataFrm['date'].values]
    #Add a days column
    dataFrm['days'] = days
    #group by days
    grouped_tweets = dataFrm[['days', 'number_tweets']].groupby('days')

    tweet_growth = grouped_tweets.sum()

    #adding a days column
    tweet_growth['days']= tweet_growth.index

    ############### Plot a bar graph with number of tweets by date
    fig = plt.figure()
    tweetByDatePlot = plt.subplot(111)
    x_pos = np.arange(len(tweet_growth['days'].values))
    tweetByDatePlot.bar(x_pos, tweet_growth['number_tweets'].values, align='center')
    tweetByDatePlot.set_xticks(x_pos)
    tweetByDatePlot.set_title(q + ' Number of Tweet by Day')
    tweetByDatePlot.set_ylabel("number tweets")
    tweetByDatePlot.set_xticklabels(tweet_growth['days'].values)
    fig.savefig(fileName)
    
    
def saveTweetsInFiles(tweetResults,fileName):
    # name used for JSON file storage        
    tweetsJson = fileName+'.json'  
    
    # name for text file for review of results
    tweetsFull = fileName+'_full.txt'  
    
    # name for text from tweets
    tweetsPartial = fileName+'_part.txt'  
    # -------------------------------------
    # working with JSON files composed of multiple JSON objects
    # results is a list of dictionary items obtained from twitter
    # these functions assume that each dictionary item
    # is written as a JSON object on a separate line
    item_count = 0  # initialize count of objects dumped to file
    with open(tweetsJson, 'w') as outfile:
        for dict_item in tweetResults:
            json.dump(dict_item, outfile, encoding = 'utf-8')
            item_count = item_count + 1
            if item_count < len(tweetResults):
                outfile.write(line_termination)  # new line between items
                        
    # -------------------------------------
    # working with text file for reviewing multiple JSON objects
    # this text file will show the full contents of each tweet
    # results is a list of dictionary items obtained from twitter
    # these functions assume that each dictionary item
    # is written as group of lines printed with indentation
    item_count = 0  # initialize count of objects dumped to file
    with open(tweetsFull, 'w') as outfile:
        for dict_item in tweetResults:
            outfile.write('Item index: ' + str(item_count) +\
                ' -----------------------------------------' + line_termination)
            # indent for pretty printing
            outfile.write(json.dumps(dict_item, indent = 4))  
            item_count = item_count + 1
            if item_count < len(tweetResults):
                outfile.write(line_termination)  # new line between items  
            
    # -------------------------------------
    # working with text file for reviewing text from multiple JSON objects
    # this text file will show only the text from each tweet
    # results is a list of dictionary items obtained from twitter
    # these functions assume that the text of each tweet 
    # is written to a separate line in the output text file
    item_count = 0  # initialize count of objects dumped to file
    with open(tweetsPartial, 'w') as outfile:
        for dict_item in tweetResults:
            outfile.write(json.dumps(dict_item['text']))
            item_count = item_count + 1
            if item_count < len(tweetResults):
                outfile.write(line_termination)  # new line between text items  






# -------------------------------------
# use the predefined functions from Russell to conduct the search
# this is the Ford Is Quality Job One example

twitter_api = oauth_login()   
print(twitter_api)  # verify the connection


######################## Collecting AMAZON ECHO ##############################
#using top10 hastags for amazon echo
#https://ritetag.com/best-hashtags-for/amazonecho
# #amazonecho , #alexa , #artificialintellifgence, #googlehome, #amazonalexa
# for some reason the OR search query gathers less number of tweets, so doing each hashtag alone, then combining results
#q = "#amazonecho OR #alexa OR #amazonalexa"
#q = "#amazonecho #alexa #amazonalexa"
q = "#amazonalexa" 

results = twitter_search_loop(twitter_api, q, 2000)  # limit to 2000 tweets

q = "#amazonecho" 

results += twitter_search_loop(twitter_api, q, 2000)  # limit to 2000 tweets

q = "#alexa" 

results += twitter_search_loop(twitter_api, q, 2000)  # limit to 2000 tweets

print("total number of collected tweets")
print(len(results))
plotTweetByDate(results,"amazon-echo-tweet-mention-bydate.png")
saveTweetsInFiles(results,"amazon-echo")

######################## Collecting GOOGLE HOME ##############################
q = "#googlehome" 

googleResults = twitter_search_loop(twitter_api, q, 2000)  # limit to 2000 tweets
print("total number of collected tweets")
print(len(googleResults))
plotTweetByDate(googleResults,"google-home-tweet-mention-bydate.png")
saveTweetsInFiles(googleResults,"google-home")



