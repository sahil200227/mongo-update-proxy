from pymongo import MongoClient
from bson import ObjectId
import datetime, os, json

def handler(request, response):
    try:
        if request.method != "POST":
            response.status_code = 405
            response.send("Method not allowed")
            return

        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            response.status_code = 500
            response.send("Missing MONGO_URI environment variable")
            return

        client = MongoClient(mongo_uri)
        db = client["jobcrm"]
        col = db["campaign_recipients"]

        body = json.loads(request.body or "{}")
        if "_id" not in body:
            response.status_code = 400
            response.send("Missing _id in request")
            return

        oid = ObjectId(body["_id"])
        update_fields = {
            "status": body.get("status", "sent"),
            "last_sent_at": datetime.datetime.utcnow()
        }

        result = col.update_one({"_id": oid}, {"$set": update_fields})
        client.close()

        response.status_code = 200
        response.send(json.dumps({
            "matchedCount": result.matched_count,
            "modifiedCount": result.modified_count
        }))
    except Exception as e:
        response.status_code = 500
        response.send(str(e))

