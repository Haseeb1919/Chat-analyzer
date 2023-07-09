
import re
import pandas as pd
import os 
import datetime

def preprocess(input_content):
    # Function to convert time to 24-hour format take input from the user through the file uploaded
    def convert_time_to_24_hour_format(match):
        hour = int(match.group(1))
        minute = int(match.group(2))
        period = match.group(3).lower()

        if period == 'pm' and hour < 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0

        return f"{hour:02d}:{minute:02d}"

    # Define the regular expression pattern for matching the time format
    time_pattern = r"(\d{1,2}):(\d{2})\s?([APap][Mm])"

    # Replace the matched time formats with 24-hour format
    converted_content = re.sub(time_pattern, convert_time_to_24_hour_format, input_content)


    #pattern to match the date and time format in the file
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'


    #extracting messages with user names
    messages = re.split(pattern, converted_content)[1:]


    #extracting dates with time
    dates = re.findall(pattern, converted_content)


    #create dataframe with two columns
    df=pd.DataFrame({'user_messages':messages , 'user_dates': dates })
    df['user_dates'] = pd.to_datetime(df['user_dates'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
    df.rename(columns={'user_dates': 'datetime'}, inplace=True)


    #spliting the user name and message
    users=[]
    messages=[]
    for message in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user']=users
    df['message']=messages
    df.drop(columns=['user_messages'], inplace=True)




    #extracting year, month name, day, hour and minute

    #extract the year
    df['year'] = pd.DatetimeIndex(df['datetime']).year

    #extracting busiest day in the group
    df['day_name']=df['datetime'].dt.day_name()

    #extract the date for daily timeline
    df['onlydate'] = pd.DatetimeIndex(df['datetime']).date

    #extract the month name
    df['month'] = pd.DatetimeIndex(df['datetime']).month_name()

    #extract the month number
    df['month_num'] = df['month'].apply(lambda x: datetime.datetime.strptime(x, '%B').month)

    #extract the day name
    df['day'] = pd.DatetimeIndex(df['datetime']).day

    #extract the hour
    df['hour'] = pd.DatetimeIndex(df['datetime']).hour

    #extract the minute
    df['minute'] = pd.DatetimeIndex(df['datetime']).minute



    #for making the heatmap activity time  
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str(00))
        elif hour == 0:
            period.append(str(00) + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df

