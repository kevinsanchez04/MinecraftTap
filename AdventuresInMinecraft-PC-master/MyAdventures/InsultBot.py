import random
from botFramework import BotFramework

class InsultBot(BotFramework):
    insults = ["Ets burro","Ets tonto", "Ets cavero"]
    def doSomething(self):
        self.mc.postToChat(random.choice(self.insults))
    
    def getEvent(self):
        return ":Activar" #Cadena de caracters que actuara com una comanda d'activació del bot
    
insultBot = InsultBot()


    