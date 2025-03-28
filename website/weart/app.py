# Création par Thibault BENOIT-GUIRY - Contribution Like : Clémence CHATEAU - Noé CALLEJON
from flask import Flask, request, redirect, url_for, render_template, session, flash, abort
from datetime import datetime, date 
from .algo import suggestion

import bcrypt
import json
import os
import random 
import paramiko

app = Flask(__name__)
app.secret_key = 'F0AO4Vgqg@g25#' # Signature du cookie pour notre infrastructure

MAINTENANCE_MODE = False  
"""
=================================================================
#                          CHECKPOINT                           #
=================================================================
* Déclaration des fonctions essentielles pour la suite des routes

"""
# DEFINITION DU VPS PRINCIPAL 
SFTP_HOST = '83.150.217.109'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'F0AO4Vgqg@g25#'

# DEFINITION DU VPS STOCKAGE
SFTP_HOST_STOCK = '93.127.158.145'
SFTP_PORT_STOCK = 22
SFTP_USER_STOCK = 'root'
SFTP_PASS_STOCK = 'HT3j02YGbL'

def get_json_file_path(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

# FONCTION DE GENERATION D'ID (Pour Oeuvre, User etc...)
def generate_id():
    return str(random.randint(10**17, 10**18 - 1))

# SYSTEME D'UPLOAD POUR LE VPS PRINCIPAL
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

# SYSTEME D'UPLOAD POUR LE VPS STOCKAGE
def stock_upload_file_sftp(local_file_path, remote_file_path):
    try:
        transport = paramiko.Transport((SFTP_HOST_STOCK, SFTP_PORT_STOCK))
        transport.connect(username=SFTP_USER_STOCK, password=SFTP_PASS_STOCK)
        sftp = paramiko.SFTPClient.from_transport(transport)

        directories = remote_file_path.rsplit('/', 1)[0]
        try:
            sftp.chdir("/")  
            for directory in directories.split("/"):
                if directory:
                    try:
                        sftp.chdir(directory)  
                    except IOError:
                        sftp.mkdir(directory)  
                        sftp.chdir(directory)
        except Exception as e:
            print(f"Erreur lors de la creation du dossier: {e}")

        # Upload du fichier
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
        print(f"Fichier bien envoyé vers : {remote_file_path}")
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier : {e}")

# Vérification du mot de passe avec bcrypt
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash)

# Deuxième fonction de génération d'ID mais avec verification dans les json en cas d'une éventuelle duplication d'Id
def generate_unique_id(file_name, user_type):
    existing_ids = set()
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
            for user in users:
                existing_ids.add(user.get(f"Id{user_type}", ""))
    
    while True:
        new_id = str(random.randint(10**17, 10**18 - 1))
        if new_id not in existing_ids:
            return new_id

""" 
Fonction pour sauvegarder les données lors de l'inscription en fonction du compte 
  Artiste => artiste.json
  Amateur => amateur.json
"""
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


""" Permet de chercher un utilisateur par son user_id dans deux fichiers JSON différents
  => Si c'est dans artiste.json : son identifiant sera sous la clé 'IdAr'
  => Si c'est dans amateur.json : son identifiant sera sous la clé 'IdAm'
"""
def get_user_from_json(user_id):
    file_path_artiste = get_json_file_path("artiste.json")
    file_path_amateurs = get_json_file_path("amateur.json")

    with open(file_path_artiste) as f:
        artists = json.load(f)
    with open(file_path_amateurs) as f:
        amateurs = json.load(f)
    
    user = next((u for u in artists if u.get("IdAr") == user_id), None) or \
           next((u for u in amateurs if u.get("IdAm") == user_id), None)
    
    return user


# Fonction qui permet de vérifier si le mot de passe transmis par l'utilisateur correspond au mot de passe crypter qu'on a dans les JSON respectives. 
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash.encode())

# Fonction qui oblige la connexion à toute utilisateurs. 
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Fonction qui oblige en cas de mode maintenance activer (cf => variable l.15)
def maintenance_required(f):
    def wrapper(*args, **kwargs):
        if MAINTENANCE_MODE:
            return render_template('maintenance.html')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

"""
=================================================================
#                          CHECKPOINT                           #
=================================================================
* Déclaration des routes les plus complexes

"""

# Fonction de la route principale de l'application '/', avec protection du mode maintenance + obligation d'être connecté sinon redirigé sur les pages de connexion.
@app.route('/', methods=['GET', 'POST'])
@login_required
@maintenance_required
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))
    
    user_id = session.get('user_id')
    idAmateurMain = int(user_id)
    
    print(f" user_id récupéré : {user_id} (Type : {type(user_id)})")
    
    try:
        # Appel à la fonction suggestion pour obtenir la liste des ID d'œuvres suggérées
        oeuvre_ids = suggestion(idAmateurMain)
        print(f" ID des œuvres suggérées : {oeuvre_ids}")
        
        file_path_oeuvres = get_json_file_path("oeuvres.json")
        with open(file_path_oeuvres) as file:
            oeuvres = json.load(file)
        
        suggestions = [oeuvre for oeuvre in oeuvres if str(oeuvre['IdOeu']) in map(str, oeuvre_ids)]
        
        if not suggestions:
            print("Aucune œuvre suggérée. On prend une œuvre aléatoire parmi toutes les œuvres.")
            current_suggestion = random.choice(oeuvres)  #
            next_index = 3  
        else:
            current_index = int(request.args.get('index', 0))

            if current_index + 1 >= len(suggestions):
                print("Fin de la liste des suggestions. On prend une œuvre aléatoire.")
                current_suggestion = random.choice(oeuvres)
                next_index = 3  
            else:
                current_suggestion = suggestions[current_index]
                next_index = current_index + 1

        current_suggestion['path'] = current_suggestion['path'].replace('/root/', '')

        if suggestions:
            for oeuvre in suggestions:
                oeuvre['path'] = oeuvre['path'].replace('/root/', '')

        has_next = next_index < len(suggestions) if next_index != -1 else False

    except Exception as e:
        print(f"ERREUR lors de l'appel à suggestion(): {e}")
        current_suggestion = None
        has_next = False
        next_index = -1

    return render_template("index.html", 
                        username=session['username'], 
                        user_role=session.get('user_role'), 
                        user_id=user_id,
                        current_suggestion=current_suggestion,
                        has_next=has_next,
                        next_index=next_index)


# Fonction de la route principale de l'application '/', avec protection du mode maintenance + obligation d'être connecté sinon redirigé sur les pages de connexion.
@app.route("/signin", methods=["GET", "POST"])
@maintenance_required
def signin():
    username = None 
    password = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    file_path_artiste = get_json_file_path("artiste.json")
    file_path_amateurs = get_json_file_path("amateur.json")

    with open(file_path_artiste) as f:
        artists = json.load(f)
    with open(file_path_amateurs) as f:
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


""""
Fonction de la route d'insciption, on récupère les données écrite. Le mode maintenance rend la page inacessible 
On fait une vérification en 3 étapes : 

 => L'utilisateur a t-il plus de 15 ans ? (cf => vie-publique.fr - Site du gouvernement - https://urlr.me/bdWnzg.)"
 => Le pseudonyme est-il déjà utiliser ? Pour éviter toute confussion et de faux compte.
 => L'adresse email est-il déjà utiliser ? Pour éviter les doubles comptes, du moins un peu lutter...

 Si tout est valide : on le sauvegarde dans le JSON respective, et on le retourne dans la page de connexion (signin)
 Si y a un soucis : on lui renvoie sur la page d'inscription avec le message d'erreur que flask nous envoie.
"""
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
            flash("L'âge légal pour s'inscrire en France est de 15 ans.", "error")
            return render_template("signup.html")

        file_path_artiste = get_json_file_path("artiste.json")
        file_path_amateurs = get_json_file_path("amateur.json")

        with open(file_path_artiste) as f:
            artists = json.load(f)
        with open(file_path_amateurs) as f:
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

""""
Fonction de la route settings, pour modifier son compte :
=> Son pseudonyme 
=> Sa biographie, par défault marqué "None".

Le mode maintenance rend la page inacessible.
"""
@app.route("/settings", methods=["GET", "POST"])
@maintenance_required
@login_required
def settings():
    user_id = session.get('user_id')  

    file_path_artiste = get_json_file_path("artiste.json")
    file_path_amateurs = get_json_file_path("amateur.json")

    with open(file_path_artiste) as f:
        artists = json.load(f)
    with open(file_path_amateurs) as f:
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
            file_path_artiste = get_json_file_path("artiste.json")

            with open(file_path_artiste) as f:
                json.dump(artists, f, indent=2)
        elif 'IdAm' in user:
            amateurs = [u if u["IdAm"] != user["IdAm"] else user for u in amateurs]
            file_path_amateur = get_json_file_path("amateur.json")
            with open(file_path_amateur) as f:
                json.dump(amateurs, f, indent=2)

        flash("Profil mis à jour avec succès.", "success")

        return redirect(url_for('index'))

    return render_template("settings.html", user=user, user_role=session.get('user_role'))

""""
Fonction de la route upload, pour publier une oeuvre sous l'identité de l'Artiste :
=> L'accès est restreint que pour les comptes Artistes.

L'image est envoyé directement sur le VPS stockage dans l'ordre suivant :
* L'année (Ex : 2025)
* Le mois (Ex : 07 => Juillet)
* Le jour (Ex : 22)
=> Soit le 22 Juillet 2025 (2025/07/22/image_upload.jpg)

Le mode maintenance rend la page inacessible.
"""
@app.route('/upload', methods=['GET', 'POST'])
@login_required
@maintenance_required
def upload_file():
    user_id = session.get('user_id')  
    file_path_artiste = get_json_file_path("artiste.json")

    with open(file_path_artiste) as f:
        artists = json.load(f)

    user = next((u for u in artists if u.get('IdAm') == user_id or u.get('IdAr') == user_id), None)
    
    if not user:
        abort(403)  

    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            abort(400)

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

        new_oeuvre = {
            "IdOeu": id_oeuvre,
            "path": remote_file_path,
            "IdAr": user_id if 'IdAr' in user else None, 
            "titre": titre,
            "description": description
        }
        oeuvres.append(new_oeuvre)

        with open('oeuvres.json', 'w') as oeuvres_file:
            json.dump(oeuvres, oeuvres_file, indent=4)

        return redirect(url_for('upload_success', filename=file.filename, path=remote_file_path))

    return render_template('upload.html')

# Route basique pour confirmer l'upload d'une oeuvre. Connexion obligatoire + Le mode maintenance rend la page inacessible.
@app.route('/upload_success')
@maintenance_required
@login_required
def upload_success():
    user_id = session.get('user_id')  
    file_path_artiste = get_json_file_path("artiste.json")

    with open(file_path_artiste) as f:
        artists = json.load(f)

    user = next((u for u in artists if u.get('IdAm') == user_id or u.get('IdAr') == user_id), None)
    
    if not user:
        abort(403)  

    filename = request.args.get('filename')
    path = request.args.get('path')
    return render_template('upload_success.html', filename=filename, path=path)


"""
Route de l'affichage du compte suivi de l'IdAr/Am :
=> Si le compte n'existe pas (IdAr ou IdAm introuvable) : on lui envoi un erreur 404

Sinon, on lui affiche son compte suivi des informations suivant :
* Son pseudonyme
* Sa biographie
* Sa photo de profil (hébergé en static sur le VPS principal)
* Les badges (Pour des idées futurs : si une personne gagne à un évenement, il peut gagner un badge pour avoir un côté esthétique trop CoOl,
 ou afficher les membres du projet)

Le mode maintenance rend la page inacessible.
"""
@app.route("/account/<user_id>")
@login_required  
@maintenance_required
def account(user_id):
    with open('badge.json', 'r') as file:
        badges = json.load(file)
    
    user = get_user_from_json(user_id)  
    user_id = session.get('user_id')  

    if not user:
        abort(404)
        return redirect(url_for('index'))

    user_badges = [badges[badge_id] for badge_id in user.get('badges', [])] 

    if 'username' not in session:
        return redirect(url_for('signin'))

    return render_template("account.html", username=session['username'], user_role=session.get('user_role'), user=user, badges=user_badges, user_id=user_id, )

"""
=================================================================
#                          CHECKPOINT                           #
=================================================================
* Passage sur les routes plus simple, avec des fonctions rapide
"""

# Route simple : si l'utilisateur va dessus, notre application déconnecte le compte de la personne et le renvoi sur la page de connexion.
@app.route("/logout")
@maintenance_required
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('signin'))


# Route pour la page de maintenance en cas de maintenance (cf => variable l.15)
@app.route("/maintenance")
def maintenance():
    return render_template("maintenance.html")

# Route pour les conditions d'utilisation universel 
@app.route("/terms_of_service")
def terms_of_service():
    return render_template("terms_of_service.html")

# Route pour les politique de confidentialité  
@app.route("/privacy_policy")
def privacy_policy(): 
    return render_template("privacy_policy.html")

# Toute les erreurs prisent en charge 
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