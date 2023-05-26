from flask import Blueprint, request, send_file,jsonify, abort
from functions.authentication import require_api_key
from Json2Word.compose import compose_doc
from functions.SQL_commands import Sql
import io,base64
import requests
import docx
html_pages = Blueprint('html pages', __name__)


@html_pages.route("/api/Json2Word", methods=["GET"])
def word_preview():
    # I want to check if a route is in my routes and if it is i assign an extra random letter to it
    # I may want to have an internal storage of all my json files that gets discarded after some time.
    # Maybe just store it in a database file?
    file_id = request.args.get('file')
    js = {}
    file = run(js)
    
    return send_file(file)


@html_pages.route('/ip')
def get_external_ip():
    remote_addr = requests.get('https://ifconfig.me/ip').content.decode('utf-8')
    return f'The external IP address is: {remote_addr}'
def run(js):
    doc = compose_doc(js)
    file = io.BytesIO()
    doc.save(file)
    file.seek(0)
    return file