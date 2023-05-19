from bs4 import BeautifulSoup
import os
import zipfile
import io

def fix_excel_file(xlsx_data):
    with zipfile.ZipFile(io.BytesIO(xlsx_data), mode='r') as zf:

        sheet1_data = zf.read('xl/worksheets/sheet1.xml').decode('utf-8')

        soup = BeautifulSoup(sheet1_data, 'xml')

        functions = soup.find_all("f")
        for f in functions:
            if "!" in f.text:
                print(f.text)
                f.extract()
        files = {x: zf.read(x) for x in zf.namelist()}
        modified_sheet1_data = str(soup)
        files['xl/worksheets/sheet1.xml'] = modified_sheet1_data

    # Create a new in-memory ZipFile object
    output_zip = io.BytesIO()
    with zipfile.ZipFile(output_zip, mode='w') as zkf:
        for name, file in files.items():
            # Add each file to the new zipfile
            zkf.writestr(name, file)

    # Reset the output_zip's file pointer to the beginning
    output_zip.seek(0)
    return output_zip