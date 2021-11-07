#L'objectif de ces fonctions est de compter les festivals ayant lieu dans chaque région pour savoir où il y a le plus de festivals.

import pandas as pd 
import numpy as np 

#On parcourt la base de données pour récupérer le nombre de festivals ayant lieu dans chaque région.
#On crée un dictionnaire qui aura pour clés les noms des régions et pour valeurs associées le nombre de festivals dans la région.
#Si on trouve une nouvelle région, on l'ajoute aux clés du dictionnaire.
#Si elle y est déjà, on ajoute 1 à la valeur associée.

def compte_reg(base):
    dic={}
    for i in range(len(base)):
        row=base.loc[i]
        case=row["Région"]
        if case not in dic.keys():
            dic[case]=1
        elif case in dic.keys():
            dic[case]+=1
    return dic

