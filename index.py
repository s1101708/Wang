from flask import Flask, render_template, request, make_response, jsonify 
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials. Certificate("serviceAccountKey.json")
firebase_admin.initialize_app (cred)
db = firestore.client()
app = Flask(__name__)

@app.route("/")
def index():
  homepage  = "<h1>Python讀取Firestore</h1>"
  homepage += "<a href=/search>Mc</a><br><br>"
  return homepage


@app.route("/webhook", methods=["POST"])
def webhook():
  # build a request object
  req = request.get_json(force=True) 
  # fetch queryResult from json
  action = req.get("queryResult").get("action")
  # msg = req.get("queryResult").get("queryText") 
  #info = "動作: " + action + "; 查詢內容: " + msg
  if(action == "choice"):
    flavor = req.get("queryResult").get("parameters").get("flavor") 
    info = "您選擇的口味是:" + flavor + ",相關資料:\n\n"
    collection_ref = db.collection("樂事餅乾")
    docs = collection_ref.get()
    result = ""
    for doc in docs:
      dict = doc.to_dict()
      if flavor in dict["flavor"]:
        result += "品名:" + dict["name"] + "\n\n"
        result += "口味:" + dict["flavor"] + "\n\n"
        result += "介紹:" + dict["intro"] + "\n\n"
    info += result
  return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()


