import Pyro5.api

@Pyro5.api.expose
class UseServer():
    def send_message(self, message):
        with open('./AdventuresInMinecraft-PC-master/MyAdventures/pyro.txt','w') as archivo:
            archivo.write(f'{message}\n')
        print(f"Received message:{message}")
        return "Message received"
    
daemon = Pyro5.api.Daemon(host="192.168.1.107")
uri = daemon.register(UseServer)
print(f"This is the uri they need for the server is --> {uri} <--")
daemon.requestLoop()
print("HOLA")