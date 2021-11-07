#Ensemble de programmes qui teste sur une petite base de données (lignes recopiées de la base de données des musées de France), que les programmes de filtres géographiques fonctionnent correctement.
import sys
import os
from pathlib import Path

scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))

import numpy as np
import pandas as pd 
import copy
from pytest import *
from data_extraction.filtre_base_de_donnees import filtre_par_villes, filtre_par_departements, filtre_par_regions

def test_filtre():
    données_exemple = [["ÎLE-DE-FRANCE", "VAL D'OISE", "Musée de la Renaissance - Château d'Ecouen", "9520501",	"Château", "95440", "ECOUEN", "0134383850", "134383878", "www.musee-renaissance.fr ou www.musee-château-ecouen.fr"], ["ÎLE-DE-FRANCE", "PARIS", "Petit Palais, Musée des Beaux-Arts de la ville de Paris",	"7510808",	"Avenue Winston-Churchill", "75008", "PARIS", "0142651273", "142652460", "www.petitpalais.paris.fr"], ["ÎLE-DE-FRANCE", "VAL D'OISE", "Musée Camille Pissarro", "9550002", "17, Rue du Château", "95300", "PONTOISE", "0130380240", "130305056", "www.ville-pontoise.fr"], ["ALSACE", "BAS-RHIN", "Musée alsacien", "1234567", "1, place Joseph Thierry", "67500", "HAGUENAU", "0101010101", "010101215", "www.ville-haguenau.fr/pages/culture/musee.htm"]]
    base_de_données=pd.DataFrame(données_exemple, columns=["NEW REGIONS", "NOMDEP", "nom", "code1", "adresse", "code postal", "VILLE", "code2", "code3", "site internet"])
#La base de données ci-dessus sert pour le test, des données y ont été modifiées
    base_Ecouen=filtre_par_villes(base_de_données, "Ecouen")
    nom_Ecouen=base_Ecouen.iloc[0, 2]
    assert nom_Ecouen=="Musée de la Renaissance - Château d'Ecouen" #On vérifie qu'il y a correspondance entre une des cases extraites et la case censée être obtenue.

    base_val_d_oise=filtre_par_departements(base_de_données, "Val d'Oise")
    print(base_val_d_oise)
    nom_musee=base_val_d_oise.iloc[1, 2]
    assert nom_musee=="Musée Camille Pissarro" #De même on vérifie qu'on récupère le bon musée

    base_alsace=filtre_par_regions(base_de_données, "alsace")
    print(base_alsace)
    nom_musee2=base_alsace.iloc[0,2]
    assert nom_musee2=="Musée alsacien" #idem

