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
import urllib.request
import PyPDF2
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup as soup

base_url = 'https://whitepaperdatabase.com/?s='

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



def base_page(base_url, term):
    new_url = base_url + term
    uClient = Ureq(new_url)
    raw_content = uClient.read()
    uClient.close()
    page_soup = soup(raw_content)
    return page_soup

def get_paper_url(page_soup):
    containers = page_soup.findAll("a")
    url = containers[8]['href']
    return url

def get_pdf_link(paper_url):
    uClient = Ureq(paper_url)
    raw_content = uClient.read()
    uClient.close()
    page_soup = soup(raw_content)
    pdf_link = page_soup.findAll("a", {"class":"pdfemb-viewer"})
    return pdf_link[0]['href']

def get_pdf(ticker, pdf_link):
    filename = '../../data/whitepapers/' + ticker + '_whitepaper.pdf'
    urllib.request.urlretrieve(pdf_link, filename)

def read_pdf(ticker):
    corpus = ''
    filename = '../../data/whitepapers/' + ticker + '_whitepaper.pdf'
    pdf_obj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf_obj)
    pages = pdfReader.numPages
    for i in range(pages):
        raw_text = pdfReader.getPage(i)
        corpus = corpus + raw_text.extractText()
    return corpus

def check_sent(corpus):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(corpus)
    return sentiment