
from flask import Blueprint, render_template, request
from functions.Sharepoint.get_sharepoint_columns import get_body_from_sharepoint_api, get_fields
from functions.authentication import require_api_key


flow_starting_page = Blueprint('flow_starting_page', __name__)
get_sharepoint_columns_ = Blueprint('get_sharepoint_columns_', __name__)
get_kontrollmoment = Blueprint('get_kontrollmoment',__name__)


@flow_starting_page.route("/api/flows")
def flows_starting_page():
    return render_template("flows_starting_template.html")


@get_sharepoint_columns_.route("/api/flows/get_sharepoint_columns", methods=['POST'])
@require_api_key
def get_sharepoint_columns():
    js = request.json

    result = get_body_from_sharepoint_api(js)
    return result

@get_kontrollmoment.route("/api/flows/get_sharepoint_columns_v2", methods=['GET'])
@require_api_key
def get_kontrollmoment_():
    list_ = request.args.get("list")
    site = request.args.get("site")
    
    result = get_fields(site,list_)
    return result