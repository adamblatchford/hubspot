import os
from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/trigger', methods=['POST'])
def handle_trigger():
    data = request.get_json()
    # Process the data and perform necessary actions
    response = {'message': 'Trigger received', 'data': data}
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
