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
import time
import requests

#Functions for ICO Watch API

def get_TrackICOAPI(P):
    '''
    Function that calls 4,000 cryptos (ICO and IEO) and  from TrackICO. All features included.
    Tickers as index.
    Features = ['title', 'type', 'ticker', 'rating', 'status', 'country', 'platform', 'pre_ico_start', 'pre_ico_end', 'ico_start', 'ico_end']
    Returns df
    No 
    '''
    
    ICO_df = pd.DataFrame()
    for i in range(1,P+1):
        time.sleep(1)
            
        response = requests.get(f"https://api.trackico.io/v1/icos/all/?page={i}&page_size=24")
        response = response.json()
        
        print(f'Checking page{i}')
        
        for coin in response['results']:
            
            result = pd.DataFrame.from_dict(response['results'])

            ICO_df = pd.concat([result,ICO_df])
            
            print('Joining Dataframe')
            
    ICO_df.drop(['slug','id','category','profile_url','logo_url','short_description'], axis=1, inplace=True)
    ICO_df.reset_index(drop=True, inplace = True)
    ICO_df.rename(index=str, columns={"ticker": "Ticker", "title": "Name"}, inplace = True)
    
    #ICO_df.set_index('Ticker', inplace = True)

    ICO_df = ICO_df.drop_duplicates() 
    
    dummy_date = ICO_df['ico_end'][0]
    
    ICO_df[['pre_ico_end','pre_ico_start','ico_end','ico_start']] = ICO_df[['pre_ico_end','pre_ico_start','ico_end','ico_start']].replace(to_replace=[None], value=dummy_date)
    
    ICO_df['End'] = ICO_df['ico_end'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df['Start'] = ICO_df['ico_start'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df['pre_ico_start'] = ICO_df['pre_ico_start'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df['pre_ico_end'] = ICO_df['pre_ico_end'].apply(lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    ICO_df["Duration"] = ICO_df['End'] - ICO_df['Start']
    ICO_df["pre_Duration"] = ICO_df['pre_ico_end'] - ICO_df['pre_ico_start']
    
    ICO_df.drop(columns = ['ico_end','ico_start'], axis=1, inplace = True)

    return ICO_df