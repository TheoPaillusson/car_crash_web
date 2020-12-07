
import streamlit as st
import datetime
import requests
import ipdb

st.markdown("""# Predict the dangerousness of a car trip

How dangerous is your trip today ?""")



# input
departure = st.text_input('Departure')
arrival = st.text_input('Arrival')

# return departure & arrival inputs
def return_inputs():
    '''function wich return the departure & arrival entered by user'''
    return departure, arrival

# @st.cache
# def get_map_data():
#     print('get_map_data called')
#     return pd.DataFrame(
#             np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#             columns=['lat', 'lon']
#         )

# if st.checkbox('Show map', False):
#     df = get_map_data()

#     st.map(df)
# else:
#     from PIL import Image
#     image = Image.open('images/map.png')
#     st.image(image, caption='map', use_column_width=False)


# bouton pour exécuter la requête
url = ''
params = {'d_long':, 'd_lat':, 'a_long':, 'a_lat':}
response = requests.get(url, params=params)