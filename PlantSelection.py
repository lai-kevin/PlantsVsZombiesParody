from Cited.cmu_112_graphics import *
from Objects.Zombies import *
from Objects.Plants import *
#This file contains the class for the selection menu on the left of the screen
class PlantSelection(object):
    def __init__(self, game, images):
        self.game = game
        self.images = images #already scaled
        self.leftMargin = 5
        self.topMargin = 50
        self.cellWidth = 80
        self.cellHeight = 80
        self.highlight = None
        self.plantSelected = None
        self.borders = []
        for imageCol in range(len(self.images)):
            x0 = self.leftMargin + self.cellWidth
            x1 = x0 + self.cellWidth
            y0 = imageCol * self.cellHeight + self.topMargin
            y1 = y0 + self.cellHeight
            plant = imageCol
            self.borders.append((x0, y0, x1, y1, plant))

    def checkBounds(self, x, y):
        for x0, y0, x1, y1, plant in self.borders:
            if x0 < x < x1 and y0 < y < y1:
                self.highlight = x0, y0, x1, y1
                self.plantSelected = self.strPlant(plant)
                return True

    def strPlant(self, plantNum):
        if plantNum == 0:
            return "peaShooter"
        if plantNum == 1:
            return "sunFlower"
        if plantNum == 2:
            return "walnut"

    def render(self,canvas):
        for imageCol in range(len(self.images)):
            x0 = self.leftMargin + self.cellWidth
            x1 = x0 + self.cellWidth
            y0 = imageCol * self.cellHeight + self.topMargin
            y1 = y0 + self.cellHeight
            canvas.create_rectangle(x0-self.cellWidth//2,y0,x1,y1,fill="green")
            if (x0, y0, x1, y1) == self.highlight:
                canvas.create_rectangle(x0, y0, x1, y1, fill="Yellow")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="Black")
            canvas.create_image((x0+x1)//2, (y0+y1)//2, image=ImageTk.PhotoImage(self.images[imageCol]))
            textX = (x0-self.cellWidth//2 + x0)//2
            textY = (y0+y1)//2
            cost = ""
            if imageCol == 0: cost = "100"
            if imageCol == 1: cost = "50"
            if imageCol == 2: cost = "50"
            canvas.create_text(textX, textY, text=cost, font="Arial 15 bold", fill="yellow")

