
import streamlit as st
import datetime
import requests
import ipdb
import os
from os.path import join, dirname
from dotenv import load_dotenv
from itinerary import get_coordinates, itinerary
import json
from fastapi import FastAPI


api = FastAPI()

# for google api key
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)
google_map_api = os.environ.get('GOOGLE_MAP_API')



st.markdown("""# Predict the dangerousness of a car trip 🚗

## How dangerous is your trip today ?""")


# ----------------------------------
############### INPUT ##############
# ----------------------------------

# departure & arrival
departure = st.text_input('Departure')
arrival = st.text_input('Arrival')

# day of the week and datetime
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day = st.selectbox('Select the day of your departure', days)

hour = st.text_input('Hour of departure')

# ----------------------------------
############### API ################
# ----------------------------------

# bouton pour exécuter la requête
if st.button('Predict'):
    st.write('I was clicked 🎉')
    # get coordinates from google api & return dict of roads
    coordinates = get_coordinates(departure=departure, arrival=arrival, api=google_map_api)
    itineraire = itinerary(coordinates)
    st.write(type(itineraire))
    url_iti = 'http://127.0.0.1:8000/danger'
    
    headers = {'content-type' : 'application/json'}


    body = {'steps':itineraire, 'day':day, 'hour':hour}
    st.write(body)
    request = requests.post(url_iti, json=body, headers=headers)
    r = request.json()
    r
else:
    st.write('I was not clicked 😞')


st.map()
