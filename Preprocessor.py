import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\s[A-Z]{2}\]\s~\s'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    formatted_dates = []
    for date_string in dates:
        # Strip the additional characters at the end
        stripped_date_string = date_string.split(']')[0]
        # Parse the date string using strptime
        dt_object = datetime.strptime(stripped_date_string.strip('['), '%d/%m/%y, %I:%M:%S %p')
        # Format the date string using strftime
        formatted_date = dt_object.strftime('%d/%m/%y, %I:%M:%S %p')
        formatted_dates.append(formatted_date)

    df = pd.DataFrame({'user_message': message, 'message_date': formatted_dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    df['users'] = df['user_message'].apply(lambda x: x.split(':')[0])  # splittiing names from user_message
    df['message'] = df['user_message'].apply(lambda x: x.split(':')[1])  # splitting message from user message

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df