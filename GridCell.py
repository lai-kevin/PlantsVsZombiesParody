from Objects.Plants import *
from Cited.cmu_112_graphics import *
#This file contains the class of the cells of the yard
#Each cell has a plant attribute
class GridCell(object):
    def __init__(self, game, row, col):
        self.col = col
        self.row = row
        self.game = game
        self.cellWidth = self.game.cellWidth
        self.cellHeight = self.game.cellHeight
        self.leftMargin = 245
        self.topMargin = 75
        self.brighten = False
        self.plant = None
        self.selected = False
        x0 = self.cellWidth * self.col + self.leftMargin
        x1 = x0 + self.cellWidth
        self.centerX = (x0 + x1)//2

    def renderCell(self,canvas):
        x0 = self.cellWidth * self.col + self.leftMargin
        x1 = x0 + self.cellWidth
        y0 = self.cellHeight * self.row + self.topMargin
        y1 = y0 + self.cellHeight
        centerX, centerY = (x0 + x1)//2, (y0 + y1)//2
        if self.brighten: 
            canvas.create_rectangle(x0, y0, x1, y1, fill="Gray60")
        if self.plant != None:
            canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(self.plant.image))
    
    def takeSun(self):
        if isinstance(self.plant, SunFlower):
            self.plant.takenSun()
            self.game.sunsCollected += 25

    def renderSpawnedSun(self,canvas):
        if isinstance(self.plant, SunFlower):
            x0 = self.cellWidth * self.col + self.leftMargin
            x1 = x0 + self.cellWidth
            y0 = self.cellHeight * self.row + self.topMargin
            y1 = y0 + self.cellHeight
            centerX, centerY = (x0 + x1)//2, (y0 + y1)//2
            if self.plant.spawnSun:
                canvas.create_oval(x0, y0, x1, y1,width=0, onClick= self.takeSun)
                canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(self.plant.sunImage))

