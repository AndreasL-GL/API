## Project name: GL API
### Description:
This Project assumes the developer has some basic understanding of programming in python and Flask.
There are many different libraries in use and these vary mainly in the functions-section.

#### Routes:
All routes are specified in the files ending with 'blueprint.py' : '{api_section}_blueprint.py'
Inside are the relevant Flask Blueprints that are being called in app.py for each api section

#### Functions:
All simple functions are located in the folder functions. See readme-functions.md in ./functions.

#### How do I add a route?
To add a route blueprint, simply copy the structure showed in the blueprints, or use this example:
´´
from flask import Blueprint, render_template

route_blueprint = Blueprint('myroute', __name__)
@route_blueprint.route("/myroute", methods=["POST"])
@require_api_key # Optional
def myroute():
    return render_template("myroute.html")
´´
Remember to add this to the file "app.py"
´´
from YOUR_FILE import route_blueprint
app.register_blueprint(route_blueprint)
´´

#### How do I add a function?
Functions are usually just called inside the route function.
So like standard python code, import the function in the blueprint file and run it inside your route.
All functions are stored inside root/functions for simplicity.

#### Configurations and Environment variables
To not make it too complicated and hard to navigate, all configuration and environment variables are set in the config.ini file inside the config folder.