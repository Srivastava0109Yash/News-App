import base64

import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
nltk.download('punkt')


st.set_page_config(page_title='Your News Portal')


def fetch_topics(topic):
    site='https://news.google.com/rss/search?q={}'.format(topic)
    op=urlopen(site)
    read=op.read()
    op.close()
    sp_page=BeautifulSoup(read,'xml')
    news=sp_page.find_all('item')
    return news


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)
    read = op.read()
    op.close()
    sp_page = BeautifulSoup(read, 'xml')
    news_list = sp_page.find_all('item')
    return news_list


def fetch_categories(topic):
    site='https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op=urlopen(site)
    read=op.read()
    op.close()
    sp_page=BeautifulSoup(read,'xml')
    news=sp_page.find_all('item')
    return news


def fetch_poster(link):
    try:
        url = urlopen(link)
        data = url.read()
        image = Image.open(io.BytesIO(data))
        st.image(image, use_column_width=True)
    except:
        image = Image.open("C:/Users/Yash/Downloads/Compressed/InNews-master/InNews-master/Meta/no_image.jpg")
        st.image(image, use_column_width=True)

def display_news(list,quantity):
    count=0

    for news in list:
        count+=1

        st.write('**({}) {}**'.format(count, news.title.text))
        data=Article(news.link.text)
        try:
            data.download()
            data.parse()
            data.nlp()

        except Exception as e:
            st.error(e)

        fetch_poster(data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)

        if count>= quantity:
            break


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
     <style>
     .stApp {{
         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
         background-size: cover
     }}
     </style>
     """,
        unsafe_allow_html=True
    )


add_bg_from_local("C:/Users/Yash/Downloads/Video/preview-195598-wSPLWjfONB-high_0000.avif")

def run():
        new_title = '<p style="font-family:serif; color:black;border-radius:100px ;background-color: orange;text-align: center; font-size: 42px;"><b>News App</b></p>'
        st.markdown(new_title, unsafe_allow_html=True)
        image=Image.open("C:/Users/Yash/Downloads/Video/images.jpeg")
        col1, col2, col3 = st.columns([3, 5, 3])

        with col1:
            st.write("")

        with col2:
            st.image(image, use_column_width=False)

        with col3:
            st.write("")
        category = ['--Select--', 'Trending News🔥', 'Favourite💙 Topics', 'Search🔍 Topic']
        cat_op = st.selectbox('Select your Category', category)
        if cat_op == category[0]:
            st.warning('Please select Type!!')
        elif cat_op == category[1]:
            st.subheader("👉 Here is the Trending🔥 news for you")
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_top_news()
            display_news(news_list, no_of_news)
        elif cat_op == category[2]:
            av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS',
                         'SCIENCE',
                         'HEALTH']

            st.subheader("Choose Your Favourite Topic")
            chosen_topic=st.selectbox("Choose your favourite Topic", av_topics)
            if chosen_topic==av_topics[0]:

                st.warning("Please Choose A Topic!!")
            else:
                no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
                news_list = fetch_categories(chosen_topic)
                if news_list:
                    st.subheader("👉 Here are the some {} News for you".format(chosen_topic))
                    display_news(news_list, no_of_news)
                else:
                    st.error("No News found for {}".format(chosen_topic))


        elif cat_op==category[3]:
            user_topic=st.text_input("Enter Your Topic")
            no_of_news=st.slider('Number of News:', min_value=5, max_value=15, step=1)

            if st.button("Search") and user_topic != '':
                user_topic_pr = user_topic.replace(' ', '')
                news_list = fetch_topics(topic=user_topic_pr)
                if news_list:
                    st.subheader("👉 Here are the some {} News for you".format(user_topic.capitalize()))
                    display_news(news_list, no_of_news)
                else:
                    st.error("No News found for {}".format(user_topic))
            else:
               st.warning("Please write Topic Name to Search🔍")

run()
