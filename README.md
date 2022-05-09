<div align="center">
  <img src="https://image.freepik.com/vecteurs-libre/hommes-femmes-visitant-musee-illustration-galerie-art_1262-18948.jpg"><br>
</div>

-----------------

# FindMeCulture : Ou comment se cultiver en France.


## Notre projet en quelques mots

A partir de bases de données regroupant des informations sur les musées et les festivals en France, 
l'utilisateur peut **accéder à des propositions ciblées** : d'une part les **musées** situés près de chez lui à partir de son **adresse**, 
d'autre part les **festivals** qui correspondent à son choix de **département** et de **thème.** 
Il lui est également proposé de lire des **diagrammes** représentant leur répartition géographique.

## Principales fonctionnalités
  - Affiche une liste de musées à l'utilisateur autour d'une adresse en entrée, dans une limite de distance paramétrable, dans la ville choisie.
    Il peut également spécifier un nombre maximal de musée les plus proches à afficher. L'utilisateur peut voir pour chaque musée le nom, l'adresse, les coordonnées, le site web, 
    la distance par rapport à l'adresse entrée et les horaires d'ouvertures.
  - Affiche une liste de festivals dans un département donné par l'utilisateur, qu'il peut trier selon les domaines de festivals disponibles dans le département.
    L'utilisateur voit alors les noms des festivals, la date auquel celui-ci à lieu, le site web associé ainsi que le domaine du festival. (ex: Musiques actuelles, Danse, etc.)
  - Affiche à l'utilisateur une liste de graphiques analysant les bases de données sur les musées et festivals en France.

  

## Comment l'obtenir ?

Le code source est hébergé sur GitLab à l'adresse : [**Plan Culture**](https://gitlab-cw8.centralesupelec.fr/2019ahvound/projet-coding-weeks)
Il suffit alors de lancer le fichier **main.py** dans un terminal python.




## Bibliothèques nécessaire au fonctionnement 
- [Pandas](https://pypi.org/project/pandas/): 0.25.3 ou plus récent
- [geopy](https://pypi.org/project/geopy/): 1.20.0 ou plus récent
- [geopandas](https://pypi.org/project/geopandas/) 0.6.2 ou plus récent

De plus, une version de Python **3.7.3** ou plus récente est recommendée car le script fait appel à des fonctions contenues dans le package Python.



## Tests des fonctions
Des modules de test ont été implémentés dans notre projet, ils permettent de tester les fonctions de filtrages de données.
Pour lancer les tests, il est nécessaire d'avoir le package [pytest](https://pypi.org/project/pytest/)

On lance alors la commande suivante dans un terminal Python, à partir du fichier *projet-coding-weeks*

```sh
pytest --cov=tests --cov-report html

```
Ou s'il y a une erreur 

```sh
python -m pytest --cov=tests --cov-report html

```

## Comment le programme fonctionne t-il ?
Pour ce projet, il a fallu diviser le produit à obtenir en différentes fonctionnalités, les premières permettant d'obtenir un MVP.

Dans un premier temps, nous avons décidé de traiter uniquement une base de données concernant les musées de France.
Il a fallu extraire les informations du fichier Excel, construire une base de données (Dataframe) avec pandas en utilisant la programmation objet.
Puis des fonctions filtre ont été écrites, qui permettent à l'utilisateur de choisir où il veut aller au musée.
Un programme demande donc en entrée un endroit, détermine son type (région/ département/ ville) et extrait de la dataframe avec tous les musées de France ceux qui sont dans cet endroit.
D'autre part, des fonctions de comptage associées à Matplotlib ont permis d'effectuer une première étude statistique de la répartition des musées en France, en fonction de la géographie, mais aussi de la démographie.
On a pu tracé des pie charts et des histogrammes donnant les endroits (régions et villes) où il y a le plus de musées, le classement des régions en fonction du rapport musée/habitant et la répartition des musées dans les villes.

Une amélioration a consisté à introduire la géolocalisation de l'utilisateur.
Avec le module geopy on convertit les adresses des musées et celle de l'utilisateur en coordonnées (latitude, longitude).
On calcule la distance de l'utilisateur aux musées et on indique les musées les plus proches.

Une autre amélioration a été l'utilisation de l'interface graphique Tkinter pour le choix du musée.

Nous avons ensuite décidé de traiter une base de données contenant les festivals en France de façon analogue.
De même les données ont été extraites du fichier Excel sous forme de Dataframe.
Des filtres permettent de faire des sélections par endroit mais aussi par période de l'année (mois) et par domaine.
Dans l'interface graphique l'utilisateur peut désormais choisir un département, puis des domaines et une période et voit s'afficher les informations sur les festivals correspondants.
Des études statistiques ont également été effectuées et visualisées avec Dash.
Elles portent sur le nombre de festivals par région, par mois et par domaine, ainsi que sur les départements ayant plus ou moins de festivals (intervalles).


## Arborescence de notre projet

<div>
  <img src="https://i.ibb.co/BPFF7Kh/Arborescence.png"><br>
</div>

## Chronologie du projet :

###                                       **MVP 1** : 
A partir de la base de données listant les **musées français**, nous avons affiché le nombre de musées 
par *ville/région/département* sous la forme d'un [**piechart**](https://ibb.co/PcwQ4vq)


###                                      **MVP 2** : 
Dans un second temps, nous souhaitions renvoyer à un utilisateur la liste des X musées les plus proches d'une adresse qu'il entre, 
ainsi que d'afficher des informations relatives à ceux-ci *(horaires d'ouvertures, site web, évènements spécifiques, etc.)*,
nous avons donc choisi de faire une interface avec **tkinter**. 
De plus, cette interface permet une **analyse des données** : elle peut afficher les histogrammes représentant le **nombre de musée par million d'habitant**, 
ainsi qu'un autre qui affiche la **population dans ces régions**, 
le but étant de mettre en évidence la **corrélation**, ou pas, entre ces deux facteurs. 
Exemple d'[**histogramme**](https://ibb.co/3MPV7Rw)


###                                       **MVP 3** : 
Enfin, nous avons chargé une autre base de donnée, celle de **festivals en France**, cette fois,
l'utilisateur peut **chercher les festivals** pour un **département donné** et 
ensuite **sélectionner** le **thème** du festival qui l'intéresse, 
parmi ceux qui sont disponible dans le **département choisi.**

## Bases de données utilisées :

- [Liste et localisation des Musées de France au 31/12/2017](https://www.data.gouv.fr/fr/datasets/liste-et-localisation-des-musees-de-france/)
- [Panorama des festivals français](https://www.data.gouv.fr/fr/datasets/r/4415a028-aa8e-447d-a2e9-d3917b9bd278)
- [Population des régions françaises](https://www.insee.fr/fr/statistiques/fichier/3677785/ensemble.xls)


## License

Ce projet est sous license de type MIT voir le fichier [LICENSE.md](LICENSE.md) pour plus de détails.

