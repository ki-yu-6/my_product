import requests
from math import radians, sin, cos, sqrt, asin

API_KEY='AIzaSyBdw2tFIyC7DBe5MiU_yrb_Juz1HuZhop0'

def geocode(address):
    url=f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
    response=requests.get(url).json()
    location=response['results'][0]['geometry']['location']
    #lat:緯度、lng:経度
    return location['lat'], location['lng']

def haversine(lat1, lng1, lat2, lng2):
    R = 6371  #地球の半径
    dlat=radians(lat2 - lat1)
    dlng=radians(lng2 - lng1)
    lat1=radians(lat1)
    lat2=radians(lat2)
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    return round(2 * R * asin(sqrt(a)), 1)

def calc(user_lat, user_lng, min_dist, max_dist, df):
    df=df.copy()
    df['dist']=None

    for i in df.index:
        lat=df.at[i, 'lat']
        lng=df.at[i, 'lng']
        df.at[i, 'dist']=haversine(user_lat, user_lng, lat, lng)
    return df[(min_dist<=df['dist'])&(df['dist']<=max_dist)].sort_values('dist')