from Cited.cmu_112_graphics import *
from Cited.Snippets import *
from Objects.Zombies import *
from Objects.Plants import *
import os
import pickle
#This file contains the Start mode which contains the button to enter game
#and button to load a saved game

class Start(Mode):
    def appStarted(self):
        #Image from: https://images8.alphacoders.com/419/thumb-1920-419230.jpg
        self.background = self.loadImage('startBackground.jpg')
        width,height = self.background.size
        self.background = self.scaleImage(self.background, 1500/width)
        self.enterValidPrompt = None
        self.content = None
        self.play = self.getMode("play")

    def enterGame(self):
        self.setActiveMode("play")
    
    def readSavedGame(self):
        for item in os.listdir("Saves"):
            itemPath = "Saves" + os.sep + item
            if os.path.isfile(itemPath):
                itemName = item.split(".")[0]
                if itemName == self.savedGameName:
                    with open(itemPath, "r+") as save:
                        content = save.read()
                        return content
        print("File not found")
        return False

    def loadSave(self):
        savedGame = self.getUserInput("Enter Save Name")
        if savedGame != None:
            savedGamePath = savedGame + ".dat"
            try:
                print("tried")
                content = pickle.load(open(savedGamePath, "rb"))
            except:
                self.enterValidPrompt = True
            else:
                print("File exists")
                content = pickle.load(open(savedGamePath, "rb"))
                self.enterGame()
                self.play.sunsCollected = content["suns"]
                self.play.time = content["time"]
                self.play.score = content["score"]
                self.play.currentRound = content["currentRound"]

                for col, row, name, health in content["gridInfo"]:
                    newPlant = None
                    if name == "PeaShooter":
                        newPlant = PeaShooter(self.play, row, col, self.play.plantImages[0])
                    if name == "SunFlower":
                        newPlant = SunFlower(self.play, row, col, self.play.plantImages[1], self.play.spriteImages[3])
                    if name == "Walnut":
                        newPlant = Walnut(self.play, row, col, self.play.plantImages[2])
                    newPlant.health = health
                    for cell in self.play.grid:
                        if cell.row == row and cell.col == col:
                            cell.plant = newPlant

                for spawnRow, x, health, name in content["zombies"]:
                    newZombie = None
                    if name == "basic":
                        newZombie = Zombie(self.play, spawnRow, ImageTk.PhotoImage(self.play.spriteImages[4]), self.play.grid)
                    if name == "cone":
                        newZombie = ConeHead(self.play, spawnRow, ImageTk.PhotoImage(self.play.spriteImages[8]), self.play.grid)
                    if name == "path":
                        newZombie = PathFindingZombie(self.play, spawnRow, ImageTk.PhotoImage(self.play.spriteImages[7]), self.play.grid)
                    newZombie.health = health
                    newZombie.x = x
                    self.play.zombies.append(newZombie)

    def redrawAll(self,canvas):
        canvas.create_image(self.width//2,self.height//2,
                            image=ImageTk.PhotoImage(self.background))
        drawButton(canvas, self.width//2, self.height//2, self.width//5,
                    self.height//10, self.enterGame, "New Game")
        drawButton(canvas, self.width//2, self.height//2 + 70, self.width//5,
                    self.height//10, self.loadSave, "Load Saved Gane")
        if self.enterValidPrompt:
            canvas.create_rectangle(self.width-300, 0, self.width, 100, fill="red")
            canvas.create_text(self.width-150, 50, text="ENTER EXISTING SAVE NAME!")
        x0 = self.width//2 - 300
        x1 = x0 + 600
        y0 = self.height//2 - 250
        y1 = y0 + 100
        canvas.create_rectangle(x0,y0,x1,y1,fill="Black")
        canvas.create_text(self.width//2, self.height//2 - 200, text="PLANTS VS SMART ZOMBIES", font="Arial 30 bold", fill="White")
