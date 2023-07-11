from flask import Blueprint, render_template, request,make_response, jsonify
from functions.Sharepoint.sharepoint_list_operations import copy_list_and_all_items, get_fieldtypes, request_fields
from functions.Sharepoint.get_sharepoint_columns import get_sharepoint_access_headers_through_client_id, get_fields_v2
from functions.authentication import require_api_key
from functions.Sharepoint.Sharepoint_Site import filter_sites


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
        headers=get_sharepoint_access_headers_through_client_id()
        rs = request_fields(site,list_name,get_fields=False,field=field,headers=headers)
        response = make_response("Success")
        response.status_code = rs.status_code
    except Exception as e:
        response = make_response(str(e))
        response.status_code = 500
    return response

@sharepoint.route("/api/sharepoint/get_sites", methods=["POST"])
@require_api_key
def get_sites():
    return jsonify(filter_sites(request.get_json()))


@sharepoint.route("/api/sharepoint/get_fields_v2", methods=["POST"])
@require_api_key
def get_fields_v22():
    js = request.get_json()
    site = js["Site"]
    list_name = js["List"]
    ID = js["ID"]
    
    return get_fields_v2(site,list_name,ID)