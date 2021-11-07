#Ce module a pour but d'afficher un graphique représentant le ratio du nombre de musées par millier d'habitants, pour comparer plus pertinement 
#nos données, il prend en entrée deux dataframes : l'un liste les musées de france et l'autre les populations dans les régions françaises
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

#On commence par charger les données sous forme de dataframe
objet_musee= data_extraction.extract_data.load_data(filename='museums')
df_musee = objet_musee.data
objet_pop=data_extraction.extract_data.load_data(filename='population')
df_pop=objet_pop.data


#On créé un dictionnaire qui vont contenir le nombre de musées pour chaque région
dico_region_nbmus={}
dico_region_pop={}


for ligne in df_pop["Nom de la région"].to_numpy():
    
    if ligne == "ÎLE-DE-France":
        nombre_de_musee_de_la_region=len(df_musee[df_musee['NEW REGIONS']==ligne])
        dico_region_nbmus[ligne]=nombre_de_musee_de_la_region 
        
    elif ligne == "HAUTS-DE-France":
        nombre_de_musee_de_la_region=len(df_musee[df_musee['NEW REGIONS']==ligne])
        dico_region_nbmus[ligne]=nombre_de_musee_de_la_region    
        
    else:    
        nombre_de_musee_de_la_region=len(df_musee[df_musee['NEW REGIONS']==ligne.upper()])

        dico_region_nbmus[ligne]=nombre_de_musee_de_la_region

#On va plot le nombre de musées par région
#La fonction qui suit permet d'obtenir un gradient de couleur sur les barres du plot 

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


#On va maintenant plot le nombre de musée par région, en triant les barres par hauteur croissante
 
dico_trie_nbmus={}

for cle,valeur in sorted(dico_region_nbmus.items(),key=lambda x:x[1]):
    dico_trie_nbmus[cle]=valeur     
plt.figure(figsize=(12,5))
gradientbars(plt.barh(range(len(dico_trie_nbmus)),dico_trie_nbmus.values()),dico_trie_nbmus,1)
plt.yticks(range(len(dico_trie_nbmus)),[x for x in dico_trie_nbmus],color='darkred',fontfamily='fantasy')
plt.title("Nombre de musée dans chaque région",fontdict=font)
plt.subplots_adjust(left=0.3)


#On va remplacer la valeur 'nombre de musée pour la région X' par ' nombre de musées par million d'habitants' dans le dictionaire

for region in dico_region_nbmus:
    pop_region=df_pop[df_pop["Nom de la région"]==region]["Population totale"].to_numpy()
    dico_region_nbmus[region]=dico_region_nbmus[region]/pop_region[0]*1000000
    dico_region_pop[region]=pop_region[0]



#on va trier les valeurs par ordre croissant pour obtenir un plus joli plot
dico_trie_ratio={}

for cle,valeur in sorted(dico_region_nbmus.items(),key=lambda x:x[1]):
    dico_trie_ratio[cle]=valeur


#On plot simplement les graphes avec les barres
plt.figure(figsize=(12,6))
#Plot 1 avec le ratio nb musee/million d'habitants
plt.subplot(121)

##Couleur des barres avec gradient
gradientbars(plt.barh(y=[i for i in range(len(dico_region_nbmus))],width=[-x for x in dico_trie_ratio.values()],height=0.8,align='edge'),dico_trie_ratio,-1) 
## On inverse l'axe des abscisse
abscisse=plt.xticks()[0]
plt.xticks(ticks=abscisse[1:],labels=[str(int(abs(x))) for x in abscisse[1:]])

##On ajuste la taille du graphe pour pouvoir lire les noms de régions correctement
plt.subplots_adjust(left=0.3,wspace=0)

#Titre du graphe et format du texte



plt.yticks(range(len(dico_region_nbmus)),[x for x in dico_trie_ratio],color='red',fontfamily='fantasy')
plt.title("Nombre de musées par million d'habitants",font) 


plt.subplot(122)
##On affiche la population en millions d'habitants pour chaque région

plt.subplot(122).set_title("Population (en millions d'habitants)",font)      


gradientbars(plt.barh([i for i in range(len(dico_region_nbmus))],[x/1000000 for x in (dico_region_pop[region] for region in dico_trie_ratio.keys())]),dico_region_pop,1000000)
plt.yticks([])
plt.xticks(np.linspace(0,12,7))
plt.show()















##Ce qui suit est la partie du code ayant pour objectif d'afficher la quantité d'étudiants inscrits dans l'enseignement supérieur
## mais celle-ci a été abandonnée car elle n'était pas très pertinente

     
        
# # df_niv_etudes= pd.read_excel(os.path.join(str(scriptpath),r"data\niv_etudes.xlsx"))
# # #(dico_region_nbmus)
# # dico_effectif_sup={} 
# # for index,ligne in df_niv_etudes.iterrows():
    
# #     for region in dico_region_nbmus.keys():
# #         if ligne["Unité géographique"]==region:
# #             if region in dico_effectif_sup:
# #                 dico_effectif_sup[region]+=ligne["Nombre total d’étudiants inscrits"]
# #             else:
# #                 dico_effectif_sup[region]=ligne["Nombre total d’étudiants inscrits"]   
            

# # dico_effectif_sup_ramene_pop={}
# # for region in dico_effectif_sup:
# #     dico_effectif_sup_ramene_pop[region]=dico_effectif_sup[region]/dico_region_pop[region]
# # print(dico_effectif_sup_ramene_pop,"Pourcentage de la population inscrit dans l'enseignement supérieur")    

  

 
    

