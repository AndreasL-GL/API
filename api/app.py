from flask import Flask, render_template, request, jsonify, abort
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

logging.basicConfig(filename=os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'flask_app.log'),level=logging.INFO)
#logging.basicConfig(filename=os.path.join(os.path.dirname(__file__),'error.log'),level=logging.ERROR)
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(__file__),'config'),"config.ini"))
# Create loggers
error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('info_logger')

# Set log levels
error_logger.setLevel(logging.ERROR)
info_logger.setLevel(logging.INFO)

# Create file handlers for each log file
error_handler = logging.FileHandler(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'error.log'))
info_handler = logging.FileHandler(os.path.join(os.path.join(os.path.dirname(__file__),"logs"),'info.log'))
# Create formatters for the log messages


error_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
info_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
conn_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
# Set formatters for the handlers
error_handler.setFormatter(error_formatter)
info_handler.setFormatter(info_formatter)





# Add handler to the logger

# Add handlers to the loggers
error_logger.addHandler(error_handler)
info_logger.addHandler(info_handler)



app = Flask(__name__)
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





@app.route("/", methods=['GET', 'POST'])
def Home():
    sql = Sql()
    sql.initialize_db()
    #return render_template('home.html')


@app.before_request
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
            print(data)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()
    info_logger.info(request.data.decode())
            
    client_list = [x for x in config["ACCEPT_CONNECTIONS_FROM"]]

    json_logger()

    if any(client_list):
        if any(client_list) and request.remote_addr not in client_list:
            abort(403)  # Forbidden
        
        
@app.route("/api/Json2Word")
def api():
    return render_template("Json2Word.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)