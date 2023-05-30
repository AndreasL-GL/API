import pandas as pd
import base64, io

def join_pdf_records_and_excel(pdf,excel, type_of_join="inner"):
    excel = pd.read_excel(excel, engine="openpyxl")
    pdf = pd.DataFrame(pdf['Items'])
    if "fakturapris" in pdf.keys():
        pdf["Styckpris"] = pdf.pop("fakturapris")
    print(pdf.head())
    df = replace_column_names(excel)
    mergedf = pd.merge(pdf,df,how=type_of_join,on="Artikelnr")
    print(mergedf.head())
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
    print(df.columns)
    return df


def faktura_mot_prislista(js, jointype):
    if not jointype:jointype = "inner"
    excel = io.BytesIO(base64.b64decode(js['Excel']))
    excel.seek(0)
    df = join_pdf_records_and_excel(js['Items'],excel, jointype)
    file = io.BytesIO()
    df.to_excel(file)
    file.seek(0)
    filename = js["Handlare"]+"_"+js["Fakturanr"]+".xlsx"
    return {"Excel":base64.b64encode(file.getvalue()).decode('utf-8'), "Filename":filename}
    