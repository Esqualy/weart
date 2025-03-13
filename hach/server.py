from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__)

USER_DATA = {
    "username": "jujudu34",
    "password_hash": hashlib.sha256("motdepasse123".encode()).hexdigest()  
}

def verify_password(input_password, stored_hash):
    return hashlib.sha256(input_password.encode()).hexdigest() == stored_hash

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USER_DATA["username"] and verify_password(password, USER_DATA["password_hash"]):
            return "✅ Connexion réussie ! Bienvenue " + username
        else:
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
