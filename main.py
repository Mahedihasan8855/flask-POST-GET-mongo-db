from flask import Flask, request, jsonify
from service import ReadingService


service = ReadingService()
app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_data(as_text=True)
        print("data", data)
        success = service.store_readings(data)

        if success:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 400

    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        from_date_str = request.args.get('from')
        to_date_str = request.args.get('to')

        if not from_date_str or not to_date_str:
            return jsonify({"success": False, "message": "Both 'from' and 'to' parameters are required."}), 400

        data = service.retrieve_readings(from_date_str, to_date_str)
        return jsonify(data), 200

    except ValueError as e:
        return jsonify({"success": False, "message": "Invalid date format. Please use ISO standard dates."}), 400
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500

if __name__ == '__main__':
    app.run(debug=True)
