from flask import Flask, request, render_template
from flask_pymongo import PyMongo
import json

colors = [
    {"name": "yellow", "description": "like shining gold"},
    {"name": "blue", "description": "like the ocean"},
    {"name": "red", "description": "like passion"},
]

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "flask-colors"
app.config[
    "MONGO_URI"] = "mongodb://<user>:<pass>@ds125821.mlab.com:25821/flask-colors"

mongo = PyMongo(app)


@app.route("/")
def index():
    return "Hello to colors API-REST: /colors GET-ALL , \
    		/colors/name A COLOR, /colors POST-ONE, \
    		/colors/name PUT-ONE, /colors/name DELETE-ONE"


@app.route("/colors", methods=["GET"])
def returnAll():
    colors = mongo.db.colors
    output = []


    for color in colors.find():

        output.append({"name": color["name"], "description": color["description"]})

    return json.dumps({"colors":output})

    # return json.dumps({"colors": colors})


@app.route("/colors/<string:name>", methods=["GET"])
def returnOne(name):
    colors = mongo.db.colors

    q = colors.find_one({"name" : name})
    output = {"name": q["name"], "description": q["description"]}
    return json.dumps({"color": output})


@app.route("/colors", methods=["POST"])
def addOne():
    colors = mongo.db.colors
    color = {
        "name": request.json["name"],
        "description": request.json["description"],
    }
    
    color = colors.insert({"name":color["name"], "description":color["description"]})
    
    new_color = colors.find_one({"_id":color})

    output = {"name": new_color["name"], "description":new_color["description"]}
    print(output)
   
    return json.dumps({"result": output})


@app.route("/colors/<string:name>", methods=["PUT"])
def editOne(name):
    #: color es una referencia a colors
    #: si cambio actualizara colors
    colors = mongo.db.colors
    color = colors.find_one({"name":name})
    
    """color = [color for color in colors if color["name"] == name]
    color[0]["name"] = request.json["name"]
    color[0]["description"] = request.json["description"]
    """
    color["name"] = request.json["name"]
    color["description"] = request.json["description"]

    colors.save(color)

    updated_color = {"name":color["name"], "description":color["description"]}

    return json.dumps({"result": updated_color})


@app.route("/colors/<string:name>", methods=["DELETE"])
def deleteOne(name):
    colors = mongo.db.colors
    print(colors)
    output = []
    

    delete_color = colors.find_one({"name":name})
    colors.remove(delete_color)
    """
    color = [color for color in colors if color["name"] == name]
    colors.remove(color[0])
    """
    colors = mongo.db.colors
    for color in colors.find():
        output.append({"name": color["name"], "description": color["description"]})
    return json.dumps({"colors":output})

if __name__ == "__main__":
    app.run(debug=True)
