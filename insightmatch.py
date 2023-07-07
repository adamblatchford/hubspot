import requests
import json

#insightID = input_data['insightID']
#synopsis = input_data['synopsis']
#target_description = input_data['target_description']

insightID = "5630168713"
synopsis = "Equiteq is pleased to have advised leading infrastructure consultancy Infrata on a majority investment from private equity firm Lonsdale Capital Partners. Established in 2011, Infrata provides technical, commercial, demand, economic and ESG-focused advisory services to the financial services industry throughout the entire lifecycle of an infrastructure investment. They have deep sector-specific knowledge across airports & aviation, roads, railways, ports & waterways, and social infrastructure. The company is currently working on over 100 projects in the due diligence and monitoring phases as well as having advised on transactions worth in excess of $250 billion since inception. Infrata serves its diversified client base from its headquarters in London and offices in Colombia, Spain, and Canada. Lonsdale Capital Partners is a private equity firm focused on the lower mid-market in the UK and Europe. With Lonsdale’s backing, Infrata will target further scaling in North America and continental Europe as well as the development of existing and complementary business lines, especially those focused on rail, aviation and ESG. Lonsdale will also support the Company’s continued acquisitive growth strategy, targeting suitable specialist consultancies operating in desirable niches or locations."
target_description = "Provider of consulting services focused on infrastructure projects both public and private. The company offers services including, technical advisory, strategic and commercial advisory, demand and traffic advisory and environmental, social and governance advisory, ensuring that projects get the funding they need while giving investors the confidence to make the right decisions."

bearer_token = "pat-na1-8bb90e58-788c-431b-b107-cf2c996c0ebc"

url = "https://api.hubspot.com/crm/v3/objects/companies/search"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{bearer_token}"
}

payload = {
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "lifecyclestage",
          "operator": "EQ",
          "value": "salesqualifiedlead"
        }
      ]
    }
  ],
  "sorts": [],
  "query": "",
  "properties": [
    "hs_object_id",
    "name",
    "description",
    "specialities__linkedin_",
    "linkedin_description",
    "level_2_taxonomy",
    "level_3_taxonomy",
    "web_home_page___ai_scrape",
    "domain"
  ],
  "limit": 100,
  "after": 0
}

extracted_fields = []
limit = 100
after = 0
has_more = True
data=[]

# Pagination loop
while has_more:
    payload["after"]=after
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()
    after = after + limit
    if "paging" not in data:
        has_more = False

    for company in data["results"]:
        #ID = company["ID"]
        hs_object_id = company["properties"]["hs_object_id"]
        companyname = company["properties"]["name"]
        description = company["properties"]["description"]
        specialities__linkedin_= company["properties"]["specialities__linkedin_"]
        linkedin_description = company["properties"]["linkedin_description"]
        level_2_taxonomy = company["properties"]["level_2_taxonomy"]
        level_3_taxonomy = company["properties"]["level_3_taxonomy"]
        web_home_page___ai_scrape = company["properties"]["web_home_page___ai_scrape"]
        domain = company["properties"]["domain"]
        extracted_fields.append((hs_object_id, companyname, description,specialities__linkedin_,linkedin_description, level_2_taxonomy,level_3_taxonomy,web_home_page___ai_scrape,domain ))
        
# Create an empty list to store the rows
rows = []

# Loop through the extracted fields
for hs_object_id, companyname, description,linkedin_description,specialities__linkedin_, level_2_taxonomy,level_3_taxonomy,web_home_page___ai_scrape,domain in extracted_fields:
    # Create a dictionary for each row
    row = {
        'hs_object_id': hs_object_id,
        'name': companyname,
        'description': description,
        'linkedin_description': linkedin_description,
        'specialities__linkedin_': specialities__linkedin_,
        'level_2_taxonomy': level_2_taxonomy,
        'level_3_taxonomy': level_3_taxonomy,
        'web_home_page___ai_scrape': web_home_page___ai_scrape,
        'domain': domain
    }
    
    # Append the row dictionary to the list
    rows.append(row)

openAI_URL = "https://api.openai.com/v1/chat/completions"
openAI_bearer_token = "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"
openAI_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openAI_bearer_token}"
}

print (openAI_headers)

matches = []
counter = 1

for companyloop in rows:

    if counter>5:
        continue

    this_hs_object_id = companyloop["hs_object_id"]
    this_name = companyloop["name"]
    this_description = companyloop["description"]
    this_linkedin_description = companyloop["linkedin_description"]
    this_specialities__linkedin_ = companyloop["specialities__linkedin_"]
    this_level_2_taxonomy = companyloop["level_2_taxonomy"]
    this_level_3_taxonomy = companyloop["level_3_taxonomy"]
    this_web_home_page___ai_scrape = companyloop["web_home_page___ai_scrape"]
    this_domain = companyloop["domain"]

    openAI_payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "max_tokens": 500,
        "messages": [
            {
                "role": "system",
                "content": "You are an investment banking analyst. You have expertise in matching the fit precedent M&A transactions and companies you know (targets). You consider the following factors: (1) service lines. (2) expertise in specific technologies. (3) the fit to the stated strategy of the buyer (4) potential synergies (5) complementarity of the geographical footprint. '"
            },
            {
                "role": "assistant",
                "content": f"Here is some text about a transaction: {synopsis}[End of text about a transaction]. This is a description of the company acquired: {target_description} [End of text about the company acquired]. Please give a score on a scale of 0-10 of how relevant the transaction is to the following company, and explain why. Your output should be a JSON dictionary with two entries: (1) the score (as an integer). (2) your explanation. Consider services, technologies, strategic fit, synergies, and geography. You can use the following 5 company data sources. (1) description: {this_description} (2) LinkedIn bio: {this_linkedin_description} (3) summary of services:{this_level_2_taxonomy} (4) technology partnerships: {this_level_3_taxonomy}(5) words from their website homepage: {this_web_home_page___ai_scrape}"
            }
        ]
    }
    counter = counter + 1

    AI_response = requests.post(openAI_URL, headers=openAI_headers, json=openAI_payload)
    AI_data = AI_response.json()

    print (AI_data)

    score = ""
    explanation = ""

    try:
        AI_content = AI_data["choices"][0]["message"]["content"]
        json_AI = json.loads(AI_content)
        score = json_AI["score"]
        explanation = json_AI["explanation"]

    except KeyError:
        pass

    match = {
        'insightID' : insightID,
        'companyID' : this_hs_object_id,
        'name': this_name,
        'score': score,
        'explanation': explanation
    }
    matches.append(match)

print (matches)
quit()
#return {'matches':matches}
