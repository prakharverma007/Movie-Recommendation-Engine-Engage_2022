import streamlit as st
import pickle
import pandas as pd
import requests

# setting webpage title and layout
st.set_page_config(page_title="MOVIEFLIX",layout="wide")

# Removing Header, footer, MainMenu option of streamlit (line9-line45)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# method to disable default fullscreen option from images in streamlit
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

# Styling for the header of the webpage
st.markdown("""
<style>
.big-font {
    font-size:60px ;
    margin-top:-5%;
    color: red;
    text-align:center;
    font-weight: bold;
}
.text{
    font-size:40px ;
    color: white;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)


# header of the webpage
st.markdown('<p class="big-font">MOVIEFLIX</p>', unsafe_allow_html=True)

# function to set background image on streamlit webpage
def set_bg():
      st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://browsecat.net/sites/default/files/netflix-background-128505-385453-2432231.png");
             background-size: cover;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

set_bg()

# Declaring all the needed Libraries and Movie Dataframe
movies_dict = pickle.load(open('movie_dictionary.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('Similarity.pkl','rb'))

# function to find poster of movie from TMDB API
def find_poster(movie_id):
    res=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ce678db061ca2150428101b474a8ae98&language=en-US'.format(movie_id))
    API_movie_data=res.json()
    return "https://image.tmdb.org/t/p/w500/"+ API_movie_data['poster_path']

# function to find overview of movie from TMDB API
def find_overview(movie_id):
    res = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=ce678db061ca2150428101b474a8ae98&language=en-US'.format(
            movie_id))
    API_movie_data = res.json()
    return API_movie_data['overview']

# function to find official link of movie from TMDB API
def find_link(movie_id):
    res = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=ce678db061ca2150428101b474a8ae98&language=en-US'.format(
            movie_id))
    API_movie_data = res.json()
    return API_movie_data['homepage']

# function to find rating of movie from TMDB API
def find_rating(movie_id):
    res = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=ce678db061ca2150428101b474a8ae98&language=en-US'.format(
            movie_id))
    API_movie_data = res.json()
    return API_movie_data['vote_average']

# function to find release date of movie from TMDB API
def find_release_date(movie_id):
    res = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=ce678db061ca2150428101b474a8ae98&language=en-US'.format(
            movie_id))
    API_movie_data = res.json()
    return API_movie_data['release_date']

# function to fetch the all movie detail from TMDB API
def recommend_movie(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:11]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_overview = []
    recommended_movies_link = []
    recommended_movies_rating = []
    recommended_movies_release_date = []
    for i in movie_list:
       movie_id = movies.iloc[i[0]].movie_id
       recommended_movies.append(movies.iloc[i[0]].title)
# fetch poster from API
       recommended_movies_poster.append(find_poster(movie_id))
# fetch overview from API
       recommended_movies_overview.append(find_overview(movie_id))
# fetch official link from API
       recommended_movies_link.append(find_link(movie_id))
# fetch IMDB rating from API
       recommended_movies_rating.append(str(find_rating(movie_id)))
# fetch IMDB rating from API
       recommended_movies_release_date.append(str(find_release_date(movie_id)))
    return recommended_movies,recommended_movies_poster,recommended_movies_overview,recommended_movies_link,recommended_movies_rating,recommended_movies_release_date

# Taking the Selected movie name from selectbox
selected_movie=st.selectbox('Select / Type Movie Name',movies['title'].values)


# method to set the button in center in streamlit
col1, col2, col3 , col4, col5 ,col6, col7,col8 ,col9= st.columns(9)

with col1:
    pass
with col2:
    pass
with col3:
    pass
with col4:
    pass
with col6:
    pass
with col7 :
    pass
with col8:
    pass
with col9 :
    pass
with col5 :
    center_button = st.button('Search')


if center_button==True:
    # taking all corresponding movie detail in seperate list
    names, posters, overview, link, rating, release_date = recommend_movie(selected_movie)
    st.write('-----')

    # Creating two column left column for Selected movie poster and right column for detail
    leftcol, rightcol=st.columns(2)
    with leftcol:
        pass
        st.image(posters[0])
    with rightcol:
        st.header(selected_movie)
        st.write('----------')
        st.write(overview[0])
        st.write('----------')
        st.write('Movie Official Link : '+link[0])
        st.write('----------')
        st.write('Rating : ' + rating[0])
        st.write('----------')
        st.write('Release Date  :  ' + release_date[0])
        st.write('----------')

    st.write('-------')
    st.markdown('<p class="text">10 Recommended Movies Based On Selected Movie</p>', unsafe_allow_html=True)
    st.write('-------')

# creating five column for first 5 recommeneded movies
    col1, col2, col3, col4, col5 =st.columns(5)
    with col1:
        st.image(posters[1])
        st.write('----------')
        st.write(names[1])
        st.write('Rating : ' + rating[1])
        st.write('----------')

    with col2:
        st.image(posters[2])
        st.write('----------')
        st.write(names[2])
        st.write('Rating : ' + rating[2])
        st.write('----------')

    with col3:
        st.image(posters[3])
        st.write('----------')
        st.write(names[3])
        st.write('Rating : ' + rating[3])
        st.write('----------')

    with col4:
        st.image(posters[4])
        st.write('----------')
        st.write(names[4])
        st.write('Rating : ' + rating[4])
        st.write('----------')

    with col5:
        st.image(posters[5])
        st.write('----------')
        st.write(names[5])
        st.write('Rating : ' + rating[5])
        st.write('----------')


# creating five column for second 5 recommeneded movies
    col6, col7, col8, col9, col10 =st.columns(5)
    with col6:
        st.image(posters[6])
        st.write('----------')
        st.write(names[6])
        st.write('Rating : ' + rating[6])
        st.write('----------')

    with col7:
        st.image(posters[7])
        st.write('----------')
        st.write(names[7])
        st.write('Rating : ' + rating[7])
        st.write('----------')

    with col8:
        st.image(posters[8])
        st.write('----------')
        st.write(names[8])
        st.write('Rating : ' + rating[8])
        st.write('----------')

    with col9:
        st.image(posters[9])
        st.write('----------')
        st.write(names[9])
        st.write('Rating : ' + rating[9])
        st.write('----------')

    with col10:
        st.image(posters[10])
        st.write('----------')
        st.write(names[10])
        st.write('Rating : ' + rating[10])
        st.write('----------')

# Created Two set of five columns Because
# on creating 10 columns in one row the posters are appearing very small.
