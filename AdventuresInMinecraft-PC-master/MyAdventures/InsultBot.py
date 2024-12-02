import time
import random
from botFramework import BotFramework

class InsultBot(BotFramework):
    insults = ["Ets burro","Ets tonto", "Ets cavero"]
    def doSomething(self):
        self.mc.postToChat(random.choice(self.insults))
        
bot = InsultBot()
while 1: 
    bot.getEvent()
    