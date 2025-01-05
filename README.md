# Websockets Webex Bot

This project was largely inspired by the following resources.

https://0x2142.com/how-to-building-a-basic-webex-chatbot/

https://0x2142.com/webex-chatbot-with-adaptivecards/

Big Thank's to the author ! 

It is about another way to built a python Webex Bot. Instead of using webhooks we use Websockets which are supported by webex.

The most important benefits of websockets  is that we don't need to expose our webex bot into the Internet thanks to NGROK or port forwaring on Internet firewalls. Which is Huge !!.

Another benefits is the bot code is simpler than the code needed to handle webhooks.

For these 2 reasons, this websocket technic must be for anyone who want to build a webex bot the first choice.

# Installation

## Prerequisit

You must have created a webex bot first. 

Have a look to the instructions here for that [Create a webex bot](https://github.com/pcardotatgit/Create_a_Webex_bot_for_XDR_Alerts)

## Step 1. Create a working directory

Create a working directory into your laptop. Open a terminal CMD window into it. Name It XDR_BOT for example.

## Step 2. Copy the code into your laptop

The Download ZIP Method

The easiest way for anyone not familiar with git is to copy the ZIP package available for you in this page. Click on the Code button on the top right of this page. And then click on Download ZIP.

Unzip the zip file into your working directory.

The "git clone" method with git client

And here under for those of you who are familiar with Github.

You must have a git client installed into your laptop. Then you can type the following command from a terminal console opened into your working directory.

    git clone https://github.com/pcardotatgit/webex_for_xdr_part-5_websocket.git

## Step 3. Go to the code subfolder

Once the code unzipped into your laptop, then Go to the code subfolder.

## Step 4. Create a Python virtual environment

It is still a best practice to create a python virtual environment. Thank to this you will create a dedicated package with requested modules for this application.

### Create a virtual environment on Windows

    python -m venv venv 

### Create a virtual environment on Linux or Mac

    python3 -m venv venv

Depending on the python version you installed into your Mac you might have to type either 

- python -m venv venv

or maybe

- python3 -m venv venv    : python3 for python version 3.x  

or maybe 

- python3.9 -m venv venv  : if you use the 3.9 python version

And then move to the next step : Activate the virtual environment.

### Activate the virtual environment on Windows

    venv\Scripts\activate

### Activate the virtual environment on Linux or Mac

    source venv/bin/activate    

## Step 5. Install needed python modules

You can install them with the following 2 commands one after the other ( Windows / Mac / Linux ):

The following command might be required if your python version is old.

    python -m pip install --upgrade pip   

Then install required python modules ( Windows / Mac / Linux )

    pip install -r requirements.txt
    
For information requirements.txt mention the **webex_bot** python module which is the key module for this project.

You can install it separately thanks to the **pip install webex_bot** command.

If you intend to use a python module for creating your adaptative cards ( which is not the case is this projet ), then you must install the **adaptativecardbuilder** module ( **pip install adaptativecardbuilder** )

In this project we build the adaptative card thanks to dictionnary building and we convert the final result into json at the end.

## Edit config.py and Set the initialization variables

This config file contains only 2 variables. 

Only the **BOT_ACCESS_TOKEN** variable is mandatory to have the bot work.

The second variable **DESTINATION_ROOM_ID** is optionnal. It is needed by the **4-send-advanced_dynamic_alert_message_to_room_example.py** script you might recognize if you went thru all chapter of this webex bot for XDR project.

**DESTINATION_ROOM_ID**  must be your Own Room ID !. It is needed by the **4-send-advanced_dynamic_alert_message_to_room_example.py** script for sending an example of alert formular into the room.

If you don't know you room id. you will be able to see it into the bot console when you will send any message to the bot.

## Run the Bot

    python run_bot.py
    
You should see the bot starting until you see the message : **Websocket Opened**

At that point the bot is ready and waits for messages in the Webex room.

The next step is now to go to webex client, contact the bot by it's mail and create a space with it. And then send messages to it.

Try to send anything and have a look to the bot console. Logs are very detailed. They allow you to understand everything that happen ! 

You can try to send the following commands :

- temp : the bot will send you back a message with the current temperature in Paris
- alert : the bot will send you back the alert adaptive card we used in the previous sections. And you can select objects into the formular

## Code architecture and how to add new commands

The main script is the **run_bot.py** one. This is the script to run and this one use the others scripts as resources.

The **alert_card.py** script manages the adptative card generation as we saw in the previous sections.

The **engine.py** is the script which manages the commands to send to webex room and associated actions

Here is here under how to add your own command :

Step 1 edit the **engine.py** script and add a new **cmd class** like the example bellow :

This example catch the message /check 192.168.100.45   ( or any other IP address ).
By default Space is used as a separator between command keyword and the passed message.

In our case the command keyword is **/check** and the message is all the rest ( actually one IP address 192.168.100.45 ). Separate parsing must be done if you pass into the message several variables.

    class cmdXXX(Command):
        def __init__(self):
            super().__init__(
                command_keyword="/check",
                help_message="Trigger an XDR worfklow thanks to its webhook",
                card=None,
            )

        def execute(self, message, attachment_actions, activity):
            message=message.strip() #remove any left and right spaces . Then message contains a clean IP address
            print()
            print('host on which to check : ',message)
            print()
            # Ok let's prepare a Webhook call to XDR.  XDR webhook was stored prior into the conf.XDR_WEBHOOK variable
            headers = {'Content-Type':'application/json', 'Accept':'application/json'}
            post_data = { "IP": message }
            response = requests.post(conf.XDR_WEBHOOK, headers=headers,json=post_data)
            print(response)   # check HTTP error status to check if Webhook was accepted by XDR     
            return f"OK XDR workflow triggered for host : {message}...Waiting for reply... "   # Confirm in Webex Room that we executed the action
            
In this example above we send a message to the webex room that triggers an XDR workflow and pass an IP address to it.
            
Replace XXX by a new number if you follow my own logic

In the **def __init__(self):**  function declare the command string you want to track

    command_keyword="new_command_string",

The **def execute(self, message, attachment_actions, activity):**   will be automatically launched if the string command above was sent to the bot. This is the location to insert all code instructions that must be executed.

This function ends with a **return** statement which will be a message to send into the webex room. It can be either a text, or an adpative card.

Here under an example of code for sending an adaptive card

        def execute(self, message, attachment_actions, activity):
            alert_message="Suspicious Activity Detected"
            cards_content=create_card_content(alert_message) # call a function that create the adaptive card
            response = Response()
            response.text = "XDR Alert !"
            # Attachments being sent to user
            response.attachments = cards_content[0]
            return response

Step 2 add the command management to the bot

Edit the **run_bot.py** script and add the **cmdXXX** into the import section :

    from engine import cmd,cmd2,cmd3,cmd4, cmdXXX
    
And add a new **bot.add** command before the last **bot.run()** command 

    bot.add_command(cmd3())
    bot.add_command(cmd4())
    bot.add_command(cmdXXX())
    bot.run()
    
And that's it !!  You can run the bot and test your new command.

Watch the bot console to troubleshoot and debug.

# Where to go Next : XDR alert workflow

Go to the next section

[webex_for_xdr_part-6_XDR_send_alert_workflow](https://github.com/pcardotatgit/webex_for_xdr_part-6_XDR_send_alert_workflow)

Go to previous section 

[webex_for_xdr_part-4_webhook_bot_that_handle_submitted_data](https://github.com/pcardotatgit/webex_for_xdr_part-4_webhook_bot_that_handle_submitted_data)