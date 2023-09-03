from flask import Flask, render_template, request, jsonify, abort, send_from_directory
import configparser
import os
import requests

from functions.SQL_commands import Sql
from image_api_blueprints import image_resize
from flow_tools_blueprints import flow_starting_page, get_sharepoint_columns_, get_kontrollmoment
from excel_tools_blueprints import excel_dagbok, fakturaextraktion
from blueprints_word import word_path
from html_pages_blueprints import html_pages
from blueprints_sharepoint import sharepoint
import logging, json
from flask import Flask
import datetime
import sys
# Configure logging
import Printer
from Printer import log, error_log
#logging.basicConfig(filename=os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'flask_app.log'),level=logging.INFO)
#logging.basicConfig(filename=os.path.join(os.path.dirname(__file__),'error.log'),level=logging.ERROR)
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(__file__),'config'),"config.ini"))
# Create loggers
#error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('info_logger')
request_logger = logging.getLogger("request_logger")

# Set log levels
#error_logger.setLevel(logging.ERROR)
info_logger.setLevel(logging.INFO)
request_logger.setLevel(logging.INFO)

# Create file handlers for each log file
##error_handler = logging.FileHandler(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'error.log'))
info_handler = logging.FileHandler(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'info.log'))
request_handler = logging.FileHandler(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'responses.log'))
# Create formatters for the log messages


error_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
info_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
conn_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
request_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
# Set formatters for the handlers
#error_handler.setFormatter(error_formatter)
info_handler.setFormatter(info_formatter)
request_handler.setFormatter(request_formatter)

# Create a file handler for logging
file_handler = logging.FileHandler('logs/flask.log')

# Configure the log format
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the root logger
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)


# Add handler to the logger

# Add handlers to the loggers
#error_logger.addHandler(error_handler)
info_logger.addHandler(info_handler)
request_logger.addHandler(request_handler)



app = Flask(__name__,static_folder='static')
app.secret_key = config["DEFAULTS"]["SECRET_KEY"]
app.register_blueprint(word_path)
app.register_blueprint(image_resize)
app.register_blueprint(flow_starting_page)
app.register_blueprint(get_sharepoint_columns_)
app.register_blueprint(get_kontrollmoment)
app.register_blueprint(excel_dagbok)
app.register_blueprint(fakturaextraktion)
app.register_blueprint(html_pages)
app.register_blueprint(sharepoint)




@error_log
@app.route("/", methods=['GET', 'POST'])
def Home():
    sql = Sql()
    sql.initialize_db()



    return render_template('home.html')


#@app.before_request
def limit_remote_addr():
    def json_logger(js = {
        'Time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Remote Adress':request.remote_addr,
        'User-Agent':str(request.user_agent),
        'Method':request.method,
        'URL': request.base_url,
        'Args':dict(request.args),
        'Headers':dict(request.headers),
        'Endpoint':request.endpoint,
        'Content-type':str(type(request.data))}, logfile = "connections.json"):
        data = " "
        if not os.path.exists(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),logfile)):
            with open(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),logfile), 'w', encoding='utf-8') as f: 
                json.dump([],f, ensure_ascii=False)
                data = []
                f.close()
        if type(data)==str:
            with open(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),logfile), 'r', encoding='utf-8') as f:
                #print(f.read())
                data = json.load(f)
                f.close()
        with open(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),logfile), 'w', encoding='utf-8') as f:
            data.append(js)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()
            
    client_list = [x for x in config["ACCEPT_CONNECTIONS_FROM"]]

    json_logger()

    if any(client_list):
        if any(client_list) and request.remote_addr not in client_list:
            abort(403)  # Forbidden
        
@app.after_request
def log_finished_request(response):
    
    request_logger.info("Response: "+ str(request.user_agent)+ " Endpoint: " + str(request.endpoint)+" Status Code: " + str(response.status_code))
    return response
    
@app.route("/api/Json2Word")
def api():
    return render_template("Json2Word.html")



if __name__ == '__main__':
    error_file = open(os.path.join(os.path.join(os.path.dirname(__file__),'logs'),'errors.txt'),'a')
    sys.stderr = error_file
    app.run(debug=True, host='0.0.0.0', port=5000)
    