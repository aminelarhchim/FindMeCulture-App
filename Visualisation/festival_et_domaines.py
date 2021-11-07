#Ce module permet de sélectionner les données de la data frame nous intéressant puis affiche des histogrammes analysant ces données

##Ce premier paragraphe permet de faciliter l'import de module provenant d'autres dossiers
import sys
import os
from pathlib import Path

scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import data_extraction.extract_data

from festivals.comptage_festivals_domaines import compte_domaine_principal

objet_festival_db= data_extraction.extract_data.load_data(filename='festivals',init=True)
df_festival = objet_festival_db.data

##Modifications du rendu visuel du graphique 
##La fonction suivante permet d'avoir un gradient de couleur sur les histogrammes, elle prend en argument
## les barres de l'histogramme, le dictionnaire contenant les "hauteurs" des barres en valeurs ainsi qu'un ordre de grandeur 'odg' des hauteurs des barres, pour les comparer au maximum
def gradientbars(bars,dico,odg):
      
      ax = bars[0].axes
      lim = ax.get_xlim()+ax.get_ylim()
      for bar in bars:

          bar.set_zorder(1)
          bar.set_facecolor("none")
          x,y = bar.get_xy()
          w, h = bar.get_width(), bar.get_height()
          grad = np.atleast_2d(np.linspace(0,odg*w/max([x for x in dico.values()]),256))
          ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0, norm=matplotlib.colors.NoNorm(vmin=0,vmax=1),cmap=plt.get_cmap('autumn'))
      ax.axis(lim)

#Dictonnaire de format de textes
font = {'family': 'fantasy',
        'color':  'darkred',
        'weight': 'heavy',
        'size': 10,
        }
##

dico_domaine_effectif=compte_domaine_principal(df_festival)
plt.figure(figsize=(12, 6))

#Tracé de l'histogramme avec matplotlib.pyplot :
gradientbars(plt.barh([x for x in dico_domaine_effectif],dico_domaine_effectif.values()),dico_domaine_effectif,10)
plt.subplots_adjust(left=0.3)
plt.yticks(range(len(dico_domaine_effectif)),[x for x in dico_domaine_effectif],color='red',fontfamily='fantasy')
plt.title("Nombre de festivals par domaine",font)
plt.show()

