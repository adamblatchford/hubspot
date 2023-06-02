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
	
	client = hubspot.Client.create(access_token=hubspot_app_token)
	filter = { 'propertyName': 'lifecyclestage', 'operator': 'EQ', 'value': 'salesqualifiedlead'}
	filterGroup = { 'filters': [filter] }
	sort = ''
	query = ''
	properties = ['description','specialities__linkedin_', 'linkedin_description','level_2_taxonomy','level_3_taxonomy','web_home_page___ai_scrape','domain']
	limit = 1
	after = 0
	
	publicObjectSearchRequest = {
    		'filterGroups': [filterGroup],
    		'sorts': [sort],
		'query': query,
		'properties': properties,
		'limit': limit,
		'after': after
	};
	
	try:
		api_response = client.crm.companies.search_api.do_search(publicObjectSearchRequest)
		
	except ApiException as e:
		print("Exception when calling basic_api->get_page: %s\n" % e)
	
	i = 0
	
	for thiscompany in api_response.results:
		
		i = i + 1
		
		domain = thiscompany.properties['domain']
		if domain is None:
			domain =''
		
		description = thiscompany.properties['description']
		if description is None:
			description =''
		
		linkedin_specialities = thiscompany.properties['specialities__linkedin_']
		if linkedin_specialities is None:
			linkedin_specialities = ''
		
		linkedin_description = thiscompany.properties['linkedin_description']
		if linkedin_description is None:
			linkedin_description =''
			
		level2 = thiscompany.properties['level_2_taxonomy']
		if level2 is None:
			level2 = ''
		
		level3 = thiscompany.properties['level_3_taxonomy']
		if level3 is None:
			level3 = ''
		
		webscrape = thiscompany.properties['web_home_page___ai_scrape']
		if webscrape is None:
			webscrape = ''

	response = {'counter': i, 'synopsis': synopsis, 'target_description': target_description, 'hs_object_id':  recordID, 'openAIkey': openai_api_key, 'secret': secret}
	return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
