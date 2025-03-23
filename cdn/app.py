from flask import Flask, jsonify, Response, request, render_template
import paramiko
import mimetypes

app = Flask(__name__)

API_KEY = "F0AO4Vgqg@g25#"

# 🎯 Connexion SFTP
SFTP_HOST = '93.127.158.145'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'HT3j02YGbL'
BASE_DIRECTORY = "/root"

def get_sftp_client():
    """Crée et retourne une connexion SFTP"""
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    return paramiko.SFTPClient.from_transport(transport)

@app.route("/ressources/<path:filename>")
def serve_files(filename):
    """Permet d'accéder à des fichiers via SFTP"""

    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):  
        return serve_public_files(filename)

    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        return render_template('forbidden.html'), 403  

    return serve_private_files(filename)

def serve_public_files(filename):
    """Permet d'envoyer les fichiers publics sans vérifier la clé API"""
    remote_path = f"{BASE_DIRECTORY}/{filename}".rstrip('/')

    try:
        sftp = get_sftp_client()

        try:
            stat = sftp.stat(remote_path)

            # 🖼️ Si c'est un fichier → Envoie le fichier
            mime_type, _ = mimetypes.guess_type(remote_path)
            mime_type = mime_type if mime_type else "application/octet-stream"

            with sftp.file(remote_path, 'rb') as file_obj:
                file_data = file_obj.read()

            sftp.close()
            return Response(file_data, content_type=mime_type)

        except FileNotFoundError:
            sftp.close()
            return render_template('not_found.html'), 404

    except Exception as e:
        return render_template('internal_server_error.html', error=str(e)), 500


def serve_private_files(filename):
    """Permet d'envoyer les fichiers privés avec vérification de clé API"""
    remote_path = f"{BASE_DIRECTORY}/{filename}".rstrip('/')

    try:
        sftp = get_sftp_client()

        try:
            stat = sftp.stat(remote_path)

            # 🖼️ Si c'est un fichier → Envoie le fichier
            mime_type, _ = mimetypes.guess_type(remote_path)
            mime_type = mime_type if mime_type else "application/octet-stream"

            with sftp.file(remote_path, 'rb') as file_obj:
                file_data = file_obj.read()

            sftp.close()
            return Response(file_data, content_type=mime_type)

        except FileNotFoundError:
            sftp.close()
            return render_template('not_found.html'), 404

    except Exception as e:
        return render_template('internal_server_error.html', error=str(e)), 500

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
