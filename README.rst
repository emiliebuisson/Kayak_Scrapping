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

Docker
------
Nous avons dans un premier temps configurer notre docker de façon à avoir les images suivantes : 
- selenium-firefox pour le scrapping
- mongo pour la base de données générée
- python contenant à la fois jupyter (port 8888) et un second port permettant de faire tourner notre app.py (5056)
Nous avons repris le requirement.txt du cours en y ajoutant ceux qui nous ont été nécessaires tels que selenium ou encore plotly.express. Nous n'avons pas eu le temps d'enlever les
requirements qui n'étaient pas nécessaires mais nous comptons le faire par la suite pour éviter d'avoir un conteneur de cette taille.

Scrapping
------

Nous avons choisis de scrapper le site de Kayak car nous savons qu'il y a beaucoup de données à explorer avec de nombreux résultats qui peuvent être pertinents.
Le scrapping de Kayak a été réalisé avec selenium. En effet ce dernier permet d'automatiser et de simuler l'interraction de l'utilisateur, tel que le clic sur le bouton 'load more' par exemple.
Cette fonctionnalité était essentielle pour que nous puissions avoir suffisamment de vols pour nos statistiques.
La prise en main a été au départ compliqué puis a finalement fonctionné pour les 10 destinations.
Nous avons cependant été confronté à des difficultés puisque le jour suivant, Kayak a modifié son code source (mise à jour réalisée régulièrement pour éviter le scrapping des autres sites) ce qui 
nous a fait de surcroît perdre beaucoup de temps car il fallait à nouveau renseigner des chemins XPATH différents tout en essayant de contourner les pièges que Kayak pouvait poser.
Pour être sûr d'avoir un code fonctionnel, nous avons donc préféré l'assurer en réalisant un par un le scrapping de chaque destination en mettant à la fin l'ensemble du scrapping sous format .json.
Ainsi, ce .json pourra être facilement entrer dans la base MongoDB, même si au départ nous avions réussi directement à relier notre scrapping avec MongoDB.


MongoDB
------

Comme dit précédemment, pour assurer et éviter les nouveaux problèmes de MAJ, nous avons préféré transformer notre fichier .json dans MongoDB.
Une fois cette étape réalisée, un script python 'traitement_donnees' se trouvant dans le même répertoire que app.py (flask_site) récupère cette base de données présente dans Mongo et va traiter les données
de façon à ce que l'on puisse les utiliser dans app.py. Ainsi, nous avons créer plusieurs fonctions qui permettent entre autre de retourner des boxplot, pieplot à partir des noms des collections (ici nos destinations).
Egalement, nous avons crée une fonction qui va retourner les vols ayant un prix inférieur à celui entré. Cette fonction est donc utile dans le comparateur de prix que nous avons créer pour retourner tous les prix, sans
regarder la destination puisque c'est cela finalement le concept de Adventure Travel.


