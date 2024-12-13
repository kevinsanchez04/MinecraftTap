import Pyro5.api

ns = Pyro5.api.locate_ns(host="192.168.5.207", port=9090)
uri = ns.lookup("MinecraftServer")
server = Pyro5.api.Proxy(uri)
print(server.send_message("Hola desde el cliente"))
