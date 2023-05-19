import json
import io
import base64
import datetime

def decode_file(base64_file):
    file_content=base64.b64decode(base64_file)
    file_content=io.BytesIO(file_content)
    file_content.seek(0)
    return file_content
    
    

def create_json_for_word_functions(js):
    """Creates the json structure needed specifically for GL Groups Egenkontroller protokoll.

    Args:
        js (dict): Json dictionary from POST-request.

    Returns:
        dict: Restructured json-dictionary.
    """
    for item in js['Items']['value']:
        for items in item['Kontrollmoment']:
            #print(item)
            break
    #Moment = [[i['Value'] for i in itemm] for itemm in [item['Kontrollmoment'] for item in js['Items']['value']]]
    #[print(item) for item in Moment]
    bad_keys = ["Bildkommentar","'Återkommande kontroll","Funktionskontroll klar","Test","Egenkontroll klar","Fastighetstyp","Objektnummer" "Egenkontroll klar", "Förvaltare","Ort","Extra tillsyn","Team","Turordning","Objektnummer","Fastighetstyp", \
        "{Identifier}",
"{Thumbnail}",
"{Link}",
"{Name}",
"{FilenameWithExtension}",
"{Path}",
"{FullPath}",
"{HasAttachments}",
"{VersionNumber}",
"Created",
"Author",
"Author#Claims",
"Editor",
"Editor#Claims",
"@odata.etag",
"ItemInternalId",
"ID",
"Title",
"Modified",
"Omr_x00e5_de",
"F_x00f6_rvaltare",
"Kontrollmoment",
"Kontrollmoment@odata.type",
"Kontrollmoment#Id",
"Kontrollmoment#Id@odata.type",
"OData__x00c5_terkommandekontroll",
"Egenkontrollklar",'Test',
"_x00c5_terkommandekontroll",
"Extratillsyn",
"L_x00f6_vhantering"
]
    js['Kontrollmoment'] = [item for item in js['Kontrollmoment'] if item['link'] not in bad_keys]

    links = [i['link'] for i in js['Kontrollmoment']]
    links = ["OData_"+link if link.startswith('_') else link for link in links]
    kontroller = []
    for i, item in enumerate(js['Items']['value']):
        for li in links:
            if li not in item.keys():
                item[li] = True
       # [print(link) for link in links if item[link]]
        kontrollmoment = [link for link in item.keys() if link in links and item[link] and link != "Test"]
        kontrollmoment = [js["Kontrollmoment"][key]["Moment"] for key in range(len(js["Kontrollmoment"])) if js["Kontrollmoment"][key]["link"] in kontrollmoment]
        #[print(item) for item in kontrollmoment]
        kontroller.append({
            "Område": item['Omr_x00e5_de'] + ', ' + item['Ort'],
            "Kommentar":[item["Bildkommentar"] if "Bildkommentar" in item.keys() else ""][0],
            "Klar":["Ja" if item["Egenkontrollklar"] else "Nej"][0],
            "Moment": item['Title']+'\n- '+'\n- '.join(kontrollmoment)
        })
    for item in js['Items']['value']:

        break
    fID = [{"Bild":decode_file(item['Item']), "ID":item["Item_ID"]} for item in js['Attachments']]
    items_list = []
    for item in js['Items']['value']:
        items_list.append([{
            "Bild": fIDItem["Bild"],
            "Område": item['Omr_x00e5_de'] + ', ' + item['Ort'],
            "Bildkommentar":[item["Bildkommentar"] if "Bildkommentar" in item.keys() else ""][0]
        } for fIDItem in fID if fIDItem['ID']==item['ID']])
    komplett_bildlista = []
    for i in items_list:
        for j in i:
            komplett_bildlista.append(j)
    return {"Vecka":str(datetime.datetime.now().isocalendar().week),"Utskriftsdatum":datetime.datetime.now().strftime("%Y-%m-%d"),"images": komplett_bildlista, "content":kontroller}




if __name__ == '__main__':
        
    with open('test.json', 'r', encoding="utf-8") as f:
        js = json.load(f)
    create_json_for_word_functions(js['body'])
        
    