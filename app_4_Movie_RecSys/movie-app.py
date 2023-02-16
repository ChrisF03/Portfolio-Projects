import streamlit as st
import pandas as pd
import pickle 
import requests
from PIL import Image

st.set_page_config(page_title='Movie Recommendations', page_icon=':movie_camera:',layout="wide")

st.markdown(
f"""
<style>
.stApp {{
background: url("https://img.freepik.com/free-vector/blue-pink-halftone-background_53876-99004.jpg?w=740&t=st=1676525100~exp=1676525700~hmac=20fb8f51bc71a9d8b8a9a12f0d84d32c5ee288ca527f19e310fff83db75dd8b0");
background-size: cover
}}
</style>
""",
unsafe_allow_html=True )

title_image = Image.open(r"app_4_Movie_RecSys/film-reel.png")
st.image(title_image, use_column_width=True)

st.title('Movie Recommender System')

st.markdown('''
Using recommendation systems may have been a thing of complexity and even luxury for companies in the past, but in the increasingly high-speed, high-tech world we live in today it has become a necessity to most. Recommender systems have revolutionized e-commerce, video/music streaming services, and even online dating. Corporations like Netflix, Amazon and Youtube, have vaulted themselves into being among the most valuable companies in the world due, in very large part, to the recommendation systems that consumers are so reliant on.

In this project, we will build a content-based movie recommendation system based on features such as genre, movie overview, and cast and crew, among others.  

This dataset was generated from The Movie Database API, sourced from Kaggle and can be found here : 
> **[Kaggle Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)**

The raw dataset contains 5000 movies, with release dates ranging from the year 1916 up until February 2017. 

* **Python libraries:** Streamlit, Pandas, NumPy, NLTK, Sklearn, Requests, Pickle, Pillow, Time
''')

st.write('---')

df = pd.read_csv(r"app_4_Movie_RecSys/cleaned_movies.csv")

def get_poster(movie_id) : 
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bb0679bfdbbe5216f83c0b786a34410f&language=en-US.'.format(movie_id))
    data = response.json()
    return 'http://image.tmdb.org/t/p/w300/' + data['poster_path']

def get_runtime(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9929fa51f8a285339f1ec596d538b8a&language=en-US'.format(movie_id))
    data = response.json()
    return str(data['runtime']) + ' minutes'

def get_summary(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9929fa51f8a285339f1ec596d538b8a&language=en-US'.format(movie_id))
    data = response.json()
    return  str(data['overview'])

def get_actors(movie_id):
    cast_list = df['cast'][df['movie_id']==movie_id]
    return cast_list

def get_director(movie_id):
    director = df['crew'][df['movie_id']==movie_id]
    return director

def get_genre(movie_id):
    genre = df['genres'][df['movie_id']==movie_id]
    return genre

def get_keywords(movie_id):
    keyword = df['keywords'][df['movie_id']==movie_id]
    return keyword

def release_date(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9929fa51f8a285339f1ec596d538b8a&language=en-US'.format(movie_id))
    data = response.json()
    return (data['release_date'])

def get_voting(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9929fa51f8a285339f1ec596d538b8a&language=en-US'.format(movie_id))
    data = response.json()
    return str(data['vote_average'])+ '/10'

def get_movie_budget(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9929fa51f8a285339f1ec596d538b8a&language=en-US'.format(movie_id))
    data = response.json()
    return 'USD ' + str(data['budget'])

def get_movie_revenue(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9929fa51f8a285339f1ec596d538b8a&language=en-US'.format(movie_id))
    data = response.json()
    return 'USD ' + str(data['revenue'])

movies_dict = pickle.load(open(r'app_4_Movie_RecSys/movies_dict.pkl', 'rb'))
similarity = pickle.load(open(r'app_4_Movie_RecSys/similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]
    recommended_movies_runtime = []
    recommended_movie_overview = []
    recommended_movie_actors = []
    recommended_movie_director = []
    recommended_movie_genres = []
    recommended_movie_keywords = []
    recommended_movie_date = []
    recommended_movie_vote = []
    recommended_movie_budget = []
    recommended_movie_revenue = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(get_poster(movie_id))
        recommended_movies_runtime.append(get_runtime(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_overview.append(get_summary(movie_id))
        recommended_movie_actors.append(get_actors(movie_id))
        recommended_movie_director.append(get_director(movie_id))
        recommended_movie_genres.append(get_genre(movie_id))
        recommended_movie_keywords.append(get_keywords(movie_id))
        recommended_movie_date.append(release_date(movie_id))
        recommended_movie_vote.append(get_voting(movie_id))
        recommended_movie_budget.append(get_movie_budget(movie_id))
        recommended_movie_revenue.append(get_movie_revenue(movie_id))
    return recommended_movies,recommended_movies_posters, recommended_movies_runtime,recommended_movie_overview, recommended_movie_actors, recommended_movie_director,recommended_movie_genres, recommended_movie_keywords,recommended_movie_date,recommended_movie_vote, recommended_movie_budget, recommended_movie_revenue


selected_movie_name = st.selectbox(
    'Please Select a Film',
    movies['title'].values)

columns = st.columns((2, 1, 2))

if columns[1].button('Recommend'):
    import time

    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1) 
    names,posters,runtime, overview, actors, directors,genres, keywords, date, vote, budget, revenue = recommend(selected_movie_name)
    st.write('Top 5 Suggested Movies for {}'.format(selected_movie_name))

    col1, col2, col3, col4, col5 = st.tabs(['1️', '2️', '3️', '4️', '5️'])

    with col1:
        st.header(names[0])
        st.image(posters[0])
        st.success('Overview')
        st.write(overview[0])
        st.info('Release Date')
        st.write(date[0])
        st.info('Rating')
        st.write(vote[0])
        st.info('Runtime')
        st.markdown(runtime[0])
        st.info('Genres')
        st.write(genres[0])
        st.info('Cast Members')
        st.write(actors[0])
        st.info('Crew (Director, Screenplay, Producer)')
        st.write(directors[0])
        st.info('Related Keywords')
        st.write(keywords[0])
        st.info('Movie Budget')
        st.write(budget[0])
        st.info('Box Office (Revenue)')
        st.write(revenue[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])
        st.success('Overview')
        st.write(overview[1])
        st.info('Release Date')
        st.write(date[1])
        st.info('Rating')
        st.write(vote[1])
        st.info('Runtime')
        st.markdown(runtime[1])
        st.info('Genres')
        st.write(genres[1])
        st.info('Cast Members')
        st.write(actors[1])
        st.info('Director')
        st.write(directors[1])
        st.info('Related Keywords')
        st.write(keywords[1])
        st.info('Movie Budget')
        st.write(budget[1])
        st.info('Box Office (Revenue)')
        st.write(revenue[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])
        st.success('Overview')
        st.write(overview[2])
        st.info('Release Date')
        st.write(date[2])
        st.info('Rating')
        st.write(vote[2])
        st.info('Runtime')
        st.markdown(runtime[2])
        st.info('Genres')
        st.write(genres[2])
        st.info('Cast Members')
        st.write(actors[2])
        st.info('Director')
        st.write(directors[2])
        st.info('Related Keywords')
        st.write(keywords[2])
        st.info('Movie Budget')
        st.write(budget[2])
        st.info('Box Office (Revenue)')
        st.write(revenue[2])

    with col4:  
        st.header(names[3])
        st.image(posters[3])
        st.success('Overview')
        st.write(overview[3])
        st.info('Release Date')
        st.write(date[3])
        st.info('Rating')
        st.write(vote[3])
        st.info('Runtime')
        st.markdown(runtime[3])
        st.info('Genres')
        st.write(genres[3])
        st.info('Cast Members')
        st.write(actors[3])
        st.info('Director')
        st.write(directors[3])
        st.info('Related Keywords')
        st.write(keywords[3])
        st.info('Movie Budget')
        st.write(budget[3])
        st.info('Box Office (Revenue)')
        st.write(revenue[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])
        st.success('Overview')
        st.write(overview[4])
        st.info('Release Date')
        st.write(date[4])
        st.info('Rating')
        st.write(vote[4])
        st.info('Runtime')
        st.markdown(runtime[4])
        st.info('Genres')
        st.write(genres[4])
        st.info('Cast Members')
        st.write(actors[4])
        st.info('Director')
        st.write(directors[4])
        st.info('Related Keywords')
        st.write(keywords[4])
        st.info('Movie Budget')
        st.write(budget[4])
        st.info('Box Office (Revenue)')
        st.write(revenue[4])

st.write('---')
st.write('All data is atrributed to :')
image = Image.open(r"app_4_Movie_RecSys/tmdb-logo.png")
st.image(image, use_column_width=False)
