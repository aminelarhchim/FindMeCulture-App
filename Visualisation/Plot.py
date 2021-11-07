#On plotte les graphes
#PieChart représentant la distribution des musées selon les villes, les départements et les régions
#Un histogramme qui représente la distribution des musées par tranches selon les villes

import sys
import os
from pathlib import Path
scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))
import data_extraction.extract_data
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import data_extraction.filtre_base_de_donnees as filtre

#On charge la base de données sous forme de Dataframe

museums=data_extraction.extract_data.load_data(filename='museums',test=True)
df=museums.data
test_df=museums.test_data
base_de_donnees_musee=df.to_numpy()




def list_of_cities_seuil(base_de_donnees,seuil):    #On retourne la liste des villes qui ont un nombre de musée supérieur à un seuil
    list_of_cities=[]
    donnees=base_de_donnees.to_numpy()   #Transforme le dataframe en numpy 
    for i in range(0,len(donnees)):      #Parcours le tableau
        city=donnees[i,8]                #La colonne 8 contient l'information ville
        if type(city)== str:             #Pour éviter les bugs si certaines colonnes sont vides ou mal renseignées.
                nombre_de_musee=len(filtre.filtre_par_villes(base_de_donnees,city).to_numpy())     #Compte le nombre de musée dans la ville
                if city not in list_of_cities and nombre_de_musee>seuil :                   #On garde les villes qui ont plus d'un certain nombre de musée
                    list_of_cities.append(city)
    return list_of_cities

def list_of_departement_seuil(base_de_donnees,seuil):   #On retourne la liste des départements qui ont un nombre de musée supérieur à un seuil
    list_of_departement=[]
    donnees=base_de_donnees.to_numpy()
    for i in range(0,len(donnees)):
        departement=donnees[i,1]
        if type(departement)==str:
            nombre_de_musee=len(filtre.filtre_par_departements(base_de_donnees,departement).to_numpy())
            if departement not in list_of_departement and nombre_de_musee>seuil:
                list_of_departement.append(departement)
    return list_of_departement

def list_of_region_seuil(base_de_donnees,seuil):#On retourne la liste des régionsqui ont un nombre de musée supérieur à un seuil
    list_of_region=[]
    donnees=base_de_donnees.to_numpy()
    for i in range(0,len(donnees)):
        region=donnees[i,0]
        if type(region)==str:
                nombre_de_musee=len(filtre.filtre_par_regions(base_de_donnees,region).to_numpy())
                if region not in list_of_region and nombre_de_musee>seuil:
                    list_of_region.append(region)
    return list_of_region





def camembert_villes(base_de_donnees,seuil): 
    plt.figure(figsize=(12, 6)) #Taille de la figure
    list_of_cities=list_of_cities_seuil(base_de_donnees,seuil)    
    taille=[]   #Va contenir le nombre de musee de chaque ville dans list_of_cities
    i=0
    for city in list_of_cities:
        nombre_de_musee=len(filtre.filtre_par_villes(base_de_donnees,city).to_numpy()) #On compte le nombre de musée dans la ville
        taille.append(nombre_de_musee)  
        list_of_cities[i]= city + '(' + str(nombre_de_musee) + ')'  #On écrit le nombre de musee à cote de la ville pour la lisibilité
        i+=1
    list_of_cities.append('moins de '+str(seuil)+' musee')  #On rajoute les musées 'autres' qui sont en dessous du seuil
    musee_autre=0   #Va compter le nombre de musée autres
    for city in list_of_cities_seuil(base_de_donnees,0):
        if city not in list_of_cities:
            musee_autre+=len(filtre.filtre_par_villes(base_de_donnees,city).to_numpy())# On somme les musées qui sont dans les villes autres
    taille.append(musee_autre)
    list_of_cities[-1]=list_of_cities[-1]+ '('+ str(musee_autre)+')'
    plt.pie(taille,labels=list_of_cities,textprops={'fontsize': 5})
    plt.title('Répartition des musées selon les villes',fontsize=20,y=0.4)
    plt.show()



def histogramme_villes_tranches(base_de_donnees): #Histogramme du nombre de villes qui contiennent un certain nombre de musée.
    plt.figure(figsize=(12,6)) # taille de la figure
    list_of_cities=list_of_cities_seuil(base_de_donnees,0) # liste des villes
    taille=[] # va contenir le nombre de villes correspondant à une catégorie
    nombre_de_musee=[] # va contenir le nombre de musée d'une ville 
    for city in list_of_cities: 
        nombre_de_musee.append(len(filtre.filtre_par_villes(base_de_donnees,city).to_numpy())) # On compte le nombre de musée dans la ville
        taille.append(nombre_de_musee)
    categorie_villes=['plus de 10','entre 8 et 10','entre 5 et 8','entre 2 et 5','entre 0 et 2'] # les catégories de villes
    a,b,c,d,e=0,0,0,0,0 # compteur pour les catégories
    for i in range (0,len(list_of_cities)):
        if nombre_de_musee[i]>10:
            a+=1
        elif nombre_de_musee[i]<=10 and nombre_de_musee[i]>8:
            b+=1
        elif nombre_de_musee[i]<=8 and nombre_de_musee[i]>5:
            c+=1
        elif nombre_de_musee[i]<=5 and nombre_de_musee[i]>2:
            d+=1
        elif nombre_de_musee[i]<=2 and nombre_de_musee[i]>0:
            e+=1
    plt.xlabel('Nombre de musée',fontsize=15)
    plt.ylabel('Nombre de Ville',fontsize=15)
    plt.bar(categorie_villes,[a,b,c,d,e])
    plt.show()


     
        





def camembert_departement(base_de_donnees,seuil):
    plt.figure(figsize=(12,6))
    list_of_departement=list_of_departement_seuil(base_de_donnees,seuil)
    taille=[]
    i=0
    for departement in list_of_departement:
        nombre_de_musee=len((filtre.filtre_par_departements(base_de_donnees,departement)))
        taille.append(nombre_de_musee)
        list_of_departement[i]= departement + '(' + str(nombre_de_musee) + ')'
        i+=1
    list_of_departement.append('Autre (moins de '+str(seuil)+' musee) ')
    musee_autre=0
    for departement in list_of_departement_seuil(base_de_donnees,0):
        if departement not in list_of_departement:
            musee_autre+=len(filtre.filtre_par_departements(base_de_donnees,departement).to_numpy())
    taille.append(musee_autre)
    list_of_departement[-1]=list_of_departement[-1]+ '('+ str(musee_autre)+')'
    plt.pie(taille,labels=list_of_departement,textprops={'fontsize': 8})
    plt.title('Répartition des musées selon les départements',fontsize=20)
    plt.show()

    

def camembert_region(base_de_donnees):
    plt.figure(figsize=(12,6))
    list_of_region=list_of_region_seuil(base_de_donnees,0)
    taille=[]
    i=0
    for region in list_of_region:
        nombre_de_musee=len((filtre.filtre_par_regions(base_de_donnees,region)))
        taille.append(nombre_de_musee)
        if nombre_de_musee > 10 or nombre_de_musee == 7:
            list_of_region[i]= region + '(' + str(nombre_de_musee) + ')'
        else:
            list_of_region[i]=''
        i+=1
    plt.pie(taille,labels=list_of_region)
    plt.title('Répartition des musées selon les régions',fontsize=20)
    plt.pie(taille,labels=list_of_region)
    plt.show()

if __name__ == '__main__':
    camembert_villes(df, 8)