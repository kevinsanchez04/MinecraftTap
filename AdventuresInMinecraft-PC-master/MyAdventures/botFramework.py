import mcpi.minecraft as minecraft


class BotFramework: #Definim la classe pare, el qual sera el contracte per al nostre framework de bots
    mc = minecraft.Minecraft.create()
    #Mètode del contracte que s'ha de redefinir per fer cada funcionalitat
    def doSomething(self):
        pass
    
    #Event que ens activa el framework
    def getEvent(self):
        chatEvents = self.mc.events.pollChatPosts()
        chatEvents = [chatEvent for chatEvent in chatEvents if chatEvent.message is not None] #Filter dels events del xat
        #for chatEvent in chatEvents:
            #print (chatEvent)
        if("framework" in chatEvent.message for chatEvent in chatEvents):
            self.doSomething()