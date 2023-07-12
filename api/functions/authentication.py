from functools import wraps
from flask import request, abort
import configparser, os
# from office365.runtime.auth.user_credential import UserCredential
# from office365.runtime.auth.client_credential import ClientCredential
# from office365.sharepoint.client_context import ClientContext 
import urllib.parse
import requests
import json
import logging
info_logger = logging.getLogger("info_logger")
error_logger = logging.getLogger('error_logger')
rs = logging.getLogger("request_logger")
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),"config.ini"))
tenant = config["SHAREPOINT"]["tenant"]
def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):

        api_key = request.args.get("API_KEY") if request.args.get("API_KEY") else " "
        if api_key not in config["DEFAULTS"]['API_KEYS']:
            error_logger.error("Invalid API Key: "+api_key)
            abort(401, description="Invalid API key")
            
        try: 
            return func(*args, **kwargs)
            rs.info("200")
        except Exception as e:
            error_logger.error(f"Error in function: {str(func)}, "+str(e))
            abort(500, description=str(e))
            rs.info("500 "+ str(e))
             
        #except Exception as e:
         #   abort(500,str(e))
    return decorated_function




# def get_sharepoint_context_using_user(site, username, password):
 

#     user_credentials = UserCredential(username, password)

#     # create client context object
#     ctx = ClientContext(site).with_credentials(user_credentials)

#     return ctx
# def create_sharepoint_directory(ctx,dir_name):
#     """
#     Creates a folder in the sharepoint directory.
#     """
#     if dir_name:


#         result = ctx.web.folders.add(f'Shared Documents/{dir_name}').execute_query()

#         if result:
#             # documents is titled as Shared Documents for relative URL in SP
#             relative_url = f'Shared Documents/{dir_name}'
#             return relative_url


# def get_sharepoint_context_using_app(sharepoint_url):

#     # Initialize the client credentials
#     client_credentials = ClientCredential(config["SHAREPOINT"]["client_id"], config["SHAREPOINT"]["client_secret"])

#     # create client context object
#     ctx = ClientContext(sharepoint_url).with_credentials(client_credentials)

#     return ctx

# def get_sharepoint_access_headers_through_client_id():
#     client_id = config["SHAREPOINT"]["client_id"].strip()
#     client_secret = config["SHAREPOINT"]["client_secret"].strip()
#     tenant_id = config["SHAREPOINT"]["tenant_id"].strip()
#     tenant = config["SHAREPOINT"]["tenant"]
#     client_id = client_id + '@'+tenant_id
    
#     data = {
#     'grant_type':'client_credentials',
#     'resource': "00000003-0000-0ff1-ce00-000000000000/" + tenant + ".sharepoint.com@" + tenant_id, 
#     'client_id': client_id,
#     'client_secret': client_secret
# }
#     url = "https://accounts.accesscontrol.windows.net/tenant_id/tokens/OAuth/2"
#     headers = {
#     'Content-Type':'application/x-www-form-urlencoded'
# }

#     url = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"
#     r = requests.post(url, data=data, headers=headers)
#     json_data = json.loads(r.text)
#     headers = {
#     'Authorization': "Bearer " + json_data['access_token'],
#     'Accept':'application/json;odata=verbose',
#     'Content-Type': 'application/json;odata=verbose'
# }
#     return headers

# def create_sharepoint_directory(ctx,dir_name: str):
#     """
#     Creates a folder in the sharepoint directory.
#     """
#     if dir_name:

#         result = ctx.web.folders.add(f'Shared Documents/{dir_name}').execute_query()

#         if result:
#             # documents is titled as Shared Documents for relative URL in SP
#             relative_url = f'Shared Documents/{dir_name}'
#             return relative_url

# if __name__ == '__main__':
#     with open(os.path.join(os.path.dirname(__file__),'login.txt')) as f:
#         p= eval(f.read())
#     sitename = "TrdexperternaApplikationer"
#     URL =f"https://{tenant}.sharepoint.com/sites/{sitename}"
#     headers = get_sharepoint_access_headers_through_client_id()
#     url = URL+f"/_api/web/lists/getbytitle('Dagbok_poster')/fields"
#     l = requests.get(url, headers=headers)
#     #ctx = get_sharepoint_context_using_app(sitename)
#     #create_sharepoint_directory(ctx,'test directory')
#     url = URL+f"/_api/Web/GetFolderByServerRelativeUrl('/Shared Documents')/Files/Add(url='__init__.py', overwrite=true)"
#     url = URL+f"/_api/web/getfolderbyserverrelativeurl('')/Files/add(url='__init__.py', overwrite=true)"
#     payload=os.path.join(os.path.dirname(__file__),'Image_api.py')
#     with open(payload,'rb') as f:
#         response = requests.post(url, data=payload,headers=headers)
#         print(url)
#     print(response.text)
if __name__=='__main__':
    """
    token_url = 'https://login.microsoftonline.com/a096cfba-db7b-4c9c-9506-d8e91da824ee/oauth2/v2.0/token'
    tenant_id = "a096cfba-db7b-4c9c-9506-d8e91da824ee"
    # Replace {tenant_id} with your Azure AD tenant ID
    token_url = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"

    # Microsoft Graph API endpoint for accessing Word document content
    document_url = 'https://graph.microsoft.com/v1.0/me/drive/root:/Documents/MyDocument.docx:/content'

    # Azure AD app registration details
    client_id = '2f7ad521-aec9-4fb4-9b1f-01e2b07d1f26'
    client_secret = '876df122-f497-4759-baef-26b2e1e13df0'
    # Replace with your Azure AD app registration details

    # Request an access token
    def get_access_token():
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return response

    # Make a request to retrieve Word document content
    def get_word_document_content():
        access_token = get_access_token()
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(document_url, headers=headers)
        response.raise_for_status()
        content = response.content
        return content

    document_content = get_word_document_content()
"""
if __name__=='__main__':
    
    """
    config = configparser.ConfigParser()
    config.read([os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),'config.ini'), os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),'config.dev.cfg')])
    azure_settings = config['azure']
    settings = azure_settings
    client_id = settings['clientId']
    tenant_id = settings['tenantId']
    client_secret = settings['clientSecret']
    d = get_app_only_token(tenant_id,client_id,client_secret, scope="https://greenlandscapingmalmo.sharepoint.com/.default")
    rs = requests.get("https://greenlandscapingmalmo.sharepoint.com/sites/Digitaliseringsportal/_api/web/lists", headers=d)
    print(rs.content)"""