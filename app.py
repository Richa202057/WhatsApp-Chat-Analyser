import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import ConvertStringToDataframe
from statistics import do_stats, most_busy_users, create_wordcloud, top_20_words, monthly_timeline, daily_timeline, weekly_activity,monthly_activity,creating_heatmap

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # the following code will be executed when user will upload a file successively.

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    ## converting this bytes of stream into a string
    data = bytes_data.decode("utf-8")
    ## passing this string to a function which will generate a required dataframe , so that we can analyse this data
    df = ConvertStringToDataframe(data)
    # to print dataframe on web page dataframe function of streamlit is used.
    #st.dataframe(df)

    ## creating a dropdown/selectbox to selct a user or selecting a group-level analysis.
    users_list = df["user"].unique().tolist()
    ## this is a list containing all unique users including group-notification as a user
    # so, removing this group-notification from this list
    users_list.remove("group_notification")
    users_list.sort()
    users_list.insert(0, "Group-Level Analysis")

    selected_user = st.sidebar.selectbox("Show analysis wrt", users_list)  # this is the selectbox appear always

    if st.sidebar.button("Show Analysis"):
        # when user will press this button then the following code will be executed.
        st.title("Top Statistics")
        msg, media, no_links = do_stats(df, selected_user)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Total Messages")
            st.title(msg)
        with col2:
            st.header("Number of Media shared")
            st.title(media)
        with col3:
            st.header("Number of Links shared")
            st.title(no_links)

        # # showing the top busy users in the group , so, this following things will be show when selected_user is
        # group-level analysis it is only for group - level
        if selected_user == 'Group-Level Analysis':
            st.title('Most Busy Users')
            x, new_df = most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='#09eb2f')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        ## showing the top 20 words stat
        freq_word_df = top_20_words(df, selected_user)
        st.title("Top 20 Frequently used Words")
        # st.dataframe(freq_word_df)
        # rather than displaying it in a dataframe , showing this in a bar graph
        fig, ax = plt.subplots()
        ax.barh(freq_word_df[0], freq_word_df[1],color='#f26e0a')
        ## word will be on x-axis anf frequency ony-axis.## barh means horizontal bar graph, it is a rotation of simple bar graph.
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # showing most-active day in a week using  bar-chart
        # and showing most-active month in a week using  bar-chart
        col1, col2 = st.columns(2)
        with col1:
            # showing most-active day in a week using  bar-chart
            st.title("Most Active Day in a Week")
            busy_day = weekly_activity(selected_user,df)  # busy_day is a series in which day_name is at index and it's message frequency is at value
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#0896c9')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            # showing most-active month in a week using  bar-chart
            st.title("Most Active Month")
            busy_month = monthly_activity(selected_user,df)  # busy_month is a series in which day_name is at index and it's message frequency is at value
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#e8301c')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # showing  month-year based activity in group
        st.title("Monthly Timeline Chart")
        timeline = monthly_timeline(selected_user, df)
        # st.dataframe(timeline)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # showing day-month-year based activity in a group
        st.title("Daily Timeline Chart")
        daily_timeline = daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#34e5eb')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        st.title("Activity Map for each period of day for Each day of a Week")
        pivot_df=creating_heatmap(selected_user, df) # df1 is a pivot table dataframe
        # st.dataframe(pivot_df)
        fig,ax=plt.subplots()
        ax = sns.heatmap(pivot_df)
        st.pyplot(fig)

        # generating wordcloud (for both group-level and user-level)
        st.title("Wordcloud")
        df_wc = create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)



