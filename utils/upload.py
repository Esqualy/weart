from flask import Flask, request, render_template_string
import paramiko
import os

app = Flask(__name__)

# Configuration pour SFTP
SFTP_HOST = '93.127.158.145'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'HT3j02YGbL'

# Fonction pour uploader le fichier via SFTP
def upload_file_sftp(local_file_path, remote_file_path):
    try:
        # Créer une connexion SSH
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)

        # Créer une session SFTP
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload du fichier
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
        print(f"File successfully uploaded to {remote_file_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Route d'upload de fichier
@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body>
                <h1>Upload a file</h1>
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
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Sauvegarde temporaire du fichier localement
    temp_dir = "./uploads"  
    os.makedirs(temp_dir, exist_ok=True)  # Créer le répertoire si nécessaire
    local_file_path = os.path.join(temp_dir, file.filename)
    file.save(local_file_path)

    remote_file_path = f"/root/{file.filename}" #/root pour debian

    upload_file_sftp(local_file_path, remote_file_path)

    os.remove(local_file_path)

    return f'File {file.filename} successfully uploaded to SFTP server.'

if __name__ == '__main__':
    app.run(debug=True)
