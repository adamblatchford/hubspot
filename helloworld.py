import os
from flask import Flask, request, jsonify
import json
from openAI_chatfunctions import chat
import hubspot
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException  
from hubspot.crm.companies import ApiException

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
	maxRecords = 1
	
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
			
		if key == 'maxRecords':
			maxRecords = value
	
	client = hubspot.Client.create(access_token=secret)
	filter = { 'propertyName': 'lifecyclestage', 'operator': 'EQ', 'value': 'salesqualifiedlead'}
	filterGroup = { 'filters': [filter] }
	sort = ''
	query = ''
	properties = ['hs_object_id', 'description','specialities__linkedin_', 'linkedin_description','level_2_taxonomy','level_3_taxonomy','web_home_page___ai_scrape','domain']
	limit = int(maxRecords)
	after = 0
	
	publicObjectSearchRequest = {
    		'filterGroups': [filterGroup],
    		'sorts': [sort],
		'query': query,
		'properties': properties,
		'limit': limit,
		'after': after
	};
	
	api_response = None
	
	try:
		api_response = client.crm.companies.search_api.do_search(publicObjectSearchRequest)
		
	except ApiException as e:
		print("Exception when calling basic_api->get_page: %s\n" % e)
		return 'HubSpot API failure: ' + secret,401
	
	i = 0
	results = []
	
	for thiscompany in api_response.results:
		
		i = i + 1
		
		companyID = thiscompany.properties['hs_object_id']
		if companyID is None:
			companyID =''
		
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
			
		openAIprompt = 'Here is some text about a transaction: '+ synopsis +'[End of text about a transaction]. This is a description of the company acquired:' + target_description+ '[End of text about the company acquired]. Please give a score on a scale of 0-10 of how relevant the transaction is to the following company, and explain why. Consider services, technologies, strategic fit, synergies, and geography. You can use the following 6 company data sources. (1) description: '+description + ' ; (2) service specialities: ' + linkedin_specialities + ' ; (3) LinkedIn bio:' + linkedin_description  + ' ; (4) summary of services:' + level2  +' ; (5) technology partnerships:' + level3  +' ; (6) words from their website homepage: ' +webscrape
		systemMessage = 'You are an investment banking analyst. You have expertise in matching the fit precedent M&A transactions and companies you know (targets). You consider the following factors: (1) service lines. (2) expertise in specific technologies. (3) the fit to the stated strategy of the buyer (4) potential synergies (5) complementarity of the geographical footprint. '

		response_AI = chat(systemMessage, [openAIprompt], openai_api_key)
		temp = response_AI
		completions = [c.strip() for c in temp.split('\n') if c.strip() != '']
		fit = (completions[0])
		
		thisresult = {
			'companyID': companyID,
			'insightID': recordID,
			'fit': fit,
			'rationale': 'Nothing yet'
		}
		results.append(thisresult)

	response = {'key': openai_api_key, 'counter ':i, 'results ': results}
	return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
