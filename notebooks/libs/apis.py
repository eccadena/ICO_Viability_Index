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
        
        
        

class Coin_data(self):
    
    def __init__(self):
        self.btctalk_url = 'https://bitcointalk.org/index.php?board=159.0'
        
    def get_anns(self):
        