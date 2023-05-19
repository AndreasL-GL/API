import requests
import configparser
import json, os
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),"config.ini"))


def get_sharepoint_access_headers_through_client_id():
    client_id = config["SHAREPOINT"]["client_id"].strip()
    client_secret = config["SHAREPOINT"]["client_secret"].strip()
    tenant_id = config["SHAREPOINT"]["tenant_id"].strip()
    tenant = config["SHAREPOINT"]["tenant"]
    client_id = client_id + '@'+tenant_id
    
    data = {
    'grant_type':'client_credentials',
    'resource': "00000003-0000-0ff1-ce00-000000000000/" + tenant + ".sharepoint.com@" + tenant_id, 
    'client_id': client_id,
    'client_secret': client_secret
}
    url = "https://accounts.accesscontrol.windows.net/tenant_id/tokens/OAuth/2"
    headers = {
    'Content-Type':'application/x-www-form-urlencoded'
}

    url = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"
    r = requests.post(url, data=data, headers=headers)
    json_data = json.loads(r.text)
    headers = {
    'Authorization': "Bearer " + json_data['access_token'],
    'Accept':'application/json;odata=verbose',
    'Content-Type': 'application/json;odata=verbose'
}
    return headers

def download_excel_file(site,filename):
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"

    server_relative_url = f"/sites/{site}/Delade Dokument/Sammanställningar/{filename}"
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/GetFileByServerRelativeUrl('{server_relative_url}')/$value"
    l = requests.get(url, headers=headers)
    return l