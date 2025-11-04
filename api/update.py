from pymongo import MongoClient
from bson import ObjectId
import datetime, os, json

client = MongoClient(os.environ["MONGO_URI"])
db = client["jobcrm"]
col = db["campaign_recipients"]

def handler(request, response):
    if request.method != "POST":
        response.status_code = 405
        return response.send("Method not allowed")

    body = json.loads(request.body or "{}")
    if "_id" not in body:
        response.status_code = 400
        return response.send("Missing _id")

    try:
        oid = ObjectId(body["_id"])
    except Exception:
        response.status_code = 400
        return response.send("Invalid _id")

    update_fields = {
        "status": body.get("status", "sent"),
        "last_sent_at": datetime.datetime.utcnow()
    }

    result = col.update_one({"_id": oid}, {"$set": update_fields})
    response.status_code = 200
    response.send(json.dumps({
        "matchedCount": result.matched_count,
        "modifiedCount": result.modified_count
    }))
