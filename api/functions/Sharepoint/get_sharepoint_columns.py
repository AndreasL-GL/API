import json, os
import requests
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),"config.ini"))

with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),'sharepoint_egenkontroller_remove_list.txt')) as f:
    sharepoint_columns_remove_list = [x.replace('\n','') for x in f.readlines() if x != '\n']


def get_body_from_sharepoint_api(js):
    resultlist = []
    if 'body' in js.keys(): js = js['body']
    for item in js['d']['results']:
        if item['StaticName'] not in sharepoint_columns_remove_list:
            resultlist.append({"Moment":item['Title'], "link":item['StaticName']})
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
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    site = site.split('sites/')[1]
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getbytitle('{list_}')/fields"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    js = get_body_from_sharepoint_api(js)
    return js

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
if __name__ == '__main__':
   # site = "GLMalmAB-EgenkontrollerVellingebostder"
    #list_ = "MKB Egenkontroll Oxie Periodiska 2023"
    #print(get_fields(site,list_))
    print(json.dumps(get_sites(), indent=3))