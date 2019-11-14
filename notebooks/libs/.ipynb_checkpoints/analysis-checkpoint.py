from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

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
#    ndf = pd.concat([df, df2])

    return df2