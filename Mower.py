from Cited.cmu_112_graphics import *
from Objects.Zombies import *
from Objects.Plants import *
#This class contains the class for each lawn mower
class Mower(object):
    def __init__(self, game, row):
        self.game = game
        self.sprite = image=ImageTk.PhotoImage(self.game.spriteImages[6])
        self.row = row
        self.ready = True
        self.x = 220
        self.y = self.row*self.game.cellHeight+self.game.cellHeight
        self.moving = False
        self.time = 0

    def useMower(self):
        self.ready = False
        self.moving = True
        if self.moving == True:
            limit = 50/self.game.timerDelay
            if self.time % limit == 0:
                self.x += 50

    def addTime(self):
        self.time +=1
        if self.moving:
            self.useMower()
            for cell in self.game.grid:
                if isinstance(cell.plant, Plant) and cell.plant.alive == False:
                    cell.plant = None

    def renderMower(self,canvas):
        canvas.create_image(self.x, self.y, image=self.sprite)