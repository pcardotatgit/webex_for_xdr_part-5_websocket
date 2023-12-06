from webex_bot.webex_bot import WebexBot
from engine import cmd,cmd2,cmd3,cmd4
import sys
import config  as conf
from crayons import *

api_token=conf.BOT_ACCESS_TOKEN
bot = WebexBot(api_token)
bot.add_command(cmd())
bot.add_command(cmd2())
bot.add_command(cmd3())
bot.add_command(cmd4())
bot.run()