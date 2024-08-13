import streamlit as st
import pickle
import pandas as pd
import requests

st.title("MOVIE RECOMMENDER SYSTEM")
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarities = pickle.load(open('Similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=cc6bb8af083b7ec994c716019082ebb8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['original_title']==movie].index[0]
    distances = similarities[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movieid = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_movies_poster.append(fetch_poster(movieid))
    return recommended_movies,recommended_movies_poster



Selected_movie = st.selectbox('Select the Movie',movies['original_title'])

if st.button('Recommend'):
    movie_name,movie_poster = recommend(Selected_movie)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
