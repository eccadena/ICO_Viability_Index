import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from collections import Counter
import os
from urllib.request import Request, urlopen as Ureq
import urllib.request
import requests
import PyPDF2

consumer_key = os.getenv("TWITTER_PUBLIC_API")
consumer_secret = os.getenv("TWITTER_SECRET_KEY")
nltk.download('vader_lexicon')
base_url = 'https://whitepaperdatabase.com/?s='
pdf_url = 'https://whitepaperdatabase.com/wp-content/uploads/2018/03/Augur-REP-Whitepaper.pdf'



# Functions for Sent Analysis        
        
def tokenizer(text):
    """Tokenizes text."""
    addl_stopwords = [',','`', '', 'rt', 'http', 'https', 'RT', 'BTC', 'bitcoin', 'ETH', 'LTC', 'XRP', 'co', 'crypto', 'blockchain', 'cryptocurrency', 'cripto', 'litecoin']    
    text = word_tokenize(text)
    text = [word.lower() for word in text]
    regex = re.compile("[^a-zA-Z ]")
    text = [regex.sub('', word) for word in text]
    sw = set(stopwords.words('english') + addl_stopwords)
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]
    clean_text = [word for word in text if word not in sw]
    return clean_text

def token_count(tokens, N=10):
    """Returns the top N tokens from the frequency count"""
    return Counter(tokens).most_common(N)

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

def twitter_sent_analysis(tweet_df):    
    tweet_sentiments, comp, pos, neg, neu = [],[],[],[],[]
    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweet_df.Tweet:
        sentiment = analyzer.polarity_scores(tweet),
        comp.append(sentiment[0]["compound"]),
        pos.append(sentiment[0]["pos"]),
        neg.append(sentiment[0]["neg"]),
        neu.append(sentiment[0]["neu"]),
  
    tweet_df['Compound'] = comp
    tweet_df['Positive'] = pos
    tweet_df['Negative'] = neg
    tweet_df['Neutral'] = neu

    return tweet_df

def count(df):
    '''
    Takes a DataFrame with a "compund" column and returns a basic count of positive, neutral, and negative sentiment in a dict format
    '''
    positive_count, negative_count, neutral_count = 0,0,0
    for i in df['Compound']:
        if i >= 0.05:
            positive_count += 1
        elif i <= -0.05:
            negative_count += 1
        else:
            neutral_count += 1
    count={
        'Positive Tweets': positive_count,
        'Neutral Tweets': neutral_count,
       'Negavtive Tweets': negative_count
    }
    return count



def get_twitter_scores(topic_of_tweet, num_of_tweets):
    df = get_tweets_list(topic_of_tweet, num_of_tweets)
    df = twitter_sent_analysis(df)
    return df

def twitter_df_score(df, N): 
    '''
    Scores an entire Dataframe of coins based on the last 'N' tweets.  Returns a dataframe of scores with a 
    '''
    scores = []
    df2 = pd.DataFrame()
    for name in df.Name:
        search_term = '#' + str(name)
        print(f"Searching and Scoring {search_term}")
        tweet_df = get_twitter_scores(search_term, N)
        score = {name :{
                'Compound' : tweet_df.Compound.mean(),
                'Positive' : tweet_df.Positive.mean(),
                'Negative' : tweet_df.Negative.mean(),
                'Neutral' : tweet_df.Neutral.mean(),
        }}
        scores.append(score)
        print(f"{name} scored")
        for i in progressbar(range(10), "Waiting for Twitter Rate Limit: ", 40):
            time.sleep(0.6) # any calculation you need
    print(f"Scoring of {len(scores)} tweet concluded, creating dataframe")
    
    for item in scores:
        df1=pd.DataFrame.from_dict(item).T
        df2 = pd.concat([df1,df2], sort = True)

    return df2


#Functions for Whitepapers

def base_page(base_url, term):
    new_url = base_url + term
    uClient = Ureq(new_url)
    raw_content = uClient.read()
    uClient.close()
    page_soup = soup(raw_content)
    return page_soup

def get_paper_url(soup):
    containers = soup.findAll("a")
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