import streamlit as st
import time
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import help

plt.style.use('dark_background')

st.set_page_config(page_title="Chat Analyzer", page_icon=":speech_balloon:")
st.title("***Welcome to Chat Analyzer***")
st.markdown("*Chat Analyzer is a powerful tool for analyzing WhatsApp chat data. It provides valuable statistics and visualizations, including total messages, words, media, and links. Explore insights on the most active users, commonly used words, and popular emojis. Discover chat activity trends with timeline analysis, including yearly, monthly, and daily patterns. Gain deep understanding of your WhatsApp conversations with Chat Analyzer.*")
st.sidebar.title("Chat Analyzer")

with st.sidebar.expander("How to Analyze Your WhatsApp Chats"):
    st.markdown("1. **Export Chat**: Export your WhatsApp chat without media as a text file.")
    st.markdown("2. **Upload Chat**: Drag and drop or browse to upload your chat file in the sidebar.")
    st.markdown("3. **Analyze**: Select the analysis type and click the analyze button to view the insightful results.")
    st.markdown("NOTE: Select wide mode form the setting to have good experience.")
    st.markdown("***Chat Analyzer does not collect or store any data from your chat file. All the analysis is performed locally on your device.***")



df = None  # Initialize df with None

# Upload file
uploaded_file = st.sidebar.expander("Upload your file here", expanded=True).file_uploader("Let's analysis", type=["txt"])
if uploaded_file is None:
    st.warning("Please upload a file to proceed.")
else:
    try:
        # To read file as bytes:
        input_file_content = uploaded_file.read().decode("utf-8")
        # To convert to a string based IO:
        df = preprocessor.preprocess(input_file_content)
        # complete_df = df.copy()

        # Success message
        st.success('File uploaded successfully! Analyzing data...')

        # Wait for a few seconds
        time.sleep(3)

        # Clear success message
        st.empty()

        # Fetch unique users
        unique_users = df['user'].unique().tolist()
        unique_users.remove('group_notification')
        unique_users = sorted(unique_users)
        unique_users.insert(0, "For all members")


        st.markdown("### Select analysis type:")
        selected_user = st.selectbox("Select option", unique_users)

        if selected_user != "For all members":
            st.info("Data selected for " + selected_user )
        

        else:
            st.info("Complete dataset is selected") 
        # st.dataframe(complete_df)
        

        if st.button("Analysis "+selected_user+" chat :smile:"):
            # Receive data from the help function
            num_messages, total_words, num_media, num_link, emoji_list = help.fetch_stats(selected_user, df)
            st.title("Chat Stats:")


            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.header("Total messages")
                st.subheader(num_messages)

            with col2:
                st.header("Total words")
                st.subheader(total_words)

            with col3:
                st.header("Total media")
                st.subheader(num_media)

            with col4:
                st.header("Total links")
                st.subheader(num_link)

            with col5:
                st.header("Total emojis")
                st.subheader(emoji_list)
            st.markdown("---", unsafe_allow_html=True)


        

            st.title("Timeline Analysis:")
            col1, col2 = st.columns(2)
            #timeline analysis
            #yearly timeline          

            with col1:     
                st.subheader("Yearly Analysis:")

                yearly_timeline = help.yearly_timeline(selected_user, df)

                # Create the plot
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(yearly_timeline['year'], yearly_timeline['message'], color='#ff6f00')
                plt.xticks(rotation='vertical')
                
                ax.set_title("Yearly Timeline")
                ax.set_xlabel("Number of Years")
                ax.set_ylabel("Number of Messages")
                

                # Customize the appearance
                plt.xticks(rotation='horizontal')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                st.pyplot(fig)




            with col2:
                st.subheader("Monthly Analysis:")
                #monthy timeline
                timeline = help.month_timeline(selected_user, df)

                # Create the plot
                fig, ax = plt.subplots(figsize=(8, 3))
                ax.plot(timeline['time'], timeline['message'], color='#ff6f00')
                plt.xticks(rotation='vertical')

                ax.set_title("Monthly Timeline")
                ax.set_xlabel("Number of Months")
                ax.set_ylabel("Number of Messages")
                

                # Customize the appearance
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                st.pyplot(fig)


            #daily timeline
            daily_timeline = help.daily_timeline(selected_user, df)
            st.subheader("Daily Analysis:")

            # Create the plot
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(daily_timeline['onlydate'], daily_timeline['message'], color='#ff6f00')
            ax.set_title("Daily Timeline")
            ax.set_xlabel("Number of Days")
            ax.set_ylabel("Number of Messages")
                

                # Customize the appearance
            plt.xticks(rotation='horizontal')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)
            st.markdown("---", unsafe_allow_html=True)



            #daily acivity map
            st.title("Activity maps:")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("week activity Map")
                #daily activity map
                week_map = help.week_map(selected_user, df)
                # Determine the index of the highest value
                max_index = week_map['message'].idxmax()

                # Create a list of colors, with red for the highest value and the default color for other bars
                colors = ['#ff0000' if i == max_index else '#ff6f00' for i in range(len(week_map['day_name']))]


                # Create the bar plot
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.barh(week_map['day_name'], week_map['message'], color=colors)
                ax.set_title("Busiest Day of the Week")
                ax.set_ylabel("Names of the days")
                ax.set_xlabel("Number of Messages")

                # Customize the appearance
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                st.pyplot(fig)

                #for busiest month of the year

                with col2:
                    st.subheader("Month activity Map")
                    #daily activity map
                    busy_month= help.month_activity_map(selected_user, df)
                    colors = ['#ff6f00'] * len(busy_month.index)
                    colors[0] = '#ff0000'

                    fig, ax = plt.subplots()
                    ax.barh(busy_month.index, busy_month.values, color=colors)
                    ax.set_title("Busiest month of the year")
                    ax.set_ylabel("Names of the month")
                    ax.set_xlabel("Number of Messages")

                    # Customize the appearance
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig)


                
            st.markdown("---", unsafe_allow_html=True)

            

            st.title("Activity Heat Map:")
            #weekly activity map
            user_heatmap = help.activity_heatmap(selected_user, df)
            st.subheader("Weely Map")
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            ax.set_title("Busiest hours of the day")
            ax.set_ylabel("Names of the days")
            ax.set_xlabel("time period")

            # Customize the appearance
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)




            
            # finding the activist user in group 
            if selected_user=='For all members':
                st.title("Most acive user:")
                x,new_df = help.fetch_busyusers(df)

                #for figure
                colors = ['#ff6f00'] * len(x.index)
                colors[0] = '#ff0000'

                fig, ax =plt.subplots(figsize=(7,7))
            
                col1, col2 = st.columns(2)

                with col1:
                    ax.barh(x.index,x.values,color=colors)
                    st.subheader("Top 10 participants")
                    plt.xticks(rotation='horizontal')
                    ax.set_xlabel("Number of Messages")
                    ax.set_ylabel("Participant")
                    ax.set_title("Top 10 Active Participants")

                # Customize the appearance
                    plt.xticks(rotation='horizontal')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)

                    st.pyplot(fig)
                with col2:
                    st.subheader("Percentage of all members")
                    st.dataframe(new_df)
            st.markdown("---", unsafe_allow_html=True)


        
            #wordcloud and most common words
            st.title("Commonly used words:")
            col1,col2 = st.columns(2)
            with col1:
            #wordcloud
                df_wc = help.create_wordcloud(selected_user, df)
                st.subheader("Word Cloud")
                fig,ax = plt.subplots(figsize=(7,7))
                plt.imshow(df_wc)
                st.pyplot(fig)

            with col2:
                #most common words
                # colors = ['#ff6f00'] * len(x.index)
                # colors[0] = '#ff0000'
                st.subheader("Most common words")
                most_common_df=help.most_common_words(selected_user, df)
                # Determine the index of the highest value
                max_index = most_common_df[1].idxmax()

                # Create a list of colors, with red for the highest value and the default color for other bars
                colors = ['#ff0000' if i == max_index else '#ff6f00' for i in range(len(most_common_df[0]))]


                fig, ax = plt.subplots(figsize=(8,9))
                ax.barh(most_common_df[0], most_common_df[1],color=colors)
                plt.xticks(rotation='horizontal')
                ax.set_title("Most Common Words")
                ax.set_xlabel("Number of Occurences")
                ax.set_ylabel("Word")
                

                # Customize the appearance
                plt.xticks(rotation='horizontal')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                st.pyplot(fig)

            st.markdown("---", unsafe_allow_html=True)



            #emoji analysis
            st.title("Emoji Analysis:")
            emoji_df= help.emoji_helper(selected_user, df)
            col1,col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 emojis")
                # Get the top 10 emojis and their counts
                top_emoji_df = emoji_df.head(10)

                # Define the colors for the pie chart
                colors = ['#ff6f00', '#ff9e00', '#ffb800', '#ffcd00', '#ffe200', '#fff400', '#e0ff00', '#c0ff00', '#9dff00', '#7bff00']

                # Create the pie chart
                fig, ax = plt.subplots(figsize=(7, 7))
                patches, texts, _ = ax.pie(top_emoji_df[1], labels=top_emoji_df[0], colors=colors, autopct='%1.1f%%', shadow=False)

                # Add emoji symbols to the chart labels
                for i, text in enumerate(texts):
                    emoji = top_emoji_df[0].iloc[i]
                    text.set_text(emoji)
                    text.set_fontname('Segoe UI Emoji')  # Set the font to display emojis

                # Customize the plot
                ax.set_title("Top 10 Emojis")
                ax.set_xlabel("Number of Messages")
                ax.set_ylabel("Emoji")
                ax.axis('equal')

                # Display the plot
                st.pyplot(fig)



            with col2:
                st.subheader("All emoji count")
                st.dataframe(emoji_df)

            st.markdown("---", unsafe_allow_html=True)
    
    



        
    except Exception as e:
    # Error message
        st.error("Error occurred while processing the file. Please make sure you upload the correct file.")
        st.error(str(e))  # Display the specific error message

    # Wait for a few seconds
        time.sleep(3)

    # Clear error message
        st.empty()
