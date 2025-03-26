from flask import Flask, request, redirect, url_for, render_template, session, flash, render_template_string
from requetes import like_amateur, like_amateurs, auteur, oeuvres_auteurs
from algo import selection_1, selection_2, user_oeuvres_artists
from datetime import datetime

import bcrypt
import json
import os
import random 
import paramiko

app = Flask(__name__)
app.secret_key = 'F0AO4Vgqg@g25#'  

MAINTENANCE_MODE = False  

# Configuration pour SFTP
SFTP_HOST = '83.150.217.109'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'F0AO4Vgqg@g25#'

def upload_file_sftp(local_file_path, remote_file_path):
    try:
        # Se connecter au serveur SFTP
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Télécharger le fichier
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Erreur SFTP : {e}")

# Vérification du mot de passe avec bcrypt
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash)

def generate_unique_id(file_name):
    existing_ids = set()
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
            for user in users:
                existing_ids.add(user.get("Id", ""))
    
    while True:
        new_id = str(random.randint(10**17, 10**18 - 1))
        if new_id not in existing_ids:
            return new_id

def save_user_to_json(user_type, pseudo, password, mail, ddn, nom, prenom, genre):
    file_name = f"{user_type}.json"
    user_id = generate_unique_id(file_name)
    default_pp = "https://cdn.we-art.art/static/pp/default.jpg"
    
    user_data = {
        "Id": user_id,
        "pseudo": pseudo,
        "password": password,
        "mail": mail,
        "ddn": ddn,
        "nom": nom,
        "prenom": prenom,
        "genre": genre,
        "profile_picture": default_pp,
        "bio": None  
    }
    
    users = []
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
    
    users.append(user_data)
    with open(file_name, 'w') as f:
        json.dump(users, f, indent=2)

def get_user_from_json(user_id):
    with open('artiste.json', 'r') as f:
        artists = json.load(f)
    with open('amateur.json', 'r') as f:
        amateurs = json.load(f)
    
    user = next((u for u in artists + amateurs if u["Id"] == user_id), None)
    return user

def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash.encode())

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def maintenance_required(f):
    def wrapper(*args, **kwargs):
        if MAINTENANCE_MODE:
            return render_template('maintenance.html')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def get_image_url_for_oeuvre(oeuvre_id):
    return f"http://127.0.0.1:5000/static/{oeuvre_id}.jpg"


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))
    
    user_id = session.get('user_id')

    idAmateurMain = user_id
    idOeuvresLikees = like_amateur(idAmateurMain)
    idArtistsLikes = user_oeuvres_artists(idOeuvresLikees)
    idOeuvresArtists = oeuvres_auteurs(idArtistsLikes)
    idOeuvresAProposer1 = selection_1(idOeuvresArtists, idOeuvresLikees)
    idOeuvresLikeesParAmateursOeuvresLikees = like_amateurs(idOeuvresLikees)
    idOeuvresAProposer2 = selection_2(idOeuvresLikeesParAmateursOeuvresLikees, idOeuvresLikees)

    idOeuvresAProposerFinal = list(set(idOeuvresAProposer1) | set(idOeuvresAProposer2))

    # Pour chaque ID d'œuvre, récupérer l'URL de l'image
    oeuvres_avec_images = []
    for oeuvre_id in idOeuvresAProposerFinal:
        image_url = get_image_url_for_oeuvre(oeuvre_id)  # Assure-toi que cette fonction existe
        oeuvres_avec_images.append({"id": oeuvre_id, "image_url": image_url})

    # Passer la variable oeuvres_avec_images au template
    return render_template("index.html", 
                        username=session['username'], 
                        user_role=session.get('user_role'), 
                        user_id=user_id, 
                        recommandations=oeuvres_avec_images)

@app.route("/signin", methods=["GET", "POST"])
@maintenance_required
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open('artiste.json', 'r') as f:
            artists = json.load(f)
        with open('amateur.json', 'r') as f:
            amateurs = json.load(f)

        user = None
        user_role = None

        for u in artists:
            if u["pseudo"] == username and verify_password(password, u["password"]):
                user = u
                user_role = "artiste"
                break

        if not user:
            for u in amateurs:
                if u["pseudo"] == username and verify_password(password, u["password"]):
                    user = u
                    user_role = "amateur"
                    break

        if user:
            session['username'] = username
            session['user_role'] = user_role
            session['user_id'] = user['Id'] 
            return redirect(url_for('index'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.")

    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
@maintenance_required
def signup():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        mail = request.form["mail"]
        ddn = request.form["ddn"]
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        genre = request.form["genre"]
        user_type = request.form["user_type"]

        today = datetime.today()
        birthdate = datetime.strptime(ddn, "%Y-%m-%d")
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 15:
            flash("L'âge légal en France pour s'inscrire est de 15 ans.", "error")
            return render_template("signup.html")

        with open('artiste.json', 'r') as f:
            artists = json.load(f)
        with open('amateur.json', 'r') as f:
            amateurs = json.load(f)

        for user in artists + amateurs:
            if user["pseudo"] == pseudo:
                flash("Ce pseudo est déjà pris.", "error")
                return render_template("signup.html")
            if user["mail"] == mail:
                flash("Cet email est déjà utilisé.", "error")
                return render_template("signup.html")

        password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        save_user_to_json(user_type, pseudo, password_hashed, mail, ddn, nom, prenom, genre)

        flash(f"Compte {user_type} créé avec succès !")
        return redirect(url_for('signin'))

    return render_template("signup.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    user_id = session.get('user_id')  

    if not user_id:
        flash("Vous devez être connecté pour modifier votre profil.", "error")
        return redirect(url_for('login'))  

    with open('artiste.json', 'r') as f:
        artists = json.load(f)
    with open('amateur.json', 'r') as f:
        amateurs = json.load(f)

    user = next((u for u in artists if u['Id'] == user_id), None)
    if not user:
        user = next((u for u in amateurs if u['Id'] == user_id), None)

    if not user:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for('login'))  

    if request.method == "POST":
        bio = request.form.get("bio")
        file = request.files.get("profile_picture")

        if bio:
            user["bio"] = bio

        if file:
            temp_dir = "./uploads"
            os.makedirs(temp_dir, exist_ok=True)
            local_file_path = os.path.join(temp_dir, file.filename)
            file.save(local_file_path)

            remote_file_name = f"{user['Id']}.jpg"
            remote_file_path = f"/root/cdn/static/pp/{remote_file_name}"

            upload_file_sftp(local_file_path, remote_file_path)

            user["profile_picture"] = f"https://cdn.we-art.art/static/pp/{remote_file_name}"

        # Mettre à jour les fichiers JSON avec les modifications
        if user["Id"] in [u["Id"] for u in artists]:
            artists = [u if u["Id"] != user["Id"] else user for u in artists]
            with open('artiste.json', 'w') as f:
                json.dump(artists, f, indent=2)
        elif user["Id"] in [u["Id"] for u in amateurs]:
            amateurs = [u if u["Id"] != user["Id"] else user for u in amateurs]
            with open('amateur.json', 'w') as f:
                json.dump(amateurs, f, indent=2)

        flash("Profil mis à jour avec succès.", "success")

        return redirect(url_for('upload'))

    return render_template("settings.html", user=user)

@app.route("/account/<user_id>")
@login_required  
@maintenance_required
def account(user_id):
    with open('badge.json', 'r') as file:
        badges = json.load(file)
    
    user = get_user_from_json(user_id)  
    user_id = session.get('user_id')  

    if not user:
        flash("Profil introuvable.", "error")
        return redirect(url_for('index'))

    # Récupérer les badges de l'utilisateur
    user_badges = [badges[badge_id] for badge_id in user.get('badges', [])] 

    if 'username' not in session:
        return redirect(url_for('signin'))

    return render_template("account.html", username=session['username'], user_role=session.get('user_role'), user=user, badges=user_badges, user_id=user_id)


@app.route("/logout")
@maintenance_required
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('signin'))

@app.route("/search")
@login_required  
@maintenance_required
def search():
    return render_template("search.html", username=session['username'], user_role=session.get('user_role'))

@app.route("/maintenance")
def maintenance():
    return render_template("maintenance.html")

@app.route("/terms_of_service")
@maintenance_required
def terms_of_service():
    return render_template("terms_of_service.html")

@app.route("/privacy_policy")
@maintenance_required
def privacy_policy(): 
    return render_template("privacy_policy.html")

# 🌐 Gestion des erreurs HTTP
@app.errorhandler(400)
def bad_request(error):
    return render_template('bad_request.html'), 400  

@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized.html'), 401 

@app.errorhandler(403)
def forbidden(error):
    return render_template('forbidden.html'), 403  

@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404  

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('method_not_allowed.html'), 405  

@app.errorhandler(406)
def not_acceptable(error):
    return render_template('not_acceptable.html'), 406  

@app.errorhandler(412)
def precondition_failed(error):
    return render_template('precondition_failed.html'), 412  

@app.errorhandler(415)
def unsupported_media_type(error):
    return render_template('unsupported_media_type.html'), 415  

@app.errorhandler(501)
def not_implemented(error):
    return render_template('not_impremented.html'), 501  

@app.errorhandler(502)
def bad_gateway(error):
    return render_template('bad_gateway.html'), 502  

@app.errorhandler(503)
def maintenance(error):
    return render_template('maintenance.html'), 503 

if __name__ == "__main__":
    app.run(debug=True)
