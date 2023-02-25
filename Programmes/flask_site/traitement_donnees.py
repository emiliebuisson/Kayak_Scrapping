import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient
import collections
from collections import Counter
import os



# fonction pour récupérer les données de la collection et calculer les statistiques nécessaires
def get_stats(collection_name):
    # connexion à la base de données et à la collection
    client = pymongo.MongoClient("mongodb://mongo")
    db = client["Kayak"]
    collection = db[collection_name]

    # récupération des données de la collection
    cursor = collection.find()
    prices = []
    days = []
    companies = []
    durations = []
    for document in cursor:
        prices.append(int(document["price"]))
        days.append(document["day"])
        companies.append(document["company"])
        duration = document["duration"]
        hours, minutes = duration.split("h ")
        duration_minutes = int(hours)*60 + int(minutes[:-1])
        durations.append(duration_minutes)

    # calcul des statistiques nécessaires pour les graphiques
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    price_stats = (avg_price, min_price, max_price)

    companies_data = {}
    for company in set(companies):
        company_prices = [price for i, price in enumerate(prices) if companies[i] == company]
        company_duration = [duration for i, duration in enumerate(durations) if companies[i] == company]
        companies_data[company] = (sum(company_duration)/len(company_duration), sum(company_prices)/len(company_prices))

    return days, prices, price_stats, companies_data, companies



def plot_prices(days, prices):
    # création d'un dictionnaire pour stocker la somme des prix par jour
    prices_per_day = {}
    # création d'un dictionnaire pour stocker le nombre de billets par jour
    tickets_per_day = {}

    # parcours de toutes les données de la liste de prix
    for day, price in zip(days, prices):
        # si le jour n'est pas dans le dictionnaire, on l'ajoute
        if day not in prices_per_day:
            prices_per_day[day] = 0
            tickets_per_day[day] = 0
        # on ajoute le prix du billet au total pour le jour en question
        prices_per_day[day] += price
        # on incrémente le nombre de billets pour le jour en question
        tickets_per_day[day] += 1

    # création d'une liste de tuples contenant la moyenne des prix pour chaque jour
    avg_prices = [(day, prices_per_day[day] / tickets_per_day[day]) for day in sorted(prices_per_day.keys(), reverse=True)]

    # création du graphique
    fig = px.bar(x=[x[0] for x in avg_prices], y=[x[1] for x in avg_prices], 
                 labels={"x": "Jours de la semaine", "y": "Prix moyens"}, 
                 title="Prix des billets en fonction des jours de la semaine")
    fig.show()



def plot_company_prices(companies_data):
    # récupération des données pour le graphique
    companies = list(companies_data.keys())
    durations = [data[0] for data in companies_data.values()]
    prices = [data[1] for data in companies_data.values()]

    # création du graphique
    df = pd.DataFrame({'Compagnies aériennes': companies,
                       'Durée moyenne': durations,
                       'Prix moyen': prices})
    fig2 = px.bar(df, x='Compagnies aériennes', y=['Durée moyenne', 'Prix moyen'], 
                 barmode='group', title='Statistiques par compagnie aérienne')
    fig2.show()

    

def pie_chart(companies):
    # Calcul de la part de marché de chaque compagnie
    counter = Counter(companies)
    market_share = [counter[company] for company in counter]
    total = sum(market_share)
    market_share_percentage = [round(100 * share / total, 2) for share in market_share]

    # Création du graphique
    data = {"labels": list(counter.keys()), "values": market_share_percentage}
    fig = px.pie(data_frame=data, values="values", names="labels")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title="Part de marché des compagnies aériennes")
    fig.show()

    

# fonction pour afficher les deux graphiques
def show_stats(collection_name):
    # récupération des données
    days, prices, price_stats, companies_data, companies = get_stats(collection_name)

    # affichage des graphiques
    return plot_prices(days, prices), plot_company_prices(companies_data), pie_chart(companies)


# fonction pour le comparateur de prix
def find_flights_by_price(max_price):
    # création de l'instance du client MongoClient + spécification de l'adresse IP / port du serveur de la BDD
    client = MongoClient('mongodb://mongo')
    # Accès à la BDD en spécifiant nom + infos d'identification si besoin
    db = client['Kayak']

    # connexion à la base de données et récupération de toutes les collections de vols
    flights_collections = db.list_collection_names()

    # liste pour stocker tous les vols qui coûtent moins cher que max_price
    flights = []

    # boucle sur toutes les collections de vols
    for collection_name in flights_collections:
        collection = db[collection_name]
        # récupération de tous les vols qui coûtent moins cher que max_price
        result = collection.find({"price": {"$lt": max_price}})
        # ajout des vols à la liste
        for doc in result:
            flights.append(doc)

    return flights





import pymongo
import random

import random

def find_cheaper_flights(max_price):
    client = pymongo.MongoClient("mongodb://mongo")
    db = client["Kayak"]
    # liste pour stocker tous les vols qui coûtent moins cher que max_price
    flights = []
    # liste pour stocker les noms des collections déjà traitées
    collections_done = []

    # boucle jusqu'à ce qu'on ait récupéré un vol dans 3 collections différentes
    while len(flights) < 3:
        # choix aléatoire d'une collection parmi celles qui n'ont pas encore été traitées
        remaining_collections = [col for col in db.list_collection_names() if col not in collections_done]
        if not remaining_collections:
            # si toutes les collections ont été traitées sans trouver de vol correspondant, on arrête la boucle
            break
        collection_name = random.choice(remaining_collections)
        collection = db[collection_name]
        # récupération d'un vol qui coûte moins cher que max_price dans cette collection
        result = collection.find_one({"price": {"$lt": max_price}})
        if result:
            # si un vol a été trouvé, on l'ajoute à la liste des vols trouvés
            flights.append(result)
            # on ajoute la collection traitée à la liste des collections déjà traitées
            collections_done.append(collection_name)

    return flights, collections_done