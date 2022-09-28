from Cited.cmu_112_graphics import *
import random
from Cited.Snippets import *
#This file contains the class for the falling suns
class FallingSun(object):
    def __init__(self, game):
        self.game = game
        self.x = x = random.randrange(245, (9*self.game.cellWidth + 245))
        self.y = 0
        self.time = 0
        self.stopRow = random.randint(0,4)
        self.currRow = -1
        
    def increaseTime(self):
        self.time += 1
        self.currRow = (self.y - 75) // self.game.cellHeight
        if not self.currRow == self.stopRow:
            self.y += 7
    
    def takeSun(self):
        self.game.sunsCollected += 25
        self.game.fallingSuns = []
    
    def renderSun(self,canvas):
        image = self.game.spriteImages[3]
        width, height = image.size
        yOffset = height//2
        xOffset = width//2
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(image))
        canvas.create_oval(self.x - xOffset, self.y - yOffset, self.x + xOffset, self.y + yOffset, width=0, onClick=self.takeSun)
