## Thibault Benoit
from flask import Flask, request
import bcrypt
import logging

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Hachage sécurisé avec bcrypt
password_plaintext = "motdepasse123".encode()
password_hashed = bcrypt.hashpw(password_plaintext, bcrypt.gensalt())  # Génère un hash sécurisé

USER_DATA = {
    "username": "jujudu34",
    "password_hash": password_hashed  # Stockage sécurisé du hash
}

logging.debug(f"Mot de passe bcrypt hashé stocké: {USER_DATA['password_hash']}")

def verify_password(input_password, stored_hash):
    """Vérifie si le mot de passe entré correspond au hash stocké avec bcrypt."""
    return bcrypt.checkpw(input_password.encode(), stored_hash)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        logging.debug(f"Tentative de connexion avec l'utilisateur: {username}")
        
        # Vérifier les identifiants
        if username == USER_DATA["username"] and verify_password(password, USER_DATA["password_hash"]):
            logging.info("Connexion réussie.")
            return "✅ Connexion réussie ! Bienvenue " + username
        else:
            logging.warning("Échec de la connexion : identifiants incorrects.")
            return "❌ Mot de passe ou nom d'utilisateur incorrect."

    return '''
        <form method="post">
            Nom d'utilisateur : <input type="text" name="username"><br>
            Mot de passe : <input type="password" name="password"><br>
            <input type="submit" value="Se connecter">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
