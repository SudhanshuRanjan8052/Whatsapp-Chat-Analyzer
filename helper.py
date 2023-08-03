from urlextract import URLExtract #library used for extracting urls
import datetime # importing datetime module for now()
from datetime import datetime
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user] #updating df for a particular user

    num_mssg=df.shape[0] #total number of messages

    #finding total no of words
    words=[]
    for mssg in df['message']:
        words.extend(mssg.split()) #list of all words

    #finding total no of media messages
    count=0
    for mssg in df['message']:
        if mssg=="<Media omitted>\n":
            count+=1

    #counting link messages
    extractor=URLExtract() #creating object
    link=[]
    for mssg in df['message']:
        link.extend(extractor.find_urls(mssg)) #making a list of link messages

    #counting emoji 
    total_emoji=0
    emoji1=[]

    for mssg in df['message']:
        emoji1.extend([c for c in mssg if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emoji1).most_common(len(Counter(emoji1))))
    emoji_df=emoji_df.rename(columns={0:"Emoji",1:"count"})
    total_emoji=emoji_df['count'].sum()
    

    # using now() to get current time
    current_time = datetime.now()    
    year = current_time.year
    day = current_time.day
    month = current_time.month

    for y in df['year']: #for getting year of first message
        year= year-y
        break
    
    for mname in df['month']: #for getting month of first message
        mon = datetime.strptime(mname,'%B').month #changing month name to month number
        #different cases
        if mon>month: 
            year=year-1
            month = (12-mon)+(month-1)
        else:
            month = month-mon
        break

    for d in df['day']: #for getting date of first message
        #different cases
        if d!=day:
            if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                day=(31-d)+day
                if day>31:
                    day=day-31
            else:
                day=(30-d)+day
                if day>30:
                    day=day-30

        else:
            day = day-d
        break
        
    return num_mssg,words,count,link,total_emoji,year,month,day #returning all stats 

#finding most busy user
def mostBusyUser(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100).reset_index().rename(
        columns={'index':'name','user':'percent'})
    return x,df

#finding most common words
def mostCommonWords(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    #filtering the messages
    temp = df[df['message']!="group notification"]
    temp = temp[temp['message']!="<Media omitted>\n"]

    f=open("stop_hinglish.txt","r")
    stop_words = f.read()

    words=[] #creating an empty list

    for mssg in temp['message']:
        for word in mssg.lower().split():
            if word not in stop_words: #checking conditions
                    words.append(word)

    count_df=pd.DataFrame(Counter(words).most_common(20)) #returning the most common words in a dataframe by counting the words using counter
    return count_df

#emoji analysis
def emoji_freq(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    emojis=[]
    for mssg in df['message']:
        emojis.extend([c for c in mssg if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(20))
    emoji_df=emoji_df.rename(columns={0:"Emoji",1:"Count"})

    return emoji_df

#Monthly_timeline
def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    timeline = df.groupby(['year','month','month_num']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time

    return timeline

#Daily timeline
def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    timeline = df.groupby(['only_date']).count()['message'].reset_index()
    
    return timeline

#Week activity map
def weekActivityMap(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    return df['day_name'].value_counts()

#Month activity map
def monthActivityMap(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    return df['month'].value_counts()

#heatmap
def heatmap(selected_user,df):
    if selected_user!="Overall":
        df= df[df['user']==selected_user]
    activity_hitmap=df.pivot_table(index="day_name",columns="period",values="message",
    aggfunc="count").fillna(0)

    return activity_hitmap



    

    
