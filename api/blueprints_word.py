from flask import Blueprint, render_template, request, send_file,jsonify, abort
from functions.authentication import require_api_key
from functions.Word import Protokollutskick
from functions.Word.Lekplatsprotokoll import lekplatsprotokoll
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
    print(json_content.keys())
    json_content = lekplatsprotokoll.run_functions(json_content)
    return jsonify(json_content)