import streamlit as st
import  requests
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

OMDB_API_KEY = '5a9cddc0'
movies_data = pd.read_pickle("movies.pkl")
distances = pickle.load(open('distances.pkl','rb'))


def get_poster_by_title(title):

    url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        movie_data = response.json()
        if movie_data.get('Response') == 'True':

            poster_url = movie_data.get('Poster')
            return poster_url
        else:
            return f"Error: {movie_data.get('Error', 'Unknown error')}"
    else:
        return f"Error fetching data from OMDb. Status code: {response.status_code}"

def fetchMovies(m):
    index = movies_data[movies_data['title']==m].index[0]
    distance=distances[index]
    obj=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    match_ratio=[]
    images =[]
    titles=[]
    for i in obj:
        t=movies_data.iloc[i[0]].title
        match_ratio.append(i[1])
        titles.append(t)
        try:
            images.append(get_poster_by_title(t))
        except:
            continue
    return images,titles,match_ratio


st.set_page_config(page_title="Reel Pick", page_icon="🎬", layout="wide")

if 'show_selectbox' not in st.session_state:
    st.session_state.show_selectbox = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

st.title("🎬 Reel Pick")
st.image(r"resource\frontpage.jpg", use_column_width=True)
st.write("Discover your next favorite movie with personalized recommendations!")

st.write(
    """
    **Reel Pick** helps you find movies you'll love based on your preferences. 
    Whether you're into action, comedy, drama, or documentaries, our recommender system suggests movies tailored just for you.
    """
)

st.subheader("How It Works")
st.write(
    """
    1. **Select Your Preferences**: Choose genres and types of movies you enjoy.
    2. **Get Recommendations**: Receive a curated list of movie suggestions.
    3. **Watch and Enjoy**: Discover and enjoy new movies based on your tastes.
    """
)

if st.button('Get Started'):
    st.session_state.show_selectbox = True

if st.session_state.show_selectbox:
    st.session_state.selected_option = st.selectbox(
        "Choose a movie",
        movies_data.title.values,
    )

    st.write("You selected:", st.session_state.selected_option)

if st.button('Recommend'):
    if st.session_state.selected_option is not None:
        images,titles,dist=fetchMovies(st.session_state.selected_option)
        st.columns(np.ones(len(images)))
        count=0
        for cols in st.columns(np.ones(len(images))):
            with cols:
                st.image(images[count])
                st.write(titles[count])
                count+=1


        st.subheader("📈Graphs -> ")
        c1,c2=st.columns((1,1))
        with c1:
            fig, ax = plt.subplots()
            sns.set_style('whitegrid')
            # plt.bar(titles,dist,width=0.5,label="Matched Content")
            sns.barplot(x=titles,y=dist,palette='viridis')
            plt.xticks(titles,rotation=12)
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            st.pyplot(fig)
        with c2:
            fig2, ax2 = plt.subplots()
            #plt.pie(dist,labels=titles,autopct='%1.1f%%')
            wedges, texts, autotexts = ax2.pie(
                dist,
                labels=titles,
                autopct='%1.1f%%',
                colors=sns.color_palette('plasma', len(titles))
            )

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')



            fig2.patch.set_facecolor('#0E1117')
            ax2.set_facecolor('#0E1117')

            st.pyplot(fig2)

    else:
        st.write("Choose a movie first !")

if st.button("Show DataBase"):
    st.write(movies_data)




