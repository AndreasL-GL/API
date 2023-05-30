from flask import Blueprint, request, send_file,jsonify, abort
from functions.authentication import require_api_key
from functions.Word import Protokollutskick
from functions.Word.Lekplatsprotokoll import lekplatsprotokoll
from Json2Word.compose import compose_doc
import io,base64
import docx

word_path = Blueprint('skapa word-protokoll', __name__)


@word_path.route("/api/word_dokument_for_protokoll", methods=["POST"])
@require_api_key
def accept_protokoll(): #WORKING
    json_content = request.get_json()
    json_content = Protokollutskick.run_functions(json_content)
    return jsonify(json_content)

@word_path.route("/api/word/Lekplatsbesiktning_protokoll", methods=["POST"])
@require_api_key
def protokoll(): 
    json_content = request.get_json()
    json_content = lekplatsprotokoll.run_functions(json_content)
    return jsonify(json_content)

@word_path.route("/api/word/compose_document", methods=["POST"])
@require_api_key
def compose():
    js = request.get_json()
    bio = compose_document(js)
    return jsonify({"content":base64.b64encode(bio.getvalue()).decode('utf-8')})

def compose_document(js):
    doc = compose_doc(js)
    bio = io.BytesIO()
    doc.save(bio)
    del doc, js
    bio.seek(0)
    return bio
if __name__ == '__main__':
    "Hello"