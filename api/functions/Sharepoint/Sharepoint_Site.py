import json
import os

def filter_sites(js):
    sitelist = []
    for item in js['d']['query']['PrimaryQueryResult']['RelevantResults']['Table']['Rows']['results']:
        sitedict = {}
        for i,spobject in enumerate(item['Cells']['results']):
            match spobject['Key']:
                case 'OriginalPath': sitedict['Site'] = spobject['Value']
                case 'Title': sitedict['Title'] = spobject['Value']
        if "personal" not in sitedict['Site'] and "(/portal)" not in sitedict['Site']:
            sitelist.append(sitedict)
    return sitelist

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),'spsite.json'),'r') as f:
        js = json.load(f)
    sitelist = filter_sites(js['body'])
    #print(json.dumps(sitelist,indent=4))
    with open(os.path.join(os.path.dirname(__file__),'spsites.json'),'w', encoding='utf-8') as f:
        js = json.dump(sitelist, f, indent=4)