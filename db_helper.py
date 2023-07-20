from datetime import datetime, timezone
from connection import create_mongo_connection

client = create_mongo_connection()

db = client["reading"]

def store_data(data):
    for reading in data:
        reading["time"] = datetime.fromtimestamp(int(reading["time"]), tz=timezone.utc).isoformat()

    db.readings.insert_many(data)

def get_data(from_date_str, to_date_str):
    from_date = str(parse_iso_date(from_date_str + "T00:00:00+00:00").replace(tzinfo=timezone.utc))
    to_date = str(parse_iso_date(to_date_str + "T00:00:00+00:00").replace(tzinfo=timezone.utc))

    query = {
        "time": {
            "$gte": from_date,
            "$lt": to_date
        }
    }
    readings = list(db.readings.find(query, {"_id": 0}))
    for reading in readings:
        timestamp = reading["time"]
        reading["time"] = timestamp

    return readings

def parse_iso_date(date_str):
    return datetime.fromisoformat(date_str)
