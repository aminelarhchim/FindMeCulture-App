#Ce programme trace un histogramme de la répartition des festivals par mois, de janvier à décembre.

import sys
import os
from pathlib import Path
scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))
import data_extraction.extract_data
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
# from data_extraction.filtre_base_de_donnees import *

festivals=data_extraction.extract_data.load_data(filename='festivals',test=True)
df=festivals.data


def hist_date_festival(donnees):
    plt.figure(figsize=(12, 6)) 
    mois=['01 (janvier)','02 (février)','03 (mars)','04 (avril)','05 (mai)','06 (juin)','07 (juillet)','08 (août)','09 (septembre)','10 (octobre)','11 (novembre)','12 (décembre)']
    effectif=[]
    for m in mois:
        effectif.append(len(donnees[donnees['Mois habituel de début']==m].to_numpy()))
    plt.barh(mois,effectif)
    plt.xlabel('Mois', fontsize=10)
    plt.ylabel('Nombre de festivals',fontsize=10)
    plt.show()