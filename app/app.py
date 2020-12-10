import streamlit as st
import datetime
import requests
import ipdb
import os
from os.path import join, dirname
from dotenv import load_dotenv
from itinerary import get_coordinates, itinerary, get_geojson
import json
from fastapi import FastAPI
import pandas as pd
import numpy as np
import pydeck as pdk

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
######### MAP WITH GEJSON ##########
# ----------------------------------

geojson = get_geojson(coordinates=get_coordinates(departure=departure, arrival=arrival, api=google_map_api))

df = pd.DataFrame(geojson, columns=['lat', 'lon'])
df['lon2'] = df['lon']
df['lon'] = df['lat']
df['lat'] = df['lon2']

st.map(df)

# ----------------------------------
############### PREDICT ############
# ----------------------------------

# bouton pour exécuter la requête
if st.button('Predict'):
    st.write('I was clicked 🎉')
    # get coordinates from google api & return dict of roads
    coordinates = get_coordinates(departure=departure, arrival=arrival, api=google_map_api)
    itineraire = itinerary(coordinates)
    st.write(itineraire)

    # convert dataframe to json to send to back
    trip = itineraire.to_json(orient='split')
    parsed = json.loads(trip)

    url_iti = 'http://127.0.0.1:8000/danger'

    headers = {'content-type' : 'application/json'}

    body = {'steps':parsed, 'day':day, 'hour':hour}
    request = requests.post(url_iti, json=body, headers=headers)
    r = request.json()
    r
else:
    st.write('I was not clicked 😞')

# ----------------------------------
########### COEFICIANTS ############
# ----------------------------------

D = {'handsfree phone':3.88,'handling phone':4.76,'drunk':8.53,'drugs':73.88,'drunk&drugs':78.14,'drunk&drugs&phone':85.58}

if st.checkbox('Using a phone 📞'):
    st.write('''
        Using a phone during your trip increase the dangerousness by 
        ''')

if st.checkbox('Intoxicated 🍺'):
    st.write('''
        Driving intoxicated increase the dangerousness by 
        ''')

if st.checkbox('Drugged 💊'):
    st.write('''
        Driving drugged increase the dangerousness by 
        ''')