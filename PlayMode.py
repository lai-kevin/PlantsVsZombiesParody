from Cited.cmu_112_graphics import *
from Objects.Plants import *
from Objects.Zombies import *
from GridCell import *
from Cited.Snippets import *
import sys
import random
import pickle
from PlantSelection import *
from FallingSun import *
from Mower import *
#This file contains the Play mode which handles timing, animations, and game status
class Play(Mode):
    def appStarted(self):
        self.timerDelay = 100
        self.score = 0
        self.effectiveWidth = 740
        self.effectiveHeight = 500
        self.cellWidth = self.effectiveWidth//9
        self.cellHeight = self.effectiveHeight//5
        #Image from: https://vignette.wikia.nocookie.net/plantsvszombies/images/3/38/Background1.jpg/revision/latest?cb=20160502033025
        self.background = self.loadImage('background.jpg')
        self.grid = []
        for row in range(5):
            for col in range(9):
                gridCell = GridCell(self, row, col)
                self.grid.append(gridCell)

        self.spriteImages = self.loadSprites()
        self.plantImages = [self.spriteImages[i] for i in range(3)]
        self.selectionBox = PlantSelection(self, self.plantImages) 
        self.time = 1
        self.sunsCollected = 100
        self.fallingSuns = []
        self.zombies = []
        self.peas = []
        self.shovelActive = False
        self.mowers = []
        self.selectionHistory = []
        self.timerToNext = 0
        self.zombieSpawnTotal = 0
        self.currentRound = 1
        self.maxPerRow = 3
        self.maxZombies = 5
        self.rowStrat = [] #Contains the threat and defence of each row
        for row in range(5):
            mower = Mower(self, row)
            self.mowers.append(mower)
        self.paused = False

    def loadSprites(self):
        images = []
        #Image from https://vignette.wikia.nocookie.net/plantsvszombies/images/0/09/1769829-plant_peashooter_thumb.png/revision/latest/scale-to-width-down/340?cb=20200213115004
        peaShooterImage = self.loadImage("Objects/peashooter.png")
        width, height = peaShooterImage.size
        scale = 70/width
        peaShooterImage = self.scaleImage(peaShooterImage, scale)
        images.append(peaShooterImage)
        #Imgage from https://vignette.wikia.nocookie.net/plantsvszombies/images/e/e6/1769830-plant_sunflower_smiling_thumb.png/revision/latest/scale-to-width-down/340?cb=20200119194632
        sunFlowerImage = self.loadImage("Objects/sunflower.png")
        width, height = sunFlowerImage.size
        scale = 70/width
        sunFlowerImage = self.scaleImage(sunFlowerImage, scale)
        images.append(sunFlowerImage)
        #Image from https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/1fbfcdba-5992-4f16-a756-c823fbc6ffaa/d4r1st1-f6d5cb6b-067d-4c30-bd04-4eb56fd35a83.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMWZiZmNkYmEtNTk5Mi00ZjE2LWE3NTYtYzgyM2ZiYzZmZmFhXC9kNHIxc3QxLWY2ZDVjYjZiLTA2N2QtNGMzMC1iZDA0LTRlYjU2ZmQzNWE4My5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.cjdvcX5nczmUpemB9gbNP2WBzyUwIl4-U1Q4S44v-Jc
        walnutImage = self.loadImage("Objects/walnut.png")
        width, height = walnutImage.size
        scale = 70/width
        walnutImage = self.scaleImage(walnutImage, scale)
        images.append(walnutImage)
        #Image from https://vignette.wikia.nocookie.net/plantsvszombies/images/b/b8/Sun_PvZ2.png/revision/latest/scale-to-width-down/340?cb=20160323031552
        sunImage = self.loadImage("Objects/sun.png")
        width,height = sunImage.size
        scale = 60/width
        sunImage = self.scaleImage(sunImage,scale)
        images.append(sunImage)
        #Image from https://www.pngkey.com/png/full/13-131493_zombie-png-plants-vs-zombies-zombie.png
        zombieImage = self.loadImage("Objects/zombie1.png")
        width, height = zombieImage.size
        scale = self.cellWidth/width
        zombieImage = self.scaleImage(zombieImage,scale)
        images.append(zombieImage)
        #Image from https://vignette.wikia.nocookie.net/plantsvszombies/images/b/ba/Shovel2.png/revision/latest/top-crop/width/220/height/220?cb=20120319163030
        shovelImage = self.loadImage("Objects/shovel.png")
        width,height = shovelImage.size
        scale = 80/width
        shovelImage = self.scaleImage(shovelImage,scale)
        images.append(shovelImage)
        #Image from https://www.google.com/search?q=plants+vs+zombies+lawn+mower&tbm=isch&source=iu&ictx=1&fir=DZ27DLhxr9SgNM%252CQlUfxT7XeHwaOM%252C_&vet=1&usg=AI4_-kRwQmgyw3UDzEBJfj72gXyUnu-2PA&sa=X&ved=2ahUKEwjug9rjxoLrAhWRlXIEHVxDBY0Q9QEwA3oECAoQIA&biw=1423&bih=641&dpr=2.25#imgrc=qToZKMWza6sfCM
        mowerImage = self.loadImage("Objects/mower.png")
        width,height = mowerImage.size
        scale = 60/width
        mowerImage = self.scaleImage(mowerImage,scale)
        images.append(mowerImage)
        #Image from https://t7.rbxcdn.com/19687ce95fe7a28d5b2af4ed02a3927c
        pathZombie = self.loadImage("Objects/pathFindingZombie.png")
        width,height = pathZombie.size
        scale = self.cellWidth/width
        pathZombieImage = self.scaleImage(pathZombie,scale)
        images.append(pathZombieImage)
        #Image from https://vignette.wikia.nocookie.net/plantsvszombies/images/a/a7/Conehead2009HD.png/revision/latest/scale-to-width-down/340?cb=20170904195329
        coneHeadZombie = self.loadImage("Objects/conehead.png")
        width, height = coneHeadZombie.size
        scale = self.cellWidth/width
        coneHeadZombie = self.scaleImage(coneHeadZombie,scale)
        images.append(coneHeadZombie)
        return images

    def timerFired(self):
        if self.paused == False:
            self.time += 1
            for cell in self.grid:
                if isinstance(cell.plant, Plant):
                    cell.plant.increaseTime()
            limitFallingSun = 5000//self.timerDelay
            if self.time % limitFallingSun == 0:
                if len(self.fallingSuns) == 0:
                    fallingSun = FallingSun(self)
                    self.fallingSuns.append(fallingSun)
            for sun in self.fallingSuns:
                sun.increaseTime()
            for cell in self.grid:
                if isinstance(cell.plant, Plant):
                    cell.plant.increaseTime()
            for zombie in self.zombies:
                zombie.increaseTime()
            if self.zombieSpawnTotal >= self.maxZombies:
                if self.zombies == []:
                    for cell in self.grid:
                        if isinstance(cell.plant, PeaShooter):
                            cell.plant.shoot = False
                    self.currentRound += 1
                    self.maxZombies  = 10*self.currentRound
            self.spawnZombies()
            self.loadPeasAndCheckCollison()
            for mower in self.mowers:
                mower.addTime()
            if self.selectionHistory != []:
                lastPlant, lastTime = self.selectionHistory[-1]
                self.timerToNext = 40 - (self.time - lastTime)
                if self.timerToNext < 0: self.timerToNext = 0

    def loadPeasAndCheckCollison(self):
        for cell in self.grid:
            if isinstance(cell.plant, PeaShooter):
                self.peas.extend(cell.plant.peas)
        for zombie in self.zombies:
            if zombie.alive == False:
                self.zombies.remove(zombie)

    def saveGame(self):
        self.paused = True
        saveName = self.getUserInput("Enter a name for this save")
        if saveName != None:
            self.paused = False
            allDataPath = saveName + ".dat"
            gridInfo = []
            for cell in self.grid:
                if cell.plant != None:
                    gridInfo.append((cell.col,cell.row,cell.plant.name,cell.plant.health))
            zombieInfo = []
            for zombie in self.zombies:
                zombieInfo.append((zombie.spawnRow, zombie.x, zombie.health, zombie.name))
            allData = {"time":self.time, "suns":self.sunsCollected,
                    "score":self.score, "currentRound":self.currentRound,
                    "zombies":zombieInfo, "gridInfo":gridInfo
                    }
            pickle.dump(allData, open(allDataPath,"wb"))  
        else:
            self.paused = False

    def keyPressed(self,event):
        if event.key == "s":
            self.saveGame()

    def spawnZombies(self):
        spawnFreq = (10000-self.currentRound * 1000)
        if spawnFreq < 5000:
            spawnFreq = 5000
        spawnLimit = spawnFreq//self.timerDelay
        averageRowStrength = []
        spawnGroupRow = 0
        #First Round is random
        if self.currentRound == 1:
            limit = spawnLimit                          
            if self.time % limit == 0:
                spawnRow = random.randint(0,4)
                zombieCount = 0
                for zombie in self.zombies:
                    if zombie.spawnRow == spawnRow:
                        zombieCount += 1
                if zombieCount < self.maxPerRow:
                    newZombie = Zombie(self, spawnRow, ImageTk.PhotoImage(self.spriteImages[4]), self.grid)
                    if self.zombieSpawnTotal < self.maxZombies:
                        self.zombieSpawnTotal += 1
                        self.zombies.append(newZombie)
        else:
            #Path Finding Zombie
            if self.time % (12000//self.timerDelay) == 0:
                spawnRow = random.randint(0,4)
                newZombie = PathFindingZombie(self, spawnRow, ImageTk.PhotoImage(self.spriteImages[7]), self.grid)
                if self.zombieSpawnTotal < self.maxZombies:
                    self.zombieSpawnTotal += 1
                    self.zombies.append(newZombie)

            limit = spawnLimit                                
            if self.time % limit == 0:
                threatAndDefence = []
                for row in range(5):
                    rowThreat = 0
                    rowDefence = 0
                    for cell in self.grid:
                        if cell.row == row and cell.plant != None:
                            rowThreat += cell.plant.threat
                            rowDefence += cell.plant.defence
                        if cell.row == row and cell.plant == None:
                            rowThreat += 0
                            rowDefence += 0
                    average = (rowThreat+rowDefence)/2
                    threatAndDefence.append((rowThreat, rowDefence, average))
                self.rowStrat = threatAndDefence
                total = 0
                for row in range(5):
                    rowThreat, rowDefence, average = self.rowStrat[row]
                    averageRowStrength.append(average)
                    total += average
                for row in averageRowStrength:
                    if total != 0:
                        row = row/total
                    else:
                        row = 0
                weakestRow = averageRowStrength.index(min(averageRowStrength))
                spawnGroupRow = averageRowStrength.index(max(averageRowStrength))
                choices = []
                coneZombie = ConeHead(self, weakestRow, ImageTk.PhotoImage(self.spriteImages[8]), self.grid)
                normalZombie = Zombie(self, weakestRow, ImageTk.PhotoImage(self.spriteImages[4]), self.grid)
                choices.extend([coneZombie,normalZombie])
                if self.zombieSpawnTotal < self.maxZombies:
                    newZombie = random.choice(choices)
                    self.zombies.append(newZombie) 
                    self.zombieSpawnTotal += 1
            #attacks strongest section
            limitZombieGroup = spawnFreq * 4//self.timerDelay
            if self.time % limitZombieGroup == 0:
                zombieGroup = random.randint(1,3)
                for i in range(zombieGroup):
                    newZombie = Zombie(self, spawnGroupRow, ImageTk.PhotoImage(self.spriteImages[4]), self.grid)
                    newZombie.x -= 20*i
                    if self.zombieSpawnTotal < self.maxZombies:
                        self.zombies.append(newZombie)
                        self.zombieSpawnTotal += 1

    def mousePressed(self,event):
        if self.shovelActive:
            col = (event.x - 245) // self.cellWidth
            row = (event.y - 75) // self.cellHeight
            for cell in self.grid:
                if cell.row == row and cell.col == col:
                    cell.plant = None
                    self.shovelActive = False
        else:
            self.shovelActive = False

    def mouseDragged(self,event):
        if 245 < event.x < (9*self.cellWidth + 245) and 75 < event.y < (5*self.cellHeight+75) and self.selectionBox.highlight != None:
            hoverCol = (event.x - 245) // self.cellWidth
            hoverRow = (event.y - 75) // self.cellHeight
            for cell in self.grid:
                if cell.row == hoverRow or cell.col == hoverCol:
                    cell.brighten = True
                else:
                    cell.brighten = False

    def mouseReleased(self,event):
        if not self.selectionBox.checkBounds(event.x, event.y):
            self.selectionBox.highlight = None
        if 245 < event.x < (9*self.cellWidth + 245) and 75 < event.y < (5*self.cellHeight+75):
            plantCol = (event.x - 245) // self.cellWidth
            plantRow = (event.y - 75) // self.cellHeight
            if self.selectionBox.plantSelected != None:              
                newPlant = None
                if self.selectionBox.plantSelected == "peaShooter":
                    image = self.plantImages[0]
                    width, height = image.size
                    scale = self.cellWidth/width
                    image = self.scaleImage(image, scale)
                    newPlant = PeaShooter(self, plantRow, plantCol, image)
                    self.selectionBox.plantSelected = None
                elif self.selectionBox.plantSelected == "sunFlower":
                    plantImage = self.plantImages[1]
                    width, height = plantImage.size
                    scale = self.cellWidth/width
                    plantImage = self.scaleImage(plantImage, scale)
                    sunImage = self.spriteImages[3]
                    width, height = sunImage.size
                    scale = self.cellWidth/width
                    sunImage = self.scaleImage(sunImage, scale)
                    newPlant = SunFlower(self, plantRow, plantCol, plantImage, sunImage)
                    self.selectionBox.plantSelected = None
                elif self.selectionBox.plantSelected == "walnut":
                    plantImage = self.plantImages[2]
                    width, height = plantImage.size
                    scale = self.cellWidth/width
                    plantImage = self.scaleImage(plantImage, scale)
                    newPlant = Walnut(self, plantRow, plantCol, plantImage)
                    self.selectionBox.plantSelected = None
                for cell in self.grid:
                    if cell.col == plantCol and cell.row == plantRow:
                        if cell.plant == None:
                            futureSunsCollected = self.sunsCollected - newPlant.value
                            if not futureSunsCollected < 0:
                                lastPlant, lastTime = None, None
                                if self.selectionHistory != []:
                                    lastPlant, lastTime = self.selectionHistory[-1]
                                if self.selectionHistory == [] or self.time - lastTime >= newPlant.delay:
                                    self.sunsCollected = futureSunsCollected
                                    cell.plant = newPlant
                                    self.selectionHistory.append((newPlant.name, self.time))
        for cell in self.grid:
            cell.brighten = False

    def shovel(self):
        self.shovelActive = not self.shovelActive

    def helpScreen(self):
        self.setActiveMode("help")

    def startToggle(self):
        self.setActiveMode("start")
        start = self.getMode("start")
        start.appStarted()
        self.appStarted()

    def redrawAll(self,canvas):
        canvas.create_image(self.width//2,self.height//2,   #background
                            image=ImageTk.PhotoImage(self.background))
        for cell in self.grid:  #Grid
            cell.renderCell(canvas)
            cell.renderSpawnedSun(canvas)
        self.selectionBox.render(canvas)    #selectionBox
        x0 = 30
        x1 = 180
        y0 = self.height-150
        y1 = self.height-85
        canvas.create_rectangle(30, self.height-150, 180, self.height-85, fill="Gray50", width=2)   #suns
        canvas.create_image((x0+x1)//2-30, (y0+y1)//2, image=ImageTk.PhotoImage(self.spriteImages[3]))  
        canvas.create_text((x0+x1)//2+30, (y0+y1)//2, text= str(self.sunsCollected), font= "Arial 30 bold")
        y0 = self.height-85
        y1 = self.height-10
        canvas.create_rectangle(30, self.height-85, 180, self.height-10, fill="Orange", width=2)    #Time until next plant
        canvas.create_text((x0+x1)//2, (y0+y1)//2, text= f"Time Until Next Plant:\n\t{str(self.timerToNext//10)}" , font= "Arial 10")
        drawButton(canvas, self.width//15, self.height*2//3, 80, 80, self.shovel, "hi", "black") #Shovel
        if self.shovelActive:  
            canvas.create_rectangle(self.width//15 - 40, self.height*2//3 - 40,
                                 self.width//15 + 40, self.height*2//3 + 40, fill="white")
        canvas.create_image(self.width//15, self.height*2//3, image=ImageTk.PhotoImage(self.spriteImages[5]))
        canvas.create_rectangle(self.width - 400, 0, self.width, 60, fill="lightblue",width=2)
        canvas.create_text(self.width-200, 30, text=f"Difficulty: {self.currentRound} | Score: {str(self.score)}", font= "Arial 30")

        for sun in self.fallingSuns:
            sun.renderSun(canvas)
        for cell in self.grid:
            if isinstance(cell.plant, PeaShooter):
                cell.plant.renderPea(canvas)
        for zombie in self.zombies:
            zombie.renderZombie(canvas)
        for mower in self.mowers:
            mower.renderMower(canvas)
        drawButton(canvas, self.width - 250, self.height - 50, 100, 100, self.helpScreen, "Help", "sienna3")
        drawButton(canvas, self.width - 150, self.height - 50, 100, 100, self.startToggle, "Exit", "sienna3")
        drawButton(canvas, self.width - 50, self.height - 50, 100, 100, self.saveGame, "SAVE", "sienna3")




