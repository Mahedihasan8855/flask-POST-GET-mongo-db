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

    return readings

def parse_iso_date(date_str):
    return datetime.fromisoformat(date_str)

if __name__ == "__main__":
    sample_data = [
        {"time": "1649941817", "name": "Voltage", "value": 1.34},
        {"time": "1649941817", "name": "Voltage", "value": 1.35},
    ]

    # Store sample data in MongoDB (uncomment to store the data)
    store_data(sample_data)

    from_date_str = "2022-04-10"
    to_date_str = "2022-04-16"
    data_within_date_range = get_data(from_date_str, to_date_str)

    print("Data within date range:", data_within_date_range)
