import os, datetime
printfile = os.path.join(os.path.join(os.path.dirname(__file__),'logs'),'prints.txt')
error_file = os.path.join(os.path.join(os.path.dirname(__file__),'logs'),'error.txt')
#exec(f"""import sys\nimport os\nimport builtins\ncaller_module = sys.modules['__main__']\ncaller_file = os.path.basename(caller_module.__file__)\noprint = builtins.print\ndef custom_print(*args, **kwargs):\n    with open(r'{printfile}', 'a') as file:\n        oprint("Print from file: ",caller_file, file=file)\n        oprint("_______________________________________", file=file)\n        oprint(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S "), file=file)\n        oprint(*args, **kwargs, file=file)\n        oprint("_______________________________________", file=file)\n        oprint(*args, **kwargs)\nbuiltins.print = custom_print""")

import sys
import os
import builtins
import inspect
from colorama import Fore,Back,Style
import traceback
caller_module = sys.modules['__main__']
caller_file = os.path.basename(caller_module.__file__)
oprint = builtins.print
def log(*args, **kwargs):
    with open(printfile, 'a') as file:
        
        function_name = inspect.currentframe().f_back.f_code.co_name
        oprint("Print from file: ",caller_file,"Function: ",function_name, file=file)
        oprint("_______________________________________", file=file)
        oprint(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S "), file=file)
        oprint(*args, **kwargs, file=file)
        oprint("_______________________________________", file=file)
        oprint(Fore.LIGHTCYAN_EX,"Print from file: ",caller_file,"Function: ",function_name, Style.RESET_ALL)
        oprint(Fore.LIGHTBLUE_EX,"_______________________________________")
        oprint(Fore.YELLOW,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S "),Style.RESET_ALL)
        oprint(Fore.YELLOW,*args,Style.RESET_ALL)
        oprint(Fore.LIGHTBLUE_EX,"_______________________________________",Style.RESET_ALL)
#builtins.print = log




def log_errors(*args, **kwargs):
    with open(error_file, 'a') as file:
        
        function_name = inspect.currentframe().f_back.f_code.co_name
        oprint("Print from file: ",caller_file,"Function: ",function_name, file=file)
        oprint("_______________________________________", file=file)
        oprint(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S "), file=file)
        oprint(*args, **kwargs, file=file)
        oprint("_______________________________________", file=file)
        oprint(Fore.LIGHTCYAN_EX,"Print from file: ",caller_file,"Function: ",function_name, Style.RESET_ALL)
        oprint(Fore.LIGHTBLUE_EX,"_______________________________________")
        oprint(Fore.YELLOW,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S "),Style.RESET_ALL)
        oprint(Fore.YELLOW,*args,Style.RESET_ALL)
        oprint(Fore.LIGHTBLUE_EX,"_______________________________________",Style.RESET_ALL)
def error_log(func):
    def wrapper(*args, **kwargs):
        
        try: return func(*args, **kwargs)
        except Exception as e: 
            errorstr = "".join(traceback.format_exception(e))
            log_errors(errorstr)
        

    return wrapper
if __name__ == '__main__':
    pass
        