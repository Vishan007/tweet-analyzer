import pandas as pd

def preprocess(dataset):
    df = pd.read_csv(dataset ,usecols=['User','Tweets','Country','category','likes','date'])
    df['date'] = pd.to_datetime(df['date'] , format='%Y/%m/%d')
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month
    return df