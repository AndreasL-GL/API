from flask import Blueprint, request, send_file,jsonify, abort
from functions.authentication import require_api_key
from functions.Word import Protokollutskick
from functions.Word.Lekplatsprotokoll import lekplatsprotokoll
from Json2Word.compose import compose_doc
import io,base64
import docx
html_pages = Blueprint('html pages', __name__)


@html_pages.route("/api/word_dokument_for_protokoll", methods=["POST"])
def accept_protokoll(): 
    json_content = request.get_json()
    json_content = Protokollutskick.run_functions(json_content)
    return jsonify(json_content)


@html_pages.route('/ip')
def get_external_ip():
    remote_addr = requests.get('https://ifconfig.me/ip').content.decode('utf-8')
    return f'The external IP address is: {remote_addr}'