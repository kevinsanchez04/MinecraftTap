from BotManager import BotManagerSingleton
import InsultBot
import Gemini
import TNTBot

insult = InsultBot.InsultBot()
tnt = TNTBot.TNTBot()
gemini = Gemini.Gemini()

BotManagerSingleton().managerThread.join()