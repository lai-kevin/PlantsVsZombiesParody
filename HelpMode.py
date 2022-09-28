from Cited.cmu_112_graphics import *
#This file contains the Help mode. The help mode contains the
#instructions
class Help(Mode):
    def appStarted(self):
        self.instructions ="""\
Select a plant from the menu on the left to choose a plant.
A plant can only be spawned once every 3 seconds. Use plants
to fight against the zombies. The amount of zombies increase 
every round. In the first round, zombies are randomly spawned.
After the first round, the zombies will target weak lanes
and will attack strong lanes in groups. Beware of the pathfinding
minions that will attempt to find a path to the home. Conehead
zombies have more health than regular zombies. To save your
progress press the save button or s.

Press Space to return to Game"""

    def keyPressed(self,event):
        if event.key == "Space":
            self.setActiveMode("play")

    def redrawAll(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height,fill="green")
        canvas.create_text(self.width//2,self.height//8, text="Instructions", font="Arial 20 bold")
        canvas.create_text(self.width//2,self.height//2, text=self.instructions, font="Arial 20")