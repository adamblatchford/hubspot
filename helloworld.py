import os
from flask import Flask, request, jsonify
import json
from openAI_chatfunctions import chat

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/trigger', methods=['POST'])

def handle_trigger():
	
	secret = request.headers.get('Authorization')

	openai_api_key=''
	synopsis =''
	target_description = ''
	recordID = ''
	
	if secret is None:
		return 'Unauthorized', 401
	
	data = request.get_json()
    
	# Extract key-value pairs from the API data dictionary
	
	for key, value in data.items():
		# print(f"Key: {key}, Value: {value}")
		# Perform further processing as needed
		
		if key == 'synopsis':
			synopsis = value
		
		if key == 'target_description':
			target_description = value
		
		if key == 'hs_object_id':
			recordID = value
		
		if key == 'openAIkey':
			openai_api_key = value
		
	response = {'synopsis': synopsis, 'target_description': target_description, 'hs_object_id':  recordID, 'openAIkey': openai_api_key, 'secret': secret}
	return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
