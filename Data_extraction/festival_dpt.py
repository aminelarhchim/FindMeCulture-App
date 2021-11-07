import sys
import os
from pathlib import Path

scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))

from data_extraction.filtre_base_de_donnees import filtre_festival, conversion_code_dpt, filtre_festival_dpt
import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

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

class festival:
    
    #initialize the class object
    
    
    def __init__(self,nom,date,site_web,domaine):
        self.nom = nom
        self.date=date
        self.web=site_web
        self.domaine=domaine

        
def liste_festival_dpt():
    df_festival = pd.read_excel(os.path.join(str(scriptpath), r"data", r"festivals.xlsx"))
    dict_festival_dpt={}
    for departement in conversion_code_dpt():
        dict_festival_dpt[departement]=[]
        festivals_dpt=filtre_festival(df_festival,'Nom Département',departement)
        for index,fest in festivals_dpt.iterrows():
            
            dict_festival_dpt[departement]+=[festival(fest['Nom'],fest['Mois habituel de début'],fest['Site web'],fest['Domaine'])]

    return dict_festival_dpt


# Liste des thèmes des festivaux dans le département en entrée, avec possibilité de trier par domaine

def liste_domaine_festival_departement(departement, domaine=None):
    
    liste_domaine_dpt=[]
    liste_festival_domaine=[]
    for fest in liste_festival_dpt()[departement]:
        if fest.domaine not in liste_domaine_dpt:
            liste_domaine_dpt.append(fest.domaine)

    if domaine!=None:
        for fest in liste_festival_dpt()[departement]:
            if fest.domaine==domaine:
                liste_festival_domaine.append(fest)
        return liste_festival_domaine                    
    return liste_domaine_dpt

def get_festivals_for_departement(departement):
    
    df_festival = pd.read_excel(os.path.join(str(scriptpath), r"data", r"festivals.xlsx"))

    filtered_df = filtre_festival_dpt(df_festival, departement)
    festival_list = []
    
    for id, fest in filtered_df.iterrows():
        festival_list.append(festival(fest['Nom'],fest['Mois habituel de début'],fest['Site web'],fest['Domaine']))
    
    return festival_list


def make_festival_text(festival, pos):

    festival_name = festival.nom if str(festival.nom) != 'nan' else 'information indisponible'
    festival_date = festival.date if str(festival.date) != 'nan' else 'information indisponible'   
    festival_siteweb = festival.web if str(festival.web) != 'nan' else 'information indisponible'
    festival_domain = festival.domaine if str(festival.domaine) != 'nan' else 'information indisponible'

    #correct festival date format
    festival_date = re.sub('[(]', ' ', festival_date)
    festival_date = re.sub('[])]', '', festival_date)
    
    text = "\n------------------------------------------------------------------------------------------------------ Festival numéro {} ------------------------------------------------------------------------------------------------------".format(pos+1)
    text = text + "\nNom du festival: " + festival_name
    text = text + "\nDate: " + festival_date
    text = text + "\nSite web: " + festival_siteweb
    text = text + "\nDomaine: " + festival_domain

    return text

if __name__ == '__main__':
    text = '06(juin)'
    text = re.sub('[(]|[)]', '', text)
    print(text) 


