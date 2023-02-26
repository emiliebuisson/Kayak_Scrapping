from flask import Flask, request, render_template, redirect, url_for
from traitement_donnees import * 
from data import insert_json_files

app = Flask(__name__)  

# chargement de la base de données
insert_json_files()


@app.route('/', methods =["GET"])
def accueil():
    return render_template('accueil.html')


@app.route('/comparateur', methods =["GET", "POST"])
def gfg():
    index = -1 # initialisation de l'indice
    if request.method == "POST":
        # getting input with name = fname in HTML form
        prix = request.form.get("prix")
        if float(prix)>8:
            flights, collections_done = find_cheaper_flights(float(prix))
            enum = enumerate(flights)
            return render_template("comparateur_page2.html", prix=prix, flights = flights, collections_done = collections_done, index = index, enum = enum)
        else:
            return render_template("comparateur.html", error="Veuillez mettre un montant plus important")
       
    return render_template("comparateur.html")



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
    documents = []
    documents = get_documents(ville)
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            documents = get_documents(ville)
            return redirect(url_for("ville", ville=ville))
    return render_template("ville.html", villes=villes, documents=documents, ville=ville)



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
    villes = ["", "tunis", "montreal", "bangkok", "newyork", "marrakech", "venice", "madrid", "berlin", "london", "oslo"]
    graphJSON1 = {}
    graphJSON2 = {}
    graphJSON3 = {}
    days, prices, price_stats, companies_data, companies = get_stats(ville)
    graphJSON1 = plot_prices(days, prices)
    graphJSON2 = plot_company_prices(companies_data)
    graphJSON3 = pie_chart(companies)
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            days, prices, price_stats, companies_data, companies = get_stats(ville)
            graphJSON1 = plot_prices(days, prices)
            graphJSON2 = plot_company_prices(companies_data)
            graphJSON3 = pie_chart(companies)
        return redirect(url_for("statville", ville=ville, graphJSON1 = graphJSON1, graphJSON2 = graphJSON2, graphJSON3 = graphJSON3))
    return render_template("statville.html", villes=villes, ville=ville, graphJSON1 = graphJSON1, graphJSON2 = graphJSON2, graphJSON3 = graphJSON3)

if __name__=='__main__':
   app.run(debug=True,host='0.0.0.0', port="5066")