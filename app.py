import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") #changing byte type int string type
    df = preprocessor.preprocess(data)

    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_mssg,words,count,link,emoji,year,month,day= helper.fetch_stats(selected_user,df)
        st.title("**Top Statistics**")
        col1,col2,col3,col4,col5,col6 = st.columns(6)
        str1 = year,month,day

        with col1:
            st.header("Total Messages")
            st.title(num_mssg)
        
        with col2:
            st.header("Total Words")
            st.title(len(words))

        with col3:
            st.header("Media Messages")
            st.title(count)

        with col4:
            st.header("Link Messages")
            st.title(len(link))
        
        with col5:
            st.header("Total Emojis")
            st.title(emoji)

        with col6:
            st.header("Chat Time(Y|M|D)")
            st.title(str1)

        #Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax =plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax =plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Weekly Acivity Map
        st.title("Weekly Activity Map")
        busy_day = helper.weekActivityMap(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:
            fig,ax=plt.subplots()
            ax=sns.barplot(busy_day.index, busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            fig,ax=plt.subplots()
            ax.pie(busy_day.values,labels=busy_day.index,autopct="%0.2f")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        #Monthly Acivity Map
        st.title("Monthly Activity Map")
        busy_month = helper.monthActivityMap(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:
            fig,ax=plt.subplots()
            ax=sns.barplot(busy_month.index, busy_month.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            fig,ax=plt.subplots()
            ax.pie(busy_month.values,labels=busy_month.index,autopct="%0.2f")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        #Activity heatmap
        st.title("Activity Heatmap")
        activity_heatmap = helper.heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(activity_heatmap)
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        #showing most active users(only for groups)
        if selected_user=="Overall":
            st.title("Most Active Users")
            x,percent_df= helper.mostBusyUser(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.pie(x.values,labels = x.index,autopct="%0.2f")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(percent_df)

        

        #most common words
        count_df = helper.mostCommonWords(selected_user,df)
        st.title("Most Used Words")
        col1,col2 = st.columns(2)
        with col1:
            fig,ax=plt.subplots()
            ax=sns.barplot(count_df[0],count_df[1])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
        with col2:
            st.dataframe(count_df)
            
        
        #emoji analysis
        st.title("Most Used Emojis")
        emoji_df=helper.emoji_freq(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:
            fig,ax = plt.subplots()
            ax=sns.barplot(emoji_df['Emoji'],emoji_df["Count"])
            st.pyplot(fig)
            
        with col2:
            st.dataframe(emoji_df)

        

        





