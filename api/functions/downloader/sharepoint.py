import requests
import configparser
import json, os
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),"config.ini"))

with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),'sharepoint_egenkontroller_remove_list.txt')) as f:
    sharepoint_columns_remove_list = [x.replace('\n','') for x in f.readlines() if x != '\n']

def get_sharepoint_access_headers_through_client_id():
    """Grants access to a sharepoint site for the client by getting the authentication headers necessary.
    Returns a dictionary to be used in requests as argument: headers=get_sharepoint_access_headers_through_client_id()
    """
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

def Download_icon(site="GLMalmAB-EgenkontrollerVellingebostder",filename="MKB_big.png"):
    """Downloads an icon to be added into the word-file template

    Args:
        site (str, optional): The sharepoint site where the icon is located. Defaults to "GLMalmAB-EgenkontrollerVellingebostder".
        filename (str, optional): the filename of the icon. Defaults to "MKB_big.png".

    Returns:
        _type_: Response-object.
    """
    
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    site = "GLMalmAB-EgenkontrollerVellingebostder"
    server_relative_url = f"/sites/{site}/Delade Dokument/Protokoll/Template/{filename}"
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/GetFileByServerRelativeUrl('{server_relative_url}')/$value"
    l = requests.get(url, headers=headers)
    return l

def Download_template(site,filename):
    """Used to download a word-template.

    Args:
        site (string): The sharepoint site to download the template file from.
        filename (string): Name of the template file.

    Returns:
        _type_: Response-object.
    """
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    site = "GLMalmAB-EgenkontrollerVellingebostder"
    server_relative_url = f"/sites/{site}/Delade Dokument/Protokoll/Template/{filename}"
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/GetFileByServerRelativeUrl('{server_relative_url}')/$value"
    l = requests.get(url, headers=headers)
    return l


def get_body_from_sharepoint_api(js):
    resultlist = []
    if 'body' in js.keys(): js = js['body']
    for item in js['d']['results']:
        if item['StaticName'] not in sharepoint_columns_remove_list:
            resultlist.append({"Moment":item['Title'], "link":item['StaticName']})
    return resultlist
def get_fields(site="", list_="MKB Egenkontroll Augustenborg Periodiska 2023"):
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    #site = site.split('sites/')[1]
    url = f"https://{tenant}.sharepoint.com/sites/GLMalmAB-EgenkontrollerVellingebostder/_api/web/lists/getbytitle('{list_}')/fields"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    return js

def get_item_based_on_id(id,site, list_):
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getbytitle('{list_}')/items?$filter=ID eq {id}"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    return js
def get_all_items(site, list_):
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getbytitle('{list_}')/items"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    return js

def get_by_url(url):
    headers = get_sharepoint_access_headers_through_client_id()
    l = requests.get(url, headers=headers)
    js = json.loads(l.text)
    return js


def Download_icon(url):
    """Used to download a word-template.

    Args:
        site (string): The sharepoint site to download the template file from.
        filename (string): Name of the template file.

    Returns:
        _type_: Response-object.
    """
    headers=get_sharepoint_access_headers_through_client_id()
    l = requests.get(url, headers=headers)
    return l


if __name__ == '__main__':
    # headers=get_sharepoint_access_headers_through_client_id()
    # url = "https://greenlandscapingmalmo.sharepoint.com/_api/search/query?querytext=%27contentclass:STS_SitePath:%22https://greenlandscapingmalmo.sharepoint.com/*%22%27&rowlimit=500"
    # l = requests.get(url, headers=headers)
    # js = get_all_items("Egenkontroller_Trollhttan341","Egenkontroll_lista_protokoll")
    import base64
    from PIL import Image
    import io
    with open(os.path.join(os.path.dirname(__file__), 'egenkontroll_skötsel.json'), 'r', encoding='utf-8') as f:
        js = json.load(f)
    results = js['d']['results']
    for item in results:
        for key in item.keys():
            if "bild" in key.lower() and "komm" not in key.lower(): 
                print(key)
                if item[key] is not None: 
                    print(key)
                    img = io.BytesIO(base64.b64decode(item[key]))
                    img.seek(0)
                    img = Image.open(img)
                    img.show()