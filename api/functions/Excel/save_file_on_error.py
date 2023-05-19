from flask import request, jsonify, abort
import base64
import io
import datetime, os, inspect
def get_file_from_content():
    # Get the file from the request
    file_data = request.files
    file_data = request.get_data()
    file = io.BytesIO(file_data)
    
    filebytes = io.BytesIO()
    filebytes.write(file.getvalue())
    filebytes.seek(0)
    return filebytes
    
def return_file_as_base64(file):
    filename = request.json.get('filename')
    content = request.json.get('content')
    file_content_base64 = base64.b64encode(file.read()).decode('utf-8')
    return jsonify(file_content_base64)

def save_file_on_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
            arg_names = inspect.getfullargspec(func)[0]
            if "filename" in arg_names:file_name_index=arg_names[arg_names.index("filename")]
            if "file" in arg_names:bytesfile=args[arg_names[arg_names.index("file")]]
            elif "bytefile" in arg_names:bytesfile=args[arg_names[arg_names.index("bytefile")]]
            else: bytesfile=args[0]
            if len(args>1): file_name=f"{func.__name__}_{timestamp}_{args[file_name_index]}"
            file_name = f"{func.__name__}_{timestamp}.xlsx"
            file_name = os.path.join(os.path.join(os.path.dirname(__file__),'errors'),file_name)
            
            with open(file_name, 'wb') as f:
                f.write(bytesfile)
            with open(file_name.split('.')[0]+'_logfile.txt', 'wb') as f:
                f.write(str(e))
            abort(f"An error occurred while executing {func.__name__}.\n{str(e)}")
    return wrapper