import pandas as pd
import os
from pymongo import MongoClient


# fonction qui nous permet d'insérer les fichiers JSON obtenus avec le scraping dans une base de données MongoDB

def insert_json_files():
    # création de l'instance du client MongoClient + spécification de l'adresse IP / port du serveur de la BDD
    client = MongoClient('mongodb://mongo')
    # Accès à la BDD en spécifiant nom + infos d'identification si besoin
    db = client['Kayak']
    path = 'Programmes/flask_site/static/fichiersjson'
    json_files = [f for f in os.listdir(path) if f.endswith('.json')]
    for fichier in json_files:
        coll =(pd.read_json(path + '/'+ fichier, lines = True))
        coll = coll.drop('_id', axis = 1)
        collection = db[fichier[6:-5]]
        for doc in range(coll.shape[0]):
    #         print(coll['price'][doc])
            
            collection.insert_one({"price": float(coll['price'][doc]),
                                "date":coll['date'][doc],
                                "day": coll['day'][doc],
                                "departure":coll['departure'][doc],
                                "arrival":coll['arrival'][doc],
                                "duration":coll['duration'][doc],
                                "company":coll['company'][doc]})