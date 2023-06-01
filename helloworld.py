import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/trigger', methods=['POST'])
def handle_trigger():
    data = request.get_json()
    # Extract key-value pairs from the data dictionary
    for key, value in data.items():
        print(f"Key: {key}, Value: {value}")
        # Perform further processing as needed
    
    response = {'data': data}
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
