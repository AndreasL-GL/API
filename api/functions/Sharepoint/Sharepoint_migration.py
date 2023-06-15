import requests
from functions.Sharepoint.get_sharepoint_columns import get_sharepoint_access_headers_through_client_id,get_fields
from functions.Sharepoint.sharepoint_list_operations import copy_list, add_all_items, request_fields
import os,json
import pandas as pd
from pandasgui import show

def get_items(site,_list,headers=get_sharepoint_access_headers_through_client_id()):
    url = f"{site}/_api/web/lists/getByTitle('{_list}')/Items"
    rq = requests.get(url, headers=headers).json()['d']['results']
    return rq

def get_field_choices(target_site, target_list=None,headers = get_sharepoint_access_headers_through_client_id()):
    fields = request_fields(target_site, target_list, headers=headers).json()['d']['results']
    for field in fields:
        if field['Title'] == 'Kontrollmoment':
            choices = (field['Choices']['results'])
    choicetable = []
    for a,b in enumerate(choices):
        link=[q["link"] for q in get_fields(target_site,target_list) if q["Moment"]==b]
        
        if any(link):choicetable.append({"ID":a,"Choice":b,"link":link[0]})
    return choicetable

def kontrollmoment_junction(site,_list,choices, items=None, headers=get_sharepoint_access_headers_through_client_id()):
    url = f"{site}/_api/web/lists/getByTitle('{_list}')/Items"
    if not items: items = requests.get(url, headers=headers).json()['d']['results']
    junction=[]
    for item in items:
        kontrollmoment = item['Kontrollmoment']['results']
        item_kontrollmoment=[]
        for kontroll in kontrollmoment:
            item_kontrollmoment.append([{"Item_ID":item["ID"], "Choices_ID":choice["ID"], "Klar":item[choice["link"]]} for choice in choices if choice["Choice"]==kontroll])
        [junction.append(control[0]) for control in item_kontrollmoment if any(control)]
    print(json.dumps(junction))
    return junction

import random
import string
import base64

def generate_api_key(length):
    # Generate a random string of specified length
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Encode the random string to base64
    base64_string = base64.b64encode(random_string.encode()).decode()

    return base64_string

if __name__ == '__main__':
    source_site = "https://greenlandscapingmalmo.sharepoint.com/sites/Digitaliseringsportal"
    rq = requests.get(source_site+"/_api/web/Navigation/TopNavigationBar", headers=get_sharepoint_access_headers_through_client_id())
    print(json.dumps(rq.json(),indent=4))#[item for item in rq.json()['d']['results'] if "okument" in item["Title"]], indent=4))
    print(generate_api_key(32))

if False:
    source_site = "https://greenlandscapingmalmo.sharepoint.com/sites/GLMalmAB-EgenkontrollerVellingebostder"
    
    source_list = "VEBOA Egenkontroll periodiska 2023"
    headers = get_sharepoint_access_headers_through_client_id()
    items = get_items(source_site,source_list,headers)
    ch = get_field_choices(source_site, source_list,headers)
    df = pd.DataFrame(kontrollmoment_junction(source_site,source_list,ch,items,headers))
    
    df.dropna(inplace=True)
    print(df.head(10))
    df2 = pd.DataFrame(ch)
    df2.index=df2.pop("ID")
    print(df2.head(10))
    items = pd.DataFrame(items)
    items.pop("Kontrollmoment")
    show(df,df2,items)
    #print(json.dumps(get_fields(source_site,source_list),indent=4))
    #get_fields(source_site,source_list)
    