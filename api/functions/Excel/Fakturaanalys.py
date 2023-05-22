import pandas as pd
import json
import io
import base64
import os



def read_BVB(cdf):
    df = pd.read_excel(os.path.join(os.path.dirname(__file__),"Kopia av Mall BVB - Huvudkund.xlsx"), sheet_name="Klistra in från MS-report", header=None)
    df.columns = df.iloc[4]
    df = df[5:]
    df.loc[df['Kvantitet']==0, 'Kvantitet'] = 1
    df['á pris'] = df['Omsättning']/df['Kvantitet']
    df.reset_index(drop=True, inplace=True)
    df = df[df['Artikelnr'].isin(cdf['Artikelnr'])]
    return df

def read_kundavtal(cdf):
    df=pd.read_excel(os.path.join(os.path.dirname(__file__),'Kundavtal-standardavtal.xlsx'), header = None)
    df.columns = df.iloc[1]
    df = df[2:]
    df = df.loc[df['Typ']!='Procent']
    df.reset_index(drop=True,inplace=True)
    df = df[df['partno'].isin(cdf['Artikelnr'])]
    return df

def merge_tables(cdf):
    df = read_BVB(cdf)
    #cdf = df[['Artikelnr','Artikelben1']]

    df2 = read_kundavtal(cdf)
    df = df[['á pris', 'Artikelnr', 'Artikelben1']]
    df = df.reindex(columns = ['Artikelnr', 'Artikelben1','á pris'])
    df.columns = ['Artikelnr','Benämning_BVB','pris_BVB']
    df2 = df2[['Std-avtal1', "CLASS8DESCR/PARTDESCR1", "partno"]]
    df2.columns = ['pris_centralt', "Beskrivning_centralt", "Artikelnr"]

    merged_dataframe = pd.merge(df, df2, on='Artikelnr', how='left')
    merged_dataframe = merged_dataframe.reindex(columns=['Artikelnr', 'Benämning_BVB','Beskrivning_centralt','pris_BVB', 'pris_centralt'])
    
    merged_dataframe = pd.merge(merged_dataframe,cdf, on='Artikelnr', how='inner')
    
    merged_dataframe['pris_centralt'] = pd.to_numeric(merged_dataframe['pris_centralt'], errors='coerce')
    merged_dataframe['Kvantitet'] = merged_dataframe['Kvantitet'].map(lambda x: int(x.split(',')[0]))
    merged_dataframe['Kvantitet'] = pd.to_numeric(merged_dataframe['Kvantitet'], errors='coerce')
    merged_dataframe['Summa'] = merged_dataframe['Summa'].map(lambda x: float(x.replace(',','.').replace(' ','')))
    
    
    merged_dataframe['pris_BVB'] = pd.to_numeric(merged_dataframe['pris_BVB'], errors='coerce')
    merged_dataframe['Summa_BVB'] = merged_dataframe['Kvantitet']*merged_dataframe['pris_BVB']
    merged_dataframe['Summa_centralt'] = merged_dataframe['Kvantitet']*merged_dataframe['pris_centralt']
    merged_dataframe.pop("Benämning_BVB")
    merged_dataframe.pop("Beskrivning_centralt")
    merged_dataframe=merged_dataframe.reindex(columns=['Artikelnr','Benämning', 'pris_BVB', 'pris_centralt', 'fakturapris', 
       'Kvantitet', 'Summa', 'Summa_BVB', 'Summa_centralt'])
    merged_dataframe['skillnad'] = merged_dataframe['pris_BVB']-merged_dataframe['fakturapris'].map(lambda x: float(x.replace(',','.').replace(' ','')))
    return merged_dataframe

def process_request(js):
    cdf = pd.read_json(json.dumps(js['Items']))
    df = merge_tables(cdf)
    
    column_totals = df[['Summa','Summa_BVB','Summa_centralt']].sum()

    df = pd.concat([df,column_totals])
    df.pop(0)
    df.columns = [column.replace('_',' ') for column in df.columns]
    df = df.style.apply(highlight_cells, axis=1)
    file = change_column_size_before_saving(df)
    filename = js['Handlare'] + str(js['ID']) + str(js['Datum'])
    return {"content":base64.b64encode(file.getvalue()).decode('utf-8'), "filename":filename}

def highlight_cells(row):
    if float(str(row['fakturapris']).replace(',','.').replace(' ', '')) > float(str(row['pris BVB']).replace(',','.').replace(' ', '')):
        return ['background-color: orange'] * len(row)
    elif float(str(row['fakturapris']).replace(',','.').replace(' ', '')) > float(str(row['pris centralt']).replace(',','.').replace(' ', '')):
        return ['background-color: red'] * len(row)
    else: return ['background-color: green'] * len(row)

def change_column_size_before_saving(df):
    file = io.BytesIO()
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Get the workbook and active worksheet objects
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('Sheet1')

    # Iterate over each column and set the column width to 1.2 times the default width
    for i, column in enumerate(df.columns):
        column_width = len(str(column)) * 1.2
        worksheet.set_column(i, i, column_width)

    # Save the modified Excel file
    writer.close()
    file.seek(0)
    return file
if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),'request.json'), 'r', encoding='utf-8') as f:
        js = json.load(f)
    file = process_request(js)
    with open(os.path.join(os.path.dirname(__file__),'test2.xlsx'), 'wb') as f:
        f.write(base64.b64decode(file["content"]).decode('utf-8'))
        