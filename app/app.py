import streamlit as st
import datetime
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from itinerary import get_coordinates, itinerary, get_geojson
import json
import pandas as pd
import numpy as np
import pydeck as pdk

################ SIDEBAR ################
st.set_page_config(
            page_title="CAR CRASH", # => Quick reference - Streamlit
            page_icon=":car:",
            layout="centered", # wide
            initial_sidebar_state="auto") #

# for google api key
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)
google_map_api = os.environ.get('GOOGLE_MAP_API')

st.markdown("""# Predict the dangerousness of a car trip
​
## How dangerous is your trip today ?""")

# ----------------------------------
############### INPUT ##############
# ----------------------------------

# departure & arrival
departure = st.text_input('Departure', 'Disney Concert Hall')
arrival = st.text_input('Arrival', 'Venice Beach')

# day of the week and datetime
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day = st.selectbox('Select the day of your departure', days)

time = [i for i in range(24)]
hour = st.selectbox('Select the time of your departure', time)


######### COEFICIANTS ###############
# OK
# if st.checkbox('Could your trip be any riskier?'):
#     st.write(''' :iphone: (handsfree) x1.05''')
#     st.write('''
#         :iphone: (handled) x1.29''')
#     st.write(''':wine_glass: x2.31''')
#     st.write(''':syringe: x20.02''')
#     st.write(''':syringe: & :wine_glass: x21.18''')
#     st.write(''':syringe: & :wine_glass: & :iphone: : x23.19 ''')

# st.write(f'<a name="Prediction"></a>', unsafe_allow_html=True)
# '# Prediction'

######### GEOJSON DF ###############
geojson = get_geojson(coordinates=get_coordinates(departure=departure, arrival=arrival, api=google_map_api))

df = pd.DataFrame(columns=['coordinates'])
df.at[0,'coordinates'] = geojson

# ----------------------------------
############### API ################
# ----------------------------------

# bouton pour exécuter la requête
if st.button('Predict'):
    st.write('I was clicked 🎉')
    # get coordinates from google api & return dict of roads
    coordinates = get_coordinates(departure=departure, arrival=arrival, api=google_map_api)
    itineraire = itinerary(coordinates)
    # convert dataframe to json to send to back
    trip = itineraire.to_json(orient='split')
    parsed = json.loads(trip)

    url_iti = 'http://127.0.0.1:8000/danger'

    headers = {'content-type' : 'application/json'}


    body = {'steps':parsed, 'day':day, 'hour':hour}
    request = requests.post(url_iti, json=body, headers=headers)
    r = request.json()
    r

1
######## trip on map ################
st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=34.0550,
            longitude=-118.2493,
            zoom=11,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                "TripsLayer",
                df,
                get_path="coordinates",
                get_color=  [74,128,245],
                opacity=10,
                width_min_pixels=7,
                rounded=True,
                trail_length=600,
                current_time=500,
            )
        ]
    ))


