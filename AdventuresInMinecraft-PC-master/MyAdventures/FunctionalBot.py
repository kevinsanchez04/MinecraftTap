from BotManager import BotFramework,BotManagerSingleton

class FunctionalBot(BotFramework):

    historialChat = []
    missatgeAnt = None
    def doSomething(self):
        last = BotManagerSingleton().getChat()
        if last is not None and last != self.missatgeAnt:
            if last.startswith("FuncStart"): #Filtre de les publicacions en el chat que començen en xxx
                start = lambda string: string.startswith(last.split()[-1])
                self.filter(start,"FuncStart")
            elif last.startswith("FuncFin"): #Filtre de les publicacions en el chat que acaven en xxx
                start = lambda string: string.endswith(last.split()[-1])
                self.filter(start,"FuncFin")
            elif last.startswith("MapCount"): # Map que conta el numero de lletres de cada linea de la conversa
                resul = list(map(lambda x: len(x),self.historialChat))
                self.mc.postToChat(resul)
            elif last == "FuncRestart":
                self.historialChat = []
                self.mc.postToChat(f"{self.__str__()}Historial Restarted")
            else:
                self.historialChat.append(last)
            self.missatgeAnt = last
            last = None
            print(last)

    def getEvent(self):
        return ":FuncBot" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def getStop(self):
        return ":stopFuncBot" 

    def __str__(self) -> str:
        return "<FuncBOT> "
    
    def filter(self,filtre,inici):
        lista = []
        lista.append(inici)
        lista = [item for item in self.historialChat if filtre(item)]
        self.mc.postToChat(lista)

# functionalBot = FunctionalBot()
# BotManagerSingleton.managerThread.join()
