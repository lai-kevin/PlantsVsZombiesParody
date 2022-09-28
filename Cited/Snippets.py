#This file contains code that is copied or adapted

#This function is adapted from: https://www.diderot.one/course/34/chapters/2846/
def drawButton(canvas, cx:int, cy:int, width:int, height:int, onClick, text:str, color:str="white") -> None: 
    """ Draws a rectangular button of the desired size and location.
    When clicked, the onClick function is called. Text can be displayed on 
    the button.""" 
    canvas.create_rectangle(cx-width/2, cy-height/2, cx+width/2, cy+height/2, fill=color,  
                        onClick=onClick)  
    canvas.create_text(cx, cy, text=text, font="Arial 15 bold")