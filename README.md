[![codecov](https://codecov.io/gh/kevinsanchez04/MinecraftTap/graph/badge.svg?token=5S73I6PK6V)](https://codecov.io/gh/kevinsanchez04/MinecraftTap)

<h1>Manual of Instalation of the TEST or ONLY THE BOTS</h1>

<h2>Instalation TEST</h2>
  <ol>
    <li>Go to <b>MinecraftTap/AdventuresInMinecraft-PC-master</b></li>
    <li>Execute the file <b>StartServer.bat</b></li>
    <li>Open a Command Line Interface</li>
    <li>Execute command <b>ipconfig</b> and take the IP ADRESS</li>
    <li>Go to the file <b>MinecraftTap/AdventuresInMinecraft-PC-master/MyAdventures/BotManager</b> in line 33,34 put your IP ADRESS</li>
    <li>Open a Command Line Interface</li>
    <li>Go to <b>MinecraftTap/AdventuresInMinecraft-PC-master/MyAdventures</b> with cd command</li>
    <li>Install Coverage with the command pip install coverage</li>
    <li>Execute 
      <b>
        coverage run --omit="mcpi/*,test1.py" -m unittest test1.py
      </b>
    </li>
    <li>Open Minecraft and connect to the server which is in localhost</li>
    <li>Write in the chat <b>:InsultBot</b></li>
    <li>Wait 5 seconds</li>
    <li>Write in the chat <b>:stopInsultBot</b></li>
    <li>Wait to the test to finish</li>
    <li>Once finished write in the Command Line Interface where executed the coverage this <b>command coverage report -m</b></li>
    <li>
      Now this one <b>coverage html</b>
      <p>Once done this you can open the files and see the coverage of the test and how it went</p>
    </li>
  </ol>
<h2>Instalation for PLAYING with the BOTS</h2>
  <ol>
    <li>Go to <b>MinecraftTap/AdventuresInMinecraft-PC-master</b></li>
    <li>Execute the file <b>StartServer.bat</b></li>
    <li>Open a Command Line Interface</li>
    <li>Execute command <b>ipconfig</b> and take the IP ADRESS</li>
    <li>Go to the file <b>MinecraftTap/AdventuresInMinecraft-PC-master/MyAdventures/BotManager</b> in line 33,34 put your IP ADRESS</li>
    <li>Execute the file <b>MinecraftTap/AdventuresInMinecraft-PC-master/MyAdventures/main.py</b></li>
    <li>Open Minecraft and connect to the server which is in localhost</li>
    <li>
      You can put in the chat this commands ( Activate Bot <-----> Desactivate Bot )
        <ul>
          <li><b>:InsultBot</b> <-----> <b>:stopInsultBot</b></li>
          <li><b>:TNTBot</b> <-----> <b>:stopTNTBot</b></li>
          <li><b>:Gemini</b> <-----> <b>:stopGemini<b/></li>
        </ul>
    </li>
  </ol>
<h1>!!!ENJOY!!!</h1>
