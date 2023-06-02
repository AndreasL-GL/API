import requests
import os
import json
from functions.Sharepoint.get_sharepoint_columns import get_sharepoint_access_headers_through_client_id

def rq(url,headers=get_sharepoint_access_headers_through_client_id()):
    jq = requests.get(url,headers=headers)
    #print(jq.text)
    return jq.json()

def set_field_visibility(site_url, list_name, fields=["Lampbyte"], headers = get_sharepoint_access_headers_through_client_id()):
    list_id = requests.get(f"{site_url}/_api/web/lists/GetByTitle('{list_name}')", headers=headers).json()['d']['Id']
     
    view_id = requests.get(f"{site_url}/_api/web/lists/getByTitle('{list_name}')/DefaultView", headers=headers).json()['d']['Id']

    
    fields_already_displayed = requests.get(f"{site_url}/_api/web/lists(guid'{list_id}')/Views('{view_id}')/ViewFields",headers=headers).json()['d']['Items']['results']
    req_url = f"{site_url}/_api/web/lists(guid'{list_id}')/Views('{view_id}')/ViewFields/AddViewField"

    for field in fields:
        if field not in fields_already_displayed:
            data = {"strField":field}
            rs = requests.post(req_url,data=json.dumps(data), headers=headers)



def create_list(site_url, Title='MylistTitle',data = {
        '__metadata': {'type': 'SP.List'},
        'AllowContentTypes': False,
        'BaseTemplate': 100,
        'ContentTypesEnabled': False,
        'Description': 'My new list',
        'Title': "Mylisttitle",
        'EnableAttachments':True,
        'Hidden':False
    }, headers=get_sharepoint_access_headers_through_client_id()):
    
    # SharePoint site URL
    if Title != "MylistTitle": data["Title"] = Title

    # API endpoint for creating a list
    url = f'{site_url}/_api/web/lists'

    response = requests.post(url, json=data, headers=headers)

    # Check the response status
    if response.status_code == 201:
        print('List created successfully.')
    else:
        print('Failed to create list. Status Code:', response.status_code)
        print('Error:', response.text)
    return response



def request_fields(site_url, list_name, get_fields=True, field=None, headers=get_sharepoint_access_headers_through_client_id()):


    url = f"{site_url}/_api/web/lists/getByTitle('{list_name}')/fields"
    
    if not headers: headers = get_sharepoint_access_headers_through_client_id()
    if get_fields:
        response = requests.get(url, headers=headers)
    else: 
        data = {}
        
        if field:
            data['__metadata'] = {"type":field['__metadata']["type"]}
            data['Title'] = field['Title']
            data['FieldTypeKind'] = field['FieldTypeKind']
            if (data['FieldTypeKind'] == 6 or data['FieldTypeKind'] == 15) and 'Choices' in field.keys():
                data['Choices'] = field['Choices']
            if 'Required' in field.keys(): data['Required'] = field['Required']
            if 'CustomFormatter' in field.keys(): data['CustomFormatter'] = field['CustomFormatter']
            if 'SchemaXML' in field.keys(): data['SchemaXML'] = field['SchemaXML']
            if 'Hidden' in field.keys(): data['Hidden'] = False
            if 'DefaultValue' in field.keys():data['DefaultValue'] = field['DefaultValue']
            # if "EntityPropertyName" in field.keys(): data["EntityPropertyName"] = field["EntityPropertyName"]
            #if "InternalName" in field.keys(): data["InternalName"] = field["InternalName"]
            #if "StaticName" in field.keys(): data["StaticName"] = field["StaticName"]
            if "EnforceUniqueValues" in field.keys(): data["EnforceUniqueValues"] = field["EnforceUniqueValues"]
            #if "DefaultValue" in field.keys(): data["DefaultValue"] = field["DefaultValue"]
            if "Description" in field.keys(): data["Description"] = field["Description"]
        response = requests.post(url, json=data, headers=headers)
    return response


def get_server_relative_url(site_url,list_name, headers=get_sharepoint_access_headers_through_client_id()):
    api_endpoint = f"{site_url}/_api/web/lists/getByTitle('{list_name}')?$select=Id,RootFolder/ServerRelativeUrl&$expand=RootFolder"
    response = requests.get(api_endpoint, headers=headers)
    return response.json()['d']['RootFolder']['ServerRelativeUrl']

def change_list_visibility(site_url,list_name,headers=get_sharepoint_access_headers_through_client_id()):
    # api_endpoint = f"{site_url}/_api/web/lists/getByTitle('{list_name}')"
    # Title = json.loads(requests.get(api_endpoint, headers=get_sharepoint_access_headers_through_client_id()).content)['d']['Title']
    api_endpoint = f"{site_url}/_api/web/navigation/QuickLaunch"
    if not headers: headers = get_sharepoint_access_headers_through_client_id()
    payload = {
    "__metadata": {
        "type": "SP.NavigationNode"
    },
    "IsVisible": True,  # Set to True to make the list visible in the navigation
    "ListTemplateType": "0",
    "Title": list_name,
    "Url": f"{site_url}/Lists/{get_server_relative_url(site_url,list_name, headers).split('Lists/')[1]}"
}
    response = requests.post(api_endpoint, headers=headers, json=payload)
    return response.status_code
    
def copy_list(target_site, destination_site, target_list,destination_list=None,headers = get_sharepoint_access_headers_through_client_id()):
    
    if not destination_list: destination_list = target_list
    if target_list == destination_list and target_site == destination_site:
        return "Error: Target list and destination list can't be the same."
    ### CREATE A CHECK HERE TO SEE IF A LIST EXISTS
    
    
    # Creates list and sets it to visible in quicklaunch
    rs = create_list(destination_site,destination_list, headers=headers)
    change_list_visibility(destination_site,destination_list, headers)
    
    # Gets fields from the old list and creates all fields in the new one and sets them to visible
    fields = json.loads(request_fields(target_site, target_list, headers=headers).text)['d']['results']
    fields_list = []
    with open(os.path.join(os.path.dirname(__file__),'fields_to_remain_hidden.txt'), 'r') as f: rmlist = f.read().split('\n')
    for field in fields:
        if field['EntityPropertyName'] not in rmlist:
            
            rsf = request_fields(destination_site, destination_list, get_fields=False,field=field, headers=headers)
            fields_list.append(field['Title'])
    rs = set_field_visibility(destination_site,destination_list,fields=fields_list,headers=headers)
    
    return 201
    
   
def set_visibility_for_fields(site_url, list_name, fields, headers=get_sharepoint_access_headers_through_client_id()):
    payload = {
    "__metadata": {"type": "SP.View"},
    "ViewFields": {
        "__metadata": {"type": "SP.ViewFieldCollection"},
        "ViewFields": {
            "results": fields  # Specify the desired field names
        }
    }
}
    api_endpoint = f"{site_url}/_api/web/lists/getByTitle('{list_name}')/views"
    views = requests.get(api_endpoint, headers=headers).json()['d']['results']
    view_names = [view['Title'] for view in views]
    rs = []
    for view_name in view_names:
        api_endpoint = f"{site_url}/_api/web/lists/getByTitle('{list_name}')/views/getbytitle('{view_name}')"
        rss =requests.post(api_endpoint,data=payload,headers=headers)
        rs.append(rss)
    return rs
    

def add_all_items(source_site,destination_site,source_list,headers=get_sharepoint_access_headers_through_client_id(),destination_list=None):
    if not destination_list:destination_list = source_list
    

    api_endpoint = f"{source_site}/_api/web/lists/getByTitle('{source_list}')/Items"
    source_items = requests.get(api_endpoint,headers=headers).json()['d']['results'] 
    

    with open(os.path.join(os.path.dirname(__file__),'fields_to_remain_hidden.txt'), 'r') as f: rmlist = f.read().split('\n')
    
    fields_source = requests.get(f"{source_site}/_api/web/lists/getByTitle('{source_list}')/Fields",headers=headers).json()['d']['results']
    fields_destination = requests.get(f"{destination_site}/_api/web/lists/getByTitle('{destination_list}')/Fields",headers=headers).json()['d']['results']
    #with open(os.path.join(os.path.dirname(__file__),'items.json'), 'w') as f: json.dump(source_items,f,indent=3)
    
    for item in source_items:
        newitem = {}
        newitem['__metadata'] = {'type':item['__metadata']['type']}
        for sfield in [item for item in fields_source if item["EntityPropertyName"] not in rmlist]:
            for dfield in fields_destination:
                if dfield['Title'] == sfield['Title'] or ('Rubrik' in dfield['Title'] and 'Title' in sfield['Title']) or ('Rubrik' in sfield['Title'] and 'Title' in dfield['Title']):
                    if "link" in sfield['InternalName'].lower() or "link" in sfield['StaticName'].lower() or "link" in dfield['InternalName'].lower() or "link" in dfield['StaticName'].lower() or "Title0" in [dfield['EntityPropertyName'],sfield['EntityPropertyName']]: continue
                    newitem[dfield['EntityPropertyName']] = item[sfield['EntityPropertyName']]
        newitem = {key:value for key,value in newitem.items() if value and key}
        rs = requests.post(f"{destination_site}/_api/web/lists/getByTitle('{destination_list}')/Items",json=newitem,headers=headers)
        add_attachments(source_site=source_site,source_list=source_list,destination_site=destination_site,destination_list=destination_list,item=item,item_id=rs.json()["d"]['ID'],headers=headers)
    return rs.status_code

def add_attachments(source_site,source_list,destination_site,item=None,item_id=None,destination_list=None,headers=get_sharepoint_access_headers_through_client_id()):
    if not destination_list: destination_list = source_list
    if item:    
        ks = rq(item['AttachmentFiles']['__deferred']['uri'],headers=headers)
        files = ks['d']['results']
        rslist = []
        for file in files:
            path = file['ServerRelativeUrl']
            url = f"{source_site}/_api/web/GetFileByServerRelativeUrl('{path}')/$value"
            rs = requests.get(url, headers=headers)
            filecontent = rs.content
            fname = file["FileName"]
            
            send_file_url = f"{destination_site}/_api/web/lists/getByTitle('{destination_list}')/items({item_id})/AttachmentFiles/add(FileName='{fname}')"
            response = requests.post(send_file_url, headers=headers, data=filecontent)
            rslist.append(response)
        if any(rslist): item['Attachments'] = True
        else: item['Attachments'] = False


    
def copy_list_and_all_items(source_site, source_list, destination_site,destination_list=None):
    if not destination_list:destination_list=source_list
    headers = get_sharepoint_access_headers_through_client_id()
    rs = copy_list(source_site,destination_site,source_list,destination_list,headers=headers)
    ps = add_all_items(source_site,destination_site,source_list,destination_list=destination_list,headers=headers)
    if rs < 300 and ps <300:
        return 201
    else: return 500
    
def add_field(site_url,list_name, field = {
    "__metadata": {
          "type": "SP.Field"
      },
    "Description": "Mydescription",
    "Title": "MyTitle",
    "FieldTypeKind": 6,
    "Choices": ["Choice 1", "Choice 2", "Choice 3"],
    "Required": True,
    "Hidden": False,
    "DefaultValue": "",
    "EnforceUniqueValues": True
},
    headers=get_sharepoint_access_headers_through_client_id()):
    url = f"{site_url}/_api/web/lists/getByTitle('{list_name}')/fields"
    req = requests.post(url, json=field,headers=headers)
    return req.status_code
    
    
    
def get_fieldtypes(destination_site):
    response = requests.get(f"{destination_site}/_api/web/AvailableFields?$select=FieldTypeKind&$select=TypeAsString&$filter=FieldTypeKind ne null&$orderby=FieldTypeKind&$top=1000&$apply=groupby(FieldTypeKind))", headers=headers)
    r = response.json()['d']['results']
    setlist = list(set(field_type["FieldTypeKind"] for field_type in r))
    typelist =[]
    numlist = []
    for item in setlist:
        for ftype in r:
            if ftype["FieldTypeKind"] == item and item not in numlist:
                typelist.append(ftype)
                numlist.append(item)
                continue
    return typelist
    
if __name__ == '__main__':
    source_site = "https://greenlandscapingmalmo.sharepoint.com/sites/GLMalmAB-EgenkontrollerVellingebostder"
    destination_site = "https://greenlandscapingmalmo.sharepoint.com/sites/TrdexperternaApplikationer"
    
    source_list = "MKB Egenkontroll Augustenborg Periodiska 2023"
    destination_list = source_list
    #copy_list_and_all_items(source_site,source_list,destination_site,destination_list)
    headers=get_sharepoint_access_headers_through_client_id()
    rs = copy_list_and_all_items(source_site,source_list,destination_site,destination_list)
    print(rs)
# Make the API call
    
   # r = [item for item in r if item["FieldTypeKind"]]