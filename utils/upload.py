## Thibault Benoit
from flask import Flask, request, render_template_string
import paramiko
import os
import datetime

app = Flask(__name__)

# Configuration pour SFTP
SFTP_HOST = '93.127.158.145'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'HT3j02YGbL'

def upload_file_sftp(local_file_path, remote_file_path):
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
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

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body>
                <h1>Upload un fichier</h1>
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Pas de fichier', 400
    file = request.files['file']
    if file.filename == '':
        return 'Pas de fichier sélectionné', 400

    # Sauvegarde temporaire du fichier localement
    temp_dir = "./uploads"
    os.makedirs(temp_dir, exist_ok=True)
    local_file_path = os.path.join(temp_dir, file.filename)
    file.save(local_file_path)

    # Générer le chemin distant basé sur la date actuelle
    today = datetime.date.today()
    remote_dir = f"/root/{today.year}/{today.strftime('%m')}/{today.strftime('%d')}"
    remote_file_path = f"{remote_dir}/{file.filename}"

    # Upload du fichier sur le serveur SFTP
    upload_file_sftp(local_file_path, remote_file_path)

    # Supprimer le fichier local après l'upload
    os.remove(local_file_path)

    return f'Le fichier {file.filename} a bien été upload vers {remote_file_path}.'

if __name__ == '__main__':
    app.run(debug=True)
