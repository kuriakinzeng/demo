#!/usr/bin/env python

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function
from alchemyapi import AlchemyAPI
from bs4 import BeautifulSoup
import requests
import re
import json
import sys

demo_text = "Singapore-based peer-to-peer marketplace for overseas products, Airfrov, has secured an undisclosed amount in seed funding from East Ventures.\nAirfrov will use the funds to improve its product, hire people, and raises regionally."
# demo_url = 'https://e27.co/airfrov-raises-funding-east-ventures-get-limited-edition-items-overseas-20160301/'
# demo_url = "https://e27.co/thai-fintech-startup-stockradars-raises-round-democratise-stock-trading-20160303/"
# demo_url = "https://e27.co/marvelstone-consolidates-fintech-platform-raises-us12-6m-seed-round-20160219/"
# demo_url = "https://e27.co/active-ager-asia-bags-six-figure-incentivize-singaporeans-live-healthy-20160307/"
# demo_url = "https://e27.co/driverless-cars-arent-road-yet-20160307/"
# demo_url = "http://www.straitstimes.com/business/companies-markets/sph-media-fund-invests-in-funding-for-logistics-start-up-thelorry"
# demo_url = "http://www.bloomberg.com/news/articles/2016-01-21/forescout-raises-funding-at-a-1-billion-valuation-holds-off-ipo"
# demo_url = "http://siliconangle.com/blog/2016/01/21/iot-focused-cybersecurity-firm-forescout-raises-76m-series-g-on-1b-unicorn-valuation/"
# demo_url = "https://e27.co/ninjacart-raises-us3m-e-connect-farmers-brands-retailers-india-20160308/"
# demo_url = "https://e27.co/womens-day-menstrual-tracking-app-lovecycles-raises-us700k-funding-20160308/"
# demo_url = "https://e27.co/virtual-reality-startup-smartvizx-raises-us500k-ian-stanford-angels-20160309/"
# demo_url = "https://e27.co/virtual-reality-startup-smartvizx-raises-us500k-ian-stanford-angels-20160309/"
demo_url = "https://e27.co/japans-adways-invests-singapores-gaming-company-daylight-studios-20160127/"
demo_html = '<html><head><title>Python Demo | AlchemyAPI</title></head><body><h1>Did you know that AlchemyAPI works on HTML?</h1><p>Well, you do now.</p></body></html>'
image_url = 'http://demo1.alchemyapi.com/images/vision/football.jpg'

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()
# print('')
# print('#########################################')
# print('#         Funding Information           #')
# print('#########################################')

# print('Processing url: ', demo_url)
# print('')

funding_info = {'source': demo_url}

entities = [{'relevance':0,'text':''}]

response = alchemyapi.entities('url', demo_url, {'showSourceText':1})

if response['status'] != 'OK':
    print ('Error establishing connection')

#clean up response text
response['text'] = re.sub("(Also Read:[^\.!?]*\n)","",response['text'])

#get all company entities
for entity in response['entities']:
    if (entity['type'] == 'Company'):
        entities.append(entity);

import itertools

# sentences = []
sentence_score = {'sentence':'','score':0}

print(json.dumps(entities,indent=4))

for pair in itertools.permutations(entities):
    # print(pair[0]['text'],pair[1]['text'])
    # print(pair)
    matches = re.findall(r"(^.*?\b%s\b.*\b(?:secure|raise).*?\b%s\b.*?$)" % (pair[0]['text'],pair[1]['text']), response['text'], re.M|re.I)
    if matches:
        if pair[0]['relevance'] == 0:
            score = (float(pair[1]['relevance']))
            # relevant_sentences.append(matches)
        elif pair[1]['relevance'] == 0:
            score = (float(pair[0]['relevance']))
            # relevant_sentences.append(matches)
        else:
            score =((float(pair[0]['relevance'])*2 + float(pair[1]['relevance']))/2)
            # relevant_sentences.append(matches)

        if score > sentence_score['score']:
            sentence_score = {'sentence': matches,'score': score}

        # if matches not in sentences:
            # sentences.append(matches)
            # sentences_score.append({'sentence':matches,'score':float(pair[1]['relevance'])})
        # else:
            # relevant_sentences[relevant_sentences.index(matches)]
# import sys
# sys.exit()
# print(json.dumps(sentence_score,indent=4))

response = alchemyapi.author('url', demo_url)

if response['status'] == 'OK':
    funding_info['author'] = response['author'].encode('utf-8')
#     print('## Response Object ##')
#     print(json.dumps(response, indent=4))

#     print('')
#     print('## Author ##')
#     print('author: ', response['author'].encode('utf-8'))
#     print('')
else:
    print('Error in author extraction call: ', response['statusInfo'])


# print('')
# print('')
# print('')
# print('############################################')
# print('#   Title Extraction Example               #')
# print('############################################')
# print('')
# print('')

# print('Processing url: ', demo_url)
# print('')

# response = alchemyapi.title('url', demo_url)

# if response['status'] == 'OK':
#     print('## Response Object ##')
#     print(json.dumps(response, indent=4))

#     print('')
#     print('## Title ##')
#     print('title: ', response['title'].encode('utf-8'))
#     print('')
# else:
#     print('Error in title extraction call: ', response['statusInfo'])


# print('')
# print('#######################')
# print('#   Funding Amount    #')
# print('#######################')

rel_sentence = "".join(sentence_score['sentence'])
# print('Processing text: ', rel_sentence)
# print('')

if (rel_sentence):
    sub_obj = re.split("(?:secure|raise)", rel_sentence)
    sub_obj_response = alchemyapi.entities('text', sub_obj[0])
    # print(sub_obj[0])

    if sub_obj_response['status'] == 'OK':
        companies = [entity for entity in sub_obj_response['entities'] if entity['type'] == 'Company']
        # mistaken_as_people = [entity for entity in sub_obj_response['entities'] if entity['type'] == 'Person']
        
        if companies:
            funding_info['startup'] = companies[0]['text']
        # elif mistaken_as_people:
            # funding_info['startup'] = mistaken_as_people[0]['text']
        # else:
            #get the most probable company from the original response from demo_url
            # funding_info['startup'] = entities[1]['text']
        else:
            #Imma fcking get it another way
            response_title = alchemyapi.title('url', demo_url)

            if response_title['status'] == 'OK':
                title = response_title['title']
                raise_flag = re.findall(r"(secure|raise)", title)
                invest_flag = re.findall(r"(invest)", title)
                entitiesInTitle_r = alchemyapi.entities('text', title)['entities']
                entitiesInTitle = [entity for entity in entitiesInTitle_r if entity['type'] == 'Company']

                if entitiesInTitle:
                    if raise_flag:
                        funding_info['startup'] = entitiesInTitle[0]['text']
                    elif invest_flag:
                        funding_info['startup'] = entitiesInTitle[-1]['text']
                    else:
                        funding_info['startup'] = 'Not found'
                else:
                    funding_info['startup'] = 'Not found'

                #if the word is invest, then we know the later entity is most probably a startup
                #if the word is raise/secure, then we know the former is the startup

                # response = alchemyapi.relations('text', entitiesInTitle)


                # matches = re.findall(r"(^.*?\b%s\b.*\b(?:secure|raise).*?\b%s\b.*?$)" % (pair[0]['text'],pair[1]['text']), title)
                # if matches:
                # elif:

            #     print('## Response Object ##')
            #     print(json.dumps(response, indent=4))
            #     print('')
            #     print('## Title ##')
            #     print('title: ', response_title['title'].encode('utf-8'))
            #     print('')
            else:
                print('Error in title extraction call: ', response_title['statusInfo'])
            
        # print (response['entities'])
        # print(json.dumps(companies,indent=4))
        # for entity in response['entities']:
            # if (entity['type'] == 'Company'):
                # entities.append(entity);
    else:
        print('Error in entity extraction call: ', sub_obj_response['statusInfo'])


    amounts = re.findall(r"(\w*\$\d+(?:(?:\,|\.)\d+)*\s*(?:millions*|billions*|thousands*|m|b|k)*)",rel_sentence,re.M)
    currency_amounts = {}

    if not amounts:
        currency_amounts = 'undisclosed'
        # print (currency_amounts)
    else:
        # for amount in amounts:
        amtsplit = amounts[0].split('$')
        if amtsplit[0] == 'US' or amtsplit[0] == '':
            currency_amounts['usd'] = amtsplit[1]
        elif amtsplit[0] == 'S':
            currency_amounts['sgd'] = amtsplit[1]
        else:
            currency_amounts = 'undisclosed'

        # if 'usd' in currency_amounts:
        #     print (currency_amounts['usd'])
        # else:
        #     print (json.dumps(currency_amounts,indent=4))
    funding_info['amount'] = currency_amounts
        # print(amount)
        # print (currency_amount[0],currency_amount[1])


    fround = re.findall(r"(?:seed(?=\sround|\sfunding)|series [A-K]{1}\b)",rel_sentence,re.M|re.I)
    if fround:
        funding_info['round'] = fround[0];
    else:
        funding_info['round'] = 'undisclosed';

    #investor info
    # print (sub_obj[1])
    sub_obj_response2 = alchemyapi.entities('text', sub_obj[1])
    vc_list = [{'text':investor['text'],'type':investor['type']} for investor in sub_obj_response2['entities'] if investor['type'] == 'Company']
    angel_list = [{'text':investor['text'],'type':'Angel'} for investor in sub_obj_response2['entities'] if investor['type'] == 'Person']
    # check if investors is preceded by keywords like 'led by' or 'from'
    investors_list = []
    if re.findall('angel',sub_obj[1]) and angel_list:
        funding_info['investors'] = angel_list
        investors_list = [investor['text'] for investor in angel_list]
    elif vc_list:
        funding_info['investors'] = vc_list
        investors_list = [investor['text'] for investor in vc_list]
    else:  
        funding_info['investors'] = 'Not found'
        # if investor['text'] 
    # print(json.dumps(investors,indent=4))

    # Get who the article is most probably about, excluding known investors
    if funding_info['startup'] == 'Not found':
        listOfSuspects = [entity for entity in entities if entity['text'] not in investors_list and entity['text'] is not '']
        funding_info['startup'] = sorted(listOfSuspects,key=lambda x: float(x['relevance']))[-1]['text']

    if funding_info['investors'] == 'Not found':
        listOfSuspects = [entity for entity in entities if entity['text'] != funding_info['startup'] and entity['text'] is not '']
        funding_info['investors'] = listOfSuspects
        # sorted(listOfSuspects,key=lambda x: float(x['relevance']))[-1]['text','']
        print(listOfSuspects)

else:
    funding_info = {};

# print (json.dumps(funding_info,4))