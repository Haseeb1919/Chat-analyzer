        
import pandas as pd
import seaborn as sns
import emoji
from collections import Counter
#main function that return every output
def fetch_stats(selected_user, df):
    #if the selected user is not all member then data to selected person is shown
    if selected_user != "For all members":
        df=df[df['user']==selected_user]


    #fetching the total number of messages
    num_messages = df.shape[0]
    
    #fetching the total number of words
    total_words = []
    for message in df['message']:
        total_words.extend(message.split())


    #fetching the media files
    num_media= df[df['message'] =='<Media omitted>\n'].shape[0]


    #fetching the number of links
    #extracting link 
    from urlextract import URLExtract
    extract= URLExtract()
    num_link=[]
    for message in df['message']:
        num_link.extend(extract.find_urls(message))

    len(num_link)

    #fetching the number of emojis
    emoji_list = []
    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                emoji_list.append(c)
    
    len(emoji_list)



    return num_messages, len(total_words), num_media,len(num_link),len(emoji_list)

#for fetching the activist member of the group
def fetch_busyusers(df):
    x= df['user'].value_counts().head(10)
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x,df


#for wordcloud
from wordcloud import WordCloud
def create_wordcloud(selected_user,df):
   
    from collections import Counter
    #stopwords text file
    f= open('stopwords.txt','r')
    stop_words=f.read()
    if selected_user != "For all members":
        df=df[df['user']==selected_user]


    #remove group notification and media omitted
    temp = df[(df['user'] != 'group_notification') ]
    temp= temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    
    wc = WordCloud(width=300,height=300, min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc




#for most common words
def most_common_words(selected_user,df):
    from collections import Counter
    #stopwords text file
    f= open('stopwords.txt','r')
    stop_words=f.read()

    if selected_user != "For all members":
        df=df[df['user']==selected_user]

    #remove group notification and media omitted
    temp = df[(df['user'] != 'group_notification') ]
    temp= temp[temp['message'] != '<Media omitted>\n']

    #removing stopwards
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df= pd.DataFrame(Counter(words).most_common(20))
    return most_common_df




#for most common emoji
def emoji_helper(selected_user,df):
    if selected_user != "For all members":
        df=df[df['user']==selected_user]


    import emoji
    emoji_list = []
    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                emoji_list.append(c)
    
    emoji_df=pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))

    return emoji_df



#for month timeline
def month_timeline(selected_user,df):
    if selected_user != "For all members":
        df=df[df['user']==selected_user]

    #extracting the messages sent in every month
    timeline=df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    #merging year and month
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time']=time


    return timeline


#for daily timeline
def daily_timeline(selected_user,df):
    
    if selected_user != "For all members":
        df=df[df['user']==selected_user]

    daily_timeline= df.groupby('onlydate').count()['message'].reset_index()

    return daily_timeline



#for yearly timeline
def yearly_timeline(selected_user,df):
    if selected_user != "For all members":
        df=df[df['user']==selected_user]

    #extracting the messages sent in every year
    yearly_timeline= df.groupby('year').count()['message'].reset_index()

    return yearly_timeline




#for weekly timeline
def week_map(selected_user,df):

    if selected_user != "For all members":
        df=df[df['user']==selected_user]

    #extracting the messages sent in every week
    week_map= df.groupby('day_name').count()['message'].reset_index()

    return week_map



#for monthly activity
def month_activity_map(selected_user,df):

    if selected_user != "For all members":
        df=df[df['user']==selected_user]


    return df['month'].value_counts()



#for heatmap of day and hour
def activity_heatmap(selected_user,df):
    
    if selected_user != "For all members":
        df=df[df['user']==selected_user]

    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

