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
	
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')
		
def getFacebookCommentFeedUrl(base_url):

    # Construct the URL string
    fields = "&fields=id,message,reactions.limit(0).summary(true)" + \
        ",created_time,comments,from,attachment"
    url = base_url + fields

    return url

def processFacebookComment(comment, status_id, parent_id=''):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    # comment_id = comment['id']
    comment_message = '' if 'message' not in comment else \
        unicode_decode(comment['message'])
    # comment_author = unicode_decode(comment['from']['name'])
    # num_reactions = 0 if 'reactions' not in comment else \
        # comment['reactions']['summary']['total_count']

    if 'attachment' in comment:
        attach_tag = "[[{}]]".format(comment['attachment']['type'].upper())
        comment_message = attach_tag if comment_message is '' else \
            comment_message + " " + attach_tag

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    comment_published = datetime.datetime.strptime(
        comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    comment_published = comment_published + datetime.timedelta(hours=-5)  # EST
    comment_published = comment_published.strftime(
        '%Y-%m-%d')  # best time format for spreadsheet programs

    # Return a tuple of all processed data

    return (comment_published, comment_message)
	
def scrapeFacebookPageFeedComments(page_id, access_token):
    with open('C:\Users\Home\{}_facebook_comments.csv'.format(page_id), 'w') as file:
        w = csv.writer(file)
        w.writerow(['comment_published','comment_message'])

        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        after = ''
        base = "https://graph.facebook.com/v2.9"
        parameters = "/?limit={}&access_token={}".format(
            100, access_token)

        print("Scraping {} Comments From Posts: {}\n".format(
            page_id, scrape_starttime))

        with open('C:\Users\Home\{}_facebook_statuses.csv'.format(page_id), 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for status in reader:
                has_next_page = True

                node = "/{}/comments".format(status['status_id'])
                after = '' if after is '' else "&after={}".format(after)
                base_url = base + node + parameters + after

                url = getFacebookCommentFeedUrl(base_url)
                #print(url)
                comments = json.loads(request_until_succeed(url))
                #reactions = getReactionsForComments(base_url)

                while has_next_page and comments is not None:
                    for comment in comments['data']:
                        comment_data = processFacebookComment(
                            comment, status['status_id'])
                        #reactions_data = reactions[comment_data[0]]
                        #print(comment_data + reactions_data)
                        w.writerow(comment_data)

                        if 'comments' in comment:
                            has_next_subpage = True
                            sub_after = ''

                            while has_next_subpage:
                                sub_node = "/{}/comments".format(comment['id'])
                                sub_after = '' if sub_after is '' else "&after={}".format(
                                    sub_after)
                                sub_base_url = base + sub_node + parameters + sub_after

                                sub_url = getFacebookCommentFeedUrl(
                                    sub_base_url)
                                sub_comments = json.loads(
                                    request_until_succeed(sub_url))
                                #sub_reactions = getReactionsForComments(
                                    #sub_base_url)

                                #print(sub_reactions)

                                for sub_comment in sub_comments['data']:
                                    sub_comment_data = processFacebookComment(
                                        sub_comment, status['status_id'], comment['id'])
                                    #sub_reactions_data = sub_reactions[
                                        #sub_comment_data[0]]
                                    w.writerow(sub_comment_data)

                                    num_processed += 1
                                    if num_processed % 100 == 0:
                                        print("{} Comments Processed: {}".format(
                                            num_processed,
                                            datetime.datetime.now()))

                                if 'paging' in sub_comments:
                                    if 'next' in sub_comments['paging']:
                                        sub_after = sub_comments[
                                            'paging']['cursors']['after']
                                    else:
                                        has_next_subpage = False
                                else:
                                    has_next_subpage = False

                        # output progress occasionally to make sure code is not
                        # stalling
                        num_processed += 1
                        if num_processed % 100 == 0:
                            print("{} Comments Processed: {}".format(
                                num_processed, datetime.datetime.now()))

                    if 'paging' in comments:
                        if 'next' in comments['paging']:
                            after = comments['paging']['cursors']['after']
                        else:
                            has_next_page = False
                    else:
                        has_next_page = False
                    
                            

        print("\nDone!\n{} Comments Processed in {}".format(
            num_processed, datetime.datetime.now() - scrape_starttime))
			
scrapeFacebookPageFeedComments(amazon_echo_id,access_token)
scrapeFacebookPageFeedComments(google_home_id,access_token)