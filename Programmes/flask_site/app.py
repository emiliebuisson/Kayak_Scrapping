# importing Flask and other modules
from flask import Flask, request, render_template, redirect, url_for
 
# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       prix = request.form.get("prix")
       return render_template("comparateur_page2.html", prix=prix)
    return render_template("comparateur.html")


@app.route('/accueil')
def accueil():
    return render_template('accueil.html')


@app.route('/comparateur')
def comparateur():
    return render_template('comparateur.html')


# @app.route('/destinations', methods=["GET", "POST"])
# def destinations():
#     villes = ["Tunis","Montreal", "Bangkok", "New York", "Marrakech", "Venice", "Madrid", "Berlin", "London", "Oslo"]
#     if request.method == "POST":
#         ville = request.form.get("ville")
#         return redirect(url_for("ville", ville=ville))
#     return render_template("destinations.html", villes=villes)

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


@app.route('/statistiques')
def statistiques():
    return render_template('statistiques.html')


if __name__=='__main__':
   app.run(debug=True,host='0.0.0.0', port="5066")
