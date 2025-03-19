from flask import Flask, request, redirect, url_for, render_template, session, flash
import bcrypt
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Nécessaire pour utiliser les sessions

# Vérification du mot de passe avec bcrypt
def verify_password(input_password, stored_hash):
    """Vérifie si le mot de passe entré correspond au hash stocké."""
    return bcrypt.checkpw(input_password.encode(), stored_hash)

# Fonction pour ajouter un utilisateur dans un fichier JSON
def save_user_to_json(user_type, pseudo, password, mail, ddn):
    user_data = {
        "pseudo": pseudo,
        "password": password,
        "mail": mail,
        "ddn": ddn
    }

    file_name = f"{user_type}.json"
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
    else:
        users = []

    user_id = len(users) + 1
    user_data["id_" + user_type[0:2]] = str(user_id)
    users.append(user_data)

    with open(file_name, 'w') as f:
        json.dump(users, f, indent=2)

# Route pour la page d'index
@app.route("/")
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template("index.html", username=session['username'])

# Route pour la page de connexion
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Chargement des utilisateurs (artistes + amateurs)
        with open('artiste.json', 'r') as f:
            artists = json.load(f)
        with open('amateur.json', 'r') as f:
            amateurs = json.load(f)

        # Vérification de l'existence du compte
        user = None
        for u in artists + amateurs:
            if u["pseudo"] == username and verify_password(password, u["password"].encode()):
                user = u
                break
        
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.")
            return render_template("signin.html")

    return render_template("signin.html")

# Route pour la page d'inscription
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        mail = request.form["mail"]
        ddn = request.form["ddn"]
        user_type = request.form["user_type"]

        # Hachage du mot de passe
        password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Enregistrement dans les fichiers JSON en fonction du type d'utilisateur
        save_user_to_json(user_type, pseudo, password_hashed.decode(), mail, ddn)

        flash(f"Compte {user_type} créé avec succès !")
        return redirect(url_for('signin'))

    return render_template("signup.html")

# Déconnexion
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(debug=True)
