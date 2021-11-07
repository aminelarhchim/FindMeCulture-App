#Autre test pour le filtre des musées sur les départements, qui vérifie la correspondance de manière plus précise.

import sys
import os
from pathlib import Path

scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))
import pandas as pd
from data_extraction.filtre_base_de_donnees import filtre_par_departements
from pytest import *
from pandas import isnull

def test_filtre_par_departements():
    df = pd.read_excel(r"tests\tests.xlsx")
    assert df[df.NOMDEP=="CÔTE D’OR"].applymap(lambda x: {} if isnull(x) else x).eq(filtre_par_departements(df,"CÔTE D’OR").applymap(lambda x: {} if isnull(x) else x)).all().all()
    
test_filtre_par_departements()