import pandas as pd
import json
from urllib.request import Request, urlopen
import re
import datetime
from datetime import datetime as dt

#ICO Watch List API Wrapper- Can be called with 'live', 'upcoming', and 'finished' on the end for their respective lists, otherwise calls all ICO's
#No API key needed, 1sec limit per call

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


#Not functioning properly, need to check the .apply() function and the for loops     
    def preprocess_data(self):
        '''
        Performs the 'get_df' function and removes erronus columns, converts time to DateTime objects and 
        converts the numbers to floats.
        '''
        df = self.get_ico_df()
        df.set_index('coin_symbol', inplace = True)
        df.drop(columns=['icowatchlist_url', 'image', 'website_link'], inplace = True)
        df['start_time'].apply(dt.strptime(df['start_time'], "%Y-%m-%d %H:%M:%S"))
        df['end_time'].apply(dt.strptime(df['end_time'], "%Y-%m-%d %H:%M:%S"))
        for i in ico_df['price_usd'].values:
            if i == 'NA':
                pass
            else:
                try:
                    price = re.split(',', i)
                    i = float(price[0] + price[1])
                except:
                    i = float(i)
                
        for i in df['ROI'].values:
            try:
                roi = re.split('[, %]', i)
                i = float(roi[0] + roi[1])
            except:
                pass

            return df
        
        
        

class Coin_data(self):
    
    def __init__(self):
        self.btctalk_url = 'https://bitcointalk.org/index.php?board=159.0'
        
    def get_anns(self):
        