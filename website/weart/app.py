from flask import Flask, request, redirect, url_for, render_template, session, flash, render_template_string
from requetes import like_amateur, like_amateurs, auteur, oeuvres_auteurs
from algo import selection_1, selection_2, user_oeuvres_artists
from datetime import datetime, date 

import bcrypt
import json
import os
import random 
import paramiko

app = Flask(__name__)
app.secret_key = 'F0AO4Vgqg@g25#'  

MAINTENANCE_MODE = False  

# Configuration pour SFTP VPS KVM
SFTP_HOST = '83.150.217.109'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'F0AO4Vgqg@g25#'

# Configuration pour SFTP VPS STOCKAGE
SFTP_HOST_STOCK = '93.127.158.145'
SFTP_PORT_STOCK = 22
SFTP_USER_STOCK = 'root'
SFTP_PASS_STOCK = 'HT3j02YGbL'

def generate_id():
    return str(random.randint(10**17, 10**18 - 1))

def upload_file_sftp(local_file_path, remote_file_path):
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Erreur SFTP : {e}")

def stock_upload_file_sftp(local_file_path, remote_file_path):
    try:
        transport = paramiko.Transport((SFTP_HOST_STOCK, SFTP_PORT_STOCK))
        transport.connect(username=SFTP_USER_STOCK, password=SFTP_PASS_STOCK)
        sftp = paramiko.SFTPClient.from_transport(transport)

        directories = remote_file_path.rsplit('/', 1)[0]
        try:
            sftp.chdir("/")  # Aller à la racine
            for directory in directories.split("/"):
                if directory:
                    try:
                        sftp.chdir(directory)  # Essayer d'aller dans le dossier
                    except IOError:
                        sftp.mkdir(directory)  # Si inexistant, le créer
                        sftp.chdir(directory)
        except Exception as e:
            print(f"Error creating directories: {e}")

        # Upload du fichier
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
        print(f"File successfully uploaded to {remote_file_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Vérification du mot de passe avec bcrypt
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash)

def generate_unique_id(file_name, user_type):
    existing_ids = set()
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
            for user in users:
                existing_ids.add(user.get(f"Id{user_type}", ""))  # Vérifie IdAm ou IdAr
    
    while True:
        new_id = str(random.randint(10**17, 10**18 - 1))
        if new_id not in existing_ids:
            return new_id

def save_user_to_json(user_type, pseudo, password, mail, ddn, nom, prenom, genre):
    file_name = f"{user_type}.json"
    user_id_key = "IdAr" if user_type == "artiste" else "IdAm"
    user_id = generate_unique_id(file_name, user_type)
    default_pp = "https://cdn.we-art.art/static/pp/default.jpg"
    
    user_data = {
        user_id_key: user_id,
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
    
    user = next((u for u in artists if u.get("IdAr") == user_id), None) or \
           next((u for u in amateurs if u.get("IdAm") == user_id), None)
    
    return user

def get_user_from_json(user_id):
    with open('artiste.json', 'r') as f:
        artists = json.load(f)
    with open('amateur.json', 'r') as f:
        amateurs = json.load(f)
    
    user = next((u for u in artists if u.get("IdAr") == user_id), None) or \
           next((u for u in amateurs if u.get("IdAm") == user_id), None)
    
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

    oeuvres_avec_images = []
    for oeuvre_id in idOeuvresAProposerFinal:
        image_url = get_image_url_for_oeuvre(oeuvre_id) 
        oeuvres_avec_images.append({"id": oeuvre_id, "image_url": image_url})

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
            session['user_id'] = user["IdAr"] if user_role == "artiste" else user["IdAm"]
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

    user = next((u for u in artists if u.get('IdAr') == user_id), None)
    if not user:
        user = next((u for u in amateurs if u.get('IdAm') == user_id), None)

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

            remote_file_name = f"{user['IdAr'] if 'IdAr' in user else user['IdAm']}.jpg"
            remote_file_path = f"/root/cdn/static/pp/{remote_file_name}"

            upload_file_sftp(local_file_path, remote_file_path)

            user["profile_picture"] = f"https://cdn.we-art.art/static/pp/{remote_file_name}"

        if 'IdAr' in user:
            artists = [u if u["IdAr"] != user["IdAr"] else user for u in artists]
            with open('artiste.json', 'w') as f:
                json.dump(artists, f, indent=2)
        elif 'IdAm' in user:
            amateurs = [u if u["IdAm"] != user["IdAm"] else user for u in amateurs]
            with open('amateur.json', 'w') as f:
                json.dump(amateurs, f, indent=2)

        flash("Profil mis à jour avec succès.", "success")

        return redirect(url_for('upload'))

    return render_template("settings.html", user=user, user_role=session.get('user_role'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    user_id = session.get('user_id')  
    
    if not user_id:
        return "Vous devez être connecté pour télécharger un fichier.", 403  

    with open('artiste.json', 'r') as f:
        artists = json.load(f)

    user = next((u for u in artists if u.get('IdAm') == user_id or u.get('IdAr') == user_id), None)
    
    if not user:
        return "Accès non autorisé", 403  

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Pas de fichier', 400
        file = request.files['file']
        if file.filename == '':
            return 'Pas de fichier sélectionné', 400

        temp_dir = "./uploads"
        os.makedirs(temp_dir, exist_ok=True)
        local_file_path = os.path.join(temp_dir, file.filename)
        file.save(local_file_path)

        today = date.today() 
        remote_dir = f"/root/{today.year}/{today.strftime('%m')}/{today.strftime('%d')}"
        remote_file_path = f"{remote_dir}/{file.filename}"

        stock_upload_file_sftp(local_file_path, remote_file_path)

        os.remove(local_file_path)

        titre = request.form.get('titre', '')
        description = request.form.get('description', '')

        id_oeuvre = generate_id()

        with open('oeuvres.json', 'r') as oeuvres_file:
            oeuvres = json.load(oeuvres_file)

        # Ajouter la nouvelle œuvre
        new_oeuvre = {
            "IdOeu": id_oeuvre,
            "path": remote_file_path,
            "IdAr": user_id if 'IdAr' in user else None, 
            "IdAm": user_id if 'IdAm' in user else None,
            "titre": titre,
            "description": description
        }
        oeuvres.append(new_oeuvre)

        # Sauvegarder les oeuvres mises à jour
        with open('oeuvres.json', 'w') as oeuvres_file:
            json.dump(oeuvres, oeuvres_file, indent=4)

        return f'Le fichier {file.filename} a bien été uploadé vers {remote_file_path}.'
    
    return '''
        <html>
            <body>
                <h1>Upload un fichier</h1>
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <label for="titre">Titre de l'œuvre:</label>
                    <input type="text" name="titre" required><br><br>
                    <label for="description">Description de l'œuvre:</label>
                    <input type="text" name="description"><br><br>
                    <input type="file" name="file" required>
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''

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