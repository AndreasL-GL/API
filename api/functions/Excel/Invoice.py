import pandas as pd
import base64, io, json, os

def join_pdf_records_and_excel(pdf,excel, type_of_join="inner"):
    excel = pd.read_excel(excel)
    pdf = pd.DataFrame(pdf)
    if "fakturapris" in pdf.keys():
        pdf["Styckpris"] = pdf.pop("fakturapris")
    #excel["Styckpris prislista"] = excel.pop("Pris")
    if "Beskrivning" in excel.columns: excel["Beskrivning prislista"] = excel.pop("Beskrivning")
    df = excel
    #df = replace_column_names(excel)
    df['Artikelnr'] = df['Artikelnr'].astype(str)
    pdf['Artikelnr'] = pdf['Artikelnr'].astype(str)
    mergedf = pd.merge(pdf,df,how=type_of_join,on="Artikelnr")
    return mergedf

def replace_column_names(df):
    if "Benämning" in df.columns:
        df["Beskrivning_prislista"] = df.pop("Benämning")
    if "Benämning MKUgr/Artikel" in df.columns:
        df["Beskrivning_prislista"] = df.pop("Benämning MKUgr/Artikel")
    if "Std-avtal1" in df.columns:
        df["Styckpris_prislista"] = df.pop("Std-avtal1")
    if "ArtNr" in df.columns:
        df["Artikelnr"] = df.pop("ArtNr")
    if "partno" in df.columns:
        df["Artikelnr"] = df.pop("partno")
    if "CLASS8DESCR/PARTDESCR1" in df.columns:
        df["Beskrivning_prislista"] = df.pop("CLASS8DESCR/PARTDESCR1")
    if "Nettopris" in df.columns:
        df["Styckpris_prislista"] = df.pop("Nettopris")
    df = df[["Beskrivning_prislista","Artikelnr","Styckpris_prislista"]]
    return df


def faktura_mot_prislista(js, jointype):
    if not any(js["Items"]): return {"Error": "Could not find any items in invoice."}
    if not jointype: jointype = "inner"
    excel=base64.b64decode(js['Excel'])

    with open(os.path.join(os.path.dirname(__file__),'fsss.xlsx'),'wb') as f:
        f.write(excel)
    df = join_pdf_records_and_excel(js['Items'],excel, jointype)
    file = io.BytesIO()
    df.to_excel(file)
    file.seek(0)
    filename = js["Handlare"]+"_"+js["Fakturanr"]+".xlsx"
    return {"Excel":base64.b64encode(file.getvalue()).decode('utf-8'), "Filename":filename}
    
if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),'xlsx.json'), 'r', encoding='utf-8') as f:
        js = json.load(f)
    file = faktura_mot_prislista(js, 'inner')
    print(file.keys())