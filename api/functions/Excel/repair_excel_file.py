import io, os

def repair_excel_file(file):
    import  jpype     
    import  asposecells     
    jpype.startJVM() 
    from asposecells.api import Workbook, Cells
    
    workbook = Workbook(file)
    workbook.save(file)
    jpype.shutdownJVM()
    return file
