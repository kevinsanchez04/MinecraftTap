import unittest

from InsultBot import InsultBot
from TNTBot import TNTBot
from Gemini import Gemini

from BotManager import BotManagerSingleton

class TestBotFramework(unittest.TestCase):

    @classmethod 
    def setUpClass(cls): 
        print("Setting up the class...") 
        cls.insult = InsultBot()
        cls.tnt = TNTBot()
        cls.gemini = Gemini()

    def test_instance(self):
        self.assertIsInstance(self.insult, InsultBot)
        self.assertIsInstance(self.tnt, TNTBot)
        self.assertIsInstance(self.gemini,Gemini)

    def tearDown(self):
        self.insult.__del__()
        self.tnt.__del__()
        self.gemini.__del__()
        BotManagerSingleton().stop_manager()

if __name__ == '__main__':
    unittest.main()
