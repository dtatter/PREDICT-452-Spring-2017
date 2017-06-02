import pandas as pd
import numpy as np

data = pd.read_csv('Amazon Echo_facebook_statuses.csv')

crop_data = data[data['status_published']>='2016-10-01']

total_likes = crop_data.groupby('status_published').agg({'num_likes':[np.sum]})

total_likes.to_csv('Amazon_Echo_total_likes_per_day.csv')

data1 = pd.read_csv('Google Home_facebook_statuses.csv')

total_likes_1 = data1.groupby('status_published').agg({'num_likes':[np.sum]})

total_likes_1.to_csv('Google_Home_total_likes_per_day.csv')
