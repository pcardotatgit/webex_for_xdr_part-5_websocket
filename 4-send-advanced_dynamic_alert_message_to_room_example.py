'''
    Same as example 3 but the card is dynamically builted from content for ./targets_and_observables/targets.txt and ./targets_and_observables/observables.txt file
'''
import requests
import sys, os
import config  as conf
from crayons import *
import json

ROOM_ID=conf.DESTINATION_ROOM_ID
ACCESS_TOKEN=conf.BOT_ACCESS_TOKEN
version=conf.version
URL = 'https://webexapis.com/v1/messages'
alert_message="Suspicious Activity Detected"

def read_targets(file):
    with open(file,'r') as file:
        text_content=file.read();
    list=text_content.split('\n')
    target_list=[]
    for item in list:
        objet={"title": item,"value": item}
        target_list.append(objet)
    return(target_list)
    
def read_observables(file):
    with open(file,'r') as file:
        text_content=file.read();
    list=text_content.split('\n')
    observable_list=[]
    for item in list:
        ip=item.split(';')[0]
        objet={"title": ip,"value": ip}
        observable_list.append(objet)  
    return(observable_list)    
    
def load_card_and_send_it(cards_content):
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
               'Content-type': 'application/json;charset=utf-8'}
    print(red(cards_content))
    attachment={
    "roomId": ROOM_ID,
    "markdown": "!  XDR ALERT !",
    "attachments": cards_content
    }
    response = requests.post(URL, json=attachment,headers=headers)
    if response.status_code == 200:
        # Great your message was posted!
        #message_id = response.json['id']
        #message_text = response.json['text']
        print("New message created")
        #print(message_text)
        print("====================")
        print(response)
    else:
        # Oops something went wrong...  Better do something about it.
        print(response.status_code, response.text)

def create_card_content(alert_message,target_file,observables_file):
    targets=read_targets(target_file)
    observables=read_observables(observables_file)
    cards_content=[
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {    
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "backgroundImage": {
                    "url": "https://i.postimg.cc/vBxnRp06/sky2.jpg",
                    "verticalAlignment": "Center"
                },             
                "id": "title",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "! XDR ALERT !",
                        "color": "Attention",
                        "weight": "Bolder",
                        "size": "ExtraLarge",                        
                        "horizontalAlignment": "Center"
                    },
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": alert_message,
                                "wrap": True,
                                "color": "Attention",
                                "horizontalAlignment": "Center"
                            }
                        ]
                    }                   
                ],
                "actions": [
                    {
                        "type": "Action.ShowCard",
                        "title": "Targeted Systems",
                        "card": {
                            "type": "AdaptiveCard",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "Select Systems to isolate",
                                    "color": "Warning",
                                    "size": "Medium",
                                    "wrap": True
                                },
                                {
                                    "type": "Input.ChoiceSet",
                                    "id": "targets",
                                    "style": "expanded",
                                    "isMultiSelect": True,
                                    "choices": targets
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Isolate Selected Systems",
                                    "data": {
                                        "callback_keyword": "Targets"
                                    }
                                }
                            ],
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                        }
                    },
                    {
                        "type": "Action.ShowCard",
                        "title": "Suspicious observables",
                        "card": {
                            "type": "AdaptiveCard",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "Suspicious Observables :",
                                    "color": "Warning",
                                    "size": "Medium",
                                    "wrap": True
                                },
                                {
                                    "type": "Input.ChoiceSet",
                                    "id": "observables",
                                    "style": "expanded",
                                    "isMultiSelect": True,
                                    "choices": observables
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Block Selected Objects",
                                    "horizontalAlignment": "Center",
                                    "data": {
                                        "callback_keyword": "observables"
                                    }
                                }
                            ],
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                        }
                    }                
                ]          
            }
        }
    ]    
    return(cards_content)
        
if __name__=="__main__":
    targets='./targets_and_observables/targets.txt'
    observables='./targets_and_observables/observables.txt'
    card_content=create_card_content(alert_message,targets,observables)
    load_card_and_send_it(card_content)