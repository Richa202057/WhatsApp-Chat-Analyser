import pandas as pd
import re


def ConvertStringToDataframe(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df.drop(columns=['user_message', 'date'], inplace=True)
    # to create a heatmap one will need a additional column having all slots of day
    slot = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            slot.append(str(23) + ' - ' + str('00'))
        elif hour == 0:
            slot.append(str('00') + ' - ' + str(
                hour + 1))  # to change the format of 0 to 00 so, here we write explicitly code for 0
        else:
            slot.append(str(hour) + ' - ' + str(hour + 1))
    slot.sort()
    df['time_slot'] = slot

    return df
