from flask import Flask, request, render_template, redirect, url_for
from traitement_donnees import * 
from data import insert_json_files


app = Flask(__name__)  

# ----------------------------------------------------------------------------------------------------

# chargement de la base de données
insert_json_files()

# ----------------------------------------------------------------------------------------------------

# correspond à la page accueil
@app.route('/')
def accueil():
    return render_template('accueil.html')

# ----------------------------------------------------------------------------------------------------

#correspond à la page comparateur de prix

@app.route('/comparateur', methods =["GET", "POST"])
def gfg():
     # initialisation de l'indice
    index = -1
    if request.method == "POST":
        prix = request.form.get("prix")
        if float(prix)>8: # on choisi 8 car le vol le moins cher est à 9 $
            # on utilise la fonction que nous avons créeé dans traitement_donnees.py
            flights, collections_done = find_cheaper_flights(float(prix))
            # nous permet de récupérer l'indice pour le nom des collections / vols qui ont un prix inférieur ou égal à celui entré
            enum = enumerate(flights) 
            return render_template("comparateur_page2.html", prix=prix, flights = flights, collections_done = collections_done, index = index, enum = enum)
        else:
            return render_template("comparateur.html", error="Veuillez mettre un montant plus important")
       
    return render_template("comparateur.html")

# ----------------------------------------------------------------------------------------------------

#correspond aux pages destinations

@app.route('/destinations', methods=["GET", "POST"])
def destinations():
    villes = ["", "tunis", "montreal", "bangkok", "newyork", "marrakech", "venice", "madrid", "berlin", "london", "oslo"]
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville: 
            return redirect(url_for("ville", ville=ville))
    return render_template("destinations.html", villes=villes)


@app.route('/destinations/<ville>', methods=["GET", "POST"])
def ville(ville):
    villes = ["", "tunis", "montreal", "bangkok", "newyork", "marrakech", "venice", "madrid", "berlin", "london", "oslo"]
    # on initialise la variable documents
    documents = []
    # on utilise la fonction que nous avons créeé dans traitement_donnees.py
    documents = get_documents(ville)
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            # on utilise la fonction que nous avons créeé dans traitement_donnees.py
            documents = get_documents(ville)
            return redirect(url_for("ville", ville=ville))
    return render_template("ville.html", villes=villes, documents=documents, ville=ville)

# ----------------------------------------------------------------------------------------------------

#correspond aux pages statistiques

@app.route('/statistiques', methods=["GET", "POST"])
def statistiques():
    villes = ["", "tunis", "montreal", "bangkok", "newyork", "marrakech", "venice", "madrid", "berlin", "london", "oslo"]
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            return redirect(url_for("statville", ville=ville))
    return render_template("statistiques.html", villes=villes)


@app.route('/statistiques/<ville>', methods=["GET", "POST"])
def statville(ville):
    # villes correspond à la liste de ce qu'il y a dans le menu déroulant mais aussi correspond aux noms de nos collections
    villes = ["", "tunis", "montreal", "bangkok", "newyork", "marrakech", "venice", "madrid", "berlin", "london", "oslo"]
    # on initialise nos variables graph
    graphJSON1 = {}
    graphJSON2 = {}
    graphJSON3 = {}
    # on utilise les fonctions que nous avons créeé dans traitement_donnees.py
    days, prices, companies_data, companies = get_stats(ville)
    graphJSON1 = plot_prices(days, prices)
    graphJSON2 = plot_company_prices(companies_data)
    graphJSON3 = pie_chart(companies)
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            days, prices, companies_data, companies = get_stats(ville)
            graphJSON1 = plot_prices(days, prices)
            graphJSON2 = plot_company_prices(companies_data)
            graphJSON3 = pie_chart(companies)
        return redirect(url_for("statville", ville=ville, graphJSON1 = graphJSON1, graphJSON2 = graphJSON2, graphJSON3 = graphJSON3))
    return render_template("statville.html", villes=villes, ville=ville, graphJSON1 = graphJSON1, graphJSON2 = graphJSON2, graphJSON3 = graphJSON3)

# ----------------------------------------------------------------------------------------------------

if __name__=='__main__':
   # notre application tourne sur le port 5066 à cette adresse : http://127.0.0.1:5066/
   app.run(debug=True,host='0.0.0.0', port="5066")