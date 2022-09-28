#This file contains the class for the cell of the selection box
class PlantSelection(object):
    def __init__(self, game, images):
        self.game = game
        self.images = images #already scaled
        self.leftMargin = 10
        self.topMargin = 50
        self.cellWidth = 80
        self.cellHeight = 80

    def render(self,canvas):
        for imageCol in range(len(self.images)):
            x0 = self.leftMargin + self.cellWidth
            x1 = x0 + self.cellWidth
            y0 = imageCol * self.cellHeight + self.topMargin
            y1 = y0 + self.cellHeight
            canvas.create_image((x0+x1)//2, (y0+y1)//2, image=ImageTk.PhotoImage(self.images[imageCol]))