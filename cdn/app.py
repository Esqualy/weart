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
            return render_template('not_found.html'), 404  

    except Exception as e:
        return render_template('internal_server_error.html', error=str(e)), 500  

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
    app.run(debug=True)
