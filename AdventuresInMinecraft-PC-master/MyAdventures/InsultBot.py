import random
import time
from botFramework import BotFramework, BotManagerSingleton

class InsultBot(BotFramework):
    insults = ["Ets burro","Ets tonto", "Ets cavero"]
    def doSomething(self):
        self.mc.postToChat(random.choice(self.insults))
    
    def getEvent(self):
        return ":InsultBot" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def __str__(self) -> str:
        return "<InsultBOT> "
    
insultBot = InsultBot()

BotManagerSingleton().managerThread.join()


    