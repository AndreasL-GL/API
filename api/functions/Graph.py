import requests
import configparser
import os,base64


def graph_headers(tenant_id, client_id, client_secret, scope="https://graph.microsoft.com/.default"):
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
            "grant_type": "client_credentials"
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        access_token = response.json().get("access_token")
        
        return {'Authorization': 'Bearer ' + access_token
                }
            
async def download_files(drive_id,filename=None):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    headers = graph_headers()
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

class Files:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),'config.ini'))
        azure = config["azure"]
        tenant_id = azure["tenantId"]
        client_id = azure["clientId"]
        client_secret = azure["clientSecret"]
        self.headers = graph_headers(tenant_id,client_id,client_secret)

    def get_sharepoint_site_id(self,site_name="Stena Fastigheter"):
        url = "https://graph.microsoft.com/v1.0/sites"
        headers = self.headers
        params = {
        'search': site_name
        #'$filter': f"webUrl eq '{site_url}'"
    }
        response = requests.get(url, headers=headers,params=params)
        print(response.content)
        sites = response.json()['value']
        return sites[0]['id'] if any(sites) else "No site found"

    def get_sharepoint_drive(self, site_id, library):
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        headers = self.headers

        response = requests.get(url, headers=headers)
        print(response)
        drive = response.json()["value"] if "value" in response.json().keys() else response.json()
        import json
        #print(json.dumps(drive,indent=4,ensure_ascii=False))
        print(drive)
        if type(drive)==dict:return drive['id']
        else:
            for item in drive:
                if item["name"]==library:
                    return item["id"]

    def download_file(self, drive_id,filepath, filetype = None):
        append=f":/content?format={filetype}" if filetype else ""
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:{filepath}"+append
        headers = self.headers

        rs=requests.get(url, headers=headers)

        data = rs.content
        filename = ".".join(filepath.split('/')[-1].split(".")[:-1])+"."+filetype if filetype else filepath.split('/')[-1]
        i=filename.split('.')[-1]
        
        return {"Filename":filename,"File Content":{"$content": base64.b64encode(data).decode(), "$content-type":
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if i=='docx' else
            "application/pdf" if i=="pdf"else "application/octet-stream"}}
        
    def download_file_as_pdf(self, site_name,filepath, document_library):
        site_id = self.get_sharepoint_site_id(site_name)
        drive = self.get_sharepoint_drive(site_id,document_library)
        file = self.download_file(drive,filepath, "pdf")
        return file
    
def download_pdf(Sitename,Filepath,Library):
    files = Files()
    file = files.download_file_as_pdf(Sitename,Filepath,Library)
    return file


if __name__ == '__main__':
    File = Files()
    f = {
  "Sitename": "Stena Fastigheter",
  "Filepath": "/Protokoll/Stena_Lunden_periodiska_07.Juli_2023.docx",
  "Library": "Dokument"
}
    import json
    headers = File.headers
    drive_name = "Dokument"
    site_name = "Digitalisering"
    rq = requests.get("https://graph.microsoft.com/v1.0/sites",headers=headers)
    site_id = [item for item in rq.json()['value'] if site_name in item["displayName"]][0]['id']
    graph_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    rs = requests.get(graph_url,headers=headers)
    drive_id = [item['id'] for item in rs.json()['value'] if item['name'] =='Dokument'][0]
    print(drive_id)