from flask import Flask, request, render_template, redirect, url_for
from traitement_donnees import * 
from data import insert_json_files

# Flask constructor
app = Flask(__name__)  

# load
insert_json_files()

# A decorator used to tell the application
# which URL is associated function

@app.route('/', methods =["GET"])
def accueil():
    return render_template('accueil.html')


@app.route('/comparateur', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        prix = request.form.get("prix")
        if prix:
            flights, collections_done = find_cheaper_flights(float(prix))
            return render_template("comparateur_page2.html", prix=prix, flights = flights, collections_done = collections_done)
        else:
            return render_template("comparateur.html", error="Veuillez remplir le formulaire")
       
    return render_template("comparateur.html")



@app.route('/destinations', methods=["GET", "POST"])
def destinations():
    villes = ["", "Tunis", "Montreal", "Bangkok", "New York", "Marrakech", "Venice", "Madrid", "Berlin", "London", "Oslo"]
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            return redirect(url_for("ville", ville=ville))
    return render_template("destinations.html", villes=villes)



@app.route('/destinations/<ville>')
def ville(ville):
    return render_template("ville.html", ville=ville)


@app.route('/statistiques', methods=["GET", "POST"])
def statistiques():
    villes = ["", "Tunis", "Montreal", "Bangkok", "New York", "Marrakech", "Venice", "Madrid", "Berlin", "London", "Oslo"]
    if request.method == "POST":
        ville = request.form.get("ville")
        if ville:
            return redirect(url_for("statville", ville=ville))
    return render_template("statistiques.html", villes=villes)

@app.route('/statistiques/<ville>')
def statville(ville):
    
    return render_template("statville.html", ville=ville)

if __name__=='__main__':
   app.run(debug=True,host='0.0.0.0', port="5066")