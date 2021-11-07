# Ce programme prend en entrée une base de données (dataframe python).
# Elle contient la liste de tous les musées de France avec leur localisation, et d'autres informations associées.
# Il prend également en entrée un nom de ville.
# Il renvoie en sortie une dataframe plus petite formée des lignes de tous les musées de cette ville.

# Forme générale de la base de données :
# numéro de ligne  #région  #département  #nom  #ref  #adresse  #cp  #ville  #informations pas utiles au filtre

#Il faut faire attention : les noms de région, de département, de ville notamment sont écrits tout en majuscules

# Modules à importer :
import pandas as pd
import copy
import numpy as np


def filtre_par_villes(base_de_donnees_France, nom_de_ville):
    nom_maj_ville=nom_de_ville.upper()
    base_de_donnees_ville=base_de_donnees_France.loc[base_de_donnees_France.VILLE == nom_maj_ville]
    return(base_de_donnees_ville)


#Même programme, mais où on effectue une sélection pour le département et non pour la ville :
def filtre_par_departements(base_de_donnees_France, nom_de_departement):
    nom_maj_departement=nom_de_departement.upper()
    base_de_donnees_departement=base_de_donnees_France.loc[base_de_donnees_France.NOMDEP == nom_maj_departement]
    return(base_de_donnees_departement)
 

#Enfin on peut faire la même chose pour la région et non le département ou la ville : 
def filtre_par_regions(base_de_donnees_France, nom_de_region):
    if nom_de_region.upper() in ['ÎLE-DE-FRANCE', 'HAUTS-DE-FRANCE']:
        mots = nom_de_region.split('-')
        nom_maj_region = mots[0].upper()+'-'+mots[1].upper()+'-France' 
    elif nom_de_region.upper() == 'la réunion'.upper():
        nom_maj_region = 'LA REUNION'
    else:
        nom_maj_region=nom_de_region.upper()
    base_de_donnees_region=base_de_donnees_France.loc[base_de_donnees_France["NEW REGIONS"] == nom_maj_region]
    return(base_de_donnees_region)


#Filtres pour les festivals



def conversion_code_dpt():
    DEPARTMENTS = {
    '01': 'Ain', 
    '02': 'Aisne', 
    '03': 'Allier', 
    '04': 'Alpes-de-Haute-Provence', 
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes', 
    '07': 'Ardèche', 
    '08': 'Ardennes', 
    '09': 'Ariège', 
    '10': 'Aube', 
    '11': 'Aude',
    '12': 'Aveyron', 
    '13': 'Bouches-du-Rhône', 
    '14': 'Calvados', 
    '15': 'Cantal', 
    '16': 'Charente',
    '17': 'Charente-Maritime', 
    '18': 'Cher', 
    '19': 'Corrèze', 
    '20': 'Corse', 
    '21': 'Côte-d\'Or', 
    '22': 'Côtes-d\'Armor', 
    '23': 'Creuse', 
    '24': 'Dordogne', 
    '25': 'Doubs', 
    '26': 'Drôme',
    '27': 'Eure', 
    '28': 'Eure-et-Loir', 
    '29': 'Finistère', 
    '30': 'Gard', 
    '31': 'Haute-Garonne', 
    '32': 'Gers',
    '33': 'Gironde', 
    '34': 'Hérault', 
    '35': 'Ille-et-Vilaine', 
    '36': 'Indre', 
    '37': 'Indre-et-Loire',
    '38': 'Isère', 
    '39': 'Jura', 
    '40': 'Landes', 
    '41': 'Loir-et-Cher', 
    '42': 'Loire', 
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique', 
    '45': 'Loiret', 
    '46': 'Lot', 
    '47': 'Lot-et-Garonne', 
    '48': 'Lozère',
    '49': 'Maine-et-Loire', 
    '50': 'Manche', 
    '51': 'Marne', 
    '52': 'Haute-Marne', 
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle', 
    '55': 'Meuse', 
    '56': 'Morbihan', 
    '57': 'Moselle', 
    '58': 'Nièvre', 
    '59': 'Nord',
    '60': 'Oise', 
    '61': 'Orne', 
    '62': 'Pas-de-Calais', 
    '63': 'Puy-de-Dôme', 
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées', 
    '66': 'Pyrénées-Orientales', 
    '67': 'Bas-Rhin', 
    '68': 'Haut-Rhin', 
    '69': 'Rhône',
    '70': 'Haute-Saône', 
    '71': 'Saône-et-Loire', 
    '72': 'Sarthe', 
    '73': 'Savoie', 
    '74': 'Haute-Savoie',
    '75': 'Paris', 
    '76': 'Seine-Maritime', 
    '77': 'Seine-et-Marne', 
    '78': 'Yvelines', 
    '79': 'Deux-Sèvres',
    '80': 'Somme', 
    '81': 'Tarn', 
    '82': 'Tarn-et-Garonne', 
    '83': 'Var', 
    '84': 'Vaucluse', 
    '85': 'Vendée',
    '86': 'Vienne', 
    '87': 'Haute-Vienne', 
    '88': 'Vosges', 
    '89': 'Yonne', 
    '90': 'Territoire de Belfort',
    '91': 'Essonne', 
    '92': 'Hauts-de-Seine', 
    '93': 'Seine-Saint-Denis', 
    '94': 'Val-de-Marne', 
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe', 
    '972': 'Martinique', 
    '973': 'Guyane', 
    '974': 'La Réunion', 
    '976': 'Mayotte',
    }
    dic_dpt={}
    for code in DEPARTMENTS:
        dic_dpt[DEPARTMENTS[code]]=code
    return dic_dpt  

def filtre_festival_dpt(df,departement):
    return df[df["Département"]==int(conversion_code_dpt()[departement])]

def filtre_festival(df,colonne,arg):
    return df[df[colonne]==arg]     


