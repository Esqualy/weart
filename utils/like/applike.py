## Clémance Chateau -- Noé Callejon
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Simule une base de données des likes (dictionnaire)
likes_db = {}

@app.route("/oeuvre/<int:IdOeu>")
def afficher_oeuvre(IdOeu):
    likes = likes_db.get(IdOeu, 0)  # Récupère le nombre de likes (0 par défaut)
    # Charge l'historique des utilisateurs ayant liké cette œuvre
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    
    utilisateurs_likes = [d["IdAm"] for d in data if d["IdOeu"] == IdOeu]
    return render_template("like.html", IdOeu=IdOeu, likes=likes, utilisateurs_likes=utilisateurs_likes)

@app.route("/like/<int:IdOeu>", methods=["POST"])
def like_oeuvre(IdOeu):
    # Ajoute un like
    likes_db[IdOeu] = likes_db.get(IdOeu, 0) + 1  # Ajoute 1 like
    # Ajout de l'historique du like
    IdAm = request.form.get("IdAm")  # ID de l'amateur (utilisateur dqui like)
    d = {"IdAm": IdAm, "IdOeu": IdOeu}
    
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    
    if d not in data:
        data.append(d)
        with open("amateur_oeuvre.json", "w") as f:
            json.dump(data, f)
    
    return jsonify({"likes": likes_db[IdOeu], "utilisateurs_likes": [d["IdAm"] for d in data if d["IdOeu"] == IdOeu]})

if __name__ == "__main__":
    app.run(debug=True)
