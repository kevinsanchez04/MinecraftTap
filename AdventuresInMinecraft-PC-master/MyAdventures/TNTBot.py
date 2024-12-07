import random
from botFramework import BotFramework, BotManagerSingleton
from mcpi import block

class TNTBot(BotFramework):
    def doSomething(self):
        resultat=self.mc.player.getPos()
        print(resultat)
        self.mc.setBlock(resultat.x,resultat.y,resultat.z,(block.TNT.id,1)) # Fiquem el bloc de TNT
        self.mc.setBlock(resultat.x + 1, resultat.y, resultat.z, block.FIRE.id) #Activa el bloc de TNT per a qué pugui explotar
    
    def getEvent(self):
        return ":TNTBot" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def __str__(self) -> str:
        return "<TNTBOT> "
    
tntBot = TNTBot()

BotManagerSingleton().managerThread.join()
