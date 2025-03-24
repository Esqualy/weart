from flask import Flask, request, render_template, redirect, url_for
import json
from requetes import like, auteur, like_oeuvre

app = Flask(__name__)

def get_artiste_info(IdOeu):
    """Récupère le nom et l'image de l'artiste d'une œuvre"""
    IdAr = auteur(IdOeu)
    if not IdAr:
        return None

    with open("artistes.json", "r") as f:
        artistes = json.load(f)
        for artiste in artistes:
            if artiste["IdAr"] == IdAr:
                return artiste
    return None

@app.route("/oeuvre/<int:IdOeu>", methods=["GET", "POST"])
def afficher_oeuvre(IdOeu):
    user_id = 1  # Remplace avec l'ID de l'utilisateur connecté (ex: session)

    if request.method == "POST":
        like(user_id, IdOeu)  # Ajoute un like
        return redirect(url_for("afficher_oeuvre", IdOeu=IdOeu))

    artiste = get_artiste_info(IdOeu)
    likes = len(like_oeuvre(IdOeu))

    return render_template("oeuvre.html", IdOeu=IdOeu, artiste=artiste, likes=likes)

if __name__ == "__main__":
    app.run(debug=True)
