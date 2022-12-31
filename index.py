import requests, json
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, make_response, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>楊子青Firestore資料庫存取，提供webhook</h1>"
    homepage += "<a href=/movie>讀取開眼電影即將上映影片，寫入Firestore</a><br><br>"
    homepage += "<a href=/query>電影查詢</a><br>"
    return homepage

@app.route("/webhook", methods=["POST"])
def webhook1():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req["queryResult"]["action"]
    msg =  req["queryResult"]["queryText"]
    info = "動作：" + action + "； 查詢內容：" + msg
    return make_response(jsonify({"fulfillmentText": info}))




if __name__ == "__main__":
    app.run()