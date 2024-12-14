import json
import time
import datetime
from BotManager import BotFramework

class Jugador():

    def __init__(self, x=-1, y=-1, z=-1, id=0, hora=0):
        self.x = x
        self.y = y
        self.z = z
        self.id = id
        self.hora=hora
    
    def __str__(self):
        return f"Jugador(x={self.x}, y={self.y}, z={self.z}, id={self.id}, hora={self.hora})"
    
    def fitxerInformacio(self):
        """Guarda la información del jugador en un archivo JSON con comentarios simulados."""
        data = {
            "comentari": f"Aquestes son les dades del jugador:{self.id}",
            "id": self.id,
            "posicioX": self.x,
            "posicioY": self.y,
            "posicioZ": self.z,
            "horaActualitzacio" : str(self.hora) 
        }
        filename = f"Jugador{self.id}.json" # Fem servir el fitxer amb nom Jugador1.json on 1 es la id per escriure la nova informacio
        with open(filename, "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  # indent=4 per millor la llegibilitat, ensure_ascii a false ens permet guardar caracters especials
        print(f"Informació del jugador guardada en {filename}")
    


class ReflectionBot(BotFramework):
    
    jugadors: list[Jugador] = [] #Llista buida de jugadors
    
    def doSomething(self):
        if len(self.jugadors) > 0:
            """Mitjançant reflection actualitzem la classe Persona i cridem als seus metodes"""
            for usuari in self.jugadors:
                posicio = self.mc.entity.getPos(usuari.id) #Obtindrem les dades de cada usuari en temps real
                if(hasattr(usuari, "x")): setattr(usuari,"x",posicio.x)
                if(hasattr(usuari, "y")): setattr(usuari,"y",posicio.y)
                if(hasattr(usuari, "z")): setattr(usuari,"z",posicio.z)
                if(hasattr(usuari, "hora")): setattr(usuari, "hora", datetime.datetime.now())
                if(hasattr(usuari, "fitxerInformacio")):
                    metode = getattr(usuari, "fitxerInformacio")
                    if(callable(metode)):
                        metode() #Guardem les dades de l'usuari en format JSON
                
        else:
            entityIds = self.mc.getPlayerEntityIds()
            for entityId in entityIds:
                nouJugador = Jugador()
                self.jugadors.append(nouJugador)
                nouJugador.id = entityId
        time.sleep(2) #Actualitzara el valor de tant en tant
    def getEvent(self):
        return ":ReflectionBot" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def __str__(self) -> str:
        return "<ReflectionBOT> "
    
    def getStop(self):
        return ":stopReflectionBot"
    

reflectionBot = ReflectionBot()
reflectionBot.manager.managerThread.join()