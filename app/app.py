
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
if st.button('Predict'):
    # print is visible in server output, not in the page
    print('button clicked!')
    st.write('I was clicked 🎉')
    d_long = 'theo'
    d_lat = 'test'
    a_long = 'zfz'
    a_lat = '32'

    url = 'http://127.0.0.1:8000/danger'
    params = {'departure':departure, 'arrival':arrival}
    response = requests.get(url, params=params)
    danger = response.json()
    danger
else:
    st.write('I was not clicked 😞')



