import pandas as pd
import requests

API_KEY='AIzaSyBdw2tFIyC7DBe5MiU_yrb_Juz1HuZhop0'

def geocode(address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
    response = requests.get(url).json()
    if response['status'] == 'OK':
        location = response['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

# 元CSV読み込み
df = pd.read_csv('moto_spots.csv', encoding='utf-8')
df['lat'], df['lng'] = None, None

for i, row in df.iterrows():
    lat, lng = geocode(row['address'])
    if lat and lng:
        df.at[i, 'lat'] = lat
        df.at[i, 'lng'] = lng

# 新しいCSVとして保存
df.to_csv('moto_spots_added.csv', index=False, encoding='utf-8')
print("保存完了！")