import json, os
import requests
import configparser
from flask import url_for
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),"config.ini"))

with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),'sharepoint_egenkontroller_remove_list.txt')) as f:
    sharepoint_columns_remove_list = [x.replace('\n','') for x in f.readlines() if x != '\n']


def get_body_from_sharepoint_api(js):
    resultlist = []
    if 'body' in js.keys(): js = js['body']
    for item in js['d']['results']:
        if item['EntityPropertyName'] not in sharepoint_columns_remove_list:
            resultlist.append({"Moment":item['Title'], "link":item['EntityPropertyName']})
    return resultlist

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

def get_fields(site, list_):
    try:
        headers=get_sharepoint_access_headers_through_client_id()
        tenant = "greenlandscapingmalmo"
        url = site + f"/_api/web/lists/getbytitle('{list_}')/fields"
        l = requests.get(url, headers=headers)
        js= json.loads(l.text)
        js = get_body_from_sharepoint_api(js)
        return js
    except:
        with open(os.path.join(os.path.dirname(__file__),'file.txt'),'w') as f:
            f.write("site: "+site+" list: "+list_)

def get_by_url(url):
    headers = get_sharepoint_access_headers_through_client_id()
    l = requests.get(url)
    js = json.loads(l.text)
    return js
    
    
    
def get_sites():
    headers = get_sharepoint_access_headers_through_client_id()
    url = "https://greenlandscapingmalmo.sharepoint.com/_api/search/query?querytext=%27contentClass:STS_Site%27&trimduplicates=false&selectproperties=%27SiteLogo%2cTitle%27"
    l = requests.get(url, headers=headers)
    js = json.loads(l.text)
    return js

def get_filenames_from_sharepoint():
        url = "https://greenlandscapingmalmo.sharepoint.com/sites/TrdexperternaApplikationer"+"/_api/web/lists/getbytitle('Geodata fordon')/items"
        
        js = requests.get(url,headers=get_sharepoint_access_headers_through_client_id())
        print(json.dumps(js.json()['d']['results'], indent=4, ensure_ascii=False))
        return None
def get_fields__2(site, list_, ID):

    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    url = site + f"/_api/web/lists/getbytitle('{list_}')/fields"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    js = get_body_from_sharepoint_api(js)
    item = requests.get(site+f"/_api/web/lists/getbytitle('{list_}')/items({ID})",headers=headers).json()['d']
    kontrollmoment = item["Kontrollmoment"]['results']
    boollista = []
    text = '\n'.join(["- "+object['Moment']+": "+"Kontrollmoment klart" if item[object['link']] else "- " +object['Moment']+": Ej kontrollerat" for object in js if object['Moment'] in kontrollmoment and object['Moment']])
    [boollista.append(item[object['link']]) if object["Moment"] in kontrollmoment else None for object in js]
                     
    print({'text':text, "Alla klara": "Ja" if all(boollista) else "Nej"})
    print(boollista)
    return {'text':text, "Alla klara": "Ja" if all(boollista) else "Nej"}


if __name__ == '__main__':
    f ={
  "Site": "https://greenlandscapingmalmo.sharepoint.com/sites/StenaFastigheter",
  "List": "Stena Kortedala skötsel - periodiska",
  "ID": 72
}
    
    get_fields__2("https://greenlandscapingmalmo.sharepoint.com/sites/StenaFastigheter","Stena Kortedala skötsel - periodiska", 72)
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    url = f["Site"] + f"""/_api/web/lists/getbytitle('{f['List']}')/fields"""
    [print(item["EntityPropertyName"]) for item in requests.get(url,headers=headers).json()['d']['results'] if "mment" in item["Title"]]