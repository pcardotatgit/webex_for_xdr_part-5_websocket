'''
   alert card dynamically builted from content for ./targets_and_observables/targets.txt and ./targets_and_observables/observables.txt file
'''
import sys, os

alert_message="Suspicious Activity Detected"

def read_targets():
    file='./targets_and_observables/targets.txt'
    with open(file,'r') as file:
        text_content=file.read();
    list=text_content.split('\n')
    target_list=[]
    for item in list:
        objet={"title": item,"value": item}
        target_list.append(objet)
    return(target_list)
    
def read_observables():
    file='./targets_and_observables/observables.txt'
    with open(file,'r') as file:
        text_content=file.read();
    list=text_content.split('\n')
    observable_list=[]
    for item in list:
        ip=item.split(';')[0]
        objet={"title": ip,"value": ip}
        observable_list.append(objet)  
    return(observable_list)    
    
def create_card_content(alert_message):
    targets=read_targets()
    observables=read_observables()
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
                                },
                                {
                                    "type":"ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.Submit",
                                            "title": "Isolate Selected Systems",
                                            "data": {
                                                "callback_keyword": "Targets"
                                            }
                                        }
                                    ]                                
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
        