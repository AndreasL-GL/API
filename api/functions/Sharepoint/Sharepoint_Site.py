import json
import os
import requests
from functions.Sharepoint.get_sharepoint_columns import get_sharepoint_access_headers_through_client_id
def filter_sites(js):
    with open(os.path.join(os.path.dirname(__file__),'bad_sites.txt'), 'r', encoding=('utf-8')) as fp:
        bad_sites = fp.read().split('\n')
    sitelist = []
    for item in js['d']['query']['PrimaryQueryResult']['RelevantResults']['Table']['Rows']['results']:
        sitedict = {}
        for i,spobject in enumerate(item['Cells']['results']):
            match spobject['Key']:
                case 'OriginalPath': sitedict['Site'] = spobject['Value']
                case 'Title': sitedict['Title'] = spobject['Value']
        if "personal" not in sitedict['Site'] and "(/portal)" not in sitedict['Site'] and sitedict['Title'] not in bad_sites:
            try:
                listlist = filter_lists(sitedict['Site'])
                sitedict['Lists'] = listlist
                sitelist.append(sitedict)
            except:
                pass
            
    return sitelist



def filter_lists(url):
    js = requests.get(url + '/_api/web/lists', headers=get_sharepoint_access_headers_through_client_id()).json()
    listlist = ""
    for item in js['d']['results']:
        #print(item.keys())
       # print(json.dumps(item, indent=4))
        
        if item["BaseTemplate"] == 100 and item['Title'] != "TaxonomyHiddenList":
            listlist = listlist+item['Title']+","
    return listlist[:-1]
            

        
if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),'spsite.json'),'r', encoding='utf-8') as f:
        js = json.load(f)
    sitelist = filter_sites(js['body'])
    with open(os.path.join(os.path.dirname(__file__),'spsites.json'),'w', encoding='utf-8') as f:
        json.dump(sitelist, f, indent=4)
    for item in sitelist:
        print(item['Title'])
    filter_lists(js)