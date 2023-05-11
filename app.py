import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO
import preprocessing 
from utils import *
import seaborn as sns

st.sidebar.title('Tweet Analyzer')
st.title('Tweets of top Political leader :earth_asia:')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode()
    StringData = StringIO(data)    ##converting string data to dataframe
    df = preprocessing.preprocess(StringData)

    st.dataframe(df)

    #fetch unique users
    unique_user = df['User'].unique().tolist()
    unique_user.insert(0,"All user")
    unique_user.sort()
    unique_category = df['category'].unique().tolist()
    unique_category.insert(0,"All category")
    unique_category.sort()
    unique_country = df['Country'].unique().tolist()
    
    selected_user = st.sidebar.selectbox('Show analysis of tweets',unique_user)
    selected_category = st.sidebar.selectbox('Show analysis of category',unique_category)
    
    if st.sidebar.button('Show analysis'):
        
        ##stats area
        num_tweets,num_words,num_likes,country = fetch_stats(selected_user,selected_category,df)
        col1,col2,col3,col4 = st.columns((2,2,2,3))  #(2,2,2,3) for alignment
        with col1:
            st.header('Total tweets')
            st.title(num_tweets)

        with col2:
            st.header('Total words')
            st.title(num_words)

        with col3:
            st.header('Total likes')
            st.title(num_likes)

        with col4:
            #st.markdown("<h1 style='text-align: right; color: red;'>country</h1>", unsafe_allow_html=True)
            st.title(country)

        ## finding the busiest users in the group
        if selected_user == 'All user':
            st.title('Num of tweets.')
            x,new_df = most_tweets(df)
            fig , ax = plt.subplots()
            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index , x.values , color='blue')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        ##word cloud
        st.title('Wordcloud')
        df_wc=create_wordcloud(selected_user,selected_category,df)
        fig,ax=plt.subplots()
        plt.axis('off')
        ax.imshow(df_wc)
        st.pyplot(fig) 
        ##most common words
        common_words_df=most_common_words(selected_user,selected_category,df)
        fig,ax = plt.subplots()
        ax.barh(common_words_df['Words'],common_words_df['Count'])
        ax.set_xlabel('Num of Words')
        plt.xticks(rotation = 'vertical')
        st.title('Most common words')
        st.pyplot(fig)
        ##pie chart of category
        if selected_category == 'All category' and selected_user != 'All user':
            df = df[df['User']==selected_user]
        pie_df = pd.DataFrame(df.groupby('category').count()['Tweets'] , columns=['category' , 'Tweets'])
        fig,ax = plt.subplots()
        ax.pie(x=pie_df['Tweets'], labels=pie_df.index ,autopct='%.0f%%')
        st.title('Pie chart')
        st.pyplot(fig)
        ##month wise tweets
        month_wise_tweets=monthly_tweets(selected_user,selected_category,df)
        fig,ax = plt.subplots()
        ax.scatter(month_wise_tweets.index , month_wise_tweets.values,color='green')
        ax.set_ylabel('Num of Tweets')
        plt.xticks(rotation = 'vertical')
        st.title('Monthly Tweets')
        st.pyplot(fig)
        st.title('Activity Map')
        col1 , col2 = st.columns(2)
        ##daily tweets
        with col1:
            daily = daily_tweets(selected_user,selected_category,df)
            fig,ax = plt.subplots()
            ax.plot(daily.index,daily.values , color='green')
            ax.set_xlabel('Date')
            ax.set_ylabel('Num of Tweets')
            st.title('Daily tweets')
            st.pyplot(fig)
        
        with col2:
            ##weekly tweets
            weekly_activity = weekly_tweets(selected_user,selected_category,df)
            fig,ax = plt.subplots()
            ax.bar(weekly_activity.index,weekly_activity['date'],color='orange')
            ax.set_ylabel('Num of Tweets')
            ax.set_ylabel('Num of Tweets')
            plt.xticks(rotation = 'vertical')
            st.title('Weekly tweets')
            st.pyplot(fig)

        activity_heatmap = pivot_table(selected_user,selected_category,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.title('Heat map')
        st.pyplot(fig)
