#This file contains the class of zombie types.
#All zombies inherit from the basic zombie
class Zombie(object):
    def __init__(self, game, spawnRow, sprite, plantsGrid):
        self.plantsGrid = plantsGrid
        self.spawnRow = spawnRow
        self.sprite = sprite
        self.game = game
        self.x = self.game.width - 100 #USE FOR COLLISON DETECTION
        self.y = self.spawnRow * self.game.cellHeight
        self.time = 1
        self.move = True
        self.health = 5
        self.alive = True
        self.rowChanges = 0
        self.name = "basic"

    def increaseTime(self):
        self.time += 1
        self.moveZombie()
        for pea in self.game.peas:
            if pea.x >= self.x and pea.row == self.spawnRow and pea.active:
                pea.active = False
                self.takeDamage()
        for mower in self.game.mowers:
            if mower.row == self.spawnRow:
                if abs(mower.x - self.x) < 50:
                    mower.useMower()
                    self.alive = False
        
    def takeDamage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            self.game.score += 1

    def moveZombie(self):
        limit = 100//self.game.timerDelay
        if self.game.time % limit == 0:
            for cell in self.plantsGrid:
                if cell.row == self.spawnRow and cell.plant != None and cell.centerX + cell.cellWidth >= self.x >= cell.centerX:
                    cell.plant.takeDamage()
                    self.move = False
                    if cell.plant.alive == False:
                        cell.plant = None
                        self.move = True
                if cell.row == self.spawnRow and cell.plant == None and cell.centerX + cell.cellWidth >= self.x >=cell.centerX:
                    self.move = True
        if self.move:
            self.x -= 3

        if self.x <= 245:
            for mower in self.game.mowers:
                if mower.row == self.spawnRow and mower.ready:
                    mower.useMower()
                elif mower.row == self.spawnRow and mower.ready == False:
                    self.game.setActiveMode("end")

    def renderZombie(self,canvas):
        y = self.spawnRow * self.game.cellHeight + self.game.cellHeight
        canvas.create_image(self.x, y, image=self.sprite)

class ConeHead(Zombie):
    def __init__(self, game, spawnRow, sprite, plantsGrid):
        super().__init__(game,spawnRow,sprite,plantsGrid)
        self.health = 1
        self.name = "cone"

class PathFindingZombie(Zombie):
    def __init__(self, game, spawnRow, sprite, plantsGrid):
        super().__init__(game,spawnRow,sprite, plantsGrid)
        #Change spawnRow when there is a new path
        self.maxRowChanges = 30
        self.rowChanges = 0
        self.name = "path"
        self.health = 8

    def moveZombie(self):
        limit = 100//self.game.timerDelay
        if self.game.time % limit == 0:
            for cell in self.plantsGrid:
                if self.rowChanges >= self.maxRowChanges or cell.row == self.spawnRow and cell.plant != None and cell.centerX + cell.cellWidth >= self.x >= cell.centerX:
                    moveRow = self.newDirection(self.spawnRow, self.x, self.rowChanges)
                    if moveRow == None:
                        cell.plant.takeDamage()
                        self.move = False
                        if cell.plant.alive == False:
                            cell.plant = None
                            self.move = True
                    else:
                        self.spawnRow = moveRow
                        self.rowChanges += 1
                if cell.row == self.spawnRow and cell.plant == None and cell.centerX + cell.cellWidth >= self.x >=cell.centerX:
                    self.move = True
        if self.move:
            self.x -= 5
        
        if self.x <= 245:
            for mower in self.game.mowers:
                if mower.row == self.spawnRow and mower.ready:
                    mower.useMower()
                    mower.ready = False
                elif mower.row == self.spawnRow and mower.ready == False:
                    end = self.game.getMode("end")
                    end.appStarted()
                    self.game.setActiveMode("end")

    def newDirection(self, row, x, rowChanges):
        rowAbove = row - 1
        rowBelow = row + 1
        col = ((x-245)//self.game.cellWidth)
        if rowChanges > self.maxRowChanges:
            return row
        for cell in self.game.grid: #If the cell has a plant in the way
            if cell.row == row and cell.col == col and cell.plant != None:
                pass
            if cell.row == row and cell.col == col and cell.plant == None: #if the cell is empty
                x -= 50
            if x <= 245:
                return row

        if not rowBelow > 4:
            newRow = rowBelow
            result = self.newDirection(newRow, x, rowChanges + 1)
            if result != None:
                return newRow
        if not rowAbove < 0:
            newRow = rowAbove
            result = self.newDirection(newRow, x, rowChanges + 1)
            if result != None:
                return newRow 
