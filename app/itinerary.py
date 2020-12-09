#takes two addresses, returns route
import requests

def get_coordinates(departure, arrival, api):
    ''' Takes departure & arrival in string format and return GPS coordinates in a tuple (lon_start, lat_start, lon_end, lat_end)'''
    url_start = f'https://maps.googleapis.com/maps/api/geocode/json?address={departure}&key={api}'
    url_destination =f'https://maps.googleapis.com/maps/api/geocode/json?address={arrival}&key={api}'
    response1 = requests.get(url_start).json()
    response2 =requests.get(url_destination).json()
    lon_start = response1['results'][0]['geometry']['location']['lng']
    lat_start = response1['results'][0]['geometry']['location']['lat']
    lon_end = response2['results'][0]['geometry']['location']['lng']
    lat_end = response2['results'][0]['geometry']['location']['lat']
    return lon_start, lat_start, lon_end, lat_end

def itinerary(coordinates):
     ''' Takes GPS coordinates and return route in a dict {name:distance}'''
     url = f'http://router.project-osrm.org/route/v1/driving/{coordinates[0]},{coordinates[1]};{coordinates[2]},{coordinates[3]}?overview=false&steps=true'
     response = requests.get(url).json()
     step = response['routes'][0]['legs'][0]['steps']
     names = []
     for i in range(len(step)):
         names.append(response['routes'][0]['legs'][0]['steps'][i]['name'])
     del names[-1]
     distances = []
     for i in range(len(step)):
         distances.append(response['routes'][0]['legs'][0]['steps'][i]['distance'])
     del distances[-1]
     route = dict(zip(names,distances))
     return route

# # get map
def get_geojson(coordinates):
    '''Takes coordinates and return geojson'''
    url = f'http://router.project-osrm.org/route/v1/driving/{coordinates[0]},{coordinates[1]};{coordinates[2]},{coordinates[3]}?steps=true&geometries=geojson'
    response = requests.get(url).json()
    geojson = response['routes'][0]['geometry']['coordinates']
    return geojson
