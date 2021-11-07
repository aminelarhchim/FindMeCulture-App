#Programme qui demande à l'utilisateur où et quand il veut aller à un festival, et quel thème il préfère
#Et qui renvoie en sortie une liste de festivals correspondant à ces souhaits

#liste des colonnes de la dataframe utilisée : 
#Nom de la manifestation	Région	  Domaine	Complément domaine 	Département	 Périodicité	Mois habituel de début	 Site web	N° Identification	Commune principale	Autres communes	N° de l'édition 2018	Date de début	Date de fin	Date de création	Points saillants / Têtes d'affiche de l'édition 2018	Points saillants / Têtes d'affiche de l'édition 2019	Soutenu en 2017 par le ministère de la culture 	Soutenu en 2017 par le Centre national du cinéma 	Soutenu en 2017 par le Centre national du livre 	Soutenu en 2017 par le Centre national des variétés 	Soutenu en 2018 par le ministère de la culture 	Soutenu en 2018 par le Centre national du cinéma 	Soutenu en 2018 par le Centre national du livre 	Soutenu en 2018 par le Centre national des variétés 	Code postal	Code INSEE	coordonnees_insee	Libellé commune pour calcul CP, INSEE	Dépt SK	Nom Département	Commentaires	N° de l'Ã©dition 2019	Check édition	Mois indicatif en chiffre, y compris double mois	Mois indicatif	Date début ancien	Date de fin ancien	Soutien 2017 MCC Ã  la structure	Part festival sur soutien Ã  la structure	Enquête DRAC 2017

import pandas as pd
import numpy as np


#Filtre général : non pas sur un département/ domaine/ mois... mais général
#Il prend en entrée la base de données, l'argument à chercher mais aussi la colonne dans lequel il est : région/ domaine...
#Ainsi on peut l'utiliser pour différents algorithmes
def filtre_festival(db,colonne,arg):
    return db[db[colonne]==arg]
#On a ensuite des filtres plus spécifiques qui prennent en compte les problèmes de majuscules ainsi que la présence possible de deux communes associées à un seul festival.
def filtre_commune(base, commune):
    commune_maj=commune.upper()
    if commune in base["Commune principale"]:
        base_commune=base.loc[base["Commune principale"]==commune]
    elif commune_maj in base["Commune principale"]:
        base_commune=base.loc[base["Commune principale"]==commune_maj]
    elif commune in base["Autres communes"]:
        base_commune=base.loc[base["Autres communes"]==commune]
    elif commune_maj in base["Autres communes"]:
        base_commune=base.loc[base["Autres communes"]==commune_maj]
    return(base_commune)

def filtre_reg(base, region):
    if region in base["Région"]:
        base_reg=base.loc[base["Région"]==region]
    return(base_reg)

def filtre_dep(base, dep):
    if dep in base["Nom Département"]:
        base_dep=base.loc[base["Nom Département"]==dep]
    return(base_dep)


def filtre_mois(base, mois):
    dic_num_mois={"janvier":"01", "février":"02", "mars":"03", "avril":"04", "mai":"05", "juin":"06", "juillet":"07", "août":"08", "septembre":"09", "octobre":"10", "novembre":"11", "décembre":"12"}
    info_mois=dic_num_mois[mois]+"("+mois+")"
    base_mois=base.loc[base["Mois habituel de début"]==info_mois]
    return base_mois

def filtre_sujet(base, sujet):
    if sujet in base["Domaine"]:
        base_sujet=base.loc[base["Domaine"]==sujet]
    elif sujet in base["Complément domaine"]:
        base_sujet=base.loc[base["Complément domaine"]==sujet]
    return(base_sujet)

#Algorithme de choix de festival qui sélectionne des colonnes avec les filtres précédents et n'affiche que les premiers résultats.
def choix_festival(base, endroit, mois, sujet, nombre):
    base_mois=filtre_mois(base, mois)
    base_mois_sujet=filtre_sujet(base_mois, sujet)
    if endroit in base_mois_sujet["Nom Département"]:
        base_bien=filtre_dep(base_mois_sujet, endroit)
    elif endroit in base_mois_sujet["Région"]:
        base_bien=filtre_reg(base_mois_sujet, endroit)
    elif endroit in base_mois_sujet["Commune principale"] or endroit in base_mois_sujet["Autres communes"] or endroit.upper() in base_mois_sujet["Commune principale"] or endroit.upper() in base_mois_sujet["Autres communes"]:
        base_bien=filtre_commune(base_mois_sujet, endroit)
    print("Les festivals correspondant à votre demande sont:")
    base_fini=base_bien.head(nombre)
    return(base_fini)