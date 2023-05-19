from functools import wraps
from flask import request, abort
import configparser, os
# from office365.runtime.auth.user_credential import UserCredential
# from office365.runtime.auth.client_credential import ClientCredential
# from office365.sharepoint.client_context import ClientContext 
import urllib.parse
import requests
import json


config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),"config.ini"))
tenant = config["SHAREPOINT"]["tenant"]
def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("API_KEY")
        if api_key not in config["DEFAULTS"]['API_KEYS']:
            abort(401, description="Invalid API key")
        return func(*args, **kwargs)
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