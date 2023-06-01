import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def chat(system, user_assistant, openai_api_key):
  
  #assert counter==0, counter
  
  headers = {
	    'Content-Type': 'application/json',
    	'Authorization': openai_api_key
  	}
  
  assert isinstance(system, str), "`system` should be a string"
  assert isinstance(user_assistant, list), "`user_assistant` should be a list"
  
  system_msg = [{"role": "system", "content": system}]
  
  user_assistant_msgs = [

		{"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}

			for i in range(len(user_assistant))

	]
  
  msgs = system_msg + user_assistant_msgs
  data = {
    	'model': 'gpt-3.5-turbo',
    	'temperature': 0.5,
    	'max_tokens': 200,
    	'messages': msgs
	}
  
  
  try:
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
  
  except:
    assert 1==1, 'Fucked'
    
  print(response)
  responseJson = response.json()
  status_code = responseJson["choices"][0]["finish_reason"]
  #assert status_code == "stop", f"The status code was {status_code}."
  
  #print (responseJson)
    
  return responseJson["choices"][0]["message"]["content"]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/trigger', methods=['POST'])

def handle_trigger():
    secret = request.headers.get('Authorization')
    
    if secret is None:
        return 'Unauthorized', 401
    
    data = request.get_json()
    # Extract key-value pairs from the data dictionary
    for key, value in data.items():
        print(f"Key: {key}, Value: {value}")
        # Perform further processing as needed
    
    response = {'data': data, 'secret': secret}
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
