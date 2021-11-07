import sys
import os
from pathlib import Path

scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))
import pandas as pd
import numpy as np
from pytest import *
from festivals.festivals_choix import filtre_festival

#Programmes qui testent le filtre général sur les festivals
#On crée une mini base de données pour faire les tests dessus 
data=[["FESTIVAL BOB'ARTS", "Centre-Val de Loire", "Musiques actuelles", "36", "Annuelle", "08 (août)", "DD026", "Le Blanc", np.nan, "6.0", "Indre"], ["Festival du livre de jeunesse de Rouen", "Normandie", "Livre et littérature", "Livre de jeunesse", "76", "Annuelle", "11 (novembre)", "IK011", "ROUEN", "36.0", "Seine-Maritime"], ["DIXIE FOLIES", "Nouvelle-Aquitaine", "Musiques actuelles", "Jazz, blues et musiques improvisées", "17", "Annuelle", "05 (mai)", "JD025", "LA ROCHELLE", np.nan, "Charente-Maritime"]]
base=pd.DataFrame(data, columns=["Nom de la manifestation", "Région", "Domaine", "Complément domaine", "Département", "Périodicité", "Mois habituel de début", "N° identification", "Commune principale", "num dep", "Nom département"])



def test_filtre_festival(): #On vérifie que le filtre marche bien pour un département
    base_c=filtre_festival(base,"Nom département", "Indre")
    liste_base_c=list(base_c.iloc[0])
    print(liste_base_c) #On convertit les lignes à comparer en listes et on les imprime pour vérifier le test
    liste_base_d=list(base.iloc[0]) 
    print(liste_base_d)
    assert liste_base_c==liste_base_d #On regarde si la ligne extraite et la ligne qui doit être extraite sont égales avec assert

