import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient
from collections import Counter
import random
import json
import plotly

# ----------------------------------------------------------------------------------------------------

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


    companies_data = {}
    for company in set(companies):
        company_prices = [price for i, price in enumerate(prices) if companies[i] == company]
        company_duration = [duration for i, duration in enumerate(durations) if companies[i] == company]
        companies_data[company] = (sum(company_duration)/len(company_duration), sum(company_prices)/len(company_prices))

    return days, prices, companies_data, companies

# ----------------------------------------------------------------------------------------------------

# fonction qui retourne le diagramme en bâtons des prix moyens des vols en fonction du jour de la semaine
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

    # création du graphique avec plotly express
    fig = px.bar(x=[x[0] for x in avg_prices], y=[x[1] for x in avg_prices], 
                 labels={"x": "Jours de la semaine", "y": "Prix moyens"}, 
                 title="Prix des billets en fonction des jours de la semaine")
    graphJSON1 = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    return(graphJSON1)

# ----------------------------------------------------------------------------------------------------

# fonction qui retourne la durée moyenne des trajets par compagnie aérienne ainsi que leur prix moyen
def plot_company_prices(companies_data):
    # récupération des données pour le graphique
    companies = list(companies_data.keys())
    durations = [data[0] for data in companies_data.values()]
    prices = [data[1] for data in companies_data.values()]

    # création du graphique avec plotly express
    df = pd.DataFrame({'Compagnies aériennes': companies,
                       'Durée moyenne': durations,
                       'Prix moyen': prices})
    fig2 = px.bar(df, x='Compagnies aériennes', y=['Durée moyenne', 'Prix moyen'], 
                 barmode='group', title='Statistiques par compagnie aérienne')
    graphJSON2 = json.dumps(fig2, cls = plotly.utils.PlotlyJSONEncoder)
    return(graphJSON2)

# ----------------------------------------------------------------------------------------------------
    
# fonction qui retourne un diagramme circulaire présentant la part de marché de chaque compagnie pour une destination

def pie_chart(companies):
    # Calcul de la part de marché de chaque compagnie
    counter = Counter(companies)
    market_share = [counter[company] for company in counter]
    total = sum(market_share)
    market_share_percentage = [round(100 * share / total, 2) for share in market_share]

    # Création du graphique
    data = {"labels": list(counter.keys()), "values": market_share_percentage}
    fig3 = px.pie(data_frame=data, values="values", names="labels")
    fig3.update_traces(textposition="inside", textinfo="percent+label")
    fig3.update_layout(title="Part de marché des compagnies aériennes")
    graphJSON3 = json.dumps(fig3, cls = plotly.utils.PlotlyJSONEncoder)
    return(graphJSON3)


# ----------------------------------------------------------------------------------------------------
 
# fonction pour le comparateur de prix qui va retourner un vol de chaque destination 
# (s'il en trouve un en dessous du prix indiqué), avec un prix au plus proche du prix entré

def find_cheaper_flights(max_price):
    client = pymongo.MongoClient("mongodb://mongo")
    db = client["Kayak"]
    collections = db.list_collection_names()
    flights = []
    collections_done = []
    for collection_name in collections:
        collection = db[collection_name]
        result = collection.find({"price": {"$lte": max_price}}).sort("price", pymongo.DESCENDING).limit(1)
        for doc in result:
            flights.append(doc)
            collections_done.append(collection_name)
            break
    return flights, collections_done


# ----------------------------------------------------------------------------------------------------

# fonction utilisée pour la page Destination qui retourne 15 documents d'une même collection (destination)

def get_documents(collection_name):
    client = pymongo.MongoClient("mongodb://mongo")
    db = client["Kayak"]
    collection = db[collection_name]
    documents = list(collection.find().limit(15))
    return documents

# ----------------------------------------------------------------------------------------------------
