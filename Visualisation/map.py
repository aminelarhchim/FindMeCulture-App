import sys
import os
from pathlib import Path
scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))

import geopandas as gpd 
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
import matplotlib.pyplot as plt
# from cartopy.io.img_tiles import OSM
from  extract_data import *
import pandas as pd 
from shapely.geometry import Point
from shapely.geometry import Polygon
from geopy.extra.rate_limiter import RateLimiter

from geopy.geocoders import Nominatim

def adresse_coordonnees (adresse): 
   
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(adresse,timeout = 10)
    if location is not None and location.longitude is not None:                                                       
        return (location.latitude, location.longitude)
    return (0,0)

def  coordonnees_musees (dataf):
    dataf['latitude']=0
    dataf['longitude']=0
    # for id,row in dataf.iterrows():
    #     co =adresse_coordonnees(dataf.at[id, 'ADR'])
    #     geolocator = Nominatim(user_agent="specify_your_app_name_here")

    #     geocode=RateLimiter(geolocator.geocode, min_delay_seconds=1)
    #     dataf.at[id, 'latitude']= co[0]
    #     dataf.at[id, 'longitude']= co[1]
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode=RateLimiter(geolocator.geocode, min_delay_seconds=1) 
    dataf['location']=dataf['ADR'].apply ( geocode)
    dataf['latitude']=0
    dataf['longitude']=0
    for id,row in dataf.iterrows():
        dataf.at[id, 'latitude']= dataf.loc[id,'location'][0]
        dataf.at[id, 'longitude']=dataf.loc[id,'location'][1]
        del dataf['location']
    return dataf

# def mapplot (df):
#     fig = plt.figure(figsize=(8,8))
#     ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
#     ax.set_extent([-5, 10, 42, 52])

#     imagery = OSM()
#     ax.add_image(imagery, 5)
#     # plus c'est grand, plus c'est précis, plus ça prend du temps
    
#     ax.plot(df.longitude[:5], df.latitude[:5], '.')
#     ax.title='carte de repartition des musées en France'
#     plt.show()

def map2 ( df ):
    map_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    points =[]
    for id,row in df.iterrows():
        lat=df.loc[id, 'latitude']
        lon=df.loc[id, 'longitude']
        if (lon,lat)!=(0.0,0.0):
            points.append(Point(lon, lat)) 
    enedis = gpd.GeoDataFrame(data=dict(geometry=points))
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    map_df.plot(ax=ax )
    enedis.plot(ax=ax, marker='o', color='red', markersize=2)
    ax.set_title("Carte de repartition des musees en France")
    plt.ylim(41, 54)
    plt.xlim(-6, 9)
    plt.show()  

museums = load_data(filename='museums',test=True)
df = museums.data

datacomplete=coordonnees_musees (df[0:30])
map2(datacomplete)

# mapplot (datacomplete)