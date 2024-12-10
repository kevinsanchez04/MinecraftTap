import Pyro5.api

server = Pyro5.api.Proxy("PYRO:obj_40e6a6dd034549ac8f5d8c42d8001d64@10.112.153.180:53263")
response = server.actionListener(":TNTBot")
print(response)