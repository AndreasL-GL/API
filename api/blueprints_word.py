from flask import Blueprint, request, send_file,jsonify, abort
from functions.authentication import require_api_key
from functions.Word import Protokollutskick
from functions.Word.Lekplatsprotokoll import lekplatsprotokoll
from Json2Word.compose import compose_doc
from functions.Word.json2word import create_word_document
#from functions.api_authentication import download_pdf
import io,base64
import docx

word_path = Blueprint('skapa word-protokoll', __name__)

# @word_path.route("/api/file_to_pdf", methods=["POST"])
# @require_api_key
# def file_to_pdf():
#     if not request.is_json:
#         js = {
#             "Sitename":"Digitaliseringsportal",
#             "Filepath":'/Prislistor Excel/Terås  Årsavtal år 2022.xlsx', 
#             "Library":"Fakturaanalys"
#         }
#         abort(500,jsonify({"error":"Missing json content in body"}))
#     else:
#         return download_pdf(**request.get_json())

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

@word_path.route("/api/word/compose_document_v2", methods=["POST"])
@require_api_key
def compose_v2():
    js = request.get_json()
    bio = create_word_document(js)
    return jsonify({"$content":base64.b64encode(bio.getvalue()).decode('utf-8'), "$Content-Type":""})

@word_path.route("/api/word/json2word", methods=["POST"])
@require_api_key
def json2word():
    js = request.get_json()
    bytesio = compose_document(js)
    return jsonify({"$content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document","$content":base64.b64encode(bytesio.getvalue()).decode('utf-8')})

@word_path.route("/api/word/json2wordv2", methods=["POST"])
@require_api_key
def json2wordv2():
    js = request.get_json()
    bytesio = create_word_document(js)
    return jsonify({"$content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document","$content":base64.b64encode(bytesio.getvalue()).decode('utf-8')})

@word_path.route('/api/word/merge_document',methods=['POST'])
@require_api_key
def mergefields():
    js = request.get_json()
    
    if "Json2Word" in js.keys() and "Document" in js.keys() and "Items" in js.keys():
        item = io.BytesIO(base64.b64decode(Protokollutskick.mailmerge_fun(js["Document"]['$content'],js["Items"])['$content']))
        item.seek(0)
        item = create_word_document(js['Json2Word'],item)
        return jsonify(item)

    elif "Json2Word" in js.keys() and "Document" not in js.keys():
        item = create_word_document(js['Json2Word'],item)
        return jsonify(item)
    
    elif "Document" in js.keys() and "Items" in js.keys() and "Json2Word" not in js.keys():
        return jsonify(Protokollutskick.mailmerge_fun(js["Document"]['$content'],js["Items"]["value"]))
    else: return {"Error":"Incorrect format"}
    


def compose_document(js):
    doc = compose_doc(js)
    bio = io.BytesIO()
    doc.save(bio)
    del doc, js
    bio.seek(0)
    return bio

if __name__ == '__main__':
    import os, json
    with open(os.path.join(os.path.dirname(__file__),'merge.json'), 'r') as f:
        js = json.load(f)['body']
    js = js
    #print(js['body'].keys())
    print("Json2Word" in js.keys() and "Document" in js.keys() and "Items" in js.keys())
    [print("Json2Word" in js.keys()), print("Document" in js.keys()),print("Items" in js.keys())]
    if "Json2Word" in js.keys() and "Document" in js.keys() and "Items" in js.keys():
        print("Hello")
        item = io.BytesIO(base64.b64decode(Protokollutskick.mailmerge_fun(js["Document"]['$content'],js["Items"])['$content']))
        item.seek(0)
        item = create_word_document(js['Json2Word'],item)
        print(item.keys())