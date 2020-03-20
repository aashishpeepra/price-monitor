import flask
from flask import jsonify as json
app=flask.Flask(__name__)
@app.route("/",methods=["GET"])
def home():
    return json({"message":"works"})

if __name__=="__main__":
    app.run()