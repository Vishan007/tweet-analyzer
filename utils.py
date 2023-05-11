from wordcloud import WordCloud , STOPWORDS
from collections import Counter
import pandas as pd

stop=set(STOPWORDS)
stop.update(["12","22",'weve','bin','indias','u','la','wh','de','dtype','ji','ann','leve','prince','salman','oh','let'])
def fetch_stats(selected_user , selected_category ,df):
    country = ':earth_asia:'
    if selected_user == 'All user' and selected_category =='All category':
        #1.Number of messages
        num_tweets = df.shape[0]
        #2.number of words
        words = []
        for tweet in df['Tweets']:
            words.extend(tweet.split())
        #3.number of likes
        num_likes=df['likes'].sum()
    elif selected_user != 'All user' and selected_category == 'All category':
        df=df[df['User']==selected_user]
        #1.Number of messages
        num_tweets = df.shape[0]
        #2.number of words
        words = []
        for tweet in df['Tweets']:
            words.extend(tweet.split())
        #3.number of likes
        num_likes=df['likes'].sum()
        #4.country of user
        country=df['Country'].iloc[0]
    elif selected_user == 'All user' and selected_category != 'All category':
        df=df[df['category']==selected_category]
        #1.Number of messages
        num_tweets = df.shape[0]
        #2.number of words
        words = []
        for tweet in df['Tweets']:
            words.extend(tweet.split())
        #3.number of likes
        num_likes=df['likes'].sum()
    elif selected_user != 'All user' and selected_category != 'All category':
        df= df[(df['category']==selected_category) & (df['User']==selected_user)]
        #1.Number of messages
        num_tweets = df.shape[0]
        #2.number of words
        words = []
        for tweet in df['Tweets']:
            words.extend(tweet.split())
        #3.number of likes
        num_likes=df['likes'].sum()
        #4.country of user
        country=df['Country'].iloc[0]
    return num_tweets , len(words) , num_likes , country

def most_tweets(df):
    x = df['User'].value_counts().head(8)
    df = round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','User':'percent'})
    return x ,df



def create_wordcloud(selected_user , selected_category,df):
    if selected_user != 'All user' and selected_category != 'All category':
        df = df[(df['category']==selected_category) & (df['User']==selected_user)]
        cmap = 'brg'
    elif selected_user == 'All user' and selected_category != 'All category':
        df=df[df['category']==selected_category]
        cmap = 'gist_earth'
    elif selected_user != 'All user' and selected_category == 'All category':
        df=df[df['User']==selected_user]
        cmap = 'tab20'
    elif selected_user == 'All user' and selected_category =='All category':
        df = df
        cmap = 'hsv'

    wc = WordCloud(width=500,height=500,min_font_size=10,
                   background_color='white',stopwords=stop,
                   colormap=cmap)
    df_wc = wc.generate(df['Tweets'].str.cat(sep=" "))
    return df_wc

def selected_df(selected_user,selected_category,df):
    if selected_user != 'All user' and selected_category != 'All category':
        df = df[(df['category']==selected_category) & (df['User']==selected_user)]
    elif selected_user == 'All user' and selected_category != 'All category':
        df=df[df['category']==selected_category]
    elif selected_user != 'All user' and selected_category == 'All category':
        df=df[df['User']==selected_user]
    elif selected_user == 'All user' and selected_category =='All category':
        df = df
    return df

def most_common_words(selected_user,selected_category,df):
    df = selected_df(selected_user,selected_category,df)
    most_words = [word for tweet in df['Tweets'] for word in tweet.split() if word not in stop]
    common_words_df = pd.DataFrame(Counter(most_words).most_common(20) , columns=['Words','Count'])
    return common_words_df    

def monthly_tweets(selected_user,selected_category,df):
    df = selected_df(selected_user,selected_category,df)
    timeline = df.groupby(df['date'].dt.month_name()).count()['Tweets']
    new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_wise_tweets=pd.DataFrame(timeline.reindex(new_order,axis=0))
    return month_wise_tweets

def daily_tweets(selected_user,selected_category,df):
    df = selected_df(selected_user,selected_category,df)
    daily = pd.DataFrame(df.groupby(df['date'].dt.day).count()['Tweets'])
    return daily

def weekly_tweets(selected_user,selected_category,df):
    df = selected_df(selected_user,selected_category,df)
    weekly_activity = pd.DataFrame(df['date'].dt.day_name().value_counts())
    return weekly_activity

def pivot_table(selected_user,selected_category,df):
    df = selected_df(selected_user,selected_category,df)
    activity_heatmap = df.pivot_table(index='day_name',columns='month',values='Tweets',aggfunc='count')
    return activity_heatmap