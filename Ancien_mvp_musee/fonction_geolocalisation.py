from geopy.geocoders import Nominatim
import math

#Fonction qui utilise le module geopy pour passer d'une adresse à des coordonnées (latitude, longitude)
# NB : cette fonction n'est pas utilisée telle quelle dans le produit final

def geolocalisation(adresse):

    geolocator = Nominatim(user_agent="specify_your_app_name_here") #On fait appel à la fonction Nominatim
    location = geolocator.geocode(adresse) #On répupère l'adresse de l'utilisateur
    return(location.latitude, location.longitude) #Le module la convertit en coordonnées géographiques