import mcpi.minecraft as minecraft
import threading
import time
from abc import ABC,abstractmethod
import Pyro5.api

# Classe que ens serveix de manegador, per controlar l'activació dels bots del framework que hauran sigut redefinits, només tindrem UN manegador per tots els bots
@Pyro5.api.expose
class BotManagerSingleton: 
    
    bots: list['BotFramework'] # Llista de bots als quals estem controlant, 'BotFramework' == Forward reference
    mc = minecraft.Minecraft.create() # Connexió al servidor de minecraft
    instance = None # Atributs per a que sigui un Singleton(instancia unica)
    lock = threading.Lock() # Atribut per a que el singleton funcioni correctament en threads, eliminar condicions de carrera
    managerThread = None # Thread independent que manegara los events
    activeBots = 0 # Recompte de bots que estan activats actualment
    lastMessage = None
    pyroThread = None
    message = None
    managerRun = True
    daemon = None

    def __new__(cls):
        if not cls.instance: # Si no existeix encara la instancia (primera crida)
            with cls.lock: # Semafor per controlar concurrencia en els threads
                if not cls.instance: # Doble verificació
                    cls.instance = super().__new__(cls) # Creació de primera instancia i unica
                    cls.bots = [] # Incialitzem taula de bots
                    cls.managerThread = threading.Thread(target=cls.instance.threadListener)
                    cls.managerThread.daemon = True # Eliminem thread si s'elimina el objecte
                    cls.managerThread.start()

                    cls.daemon = Pyro5.api.Daemon(host="192.168.5.206")
                    ns = Pyro5.api.locate_ns(host="192.168.5.206",port=9090)
                    uri = cls.daemon.register(BotManagerSingleton)
                    ns.register("MinecraftServer",uri)

                    cls.pyroThread = threading.Thread(target=cls.daemon.requestLoop)
                    cls.pyroThread.start()

        return cls.instance # Retornem instancia del Singleton
    
    def stop_manager(self): 
        self.managerRun = False
        self.daemon.shutdown() 
        self.managerThread.join()

    def addBot(self, newBot):
        with self.lock:
            self.bots.append(newBot)
    
    def removeBot(self, bot):
        with self.lock:
            if bot in self.bots:
                self.bots.remove(bot)
    
    def actionListener(self):
        # print(self.bots.__str__())
        chatEvents = self.mc.events.pollChatPosts()
        chatEvents = [chatEvent.message for chatEvent in chatEvents if chatEvent.message is not None]
        if len(chatEvents) > 0:
            self.lastMessage = chatEvents[-1]
            with self.lock:
                for a in self.bots:
                    if not a.threadRun and a.getEvent() in self.lastMessage:
                        a.startBot()
                        self.activeBots += 1

                    if a.threadRun and a.getStop() in self.lastMessage:
                        self.activeBots -= 1     
                        a.stopBot()
                    elif self.getStop() in self.lastMessage:
                        self.managerRun = False #El manegador es tanca i no es podran tornar a engegar bots
                        for bot in self.bots:
                            bot.stopBot()
                        
        elif self.message is not None:
            with self.lock:
                for a in self.bots:
                    if not a.threadRun and a.getEvent() in self.message:
                        a.startBot()
                        self.activeBots += 1

                    if a.threadRun and a.getStop() in self.message:
                        self.activeBots -= 1     
                        a.stopBot()
                        
            self.message = None

    def send_message(self, message):
        # print(f"Received message:{message}")
        self.message = message
        return "Message received"            

    def threadListener(self):
        while self.managerRun:
            # print(f"Thread manager corriendo. Bots activos: {list(map(lambda x: x.__str__(), self.bots))}")  # Depuración
            time.sleep(1)
            self.actionListener()
            
    def getChat(self):
        return self.lastMessage
    
    def getStop(self):
        return ":stopManager"

class BotFramework(ABC): # Definim la classe pare, el qual sera el contracte per al nostre framework de bots

    mc = None
    manager = None
    threadRun = False
    threadId = None

    def __init__(self):
        self.manager = BotManagerSingleton() # Obtenim la instancia del manegador
        self.manager.addBot(self) # Afegim el bot al nostre manager, quan fem la crida al constructor de la classe
        self.mc = self.manager.mc # Obtenim mateixa connexio per a tots els bots
    
    def __del__(self):
        self.manager.removeBot(self)
    
    def __str__(self) -> str:
        return "Soc un BOT"
    
    def threadAction(self):
        while self.threadRun:
            threading.Event().wait(2) # Espera 3 segons o fins que es estableixi l'event
            self.doSomething() # Crida a la logica del bot
                    
    def startBot(self):
        if not self.threadRun:
            self.threadRun = True
            self.threadId = threading.Thread(target=self.threadAction)
            #self.threadId.daemon = True
            self.threadId.start()
    
    def stopBot(self):
        if self.threadRun:
            self.threadRun = False
            #self.threadId.join()
    
    @abstractmethod
    def doSomething(self):
        pass
        
    @abstractmethod
    def getEvent(self):
        pass
        
    @abstractmethod
    def getStop(self):
        pass
