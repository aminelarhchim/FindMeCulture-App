#L'objectif des fonctions suivantes est de compter les festivals qui ont certaines caractéristiques afin d'effectuer des statistiques.
#Plus précisément ici on s'intéresse aux festivals qui font partie de certains domaines.

import pandas as pd 
import numpy as np 
import copy

#Les fonctions suivantes permettent de créer des dictionnaires avec comme clés le nom de chaque domaine et comme valeurs le nombre de festivals avec ce domaine.
#Le principe est le même pour le domaine principal et les autres domaines :
#On crée un dictionnaire vide, et on parcourt la base de données, plus précisément la colonne domaine ou autre domaine.
#Si le domaine est déjà dans le dictionnaire, on ajoute un à la valeur associée à cette clé.
#Sinon on le rajoute au dictionnaire avec une valeur initiale de 1

#On fait ça d'une part pour la colonne domaine et d'autre part pour la colonne autre domaine.
#On effectue ensuite une fusion des deux dictionnaires, pour considérer les eux colonnes de la DataFrame.

def compte_domaine_principal(base):
    dic={}
    for i in range(len(base)):
        row=base.loc[i]
        domaine=row["Domaine"]
        if domaine in dic.keys() and domaine!=np.nan:
            dic[domaine]+=1
        elif domaine not in dic.keys() and domaine!=np.nan:
            dic[domaine]=1
    return(dic)

def compte_domaine_complement(base):
    dic={}
    for i in range(len(base)):
        row=base.loc[i]
        domaine=row["Complément domaine"]
        if domaine in dic.keys() and domaine!=np.nan:
            dic[domaine]+=1
        elif domaine not in dic.keys() and domaine!=np.nan:
            dic[domaine]=1
    return(dic)

def compte_tous_domaines(base):
    dic_pr=compte_domaine_principal(base)
    dic_co=compte_domaine_complement(base)
    dic=dic_pr.copy()
    for domaine in dic_co.keys():
        if domaine in dic.keys():
            dic[domaine]+=dic_co[domaine]
        elif domaine not in dic.keys():
            dic[domaine]=dic_co[domaine]
    return(dic)


