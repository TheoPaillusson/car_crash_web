
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

#test map
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
############### API ################
# -------------------

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


######################## TESTTTTTTT ##############################
import requests
coordinates = (-118.249845,34.0553454,-118.4694832,33.9850469)
def itinerary(coordinates):
    ''' Takes GPS coordinates and return route in a dict {name:distance}'''
    url = f'http://router.project-osrm.org/route/v1/driving/{coordinates[0]},{coordinates[1]};{coordinates[2]},{coordinates[3]}?overview=false&steps=true'
    response = requests.get(url).json()
    step = response['routes'][0]['legs'][0]['steps']
    names = []
    count = 0
    for i in range(len(step)):
        if response['routes'][0]['legs'][0]['steps'][i]['name'] == "":
            response['routes'][0]['legs'][0]['steps'][i]['name'] = count
            count += 1
        names.append(response['routes'][0]['legs'][0]['steps'][i]['name'])
    del names[-1]
    distances = []
    for i in range(len(step)):
        distances.append(response['routes'][0]['legs'][0]['steps'][i]['distance'])
    del distances[-1]
    route = pd.DataFrame(columns=['names','distances'])
    route.names = names
    route.distances = distances
    return route

route = itinerary(coordinates)

st.dataframe(route)



geojson = get_geojson(coordinates = get_coordinates(departure=departure, arrival=arrival, api=google_map_api))

df = pd.DataFrame(geojson, columns=['lat', 'lon'])
df['lon2'] = df['lon']
df['lon'] = df['lat']
df['lat'] = df['lon2']

st.map(df)

# pickup_longitude,pickup_latitude = -118,34
# dropoff_longitude,dropoff_latitude = -118,33
# @st.cache
# def get_map_data():
#     print('get_map_data called')
#     return pd.DataFrame(
#         data= np.array([
#             [pickup_longitude,pickup_latitude],
#             [dropoff_longitude,dropoff_latitude],
#             ]),
#         columns= ['lon','lat'],
#         index=['star','end']
#         )
# if st.checkbox('Show map', False):
#     df = get_map_data()
#     #st.map(df)
#     GREEN_RGB = [0, 255, 0, 40]
#     RED_RGB = [240, 100, 0, 40]
#     st.pydeck_chart(pdk.Deck(
#          map_style='mapbox://styles/mapbox/light-v9',
#          initial_view_state=pdk.ViewState(
#              latitude=(pickup_latitude+dropoff_latitude)/2,
#              longitude=(pickup_longitude+dropoff_longitude)/2,
#              zoom=10,
#              pitch=40,
#          ),
#          layers=[
#             pdk.Layer(
#             'ScatterplotLayer',
#             df,
#             get_position=['lon', 'lat'],
#             auto_highlight=False,
#             get_radius=300,
#             get_fill_color='[180, 0, 200, 140]',
#             pickable=True
#              ),
#             pdk.Layer(
#                 "ArcLayer",
#                 data=df,
#                 get_width=6,
#                 get_source_position=[pickup_longitude, pickup_latitude],
#                 get_target_position=[dropoff_longitude, dropoff_latitude],
#                 get_tilt=2,
#                 get_source_color=GREEN_RGB,
#                 get_target_color=RED_RGB,
#                 pickable=True,
#                 opacity=100,
#                 auto_highlight=False
#                 )
#          ],
#      ))
