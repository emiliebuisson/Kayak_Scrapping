================
Adventure Travel
================

Nous avons eu l'envie de créer un comparateur qui fonctionne à l'inverse de Kayak ou autre comparateur de vols connus.
Notre objectif ? Proposer aux passionnés de voyages une solution intuitive et pratique, où il suffit simplement d'entrer son budget 
maximal pour le vol et ainsi être redirigé vers toutes les destinations du monde entier, toujours à votre budget !
Notre solution est destinée aux personnes passionnées par le voyage et n'ayant pas peur de découvrir de nouvelles cultures. 
C'est ce que nous avons essayé de recréer avec Adventure Travel, qui permet également de prendre connaissance des statistiques suivant 
les différentes destinations pour avoir une vue globale des tendances (jours où les billets sont les moins chers suivant la destination, 
compagnies plus présentes que d'autres pour certaines destination etc).
Adventure Travel est pensé pour les aventuriers qui veulent à tout prix (ou presque) partir !


Comment lancer l'app
------

Après avoir lancé Docker desktop, il faut dans un premier temps ouvrir un terminal et se placer dans le chemin du dossier.
  
  > cd ..\Kayak_Scrapping

Il faudra ensuite exécuter la commande suivante ::

  > docker-compose up -d

Nous ouvrons ensuite le terminal python de notre conteneur dans Docker puis nous exécutons la commande suivante qui va lancer notre app.py ::
    
  > python Programmes/flask_site/app.py

Nous pouvons alors accéder à l'application en suivant la première adresse proposée : 'http://127.0.0.1:5066'.


Docker
------
Nous avons dans un premier temps configuré notre docker de façon à avoir les images suivantes : 

- selenium-firefox pour le scrapping
- mongo pour la base de données générée
- python contenant à la fois jupyter (port 8888) et un second port permettant de faire tourner notre app.py (5056)

Nous avons repris le requirement.txt du cours en y ajoutant ceux qui nous ont été nécessaires tels que selenium ou encore plotly.express. Nous n'avons pas eu le temps d'enlever les
requirements qui n'étaient pas nécessaires mais nous comptons le faire par la suite pour éviter d'avoir un conteneur de cette taille.

Scraping
------

Nous avons choisi de scraper le site de Kayak car nous savons qu'il y a beaucoup de données à explorer avec de nombreux résultats qui peuvent être pertinents.
Le scraping de Kayak a été réalisé avec selenium. En effet, ce dernier permet d'automatiser et de simuler l'interaction de l'utilisateur, tel que le clic sur le bouton 'load more' par exemple. 
Cette fonctionnalité était essentielle pour que nous puissions avoir suffisamment de vols pour nos statistiques.
La prise en main a été au départ compliquée puis a finalement fonctionné pour les 10 destinations.
Nous avons cependant été confrontées à des difficultés puisque par la suite, Kayak a modifié son code source (mise à jour réalisée régulièrement pour éviter le scraping des autres sites) ce qui 
nous a fait de surcroît perdre beaucoup de temps car il fallait à nouveau renseigner des chemins XPATH différents tout en essayant de contourner les pièges que Kayak pouvait poser.
Nous avons donc fais le choix de stocker les données scrapées dans des fichiers JSON afin d'assurer le bon fonctionnement du programme. Cette méthode permettra de sécuriser le processus dans les cas de nouvelles mises à jour du code source.
Ainsi, les fichiers JSON pourront être facilement entrés dans la base MongoDB, même si au départ nous avions réussi directement à relier notre scraping avec MongoDB.

MongoDB
------

Comme dit précédemment, pour assurer et éviter les nouveaux problèmes de MAJ, nous avons préféré stocker nos données dans des fichiers JSON.
Pour ce faire, nous utilisons le terminal MongoDB dans docker à l'aide de la commande suivante ::

  > docker exec -it mongo bash


Une fois dans le terminal MongoDB, nous exportons chaque collection sous un fichier .json à l'aide de la commande ::

  > mongoexport --db Kayak --collection <nom de la collection> --out <nom du fichier à créer>.json
  > exit

Nous avons donc à ce stade les 10 fichiers .json correspondant aux 10 collections des destinations. Nous les copions vers la machine locale de la manière suivante ::

  > docker cp mongo:<chemin du fichier> <chemin local>

Nous pouvons donc maintenant récupérer les données des fichiers JSON et les importer dans MongoDB si besoin, c'est ce que nous allons faire dans le script 'data.py'.
Une fois cette étape réalisée, un script python 'traitement_donnees' se trouvant dans le même répertoire que app.py (flask_site) récupère cette base de données présente dans Mongo et va traiter les données
de façon à ce que l'on puisse les utiliser dans app.py. Ainsi, nous avons créé plusieurs fonctions qui permettent entre autre de retourner des boxplot, pieplot à partir des noms des collections (ici nos destinations).
Egalement, nous avons créé une fonction qui va retourner les vols ayant un prix inférieur à celui entré. Cette fonction est donc utile dans le comparateur de prix que nous avons créé pour retourner tous les prix, sans
regarder la destination puisque c'est cela finalement le concept d'Adventure Travel.


Pistes d'améliorations
------

Nous avons pensé à plusieurs fonctionnalités supplémentaires qui pourraient être intéressantes et pratiques. 
Premièrement, nous nous sommes limitées ici à 10 destinations en raison du temps de scraping et de la sécurisation du programme par rapport au problème de MAJ rencontré,
cependant, l'idée serait d'étendre un maximum le nombre de destinations possibles.
Ensuite, nous avons opté pour des forms de sélection déroulants, mais en utilisant Elasticsearch nous pourrions combiner le form déroulant avec une entrée de texte flexible pour chercher une destination.
Egalement, nous avons ici des vols aller pour une date précise (22/03/2023) avec une flexibilité de départ de plus ou moins 3 jours,
il serait idéal d'ajouter des options de choix pour les conditions de date, de flexibilité, de trajets aller/retour, ou encore même de bagages. Nous pourrions alors aussi ajouter 
une option pour choisir des préférences de continent ou pays.
