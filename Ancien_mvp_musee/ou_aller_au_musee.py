#Programme du MVP1, avant l'ajout de l'interface graphique et de la géolocalisation

#Ce programme part des fonctions de filtre et propose à l'utilisateur de choisir un lieu, il renvoie ensuite les musées à proximité avec les horaires et périodes d'ouverture, ainsi que le site internet...
import numpy as np 
import pandas as pd 
from filtre_base_de_donnees import filtre_par_villes, filtre_par_departements, filtre_par_regions



def choix_musee(base_de_donnees_France, endroit, nombre_affiches):

#On demande à l'utilisateur l'endroit de son choix, il faut que le programme trouve le type : ville/ région/ département :
#On fait ensuite une distinction selon le type, en utilisant un filtre adapté.
#Une fois la base de données associée obtenue on la trie pour ne pas afficher trop d'éléments inutiles sur les lignes ou les colonnes.
    nom=str(endroit)
    nom_maj=nom.upper() #il faut toujours convertir le nom de l'endroit en majuscules
   
    if nom in base_de_donnees_France[["VILLE"]]:
        base_de_donnees_ville=filtre_par_villes(base_de_donnees_France, endroit)
        nombre=max(nombre_affiches, len(base_de_donnees_ville)) 
        base_de_donnees_ville_reduite=base_de_donnees_ville.head(nombre)
        base_de_donnees_ville_infos=base_de_donnees_ville_reduite[["NOM DU MUSEE", "ADR", "TELEPHONE1", "SITWEB", "FERMETURE ANNUELLE", "PERIODE OUVERTURE", "JOURS NOCTURNES"]]
        print("Les musées que vous pouvez visiter dans cette ville sont les suivants :")
        return(base_de_donnees_ville_infos)

    elif nom in base_de_donnees_France[["NOMDEP"]]:
        base_de_donnees_departement=filtre_par_departements(base_de_donnees_France, endroit)
        nombre=max(nombre_affiches, len(base_de_donnees_departement))
        base_de_donnees_departement_reduite=base_de_donnees_departement.head(nombre)
        base_de_donnees_departement_infos=base_de_donnees_departement_reduite[["NOM DU MUSEE", "ADR", "VILLE", "TELEPHONE1", "SITWEB", "FERMETURE ANNUELLE", "PERIODE OUVERTURE", "JOURS NOCTURNES"]]   
        print("Les musées que vous pouvez visiter dans ce département sont les suivants :")
        return(base_de_donnees_departement_infos)

    elif nom in base_de_donnees_France[["NEW REGIONS"]]:
        base_de_donnees_region=filtre_par_regions(base_de_donnees_France, endroit)
        nombre=max(nombre_affiches, len(base_de_donnees_région))
        base_de_donnees_region_reduite=base_de_donnees_region.head(nombre)
        base_de_donnees_region_infos=base_de_donnees_region_reduite[["NOM DU MUSEE", "ADR", "VILLE", "NOMDEP", "TELEPHONE1", "SITWEB", "FERMETURE ANNUELLE", "PERIODE OUVERTURE", "JOURS NOCTURNES"]]
        print("Les musées que vous pouvez visiter dans cette région sont les suivants :")
        return(base_de_donnees_region_infos)

    elif nom not in base_de_donnees_France:
        return("Nous sommes désolés de vous annoncer que nous ne disposons pas d'informations sur les musées de cet endroit.")



