from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
import os
from flask import jsonify, request

def create_sharepoint_list(list_schema):
    # Set up the authentication context
    authcookie = Office365('<sharepoint_site_url>', username='<username>', password='<password>').GetCookies()

    # Connect to the SharePoint site
    site = Site('<sharepoint_site_url>', version=Version.v365, authcookie=authcookie)

    # Create the SharePoint list
    list_name = "MyList"
    list_description = "A SharePoint list created using Shareplum"
    list_result = site.AddList(list_name, list_description, template_id=100, enable_content_types=True, schema_xml=site.BuildFieldsFromSchema(list_schema))

    # Print the list result
    return jsonify(list_result)

def create_egenkontroller_sharepoint_list(list_schema):
    kontroller = request.args.get("kontroller")
    kontroller = eval(kontroller)
    for kontroll in kontroller:
        list_schema[kontroll] = "Boolean"

def get_list_schema(url, list_name,username,password):
        # Set up the authentication context
    authcookie = Office365('<sharepoint_site_url>', username='<username>', password='<password>').GetCookies()

    # Connect to the SharePoint site
    site = Site('<sharepoint_site_url>', version=Version.v365, authcookie=authcookie)

    # Get the list by its name
    list_name = "MyList"
    sp_list = site.List(list_name)

    # Get the list schema
    list_schema = sp_list.get_list_schema()

    # Print the list schema
    print(list_schema)
    
def create_sharepoint_lists_and_columns(schema):
    import requests
    from requests_ntlm import HttpNtlmAuth

    # Set up the authentication context
    username = '<username>'
    password = '<password>'
    site_url = '<sharepoint_site_url>'

    # Create the SharePoint list
    list_name = "MyList"
    list_description = "A SharePoint list created using the SharePoint REST API"
    list_url = f"{site_url}/_api/web/lists"
    list_payload = {
        'Title': list_name,
        'Description': list_description,
        '__metadata': {'type': 'SP.List'}
    }
    list_headers = {
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose',
        'odata-version': ''
    }

    response = requests.post(list_url, json=list_payload, headers=list_headers, auth=HttpNtlmAuth(username, password))
    list_data = response.json()['d']

    # Create some columns
    column_url = f"{site_url}/_api/web/lists('{list_data['Id']}')/fields"
    column_headers = {
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose',
        'odata-version': ''
    }
    column_payloads = [
        {
            '__metadata': {'type': 'SP.FieldText'},
            'FieldTypeKind': 2,
            'Title': 'Text Column',
            'MaxLength': '255'
        },
        {
            '__metadata': {'type': 'SP.FieldNumber'},
            'FieldTypeKind': 9,
            'Title': 'Number Column',
            'MinimumValue': '0',
            'MaximumValue': '100'
        }
    ]

    for column_payload in column_payloads:
        response = requests.post(column_url, json=column_payload, headers=column_headers, auth=HttpNtlmAuth(username, password))

    # Print the response
    print(f"List '{list_name}' created with ID '{list_data['Id']}' and some columns.")

if __name__=='__main__':
    list_schema = {
            "Title": "Text",
            "Description": "Text",
            "DueDate": "DateTime"
        }
    with open(os.path.join(os.path.dirname(__file__),'login.txt')) as f:
        p = eval(f.read())
    url = "https://greenlandscapingmalmo.sharepoint.com/sites/GLMalmAB-EgenkontrollerVellingebostder"
    list_name = "MKB%20Egenkontroll%20Oxie%20Periodiska%202023"
    print(url)
    #url = "https%3A%2F%2Fgreenlandscapingmalmo.sharepoint.com%2Fsites%2FGLMalmAB-EgenkontrollerVellingebostder"
    get_list_schema(url,list_name,p["user"],p["pass"])