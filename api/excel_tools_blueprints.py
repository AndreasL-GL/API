from flask import Blueprint, render_template, request, send_file,jsonify, abort
from functions.authentication import require_api_key
from functions.Excel.Get_Excel_data_to_json import  convert_file_to_workbook
from functions.Excel.Invoice import faktura_mot_prislista, fuzzy_merge, set_main_columns
from functions.Json_records.json_functions import convert_excel_table_to_json, join_json_records, fakturaanalys_v2
from functions.return_power_automate_file import detect_and_create_file
# from functions.Excel.Fakturaanalys import set_main_columns
import os,io,base64, openpyxl
from functions.Excel.Fakturaanalys import process_request
import logging
excel_dagbok = Blueprint('dagbok_trädexperterna', __name__)
fakturaextraktion = Blueprint('fakturaextraktion', __name__)

info_logger = logging.getLogger('info_logger')

@excel_dagbok.route("/api/excel_dagbok", methods=["POST"])
@require_api_key
def upload(): 
    
    file_data = request.files
    file_data = request.get_data()
    file_name = os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), 'functions'),'Excel'),'temp'),'received_file.xlsx')
    while os.path.exists(file_name):
        file_name = file_name.split('.')[0] + '1' + '.xlsx'
    with open(file_name, 'wb') as f:
        f.write(file_data)
    file = io.BytesIO(file_data)
    
    filebytes = io.BytesIO()
    filebytes.write(file.getvalue())
    filebytes.seek(0)
    excel_file,filename=convert_file_to_workbook(filebytes)
    file_content_base64 = base64.b64encode(excel_file.read()).decode('utf-8')
    return jsonify({"content":file_content_base64,"filename":filename})

@fakturaextraktion.route("/api/fakturaanalys_fix_columns", methods=['POST'])
@require_api_key
def column():
    js = request.json
    excel = set_main_columns(js["excel"])
    
    return jsonify({"excel": excel})

@fakturaextraktion.route("/api/fakturaanalys", methods=["POST"])
@require_api_key
def upload(): 
    data = request.json
    return jsonify(process_request(data))

@fakturaextraktion.route("/api/Excel/Excel2Json", methods=["GET","POST"])
@require_api_key
def excel2json(): 
    """Converts a Excel base64 item from request to json format, using $content to work with power automate.

    Returns:
        dict: Json records of the table content of the excel file.
    """
    return convert_excel_table_to_json(request.get_json())


@fakturaextraktion.route("/api/Excel/join_json")
@require_api_key
def join_json():
    """Joins 2 json records together on one or more columns with a defined method.
    {'json1':[{}],'json2':[{}],'left_on':'pris', 'right_on':'pris', 'how'='inner'}
    """
    data = request.json
    js = join_json_records(**data)
    return jsonify(js)
    
    
def upload():
    # Get the file from the request
    file = request.files['file']
    wb = openpyxl.load_workbook(file)
    wb.save(os.path.join(os.path.dirname(__file__),'temp.xlsx'))
    # Do whatever you need to do with the file here
    # ...

    return jsonify({"content": "Hello"}) 
  
  
  
  
@excel_dagbok.route("/api/excel_dagbok_base64", methods=["POST"])
@require_api_key
def get_excel_file(): #WORKING
    file_content = request.json.get('content')
    file_content=base64.b64decode(file_content)
    if b'PNG' in file_content[8:]: abort(400, "File is an image")
    file_content=io.BytesIO(file_content)
    excel_file,filename=convert_file_to_workbook(file_content)
    file_content_base64 = base64.b64encode(excel_file.read()).decode('utf-8')
    return jsonify({"content":file_content_base64,"filename":filename})

@fakturaextraktion.route("/api/excel/faktura_mot_excel", methods=["POST"])
@require_api_key
def faktura_mot_excel(): 
    data = request.json
    
    rs =faktura_mot_prislista(data, request.args.get('join'))
    return jsonify(rs)


@fakturaextraktion.route("/api/excel/fuzzy_merge", methods=["POST"])
@require_api_key
def fuzzy_merge(): 
    data = request.json
    
    rs = fuzzy_merge(data['Left'],data['Right'],data['Right_Column'],data['Left_Column'])
    return jsonify(rs)

@fakturaextraktion.route("/api/Fakturaanalys/Analysera_faktura_mot_prislistor", methods=["POST"])
#@require_api_key
def fakturaanalys_v2_route():
    js = request.get_json()
    print(js.keys())
    if 'body' in js.keys(): js = js['body']
    print(js.keys())
    file = detect_and_create_file(fakturaanalys_v2(js),content_type=".xlsx")
    
    return file

def upload():
    # Get the file from the request

    file = request.files['file']
    wb = openpyxl.load_workbook(file)
    wb.save(os.path.join(os.path.dirname(__file__),'temp.xlsx'))
    # Do whatever you need to do with the file here
    # ...

    return jsonify({"content": "Hello"}) 

