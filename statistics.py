from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter  # collections is a module , Counter is a function.
import pandas as pd
import emoji


def do_stats(df, selected_user):
    if selected_user != "Group-Level Analysis":
        ## means we want to deal with user level analysis, so modify the exact dataframe
        # creating a new dataframe for selected user which only those rows for user is the selected_user.
        df = df[df["user"] == selected_user]

    ## then formorming our general level statistics on dataframe df
    ## if it is user-level analysis , then df will automatically changed before (inside if block) comming to this part

    ## stat 1:- calculating total no. of messages
    ## since total number of rows inside the dataframe will be the total no of msgs,so
    msg = df.shape[0]

    ## stat 2:- calculating total number of media shared
    ##since at the place of media shared , media ommited is written in df["message] column, because
    ## at the time of downloading the chat user must download it without-media .

    media = df[df["message"] == '<Media omitted>\n'].shape[0]
    ## it will create a new dataframe containg only <Media omitted>\n in the df["messages] column.
    ## stat 3:- finding number of links shared in the group
    urlob = URLExtract()
    url_list = []
    for i in df["message"]:
        url_list.extend(urlob.find_urls(i))
        # urlob is a list of all links extracted from each message of df["messages"] column
    url_no = len(url_list)  # length of this list will be total links shared

    # returning all 3 stats
    return msg, media, url_no


def most_busy_users(df):
    # since it is only for group-level so we will not change dataframe
    x = df['user'].value_counts().head()
    # x is a series in which user name is at index and no. of msgs is at value.
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Group-Level Analysis':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


# finding top 20 most commonly used words
def top_20_words(df, selected_user):
    # the word should not be a  stop-word , <media messages>
    # and also the message word should not be from the group-notification messages, so delete all messages wuth user is "group-notification"
    # firstly we create a temp dataframe not containing <media messages> and group-notification

    if selected_user != "Group-Level Analysis":
        # it means it is a user-level analysis, so modify df
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != "<Media omitted>\n"]
    temp = temp[temp['user'] != 'group-notification']
    top_words_list = []
    f = open("stopwords_hinglish.txt", 'r')
    stop_word = f.read()
    for msg in temp['message']:
        msg=emoji.replace_emoji(msg, '') # removing emoji from the string msg
        for j in msg.lower().split(" "):## converting message each character into lower case , splitting each message(str) into a list of words.
            if j not in stop_word:
                top_words_list.append(j)  # appending this word if it is not a stop-word

    frequent_words_df = pd.DataFrame(Counter(top_words_list).most_common(20))
    return frequent_words_df

    # removing stop-words from this message


# function for month-year activity in a group
def monthly_timeline(selected_user, df):
    if selected_user != 'Group-Level Analysis':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Group-Level Analysis':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def weekly_activity(selected_user, df):
    if selected_user != 'Group-Level Analysis':
        df = df[df['user'] == selected_user]
    # returning the series containing day_name with it's msgs frequency.
    return df["day_name"].value_counts()

def monthly_activity(selected_user, df):
    if selected_user != 'Group-Level Analysis':
        df = df[df['user'] == selected_user]
    # returning the series containing month_name with it's msgs frequency.
    return df["month"].value_counts()

def creating_heatmap(selected_user,df):
    if selected_user != 'Group-Level Analysis':
        df = df[df['user'] == selected_user]
    # creating a pivot table
    pivot_table_df = df.pivot_table(index='day_name', columns='time_slot', values='message', aggfunc='count').fillna(0)
    return pivot_table_df

