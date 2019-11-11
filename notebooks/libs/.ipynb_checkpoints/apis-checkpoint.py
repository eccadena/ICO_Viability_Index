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
        
        
        
#Still working on the 'get_new_projects()' function
class Coin_data():
    
    def __init__(self):
        self.btctalk_ann_url = 'https://bitcointalk.org/index.php?board=159.0'
        self.cmc_base_url = 'https://coinmarketcap.com/currencies/'
        self.cmc_coin_url = 'https://coinmarketcap.com/all/views/all/'

    def get_cmc_coins(self):
        headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"} 
        request=Request(self.cmc_coin_url, headers=headers) 
        response =urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')
        coin_list = soup.findAll('a' , {'class':"currency-name-container link-secondary"})
        coins = []
        for coin in coin_list:
            coins.append(coin.text)
        return coins
        
        
    def get_new_projects(self):
        #Get list of coins on Coin Market Cap
        coin_list = self.get_cmc_coins()
        
        #Prepare BS4 to scrape bitcointalk.org announcement page
        headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"} 
        request=Request(self.btctalk_ann_url, headers=headers) 
        response =urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')
        
        #Create a list of all the post on the announcement page
        links = soup.findAll('a')
        
        #Capture the url for each post
        links = [url.get('href') for url in links if 'ANN' in url.text]
        
        #For loop over each url saving the content of each page to a dict key
        print('Looping over each url saving the content of each page to a dict key')
        coins = {}
        count = 0
        for url in links:
            count += 1
            headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"} 
            request=Request(url, headers=headers) 
            response =urlopen(request)
            soup = BeautifulSoup(response, 'html.parser')
            coins[count] = soup
            
        #For loop over each dict key (post html page) and captive the title, as well as search the body for key words
        print('Looping over each dict key (post html page) and captive the title, as well as search the body for key words')
        count = 1
        flags = ['gaurenteed', 'profit', 'government', 'approval', 'massive', 'mega', 'rich', 'money']
        name, rating = [],[]
        for i in range(len(coins)):
            count += 1
            scam_meter = 0

            for flag in flags:
                if flag in coins[i+1].text.lower():
                    scam_meter += 1
            name += [coins[i+1].title.text]
            rating += [scam_meter]
            
        #Create a dataframe to store the title and scam rating for each post
        df = pd.DataFrame({
            'Title':name,
            'Scam_Rating':rating,
        }) 
        
        #Extract the project name from the title
        
        
        #Extract the ticker from the title
        
        
        #Extract a start date from the body of each post
        
        
        #Extract an end date from the body of each post
        
        
        #Capture the offering price for each coin
        
        
        #Identify the Algo for each project 
        
        
        return df
        