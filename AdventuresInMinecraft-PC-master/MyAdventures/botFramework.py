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
    pyroThread = None
    deamon = None
    uri = None
    runThread = True # Ens permetra parar l'execucio del thread
    activeBots = 0 # Recompte de bots que estan activats actualment
    lastMessage = None
    pyroServer = None

    def __new__(cls):
    
        if not cls.instance: # Si no existeix encara la instancia (primera crida)
            with cls.lock: # Semafor per controlar concurrencia en els threads
                if not cls.instance: # Doble verificació
                    cls.instance = super().__new__(cls) # Creació de primera instancia i unica
                    cls.bots = [] # Incialitzem taula de bots
                    cls.managerThread = threading.Thread(target=cls.instance.threadListener)
                    cls.managerThread.daemon = True # Eliminem thread si s'elimina el objecte
                    cls.managerThread.start()

                    cls.daemon = Pyro5.api.Daemon(host="10.112.153.180")
                    cls.uri = cls.daemon.register(BotManagerSingleton)
                    print(f"This is the uri they need for the server is --> {cls.uri} <--")
                    cls.pyroThread = threading.Thread(cls.instance.daemon.requestLoop())
        print(cls.uri)
        return cls.instance # Retornem instancia del Singleton
    
    def addBot(self, newBot):
        with self.lock:
            self.bots.append(newBot)
    
    def removeBot(self, bot):
        with self.lock:
            if bot in self.bots:
                self.bots.remove(bot)
    
    def actionListener(self,message):
        chatEvents = self.mc.events.pollChatPosts() # Obtenim els posts del xat
        print(chatEvents)
        chatEvents = [chatEvent.message for chatEvent in chatEvents if chatEvent.message is not None] # Obtenim els missatges que tinguin contingut filtrar(functional)
        if len(chatEvents) > 0:
            self.lastMessage = chatEvents[-1]
            with self.lock:
                for a in self.bots:
                    if not a.threadRun and a.getEvent() in self.lastMessage: # Comprovem que el fil del bot no esta ja a RUN
                        a.startBot()
                        self.activeBots += 1
                    elif a.getStop() in self.lastMessage: # Si ens escriuen la comanda de desactivament del bot lo parem
                        a.stopBot()
                        self.activeBots -= 1
                        if self.activeBots == 0:
                            self.runThread = False # Parem el manegador si no tenim cap bot actiu
        if message is not None:
            print(message)
        

    # def actionListener(self,message):
    #     chatEvents = self.mc.events.pollChatPosts() # Obtenim els posts del xat
    #     print(chatEvents)
    #     chatEvents = [chatEvent.message for chatEvent in chatEvents if chatEvent.message is not None] # Obtenim els missatges que tinguin contingut filtrar(functional)
    #     if len(chatEvents) > 0:
    #         self.lastMessage = chatEvents[-1]
    #         with self.lock:
    #             for a in self.bots:
    #                 if not a.threadRun and a.getEvent() in self.lastMessage: # Comprovem que el fil del bot no esta ja a RUN
    #                     a.startBot()
    #                     # self.activeBots += 1
    #                 elif a.getStop() in self.lastMessage: # Si ens escriuen la comanda de desactivament del bot lo parem
    #                     a.stopBot()
    #                     # self.activeBots -= 1
    #     else:
    #         path = 'F:/URV/Offline/TAP/MinecraftTap/AdventuresInMinecraft-PC-master/MyAdventures/pyro.txt'
    #         with open(path,'r') as archivo:
    #             lectura = archivo.readline()
    #             if lectura is not None:
    #                 for a in self.bots:
    #                     if not a.threadRun and a.getEvent() in lectura: # Comprovem que el fil del bot no esta ja a RUN
    #                         a.startBot()
    #                         self.activeBots += 1
    #                     elif a.getStop() in lectura: # Si ens escriuen la comanda de desactivament del bot lo parem
    #                         a.stopBot()
    #                         self.activeBots -= 1
    #                         if self.activeBots == 0:
    #                             self.runThread = False # Parem el manegador si no tenim cap bot actiu
    #                 with open(path,'w') as archivo2:
    #                     archivo2.write("")


    # def actionListener(self):
    #     chatEvents = self.mc.events.pollChatPosts() # Obtenim els posts del xat
    #     chatEvents = [chatEvent.message for chatEvent in chatEvents if chatEvent.message is not None] # Obtenim els missatges que tinguin contingut filtrar(functional)
    #     if len(chatEvents) > 0:
    #         self.lastMessage = chatEvents[-1]
    #         with self.lock:
    #             for a in self.bots:
    #                 if not a.threadRun and a.getEvent() in self.lastMessage: # Comprovem que el fil del bot no esta ja a RUN
    #                     a.startBot()
    #                     self.activeBots += 1
    #                 elif a.getStop() in self.lastMessage: # Si ens escriuen la comanda de desactivament del bot lo parem
    #                     a.stopBot()
    #                     self.activeBots -= 1
    #                     if self.activeBots == 0:
    #                         self.runThread = False # Parem el manegador si no tenim cap bot actiu
    #     elif self.pyroServer is not None:
    #         self.lastMessage = self.pyroServer
    #         with self.lock:
    #             for a in self.bots:
    #                 if not a.threadRun and a.getEvent() in self.pyroServer: # Comprovem que el fil del bot no esta ja a RUN
    #                     a.startBot()
    #                     self.activeBots += 1
    #                 elif a.getStop() in self.lastMessage: # Si ens escriuen la comanda de desactivament del bot lo parem
    #                     a.stopBot()
    #                     self.activeBots -= 1
    #                     if self.activeBots == 0:
    #                         self.runThread = False # Parem el manegador si no tenim cap bot actiu
    #             # self.pyroServer = None
        
    def threadListener(self): #Si volem que no pari del tot el manegador al fer :stopTNTBot per
        while True: # Fil independent que fa la logica del manegador
            time.sleep(1)
            self.actionListener(None)
            
    def getChat(self):
        return self.lastMessage

class BotFramework(ABC): # Definim la classe pare, el qual sera el contracte per al nostre framework de bots
    mc = None
    manager = None
    threadRun = False
    threadId = None
    stop_event = threading.Event()
    
    def __init__(self):
        self.manager = BotManagerSingleton() # Obtenim la instancia del manegador
        self.manager.addBot(self) # Afegim el bot al nostre manager, quan fem la crida al constructor de la classe
        self.mc = self.manager.mc # Obtenim mateixa connexio per a tots els bots
    
    def __del__(self):
        self.manager.removeBot(self)
    
    def __str__(self) -> str:
        return "Soc un BOT"
    
    def threadAction(self):
        while not self.stop_event.is_set():
            self.stop_event.wait(3) # Espera 3 segons o fins que es estableixi l'event
            if not self.stop_event.is_set():
                self.doSomething() # Crida a la logica del bot
                
    @abstractmethod
    def doSomething(self):
        pass
        
    @abstractmethod
    def getEvent(self):
        pass
        
    @abstractmethod
    def getStop(self):
        pass
    
    def startBot(self):
        if not self.threadRun:
            self.threadRun = True
            self.stop_event.clear() #Canvia l'estat del thread, a run notifica directament al thread
            self.threadId = threading.Thread(target=self.threadAction)
            self.threadId.daemon = True
            self.threadId.start()
    
    def stopBot(self):
        if self.threadRun:
            self.threadRun = False
            self.stop_event.set() #Canviem estat del thread, a stop aquest notifica directament al thread
            self.threadId.join()

# @Pyro5.api.expose
# class UseServer():
#     def send_message(self, message):
#         print(f"Received message:{message}")
#         return "Message received"

