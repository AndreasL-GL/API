import requests
from configparser import SectionProxy
import configparser
from azure.identity.aio import ClientSecretCredential
import asyncio,os
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider
)
from msgraph import GraphRequestAdapter, GraphServiceClient

class Azure_Identity:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    adapter: GraphRequestAdapter
    app_client: GraphServiceClient

    def __init__(self, scope = "https://graph.microsoft.com/.default"):
        self.scope = scope
        config = configparser.ConfigParser()
        config.read([os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),'config.ini'), os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),'config.dev.cfg')])
        azure_settings = config['azure']
        self.settings = azure_settings
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        client_secret = self.settings['clientSecret']

        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        auth_provider = AzureIdentityAuthenticationProvider(self.client_credential) # type: ignore
        self.adapter = GraphRequestAdapter(auth_provider)
        self.app_client = GraphServiceClient(self.adapter)

    async def get_app_only_token(self):
        graph_scope = self.scope#'https://graph.microsoft.com/.default'
        access_token = await self.client_credential.get_token(graph_scope)
        self.access_token = access_token.token
        return access_token.token
    async def get_headers(self, app="graph"):
        if app=='sharepoint':self.scope = f"""https://{self.settings["tenantName"]}.sharepoint.com/.default"""
        elif app=='graph':self.scope = "https://graph.microsoft.com/.default"
        token = await self.get_app_only_token()
        headers = {'Authorization': 'Bearer ' + token}
        return headers
    
Azure = Azure_Identity()


async def get_sharepoint_lists(site_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"
    headers = await Azure.get_headers()

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    lists = response.json()['value']
    
    return lists[0]['id'] if any(lists) else "No site found"

            
async def download_files(drive_id,filename=None):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    headers = await Azure.get_headers()
    import json
    import os
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    dir_id = [dirname for dirname in response.json()['value'] if dirname["name"] == 'Protokoll'][0]['id']
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{dir_id}/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    children = response.json()['value']
    #files = [file["name"] for file in lists]
    #print(json.dumps(files,indent=4))
    files = [{"filename": child["name"],"url":child["@microsoft.graph.downloadUrl"]} for child in children if "@microsoft.graph.downloadUrl" in child.keys()]
    for file in files:
        data = requests.get(file["url"],headers=headers).content
        #print(data)
        with open(os.path.join(os.path.join(os.path.dirname(__file__),'files'),file["filename"]),'wb') as f:
            f.write(data)

    
    return None

async def graph_api_headers():
    

    graph: Azure_Identity = Azure_Identity()
    token = await graph.get_app_only_token()
    access_token = token
    headers = {'Authorization': 'Bearer ' + graph.get_headers()}
    return headers

class Files:
    def __init__(self, scope = ["sharepoint"]) -> None:
        Az = Azure_Identity()
        self.headers = {scop:asyncio.run(Az.get_headers(scop)) for scop in scope}

    async def get_sharepoint_site_id(self,site_name="Stena Fastigheter"):
        url = "https://graph.microsoft.com/v1.0/sites"
        headers = self.headers["graph"]
        params = {
        'search': site_name
        #'$filter': f"webUrl eq '{site_url}'"
    }
        response = requests.get(url, headers=headers,params=params)
        response.raise_for_status()
        sites = response.json()['value']
        return sites[0]['id'] if any(sites) else "No site found"

    async def get_sharepoint_drive(self, site_id, library):
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        headers = self.headers["graph"]

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        drive = response.json()["value"] if "value" in response.json().keys() else response.json()
        import json
        print(json.dumps(drive,indent=4,ensure_ascii=False))
        if type(drive)==dict:return drive['id']
        else:
            for item in drive:
                if item["name"]==library:
                    return item["id"]

    async def download_file(self, drive_id,filepath, filetype = None):
        append=f":/content?format={filetype}" if filetype else ""
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:{filepath}"+append
        headers = self.headers["graph"]
        import os,io,base64

        rs=requests.get(url, headers=headers)

        data = rs.content
        filename = filepath.split('/')[-1].split(".")[0]+"."+filetype if filetype else filepath.split('/')[-1]
        i=filename.split('.')[-1]
        
        return {"Filename":filename,"File Content":{"$content": base64.b64encode(data).decode(), "$content-type":
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if i=='docx' else
            "application/pdf" if i=="pdf"else "application/octet-stream"}}
        
    def download_file_as_pdf(self, site_name,filepath, document_library):
        site_id = asyncio.run(self.get_sharepoint_site_id(site_name))
        drive = asyncio.run(self.get_sharepoint_drive(site_id,document_library))
        file = asyncio.run(self.download_file(drive,filepath, "pdf"))
        return file
def download_pdf(Sitename,Filepath,Library):
    files = Files(["Graph"])
    file = files.download_file_as_pdf(Sitename,Filepath,Library)
    return file

def get_sharepoint_headers():
    Az = Azure_Identity()
    x = asyncio.run(Az.get_headers("sharepoint"))
    x.update({'Accept':'application/json;odata=verbose',
    'Content-Type': 'application/json;odata=verbose'})
    return x
def get_graph_headers():
    Az = Azure_Identity()
    x = asyncio.run(Az.get_headers("graph"))
    return x
if __name__ == '__main__':
    File = Files(["graph"])
    print(File.download_file_as_pdf("Stena Fastigheter","/Protokoll/Stena_Kortedala_daglig_tillsyn_vecka_13.docx","Dokument"))
    x = get_sharepoint_headers()
    print(x)
    #print(get_graph_headers())
    
    
    