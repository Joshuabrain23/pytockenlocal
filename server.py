from flask import Flask, request
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# YOUR EXACT LOCATION
FOLDER_PATH = r"C:\Users\user\OneDrive\Desktop\data"
FILE_PATH = r"C:\Users\user\OneDrive\Desktop\data\tocken.csv"

if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)

def get_next_token():
    now = datetime.now()
    prefix = now.strftime("%y%m") + "E"
    start_serial = 40
    
    if not os.path.exists(FILE_PATH):
        return f"{prefix}{start_serial:03d}"
    
    try:
        with open(FILE_PATH, "r") as file:
            lines = list(csv.reader(file))
            if len(lines) <= 1:
                return f"{prefix}{start_serial:03d}"
            
            last_token = lines[-1][1]
            last_serial = int(last_token[-3:])
            next_serial = last_serial + 1
            return f"{prefix}{next_serial:03d}"
    except:
        return f"{prefix}{start_serial:03d}"

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    next_token = get_next_token()
    
    try:
        file_exists = os.path.isfile(FILE_PATH)
        with open(FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Token", "Name", "Phone", "Service"])
            writer.writerow([timestamp, next_token, data.get('name'), data.get('phone'), data.get('service')])
        
        return {"status": "success", "token": next_token}
    except PermissionError:
        return {"status": "error", "message": "Close Excel!"}, 403

if __name__ == '__main__':
    app.run(port=5000)