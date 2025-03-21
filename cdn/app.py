from flask import Flask, jsonify, Response, render_template
import paramiko
import mimetypes

app = Flask(__name__, template_folder="templates", static_folder="static")  

SFTP_HOST = '93.127.158.145'
SFTP_PORT = 22
SFTP_USER = 'root'
SFTP_PASS = 'HT3j02YGbL'

BASE_DIRECTORY = "/root"  

def list_files_sftp(directory):
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        file_list = sftp.listdir(directory)
        sftp.close()
        transport.close()
        return file_list
    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des fichiers : {e}")
        return []

@app.route('/ressources/', defaults={'filename': ''})
@app.route('/ressources/<path:filename>')
def serve_files(filename):
    remote_path = f"{BASE_DIRECTORY}/{filename}".rstrip('/')

    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        try:
            stat = sftp.stat(remote_path)
            
            if stat.st_mode & 0o40000:  # Dossier
                file_list = sftp.listdir(remote_path)
                sftp.close()
                transport.close()
                return jsonify(file_list)
            else:
                mime_type, _ = mimetypes.guess_type(remote_path)
                if not mime_type:
                    mime_type = "application/octet-stream" 

                file_obj = sftp.file(remote_path, 'rb')
                file_data = file_obj.read()
                file_obj.close()
                sftp.close()
                transport.close()
                
                return Response(file_data, content_type=mime_type)
        
        except FileNotFoundError:
            sftp.close()
            transport.close()
            return render_template('404.html'), 404  

    except Exception as e:
        return f"Erreur d'accès au serveur SFTP : {e}", 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  

if __name__ == '__main__':
    app.run(debug=True)
