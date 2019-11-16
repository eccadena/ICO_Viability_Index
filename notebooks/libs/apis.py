import pandas as pd
import json
from urllib.request import Request, urlopen
import re
import datetime
from datetime import datetime as dt
import tweepy
import nltk
import os
from collections import Counter

consumer_key = os.getenv("TWITTER_PUBLIC_API")
consumer_secret = os.getenv("TWITTER_SECRET_KEY")



#Functions for ICO Watch API

class ICO_data():
    
    # Initiates the object (self) and allows variables to be set for use in any of the classes funtions
    def __init__(self):
        self.url =' https://api.icowatchlist.com/public/v1/' 
        
        
    def get_json(self):
        '''
        Sends HTTP Request to provided url and returns a json (dictionary) object.

        Arguements: 'url' - Requires a full http address including any applicable API keys, Inherents url object from parent class .
        '''
        request = Request(self.url, headers={'User-Agent': 'Python'})
        response = urlopen(request)
        raw_data = response.read()
        json_data = json.loads(raw_data)
        return json_data

    
    def get_ico_df(self):
        '''
        Performs the 'get_json()' funtion and converts it into a Pandas DataFrame
        '''
        json_data = self.get_json()
        ico_list = json_data['ico']['finished']
        df = pd.DataFrame(ico_list)
        return df


    def preprocess_data(self):
        '''
        Performs the 'get_df' function and removes erronus columns, converts time to DateTime objects and 
        converts the numbers to floats
        '''
        df = self.get_ico_df()
        
        df.drop(columns=['icowatchlist_url', 'image', 'website_link'], inplace = True)
        reordered_columns = ['Name', 'Description', 'Price(USD)', 'Start', 'End', 'ROI(Pct)', 'Timezone']
        df.rename(columns={'all_time_roi': 'ROI(Pct)',
                           'coin_symbol': 'Ticker',
                          'description': 'Description',
                           'end_time': 'End',
                           'name': 'Name',
                           'price_usd': 'Price(USD)',
                          'start_time': 'Start',
                           'timezone': 'Timezone',
                          }, inplace=True)
        df.set_index('Ticker', inplace = True)
        df=df.reindex(columns=reordered_columns)
        
        #Convert the strings to datetime objects
        df['Start'] = df['Start'].apply(lambda x: dt.strptime(x, "%Y-%m-%d %H:%M:%S"))
        df['End'] = df['End'].apply(lambda x: dt.strptime(x, "%Y-%m-%d %H:%M:%S"))
        df['Price(USD)'] = df['Price(USD)'].replace("NA",'0')
        df['ROI(Pct)'] = df['ROI(Pct)'].replace('NA','0%')
        
        #Split the price values that are over 1,000 at the ','
        df['Price(USD)'] = df['Price(USD)'].apply(lambda x: re.split(',', x))
        
        #Split the roi values at their ',', and '%'
        df['ROI(Pct)'] = df['ROI(Pct)'].apply(lambda x: re.split('[, %]', x))
        
        #Merge the strings back that are over 1,000 and turn them into floats
        try:
            df['Price(USD)'] = df['Price(USD)'].apply(lambda x: float(x[0] + x[1])) 
            
        #Convert the remaining strings back to floats    
        except:
            df['Price(USD)'] = df['Price(USD)'].apply(lambda x: float(x[0]))
        
        try:
            df['ROI(Pct)'] = df['ROI(Pct)'].apply(lambda x: float(x[0] + x[1])/100) 
        except:
            df['ROI(Pct)'] = df['ROI(Pct)'].apply(lambda x: float(x[0])/100)
            
        #Create a duration column from the start and end dates
        df["Duration"] = df['End'] - df['Start']
        return df
        

# Functions for Twitter API


def get_tweets_list(topic_of_tweet, num_of_tweets):
    '''
    Returns a dataframe of the most recent 'N' tweets from Twitter tokenized and counted.
    
    Arguements: `topic_of_tweet` : str; what hashtag is being searched 
                'num_of_tweets' : int; how many tweet do you want returned
    '''
    text,time, word_list, word_count=[],[],[],[]
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    for tweet in tweepy.Cursor(api.search, q=topic_of_tweet, tweet_mode='extended').items(num_of_tweets):
        text.append(tweet.full_text),
        time.append(tweet.created_at)
    tweets_df = pd.DataFrame({'Tweet':text}, index=time)
    [word_list.append(tokenizer(text)) for text in tweets_df.Tweet]
    tweets_df['Tokens'] = word_list
    [word_count.append(token_count(token)) for token in tweets_df.Tokens]
    tweets_df['Word_Count'] = word_count
    
    return tweets_df


#Eric Custom trackICO
def get_TrackICOAPI():
    '''
    Function that calls 4,000 cryptos (ICO and IEO) and  from TrackICO. All features included.
    Tickers as index.
    Features = ['title', 'type', 'ticker', 'rating', 'status', 'country', 'platform', 'pre_ico_start', 'pre_ico_end', 'ico_start', 'ico_end']
    Returns df
    No 
    '''
    
    ICO_df = pd.DataFrame()
    for i in range(0,1):
        time.sleep(1)
            
        response = requests.get(f"https://api.trackico.io/v1/icos/all/?page={i+1}&page_size=24")
        response = response.json()
        
        print(f'Checking page{i+1}')
        
        for coin in response['results']:
            
            result = pd.DataFrame.from_dict(response['results'])

            ICO_df = pd.concat([result,ICO_df])
            
            print('Joining Dataframe')
            
    ICO_df.drop(['slug','id','category','profile_url','logo_url','short_description'], axis=1, inplace=True)
    ICO_df.reset_index(drop=True, inplace = True)
    ICO_df.rename(index=str, columns={"ticker": "Ticker", "title": "Name"}, inplace = True)
    
    ICO_df.set_index('Ticker', inplace = True)

    ICO_df = ICO_df.drop_duplicates() 
    
    ICO_df.replace(to_replace=[None], value=ICO_API_df['ico_end'][0], inplace=True)
    
    ICO_df['End'] = ICO_df['ico_end'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df['Start'] = ICO_df['ico_start'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df['pre_ico_start'] = ICO_df['pre_ico_start'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df['pre_ico_end'] = ICO_df['pre_ico_end'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df["Duration"] = ICO_df['End'] - ICO_df['Start']
    ICO_df["pre_Duration"] = ICO_df['pre_ico_end'] - ICO_df['pre_ico_start']
    
    ICO_df.drop(columns = ['ico_end','ico_start'], axis=1, inplace = True)

    return ICO_df