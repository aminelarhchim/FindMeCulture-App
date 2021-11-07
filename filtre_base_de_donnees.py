# Ce programme prend en entrée une base de données (dataframe python).
# Elle contient la liste de tous les musées de France avec leur localisation, et d'autres informations associées.
# Il prend également en entrée un nom de ville.
# Il renvoie en sortie une dataframe plus petite formée des lignes de tous les musées de cette ville.



#Il faut faire attention : les noms de région, de département, de ville notamment sont écrits tout en majuscules

# Modules à importer :
import pandas as pd
import copy
import numpy as np


def filtre_par_villes(base_de_donnees_France, nom_de_ville):
    nom_maj_ville=nom_de_ville.upper() #On convertit le nom de la ville en majuscules car ils sont en majuscules dans la base de données
    base_de_donnees_ville=base_de_donnees_France.loc[base_de_donnees_France["ville"] == nom_maj_ville] #avec loc on extrait toutes les lignes où la case dans la colonne ville correspond à la ville choisie
    return(base_de_donnees_ville) #On renvoie la base de données obtenue


#Même programme, mais où on effectue une sélection pour le département et non pour la ville :
def filtre_par_departements(base_de_donnees_France, nom_de_departement):
    nom_maj_departement=nom_de_departement.upper() #De même, il faut passer le nom du département en majuscules
    base_de_donnees_departement=base_de_donnees_France.loc[base_de_donnees_France["NOMDEP"] == nom_maj_departement] #On procède ensuite à une extraction des lignes associées à ce département
    return(base_de_donnees_departement)
 

#Enfin on peut faire la même chose pour la région et non le département ou la ville : 
def filtre_par_regions(base_de_donnees_France, nom_de_region):
    nom_maj_region=nom_de_region.upper() #De même il faut passer le nom de la région en majuscules et ensuite procéder à la sélection
    base_de_donnees_region=base_de_donnees_France.loc[base_de_donnees_France["NEW REGIONS"] == nom_maj_region]
    return(base_de_donnees_region)
