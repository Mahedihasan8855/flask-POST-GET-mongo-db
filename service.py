from db_helper import store_data, get_data

class ReadingService:
    @staticmethod
    def store_readings(data):
        try:
            readings = parse_data(data)
            store_data(readings)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def retrieve_readings(from_date_str, to_date_str):
        try:
            data = get_data(from_date_str, to_date_str)
            return data
        except Exception as e:
            print(e)
            return []

def parse_data(data):
    lines = data.strip().split("\n")
    readings = []
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            timestamp = parts[0]
            name = parts[1]
            value = float(parts[2])
            reading = {"time": timestamp, "name": name, "value": value}
            readings.append(reading)
    return readings
