from Cited.cmu_112_graphics import *
from StartMode import *
from PlayMode import *
from EndMode import *
from HelpMode import *
class Game(ModalApp):
    def appStarted(self):
        self.addMode(Play(name="play"))
        play = self.getMode("play")
        self.addMode(End(name="end"))
        self.addMode(Start(name="start"))
        self.addMode(Help(name="help"))
        self.setActiveMode("start")



