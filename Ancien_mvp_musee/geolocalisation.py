from geopy.geocoders import Nominatim
import math

#Ce fichier contient différentes fonctions relatives à la géolocalisation de l'utilisateur qui n'ont finalement pas été utilisées telles quelles dans le mvp final.
#Les nouvelles fonctions sur la géolocalisation sont dans le dossier geolocalisation dans projet-coding-weeks.


#Fonction qui convertit une adresse en coordonnées géographiques (latitude, longitude)
def geolocalisation(adresse):

    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(adresse)
    lat=location.latitude
    lon=location.longitude
    return(lat, lon)


#Fonction qui prend en entrée une base de données avec une colonne adresses et retourne en sortie la même base de données avec en plus une colonnes coordonnées géographiques associées à l'adresse.

def base_musees_geolocalisation(base):
#Pour chaque musée, on cherche à obtenir sa géolocalisation à partir de son adresse : on ajoute une colonne coordonnées à la base de données des musées
#adresse : en 6ème position, #ville : en 8ème position
    coordonnees=[]
    for i in range(len(base)): #On parcourt la base de données
        adr=str(base.iloc[i, 6]) #On extrait l'adresse et le nom de la ville sous forme de chaine de caractères"
        ville=str(base.iloc[i, 8])
        adresse=adr+" "+ville
        #print(adresse) ligne ajoutée pour vérifier que tout va bien
        coordonnees.append(geolocalisation(adresse)) #On utilise la fonction geolocalisation et on crée une liste des coordonnées de toutes les adresses
    base.insert(len(base), "coordonnées", coordonnees, True) #on insère cette liste sous forme d'une nouvelle colonne
    return(base)
    
#Fonction qui à partir des coordonnées latitude, longitude de deux points, en déduit la distance entre les deux en km.

def distance(lat1, long1, lat2, long2):
    dlat=(lat2-lat1)*math.pi/180
    dlon=(long2-long1)*math.pi/180
    lat1=lat1*math.pi/180
    lat2=lat2*math.pi/180
    a = (math.sin(dlat / 2)**2) + ((math.sin(dlon / 2)**2)*math.cos(lat1)*math.cos(lat2))
    rayon_terre=6371
    c =2*math.asin(math.sqrt(a)) 
    return rayon_terre*c 
 
def distance_aux_musees(base_France, adresse):
    coordonnees_utilisateur=geolocalisation(adresse)
    dis=[] #On crée une liste qui va contenir la distance entre l'utilisateur et chaque musée de la base de données
    lat1=coordonnees_utilisateur[0]
    lon1=coordonnees_utilisateur[1]
    base_geoloc=base_musees_geolocalisation(base_France)
    for i in range(len(base_geoloc)):
        coor2=base_geoloc.iloc[i,16]
        lat2=coor2[0]
        long2=coor2[1]
        dis.append(distance(lat1,long1,lat2,long2))
    base_geoloc["distance_au_musee"]=dis
    return(base_geoloc)

def musees_les_plus_pres(base_France, adresse, nombre):
    base=distance_aux_musees(base_France, adresse)
#On crée une dataframe avec le nombre de musées voulus et on prend les premiers.
    les_plus_pres=base.head(nombre)
#On parcourt ensuite la dataframe de tous les musées et on compare les distances avec la plus grande de la dataframe à renvoyer.
    for j in range(nombre, len(base)):
#On regarde quel musée a la plus grande distance dans la dataframe à renvoyer et on compare avec la grande dataframe; on remplace éventuellement.        
        liste_dist=list(les_plus_pres["distance_au_musee"])
        grande_dist=max(liste)
        indice=liste.index(grande_dist)
        if base[j,17]<grande_dist:
            les_plus_pres[indice]=base[j]
    return(les_plus_pres)




