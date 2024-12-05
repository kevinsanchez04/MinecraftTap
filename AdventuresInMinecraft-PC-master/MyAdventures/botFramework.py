import mcpi.minecraft as minecraft
import threading
import time

#Classe que ens serveix de manegador, per controlar l'activació dels bots del framework que hauran sigut redefinits, només tindrem UN manegador per tots els bots
class BotManagerSingleton: 
    bots: list['BotFramework'] #Llista de bots als quals estem controlant, 'BotFramework' == Forward reference
    mc = minecraft.Minecraft.create() #Connexió al servidor de minecraft
    instance = None #Atributs per a que sigui un Singleton(instancia unica)
    lock = threading.Lock() #Atribut per a que el singleton funcioni correctament en threads, eliminar condicions de carrera
    managerThread = threading.Thread(target='threadListener') #Thread independent que manegara los events
    def __new__(cls):
        if not cls.instance: #Si no existeix encara la instancia (primera crida)
            with cls.lock: #Semafor per controlar concurrencia en els threads
                if not cls.instance: #Doble verificació
                    cls.instance = super().__new__(cls) #Creació de primera instancia i unica
        return cls.instance #Retornem instancia del Singleton
    
    def addBot(self, newBot):
        with self.lock:
            self.bots.append(newBot)
    
    def removeBot(self, bot):
        with self.lock:
            if bot in self.bots:
                self.bots.remove(bot)
    
    def actionListener(self):
        chatEvents = self.mc.events.pollChatPosts() #Obtenim els posts del xat
        chatEvents = [chatEvent.message for chatEvent in chatEvents if chatEvent.message is not None] #Obtenim els missatges que tinguin contingut filtrar(functional)
        if (len(chatEvents) > 0 ):
            lastMessage = chatEvents[-1]
            with self.lock:
                for a in self.bots:
                    if a.getEvent in lastMessage:
                        print(f"S'activat el BOT! {a}")

    def threadListener(self):
        while True:
            time.sleep(2)
            self.actionListener
    
    
    
class BotFramework: #Definim la classe pare, el qual sera el contracte per al nostre framework de bots
    mc = None
    manager = None
    def __init__(self):
        self.manager = BotManagerSingleton() #Obtenim la instancia del manegador
        self.manager.addBot(self) #Afegim el bot al nostre manager, quan fem la crida al constructor de la classe
        self.mc = self.manager.mc #Obtenim mateixa connexio per a tots els bots
        #TODO Crear thread que farà crida al actionListener que permetrà actuar cada vegada que tinguem un post al chat
        
    #Quan s'elimina instancia de la classe, es borra el bot també per tant deixa de funcionar
    def __del__(self):  self.manager.removeBot(self)
    
    #Important sobreescriu el metode toString per saber de quin bot es tracta, tot i que cadascun tindra una funcionalitat i activació diferent    
    def __str__(self) -> str:
        return "Soc un BOT"
    
    #Mètode del contracte que s'ha de redefinir per fer cada funcionalitat
    def doSomething(self):
        pass
    
    #Event que ens activa el framework, depen de cada bot s'activarà amb una paraula clau diferent (comanda d'execucio dels bots) FORMAT= ':nomComanda'
    def getEvent(self):
        pass


    