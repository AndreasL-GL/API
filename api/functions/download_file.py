from flask import request
import base64
import io
from functions.Sharepoint.get_sharepoint_columns import get_sharepoint_access_headers_through_client_id
import requests
import tempfile, os
import subprocess


def get_file_base64():
    file_content = request.json.get('content')
    file_content=base64.b64decode(file_content)
    file_content=io.BytesIO(file_content)
    return file_content

def download_file(site, relative_file_location, run_after=False):
    site = site[:-1] if site.endswith('/') else site
    sitename = site.split('/')[-1]
    url = site + f"/_api/web/GetFileByServerRelativeUrl('/sites/{sitename}/{relative_file_location}')/$value"
    rs = requests.get(url, headers = get_sharepoint_access_headers_through_client_id())
    print(rs)
    if run_after:
        run_file(rs.content)
        
    return rs
    
def run_file(file_content):
    

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "tempfile.xlsx")
    with open(temp_path,'wb') as f:
        f.write(file_content)
    

    subprocess.call(['start', '', temp_path], shell=True)
    
if __name__ == '__main__':
    rs = download_file("https://greenlandscapingmalmo.sharepoint.com/sites/TrdexperternaApplikationer","Delade dokument/Prislista.xlsx",run_after=True)
    #with open(temp_path,'wb') as f:
    #    f.write(rs.content)
    #import subprocess

    #subprocess.call(['start', '', temp_path], shell=True)
    