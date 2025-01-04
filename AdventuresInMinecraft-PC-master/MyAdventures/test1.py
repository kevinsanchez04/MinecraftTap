import unittest
import time
import os
import Pyro5.api
import mcpi.connection
import mcpi.minecraft as minecraft
import mcpi as mcpi

from InsultBot import InsultBot
from TNTBot import TNTBot
from Gemini import Gemini

from BotManager import BotManagerSingleton,BotFramework

class TestBotFramework(unittest.TestCase):

    @classmethod 
    def setUpClass(cls): 
        print("Setting up the class...") 
        cls.insult = InsultBot()
        cls.tnt = TNTBot()
        cls.gemini = Gemini()

    @classmethod 
    def tearDownClass(self):
        self.insult.__del__()
        self.tnt.__del__()
        self.gemini.__del__()
        BotManagerSingleton().stop_manager()

    def test_instance(self):
        self.assertIsInstance(self.insult, InsultBot)
        self.assertIsInstance(self.tnt, TNTBot)
        self.assertIsInstance(self.gemini,Gemini)

    def test_str(self):
        self.assertEqual(self.insult.__str__(),"<InsultBOT> ")
        self.assertEqual(self.tnt.__str__(),"<TNTBOT> ")
        self.assertEqual(self.gemini.__str__(),"<Gemini> ")
        self.assertEqual(self.insult.getStop(),":stopInsultBot")
        self.assertEqual(self.tnt.getStop(),":stopTNTBot")
        self.assertEqual(self.gemini.getStop(),":stopGemini")
        self.assertEqual(self.insult.getEvent(),":InsultBot" )
        self.assertEqual(self.tnt.getEvent(),":TNTBot")
        self.assertEqual(self.gemini.getEvent(),":Gemini")

    def test_actionListener(self):
        con = True
        while con: 
            message =  BotManagerSingleton().lastMessage  
            if message is not None:
                self.assertEqual(message,":InsultBot")
                time.sleep(2)
                self.assertTrue(self.insult.threadRun)
                BotManagerSingleton().lastMessage = None
                while con:
                    message =  BotManagerSingleton().lastMessage  
                    if message is not None:
                        self.assertEqual(message,":stopInsultBot")
                        time.sleep(2)
                        self.assertFalse(self.insult.threadRun)
                        con = False

    def test_something(self):
        self.insult.startBot()
        self.assertEqual(self.insult.threadRun,True)
        # self.assertEqual(True,self.methodAuxiliar())
        self.insult.stopBot()
        self.assertEqual(self.insult.threadRun,False)
        time.sleep(5)
        self.assertTrue(self.methodAuxiliar(self.insult.getMessages()))

    def test_getChat(self):
        BotManagerSingleton().lastMessage = "aquesta es una prova"
        self.assertEqual(BotManagerSingleton().getChat(),'aquesta es una prova')

    def test_stopManager(self):
        self.assertEqual(BotManagerSingleton().getStop(),":stopManager")
    
    def test_geminiBot(self):
        self.gemini.startBot()
        BotManagerSingleton().lastMessage = "gemini what de we are today?"
        time.sleep(5)
        self.gemini.stopBot()
        self.assertTrue(self.methodAuxiliar("I'm Gemini and "))

    def test_tntBot(self):
        mc = minecraft.Minecraft.create()
        con = True
        while con :
            try:
                con = False
                # print(mc.player.getPos())
                self.tnt.startBot()
                self.assertEqual(self.tnt.threadRun,True)
                time.sleep(3)
                self.tnt.stopBot()
                self.assertEqual(self.tnt.threadRun,False)
            except mcpi.connection.RequestError :
                 print("No player found so you have failed")

    def test_pyro(self):
        ns = Pyro5.api.locate_ns(host="192.168.5.206", port=9090)
        uri = ns.lookup("MinecraftServer")
        server = Pyro5.api.Proxy(uri)
        self.assertEqual(server.send_message(":InsultBot"),"Message received")
        time.sleep(5)
        self.assertEqual(server.send_message(":stopInsultBot"),"Message received")
        BotManagerSingleton().stop_manager()
    
    def methodAuxiliar(self, listInsult):
        trobat = False
        file_name = '../Server/logs/latest.log'
        file_path = os.path.abspath(file_name)
        with open(file_path,'r') as file:
            lines = file.readlines()
            cmp = 0
            for line in reversed(lines):
                print(line)
                if trobat or cmp == 3:
                    break
                for word in listInsult:
                    if word in line:
                        trobat = True
                        break
                cmp += 1
        return trobat

if __name__ == '__main__':
    unittest.main()