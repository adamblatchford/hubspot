import requests
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
  
  response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
  #print(response)
  responseJson = response.json()
  status_code = responseJson["choices"][0]["finish_reason"]
  #assert status_code == "stop", f"The status code was {status_code}."
  
  #print (responseJson)
    
  return responseJson["choices"][0]["message"]["content"]


