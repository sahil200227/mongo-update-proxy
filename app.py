# api/update.py
from pymongo import MongoClient
from bson import ObjectId
import datetime
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# connect to your MongoDB Atlas cluster
client = MongoClient(os.environ["MONGO_URI"])
db = client["jobcrm"]
col = db["campaign_recipients"]

@app.route("/update", methods=["POST"])
def update_document():
    data = request.get_json()
    try:
        oid = ObjectId(data["_id"])
    except Exception:
        return jsonify({"error": "Invalid _id"}), 400

    update_fields = {
        "status": data.get("status", "sent"),
        "last_sent_at": datetime.datetime.utcnow()
    }

    result = col.update_one({"_id": oid}, {"$set": update_fields})
    return jsonify({"matchedCount": result.matched_count, "modifiedCount": result.modified_count})
