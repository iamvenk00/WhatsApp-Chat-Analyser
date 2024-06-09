import re
import pandas as pd

def preprocess(data):

    pattern='\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'],format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date':'date and time'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('System Notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    df['date']=df['date and time'].dt.date
    df['year']=df['date and time'].dt.year
    df['month number']=df['date and time'].dt.month
    df['month']=df['date and time'].dt.month_name()
    df['day']=df['date and time'].dt.day
    df['day name']=df['date and time'].dt.day_name()
    df['hours']=df['date and time'].dt.hour
    df['minutes']=df['date and time'].dt.minute
    period=[]
    for hour in df[['day name','hours']]['hours']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period

    return df