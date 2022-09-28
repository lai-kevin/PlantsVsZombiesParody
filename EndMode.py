from Cited.cmu_112_graphics import *
#This file contains the class for the end screen
class End(Mode):
    def appStarted(self):
        self.game = self.getMode("play")
        self.score = self.game.score
    def keyPressed(self,event):
        if event.key == "r":
            self.game.appStarted()
            self.setActiveMode("play")
    def redrawAll(self,canvas):
        canvas.create_rectangle(0,0,5000,5000, fill="Green")
        canvas.create_text(self.width//2, self.height//2 - 100, text="YOU ARE DEAD",font="Arial 50 bold", fill="White")
        canvas.create_text(self.width//2, self.height//2, text=f" Score: {str(self.score)}",font="Arial 50 bold", fill="White")
        canvas.create_text(self.width//2, self.height//2 + 100, text="Press r to restart",font="Arial 40 bold", fill="White")