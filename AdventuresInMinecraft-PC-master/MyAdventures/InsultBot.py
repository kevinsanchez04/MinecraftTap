import random
import time
from BotManager import BotFramework, BotManagerSingleton

class InsultBot(BotFramework):
    insults = ["Ets burro","Ets tonto", "Ets cavero"]
    def doSomething(self):
        self.mc.postToChat(random.choice(self.insults))
    
    def getEvent(self):
        return ":InsultBot" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def __str__(self) -> str:
        return "<InsultBOT> "
    
    def getStop(self):
        return ":stopInsultBot"
    
    def getMessages(self):
        return self.insults

# insult = InsultBot()
# BotManagerSingleton.managerThread.join()
    