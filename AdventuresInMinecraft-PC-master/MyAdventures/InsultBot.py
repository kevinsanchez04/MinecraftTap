import random
from botFramework import BotFramework

class InsultBot(BotFramework):
    #insults = ["Ets burro","Ets tonto", "Ets cavero"]
    insults = ["Satxa DETONA a la MIMI", "Raul la mama", "Lyubo es gay en secret"]
    def doSomething(self):
        self.mc.postToChat(random.choice(self.insults))
    
    def getEvent(self):
        return ":activar" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def __str__(self) -> str:
        return "<InsultBOT> "
insultBot = InsultBot()


    