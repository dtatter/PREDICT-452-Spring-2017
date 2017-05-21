import urllib2
import json
import datetime
import csv
import time

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
	
app_id = "-"
app_secret = "-"

access_token = app_id + "|" + app_secret

amazon_echo_id = '293444394190504'

google_home_id = '314454728919469'

def pp(o):
    print json.dumps(o, indent = 4, sort_keys = True)
	

# Helper function to catch HTTP Error 500
def request_until_succeed(url):
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()
	
# decoding unicode to CSV
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')
		
def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data
	
#test_status = getFacebookPageFeedData(google_home_id, access_token, 10)["data"][-4]
#pp(test_status)

def processFacebookPageFeedStatus(status):
    
    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.
    
    # Additionally, some items may not always exist,
    # so must check for existence first
    
    status_id = status['id']
    # status_message = '' if 'message' not in status.keys() else status['message'].encode('utf-8')
    # link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
    # status_type = status['type']
    # status_link = '' if 'link' not in status.keys() else status['link']
    
    
    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.
    
    status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    status_published = status_published.strftime('%Y-%m-%d') # best time format for spreadsheet programs
    
    # Nested items require chaining dictionary keys.
    
    num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
    # num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    # num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']
    
    # return a tuple of all processed data
    return (status_id,status_published, num_likes)

# processed_test_status = processFacebookPageFeedStatus(test_status)
# print processed_test_status

def scrapeFacebookPageFeedStatus(page_id, access_token):
    with open('C:\Users\Home\%s_facebook_statuses.csv' % page_id, 'wb') as file:
        w = csv.writer(file)
        w.writerow(["status_id","status_published", "num_likes"])
        
        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()
        
        print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)
        
        statuses = getFacebookPageFeedData(page_id, access_token, 100)
        
        while has_next_page:
            for status in statuses['data']:
                w.writerow(processFacebookPageFeedStatus(status))
                
                # output progress occasionally to make sure code is not stalling
                num_processed += 1
                if num_processed % 1000 == 0:
                    print "%s Statuses Processed: %s" % (num_processed, datetime.datetime.now())
                    
            # if there is no next page, we're done.
            try:
                if 'paging' in statuses.keys():
                    statuses = json.loads(request_until_succeed(statuses['paging']['next']))
            except KeyError:
                has_next_page = False
                
        
        print "\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)

		
scrapeFacebookPageFeedStatus(google_home_id, access_token)
scrapeFacebookPageFeedStatus(amazon_echo_id, access_token)