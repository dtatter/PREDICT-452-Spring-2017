# Python code that combines all gathered comment from twitter, facebook and cnet texts in two files
# amazon_echo_combined_text.txt and google_home_combined_text.txt
# These files are used for Topic Analysis

import time
import pandas as pd

# AMAZON
# Open the Amazon combined text

amazonFulltext_filename = '../../data/topic/amazon_echo_combined_text.txt'
amazoneFulltext_fileIO = open(amazonFulltext_filename, "a")
    
    
    
# Open cnet files and grab text input
# TO DO GET TEXT FILES WITH NO DATE
# %s\n
cnet_filename = '../../data/cnet/Amazon_Echo_User_Reviews.txt'
cnet_fileIO = open(cnet_filename, "r")
for line in cnet_fileIO.readlines():
    print"Reading Cnet"
    #print line
    amazoneFulltext_fileIO.write(line)
cnet_fileIO.close()
   
# Open facebook files and grab text input
# %s\n
facebook_filename = '../../data/facebook/Amazon Echo_facebook_comments.csv'
facebook_dataframe = pd.read_csv(facebook_filename, delimiter = ',',index_col=None, header=1, parse_dates=True)
for row in facebook_dataframe.values:
    print("Reading FB")
    # Comment is in second row
    #print(row[1])
    amazoneFulltext_fileIO.write(row[1])
    
# Open twitter files and grab text input
# %s\n
twitter_filename = '../../data/twitter/amazonecho_tweet_text_file.txt'
twitter_fileIO = open(twitter_filename, "r")
for line in twitter_fileIO.readlines():
    print"Reading Twitter"
    print line
    amazoneFulltext_fileIO.write(line)
twitter_fileIO.close()   
    

amazoneFulltext_fileIO.close()

# Google Home
# Open the Google combined text

googleFulltext_filename = '../../data/topic/google_echo_combined_text.txt'
googleFulltext_fileIO = open(googleFulltext_filename, "a")
    
    
    
# Open cnet files and grab text input
# TO DO GET TEXT FILES WITH NO DATE
# %s\n
cnet_filename = '../../data/cnet/Google_Home_User_Reviews.txt'
cnet_fileIO = open(cnet_filename, "r")
for line in cnet_fileIO.readlines():
    print"Reading Cnet"
    #print line
    googleFulltext_fileIO.write(line)
cnet_fileIO.close()
   
# Open facebook files and grab text input
# %s\n
facebook_filename = '../../data/facebook/Google Home_facebook_comments.csv'
facebook_dataframe = pd.read_csv(facebook_filename, delimiter = ',',index_col=None, header=1, parse_dates=True)
for row in facebook_dataframe.values:
    print("Reading FB")
    # Comment is in second row
    #print(row[1])
    googleFulltext_fileIO.write(row[1])
    
# Open twitter files and grab text input
# %s\n
twitter_filename = '../../data/twitter/googlehome_tweet_text_file.txt'
twitter_fileIO = open(twitter_filename, "r")
for line in twitter_fileIO.readlines():
    print"Reading Twitter"
    print line
    googleFulltext_fileIO.write(line)
twitter_fileIO.close()   
    

googleFulltext_fileIO.close()
   
   
