#This file contains classes of all plants
#All plants inherit from the basic plant
#Collision associated with plants are handled here
class Plant(object):
    def __init__(self, game, row, col, image):
        self.game = game
        self.row = row
        self.col = col
        self.health = 5
        self.image = image
        self.time = 1
        self.locationX = self.game.cellWidth * self.col + 275 + self.game.cellWidth*4//5 #USE FOR COLLISION DETECTION
        self.alive = True
        self.limit = 1000//self.game.timerDelay
        self.damage = False
        self.threat = 0
        self.defence = 5
        self.delay = 30

    def takeDamage(self):
        self.damage = True
    
    def increaseTime(self):
        self.time += 1
        if self.damage == True:
            if self.time % self.limit == 0:
                self.health -= 1
                if self.health == 0:
                    self.alive = False
        for mower in self.game.mowers:
            if mower.x - 30 < self.locationX < mower.x + 30 and mower.row == self.row:
                self.alive = False

class PeaShooter(Plant):
    def __init__(self, game, row, col, image):
        super().__init__(game, row, col, image)
        self.attack = 1
        self.peas = [] #Use for pea collison
        self.shoot = False
        self.value = 100
        self.name = "PeaShooter"
        self.threat = 10
    def increaseTime(self):
        super().increaseTime()

        for zombie in self.game.zombies:
            if zombie.spawnRow == self.row: 
                if abs(zombie.x-self.locationX) < (self.game.cellWidth*5) and zombie.x < (245 + self.game.cellWidth*10) and zombie.alive:
                    self.shoot = True
                    break
                else:
                    self.shoot = False
            else:
                self.shoot = False
        if self.shoot:
            shootLimit = 2500/self.game.timerDelay
            if self.time % shootLimit == 0:
                newPea = Pea(self.game, self.row, self.col)
                self.peas.append(newPea)
            for pea in self.peas:
                pea.x += 10
    
    def renderPea(self, canvas):
        if self.shoot:
            for pea in self.peas:
                if pea.active == True:
                    canvas.create_oval(pea.x-pea.peaRadius, pea.y-pea.peaRadius,
                                    pea.x+pea.peaRadius, pea.y+pea.peaRadius, fill="Green")
    
    def __eq__(self,other):
        if isinstance(other,PeaShooter):
            return True
        return False

class Pea(object):
    def __init__(self, game, row, col):
        self.active = True
        self.game = game
        self.row = row
        self.col = col
        self.peaRadius = 10
        self.x = self.game.cellWidth * self.col + 275 + self.game.cellWidth*4//5
        self.y = self.game.cellHeight * self.row + 75 + self.game.cellHeight*1//3
        self.name = "Pea"

class SunFlower(Plant):
    def __init__(self, game, row, col, plantImage, sunImage):
        super().__init__(game, row, col, plantImage)
        self.sunImage = sunImage
        self.sunSpawnFreq = 20000
        self.spawnSun = False
        self.value = 50
        self.name = "SunFlower"
        self.defence = 5
    def createSun(self):
        self.spawnSun = True

    def increaseTime(self):
        super().increaseTime()
        limit = self.sunSpawnFreq//self.game.timerDelay
        if self.time % limit == 0:
            if self.spawnSun == False:
                self.createSun()
    
    def takenSun(self):
        self.spawnSun = False

    def __eq__(self,other):
        if isinstance(other,SunFlower):
            return True
        return False
class Walnut(Plant):
    def __init__(self, game, row, col, plantImage):
        super().__init__(game, row, col, plantImage)
        self.health = 20
        self.value = 50
        self.name = "Walnut"
        self.defence = 20
    def __eq__(self,other):
        if isinstance(other,Walnut):
            return True
        return False
        

