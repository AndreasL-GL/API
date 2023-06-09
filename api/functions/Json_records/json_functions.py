import pandas as pd
from fuzzywuzzy import fuzz
import base64, io, json, os
import docx
import logging
from functions.return_power_automate_file import detect_and_create_file

log = logging.getLogger('info_logger')

def join_pdf_records_and_excel(pdf,excel, type_of_join="inner"):
    excel = pd.read_excel(excel)
    pdf = pd.DataFrame(pdf)
    if "Pris" in excel.columns:
        excel['Styckpris_prislista'] = excel.pop('Pris')
    if "fakturapris" in pdf.keys():
        pdf["Styckpris"] = pdf.pop("fakturapris")
    #excel["Styckpris prislista"] = excel.pop("Pris")
    if "Beskrivning" in excel.columns: excel["Beskrivning prislista"] = excel.pop("Beskrivning")
    df = excel
    #df = replace_column_names(excel)
    if df['Artikelnr'].dtype == 'Float64':
        df["Artikelnr"] = df["Artikelnr"].astype(int)
    if pdf['Artikelnr'].dtype == 'Float64':
        pdf["Artikelnr"] = pdf["Artikelnr"].astype(int)
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

    df = join_pdf_records_and_excel(js['Items'],excel, jointype)
    if df.empty: return {"Excel":"None"}
    file= io.BytesIO()
    df.to_excel(file)
    file.seek(0)
    
    file = change_column_size_before_saving(df)
    filename = js["Handlare"]+"_"+js["Fakturanr"]+".xlsx"
    return {"Excel":base64.b64encode(file.getvalue()).decode('utf-8'), "Filename":filename}

def change_column_size_before_saving(df):
    file = io.BytesIO()
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('Sheet1')
    for i, column in enumerate(df.columns):
        column_width = len(str(column)) * 1.1
        worksheet.set_column(i, i, column_width)
    writer.close()
    file.seek(0)
    return file

def set_main_columns(excel):
    if len(excel) < 14: return "ERROR: No content in excel file."
    excel = pd.read_excel(base64.b64decode(excel))
    if "Kvantitet" not in excel.columns: excel["Kvantitet"] = 1
    excel = excel[["Styckpris","Artikelnr","Beskrivning","Kvantitet","Styckpris_prislista"]]
    excel["Prisskillnad"] = excel["Styckpris_prislista"] -  excel["Styckpris"].apply(lambda x:float(str(x).replace(',','.').replace(' ', '')))
    excel["Kvantitet"] =  excel["Kvantitet"].apply(lambda x:float(str(x).replace(',','.').replace(' ', '')))
    excel["Summa Prisskillnad"] = excel["Prisskillnad"].mul(excel["Kvantitet"])
    excel.loc[excel.index[-1] + 1, 'Summa Prisskillnad'] = excel["Summa Prisskillnad"].sum()
    excel.at[excel.index[-1], 'Beskrivning'] = " SUMMA"
    exio = io.BytesIO()
    excel.to_excel(exio)
    exio.seek(0)
    exio = change_column_size_before_saving(excel)
    return base64.b64encode(exio.getvalue()).decode('utf-8')

def fuzzy_merge(df1,df2, column1='Beskrivning',column2='CLASS8DESCR/PARTDESCR1'):
    df1 = pd.read_excel(io.BytesIO(base64.b64decode(df1)))
    df2 = pd.read_excel(io.BytesIO(base64.b64decode(df2)))
    def find_best_match(row1):
        scores = df2['column_name'].apply(lambda x: fuzz.ratio(row1['column_name'], x))
        best_match_index = scores.idxmax()
        best_score = scores.loc[best_match_index]

        if best_score:  # Set a threshold for the match score
            return row1.tolist() + df2.loc[best_match_index].tolist()
    df1 = df1.rename(columns={column1: 'column_name'})
    df2 = df2.rename(columns={column2: 'column_name'})

    joined_data = df1.apply(find_best_match, axis=1).tolist()
    joined_df = pd.DataFrame(joined_data, columns=df1.columns.tolist() + df2.columns.tolist())
    
    # joined_df[column1] = joined_df.pop('column_name')
    return joined_df

def convert_excel_table_to_json(file):
    file = base64.b64decode(file["$content"])
    file = io.BytesIO(file)
    file.seek(0)
    df = pd.read_excel(file)

    return json.loads(df.to_json(orient="records", force_ascii=False))


def join_json_records(prislista1,prislista2, left_on=["pris"], right_on=["pris"], how = 'inner'):
    prislista1,prislista2 = json.loads(prislista1) if type(prislista1) == str else prislista1, json.loads(prislista2) if type(prislista2) == str else prislista2
    con1,con2 = not any([left_on[0] in key.keys() for key in prislista1]),not any([right_on[0] in key.keys() for key in prislista2])
    if con1 or con2:
        return {"Error": f"Kolumnnamnet saknas i Prislista: {'1' if con1 and not con2 else '2' if con2 and not con1 else '1, 2'}"}
    P1 = pd.DataFrame(prislista1)
    P2 = pd.DataFrame(prislista2)
    
    P3 = pd.merge(P1,P2,how=how, left_on=left_on,right_on=right_on)
    
    return json.loads(P3.to_json(orient="records", force_ascii=False))
    
def transform_text_to_float(num):
    num = str(num).replace(',','.').replace(' ', '').replace('$','')
    num = ''.join(['' if char.isalpha() else char for char  in num])
    return float(num) if int(float(num)) != float(num) else int(float(num))
    
def fakturaanalys_v2(js, how = "left", left_on="Artikelnr",right_on="Artikelnr"):
    excel = js["Excel"]
    faktura = js["Faktura"]
    items = pd.DataFrame([
        {
            "Artikelnr": transform_text_to_float(item["fields"]["productCode"]["valueText"]),
            "Styckpris":transform_text_to_float(item["fields"]["unitPrice"]["valueText"]),
            "Beskrivning":item["fields"]["description"]["valueText"],
            "Kvantitet": transform_text_to_float(item["fields"]["quantity"]["valueText"])
            
            } 
        for item in faktura["Items"] if "productCode" in item['fields'].keys()
        ])

    for i,item in enumerate(excel):
        name = item["Name"]
        df = pd.DataFrame(json.loads(item["File"]))

        #print(items["Artikelnr"].dtype, str(df["Artikelnr"].dtype))
        items['Artikelnr'] = items['Artikelnr'].astype('str')
        df['Artikelnr'] = df['Artikelnr'].astype('str')

        items = pd.merge(items, df, how=how, left_on=left_on, right_on=right_on, suffixes = [f" (Faktura)" if i==0 else f" ({excel[i-1]['Name']})",f" ({item['Name']})"])
    print(type(items))
    items = items.dropna(axis=1, how='all')
    if any(excel):
        return {"File Content":detect_and_create_file(items,'.xlsx'), "Filename": str(js['Faktura']["Handlare"])+"_"+str(js['Faktura']["Fakturanr"])+".xlsx"}
    
if __name__ == '__main__':
    from functions.download_file import run_file
    with open(os.path.join(os.path.dirname(__file__),"fakturaanalysv2.json"), 'r', encoding='utf-8') as f:
        js = json.load(f)
    d = fakturaanalys_v2(js['body']) if 'body' in js.keys() else fakturaanalys_v2(js)
    run_file(base64.b64decode(d['File Content']['$content']))
    
    #file = detect_and_create_file(df,content_type='.xlsx')
    #print(df)
    #print(df.columns)
    