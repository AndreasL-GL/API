from flask import Flask, render_template, request, jsonify, abort
import configparser
import os

from functions.SQL_commands import Sql
from image_api_blueprints import image_resize
from flow_tools_blueprints import flow_starting_page, get_sharepoint_columns_, get_kontrollmoment
from excel_tools_blueprints import excel_dagbok, fakturaextraktion
from blueprints_word import word_path
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(__file__),'config'),"config.ini"))

app = Flask(__name__)
app.secret_key = config["DEFAULTS"]["SECRET_KEY"]
app.register_blueprint(word_path)
app.register_blueprint(image_resize)
app.register_blueprint(flow_starting_page)
app.register_blueprint(get_sharepoint_columns_)
app.register_blueprint(get_kontrollmoment)
app.register_blueprint(excel_dagbok)
app.register_blueprint(fakturaextraktion)

@app.route("/", methods=['GET', 'POST'])
def Home():
    Sql.initialize_db()
    return render_template('home.html')

@app.route("/help")
def help():
    return jsonify(eval(config["DEFAULTS"]["API_KEYS"]))

@app.before_request
def limit_remote_addr():
    print(config["ACCEPT_CONNECTIONS_FROM"])
    client_list = [x for x in config["ACCEPT_CONNECTIONS_FROM"]]
    if any(client_list):
        if any(client_list) and request.remote_addr not in client_list:
            abort(403)  # Forbidden
        
        
@app.route("/api")
def api():
    return render_template("api_description.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
