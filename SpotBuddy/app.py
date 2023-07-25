from api import *
import pandas as pd
import time
import streamlit.components.v1 as components
import streamlit as st

#title of page
st.title("SpotBuddy 🎵")
                                                                                                                                                   


#hiding menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


st.header("Hello! Not sure what songs to listen to? I can help 😊")
st.write("Tell me your favorite song and I'll recommend new songs you should try out!")


#user input
songname = st.text_input('Enter song name')
artistname = st.text_input('Enter artist name')
genre= st.multiselect(
    'Select a maximum of three genres',
    ['pop','classical','indian','rock','hiphop','k-pop'],max_selections=3) 
#you can add more genres as options
limit=st.number_input('No. of recommendations', min_value=5, max_value=None, step=1)

#upon clicking button
if st.button(label="Recommend",key="Recommend"):

    #getting meta data of the song that user inputs
    all = get_meta(songname,artistname, search_type="track")
    df = pd.DataFrame(
        all, columns=['track_name', 'track_id', 'artist_name', 'artist_id'])

    #getting artist id and track/song id from the result returned
    artistid = df['artist_id'].iloc[0]
    trackid = df['track_id'].iloc[0]

    st.header("Here's your song....")
    link="https://open.spotify.com/embed/track/"+trackid

    #adding component
    components.iframe(link, height=300)



    st.header("Since you liked "+songname+", you should try out...")

    #getting result of the api of get_recommendations
    reccs = get_reccomended_songs(limit, seed_artists=str(artistid), seed_tracks=str(trackid),seed_genres=str(genre))
    df = pd.DataFrame(reccs, columns=["Songs", "Artists", "Link"]).rename_axis('Index', axis=1)

    #getting list of links from dataframe
    links=df["Link"]

    #adding components/widgets in streamlit to allow users to preview the song
    for link in links:
        #link is of the form 
        #https://open.spotify.com/track/xxxxxxxxxxxxxxxxx"
        #we need to add embed before "track"
        substring="track"
        insertsubstring="embed/"
        idx = link.index(substring)
        link=link[:idx] + insertsubstring + link[idx:]
    
        #adding component
        components.iframe(link, height=300)

    

