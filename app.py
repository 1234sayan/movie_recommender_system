import pickle
import pandas as pd
import streamlit as st
import requests
import numpy as np


st.title('Movies Recommender System')

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

with np.load("top_similar_movies.npz") as data:
    top_indices = data["top_indices"]

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a2eb0959abd16e19b7e27072d735f64c'.format(movie_id))
    data_path = response.json()
    #print(data)
    return  "https://image.tmdb.org/t/p/w500" + data_path['poster_path']


### def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters ###
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    recommended_indices = top_indices[movie_index][:5]

    name = []
    poster = []

    for idx in recommended_indices:
        movie_id = movies.iloc[idx]["movie_id"]
        name.append(movies.iloc[idx]["title"])
        poster.append(fetch_poster(movie_id))

    return name, poster


selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

#st.write("You selected:", option)
st.button("Reset", type="primary")
if st.button('Show Recommendation'):
    name ,poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])

