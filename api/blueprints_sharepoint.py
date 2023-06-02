from flask import Blueprint, render_template, request,make_response, jsonify
from functions.Sharepoint.sharepoint_list_operations import copy_list_and_all_items, get_fieldtypes, add_field
from functions.authentication import require_api_key


sharepoint = Blueprint('sharepoint', __name__)


@sharepoint.route("/api/sharepoint/copy_list_and_all_items", methods=["POST"])
@require_api_key
def copy_list():
    js = request.get_json()
    rs = copy_list_and_all_items(
        source_site=js['Source Site'],
        source_list=js["Source List"],
        destination_site=js["Destination Site"],
        destination_list=js["Destination List"]
    )
    if rs==201:
        response = make_response("List created and items copied!")
        response.status_code=201
    else:
        response = make_response("Failed to create list or copy items.")
        response.status_code=500
    return response

@sharepoint.route("/api/sharepoint/FieldTypes", methods=["GET"])
@require_api_key
def fieldtype():
    site = request.args.get('site')
    return jsonify(get_fieldtypes(site))

@sharepoint.route("/api/sharepoint/AddField", methods=["POST"])
@require_api_key
def add_sp_field():
    js = request.get_json()
    site = js["Site Url"]
    list_name = js["List"]
    field = js["Field"]
    
    try: 
        rs = add_field(site,list_name,field)
        response = make_response("Success")
        response.status_code = rs.status_code
    except Exception as e:
        response = make_response(str(e)) 
        response.status_code = 500
    return response