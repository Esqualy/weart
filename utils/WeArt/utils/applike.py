from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simule une base de données des likes (dictionnaire)
likes_db = {}

@app.route("/oeuvre/<int:IdOeu>")
def afficher_oeuvre(IdOeu):
    likes = likes_db.get(IdOeu, 0)  # Récupère le nombre de likes (0 par défaut)
    return render_template("like.html", IdOeu=IdOeu, likes=likes)

@app.route("/like/<int:IdOeu>", methods=["POST"])
def like_oeuvre(IdOeu):
    likes_db[IdOeu] = likes_db.get(IdOeu, 0) + 1  # Ajoute 1 like
    return jsonify({"likes": likes_db[IdOeu]})  # Renvoie le nouveau nombre de likes

if __name__ == "__main__":
    app.run(debug=True)
