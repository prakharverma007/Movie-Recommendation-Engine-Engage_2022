import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:60px ;
    color: red;
    text-align:center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">MOVIEFLIX</p>', unsafe_allow_html=True)


def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://browsecat.net/sites/default/files/netflix-background-128505-385453-2432231.png");
             background-size: cover
             
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
set_bg_hack_url()

movies_dict=pickle.load(open('movie_dictionary.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('Similarity.pkl','rb'))


def recommend_movie(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
       movie_id = movies.iloc[i[0]].movie_id
       recommended_movies.append(movies.iloc[i[0]].title)
       # fetch poster from API
       recommended_movies_poster.append(find_poster(movie_id))
    return recommended_movies,recommended_movies_poster

def find_poster(movie_id):
    res=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ce678db061ca2150428101b474a8ae98&language=en-US'.format(movie_id))
    API_movie_data=res.json()
    return "https://image.tmdb.org/t/p/w500/"+ API_movie_data['poster_path']



selected_movie=st.selectbox(
    'Select Movie For Recommendation ',
    movies['title'].values)

if st.button('Recommend'):
    st.header('Selected movie : '+selected_movie)
    st.write('----------------------------------------------------------------------------------------------------------')
    st.header('5 Recommended Movie based on : '+selected_movie)
    st.write('----------------------------------------------------------------------------------------------------------')
    names,posters =recommend_movie(selected_movie)

    col1, col2, col3, col4, col5 =st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])

    with col2:
        st.write(names[1])
        st.image(posters[1])

    with col3:
        st.write(names[2])
        st.image(posters[2])

    with col4:
        st.write(names[3])
        st.image(posters[3])

    with col5:
        st.write(names[4])
        st.image(posters[4])