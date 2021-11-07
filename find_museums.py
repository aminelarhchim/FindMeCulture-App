import os.path
import sys
from pathlib import Path

scriptpath = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)
sys.path.insert(0, scriptpath)
pickle_path = os.path.join(scriptpath, r'geolocalisation', r'museums_.pkl')

import re
import pandas as pd
import pickle
from geopy.geocoders import BANFrance
from geopy.distance import distance

global df
df = pd.read_pickle(pickle_path)

def correct_museum_data():
    
    from data_extraction.extract_data import load_data

    regions = {'AUVERGNE-RHÔNE-ALPES': 'Auvergne-Rhône-Alpes', 'BOURGOGNE-FRANCHE-COMTE': 'Bourgogne-Franche-Comté',
            'BRETAGNE': 'Bretagne', 'CENTRE-VAL DE LOIRE': 'Centre-Val de Loire', 'CORSE': 'Corse',
            'GRAND EST': 'Grand Est', 'GUADELOUPE': 'Guadeloupe', 'GUYANE': 'Guyane', 'HAUTS-DE-France': 'Hauts-de-France',
            'ÎLE-DE-France': 'Île-de-France', 'LA REUNION': 'La Réunion', 'MARTINIQUE': 'Martinique', 'NORMANDIE': 'Normandie',
            'NOUVELLE-AQUITAINE': 'Nouvelle-Aquitaine', 'OCCITANIE': 'Occitanie', 'PAYS DE LA LOIRE': 'Pays de la Loire',
            "PROVENCE-ALPES-CÔTE D'AZUR": "Provence-Alpes-Côte d'Azur", 'MAYOTTE': 'Mayotte'}

    museum_data = load_data(filename='museums').data
    
    for id, row in museum_data.iterrows():
        try:
            region = row['NEW REGIONS']
            df.at[id, 'NEW REGIONS'] = regions[region]
        except:
            pass
    
    pickle_path = os.path.join(scriptpath, r'geolocalisation', r'museums_.pkl')
    df.to_pickle(pickle_path)

#filter the museum data by region to reduce processing time
def filter_by_region(df, region):
    df=df.loc[df["NEW REGIONS"] == region]
    return(df)

def find_nearest_museums(adress, ville, num_museums=3, max_distance=100000, test=False):
    
    #load the coordinate dict pickle
    pickle_dir = os.path.join(scriptpath, r"geolocalisation", r"coordinate_dict.pkl")
    with open(pickle_dir, 'rb') as coordinate_pickle:
        coordinates_dict = pickle.load(coordinate_pickle)

    #initilize the adress locator
    fr_locator = BANFrance()
    
    #get the coordinates and region of the given adress
    adress = fr_locator.geocode(adress+' '+ville)
    region = adress.raw['properties']['context'].split(',')[-1].strip()
    adress_coordinates = adress.raw['geometry']['coordinates']
    
    # filter the dataframe to avoid processing unlikely candidates
    filtered_df = filter_by_region(df, region)
    
    #initilize the list of results
    list_of_museums = []
    
    #initial loop to fill the result list with random entries
    for id, row in filtered_df.iterrows():
        
        if len(list_of_museums) == num_museums:
            break
        
        try:
            
            #get the museum adress, the coordinates
            museum_id = row['ID MUSEE']
            museum_coordinates = coordinates_dict[museum_id]

            #calculate the distance to the given adress
            distance_to_adress = distance(adress_coordinates, museum_coordinates).kilometers
        
        except:
            continue
        
        #ignore the museum if it's too far away
        if distance_to_adress >= max_distance:
            continue
        
        #if all is well, append it to the list of results
        list_of_museums.append((row, distance_to_adress))

    #sort the list of results based on the distance to the adress
    list_of_museums.sort(key=lambda tup:tup[1])

    #if there is not enough data, the next part is unessary so we just return the initial list of results
    if len(list_of_museums) < num_museums:
        return enumerate(list_of_museums)

    #get the distance of the farthest museum
    museum_dist = list_of_museums[-1][1]

    for i, (id, row) in enumerate(filtered_df.iterrows()):
        
        #the first part of the list of results has already been dealt with
        if i <= num_museums:
            continue
        
        try:
            
            #get the museum adress, the coordinates
            museum_id = row['ID MUSEE']
            museum_coordinates = coordinates_dict[museum_id]
            
            #calculate the distance to the given adress
            distance_to_adress = distance(adress_coordinates, museum_coordinates).kilometers
        
        except:
            continue
        
        #ignore the museum if it's too far away
        if distance_to_adress > max(museum_dist, max_distance):
            continue
        
        #remove the unwanted museum
        list_of_museums.append((row, distance_to_adress))
        list_of_museums.sort(key=lambda tup:tup[1])
        list_of_museums.pop()

    return enumerate(list_of_museums)

def text_to_show_for_museum(museum, pos):
    
    #get the relevant data
    museum_name = str(museum[0]['NOM DU MUSEE']) if str(museum[0]['NOM DU MUSEE']) != 'nan' else 'information non disponible'
    museum_tel = str(int(museum[0]['TELEPHONE1'])) if str(museum[0]['TELEPHONE1']) != 'nan' else 'information non disponible'
    museum_ouverture = str(museum[0]['PERIODE OUVERTURE']) if str(museum[0]['PERIODE OUVERTURE']) != 'nan' else 'information non disponible'
    museum_siteweb = str(museum[0]['SITWEB']) if str(museum[0]['SITWEB']) != 'nan' else 'information non disponible'
    museum_adress = str(museum[0]['ADR']) if str(museum[0]['ADR']) != 'nan' else 'information non disponible'
    museum_ville = str(museum[0]['VILLE']) if str(museum[0]['VILLE']) != 'nan' else 'information non disponible'
    museum_distance = "{0:.2f}".format(museum[1])
    
    museum_adress = re.sub('\n', ' ', museum_adress)

    #make the output text for the museum
    text = "\n------------------------------------------------------------------------------------------------------ Musée numéro {} -------------------------------------------------------------------------------------------------------".format(pos+1)
    text = text + "\nNom du musée: "+museum_name
    text = text + "\nNuméro tel: "+museum_tel
    text = text + "\nSite web: "+museum_siteweb
    text = text + "\nAdresse: "+museum_adress+', '+museum_ville
    text = text + "\nDistance: "+museum_distance+' km'
    text = text + "\nHoraires d'ouverture: "+museum_ouverture

    return text

#precalculate the coordinates
def calculate_museum_coordinates(df):
    
    fr_locator = BANFrance()
    coordinate_dict = {}
    
    for id, row in df.iterrows():
        
        try:
            museum_adress = str(row['ADR']) + ' ' + str(row['VILLE'])
            museum_adress = fr_locator.geocode(museum_adress)
            museum_coordiantes = museum_adress.raw['geometry']['coordinates']
            museum_id = row['ID MUSEE']
            coordinate_dict[museum_id] = museum_coordiantes
        
        except:
            pass
    
    pickle_dir = os.path.join(scriptpath, r"geolocalisation", r"coordinate_dict.pkl")
    with open(pickle_dir, "wb") as coordinates_pickle:
        pickle.dump(coordinate_dict, coordinates_pickle)
    
    return coordinate_dict
