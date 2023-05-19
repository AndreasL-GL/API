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
        if item['EntityPropertyName'] not in sharepoint_columns_remove_list:
            resultlist.append({"Moment":item['Title'], "link":item['EntityPropertyName']})
    removelist2 = ["Data__ModerationComments",
"OData__x00c5_terkommandekontroll",
"OData__ColorHex",
"OData__ColorTag",
"OData__Emoji",
"OData__HasCopyDestinations",
"OData__CopySource",
"OData__UIVersion",
"OData__UIVersionString",
"OData__ModerationStatus",
"OData__EditMenuTableStart",
"OData__EditMenuTableStart2",
"OData__EditMenuTableEnd",
"OData__Level",
"OData__IsCurrentVersion",
"OData__ComplianceFlags",
"OData__ComplianceTag",
"OData__ComplianceTagWrittenTime",
"OData__ComplianceTagUserId",
"OData__IsRecord",
"OData__VirusStatus",
"OData__VirusVendorID",
"OData__VirusInfo",
"OData__CommentFlags","OData__ModerationComments",
"OData__CommentCount","_ModerationComments OData__ModerationComments","_x00c5_terkommandekontroll OData__x00c5_terkommandekontroll","_ColorHex OData__ColorHex","_ColorTag OData__ColorTag","_Emoji OData__Emoji","_HasCopyDestinations OData__HasCopyDestinations","_CopySource OData__CopySource","_UIVersion OData__UIVersion","_UIVersionString OData__UIVersionString","_ModerationStatus OData__ModerationStatus","_EditMenuTableStart OData__EditMenuTableStart","_EditMenuTableStart2 OData__EditMenuTableStart2","_EditMenuTableEnd OData__EditMenuTableEnd","_Level OData__Level","_IsCurrentVersion OData__IsCurrentVersion","_ComplianceFlags OData__ComplianceFlags","_ComplianceTag OData__ComplianceTag","_ComplianceTagWrittenTime OData__ComplianceTagWrittenTime","_ComplianceTagUserId OData__ComplianceTagUserId","_IsRecord OData__IsRecord","_VirusStatus OData__VirusStatus","_VirusVendorID OData__VirusVendorID","_VirusInfo OData__VirusInfo","_CommentFlags OData__CommentFlags","_CommentCount OData__CommentCount"
]
    resultlist = [item for item in resultlist if item['link'] not in removelist2]
    
    

    return resultlist
def get_fields(site="GLMalmAB-EgenkontrollerVellingebostder", list_="MKB Egenkontroll Periodiska 2023"):
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    #site = site.split('sites/')[1]
    url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/lists/getbytitle('{list_}')/fields"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    
    js = get_body_from_sharepoint_api(js)
    return js

if __name__ == '__main__':
#     headers=get_sharepoint_access_headers_through_client_id()
#     #url = "https://greenlandscapingmalmo.sharepoint.com/_api/search/query?querytext=%27contentclass:STS_SitePath:%22https://greenlandscapingmalmo.sharepoint.com/*%22%27&rowlimit=500"
#     #l = requests.get(url, headers=headers)
#     headers=get_sharepoint_access_headers_through_client_id()
#     tenant = "greenlandscapingmalmo"
#     site = "Funktionskontrolllekplatsdemo"
#     filename = "Protokoll_2379_Svaleboskolan_Veberöd_2023-05-11.docx"
#     #server_relative_url = f"/sites/{site}/Delade Dokument/Protokoll lekplats besiktning demo/{filename}"
#     #url = f"https://{tenant}.sharepoint.com/sites/{site}/_api/web/GetFileByServerRelativeUrl('{server_relative_url}')/$value"
#     #l = requests.get(url, headers=headers)
#     server_relative_url = f"/sites/{site}/Delade Dokument/Protokoll lekplats besiktning demo" #PowerBI"#
#     url = f"""https://{tenant}.sharepoint.com/sites/{site}/_api/Web/GetFolderByServerRelativeUrl('{server_relative_url}')/Files?$filter= substringof('Ugglehallen', name)"""#name eq '2716_2020 - (Sida 2).png'"""
#     l = requests.get(url, headers=headers)
#     js = json.loads(l.content)

    
    
    
    site = "GLMalmAB-EgenkontrollerVellingebostder"
    list_="MKB Egenkontroll Periodiska 2023"
    headers=get_sharepoint_access_headers_through_client_id()
    tenant = "greenlandscapingmalmo"
    #site = site.split('sites/')[1]
    url = f"https://{tenant}.sharepoint.com/sites/GLMalmAB-EgenkontrollerVellingebostder/_api/web/lists/getbytitle('{list_}')/fields"
    l = requests.get(url, headers=headers)
    js= json.loads(l.text)
    
    resultlist = []
    if 'body' in js.keys(): js = js['body']
    count = 4 
    for item in js['d']['results']:
        #if item["StaticName"] != item['EntityPropertyName']:
            #print(item["StaticName"],  item['EntityPropertyName'])
        if count == 0: break
        #count -=1