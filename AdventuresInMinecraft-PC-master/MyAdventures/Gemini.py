import google.generativeai as genai
from BotManager import BotFramework, BotManagerSingleton


class Gemini(BotFramework):
    
    genai.configure(api_key="AIzaSyDQGxOj5gcORaUfp3sulsiDrEhAmcBfVhI")
    model = genai.GenerativeModel("gemini-1.5-flash")    
    clau = "gemini"
    missatgeAnt = None

    def doSomething(self):
        chat = BotManagerSingleton().getChat()
        if self.clau in chat and self.missatgeAnt != chat :
            response = self.model.generate_content(chat)
            self.mc.postToChat(response.text)
            print(response.text)
        self.missatgeAnt = chat

    def getEvent(self):
        return ":Gemini" #Cadena de caracters que actuara com una comanda d'activació del bot
    
    def __str__(self) -> str:
        return "<Gemini> "
    
    def getStop(self):
        return ":stopGemini"