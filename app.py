from flask import Flask
from flask import g
import simplejson as json
from flask import request
from DBMaster import DBMaster
import os
from flask import render_template
from flask import jsonify

app=Flask(__name__)


@app.before_request
def db_connect():
    g.dbHandler=DBMaster()

@app.after_request
def db_disconnect(response):
    g.dbHandler.closeConnection()
    return response

# @app.route('/')
# def getHomePage():
#     return render_template('index.html')
#
#
# @app.route('/home')
# def homePage():
#     return render_template('index.html')

@app.route('/autoComplete',methods=['POST'])
def autoComplete():
    req_json = request.get_json()
    result=g.dbHandler.autoComplete(req_json)
    return json.dumps({"courses":result})

@app.route('/search',methods=['POST'])
def search():
    req_json=request.get_json()
    result=g.dbHandler.search(req_json)
    return jsonify({"airports":result})



if __name__ == "__main__":
    app.run(debug=True)