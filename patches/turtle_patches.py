import turtle, math
from turtle import Vec2D

#============================================================================================
"""The following patch is not mine. I found it from a certain Claudio on stackoverflow
    while I was searching for a way to rotate a text using the turtle module. Turtle is
    built on Tkinter, who can rotate text from version 8.6 (for checking run on terminal
    python -m tkinter).
    He saved me from loosing inside the Tkinter's maze because it is not between my research purpose
    using tkinter directly; my goal is to use what I have learned so far with at least a few
    little tip I saw here and there. I have understood that canvas was responsible about writing
    things in turtle, but because I don't know enough about programming I didn't want to modify
    anything on turtle.py.
    I'm leaving it here for two reasons:
    - It serves for some commands that I implemented and I don't want to spend time cleaning it
        just to erase this few line's patch;
    - This method taught me that I can modify other modules without touching them directly
    using aliasing."""
#============================================================================================
class Patch_txt_angle:
    def RawTurtleDOTwrite(self, arg, move=False, align="left", font=("Arial", 11, "normal"), txt_angle=0):
        if self.undobuffer:
            self.undobuffer.push(["seq"])
            self.undobuffer.cumulate = True
        end = self._write(str(arg), align.lower(), font, txt_angle)
        if move: x, y = self.pos() ; self.setpos(end, y)
        if self.undobuffer: self.undobuffer.cumulate = False
    def RawTurtleDOT_write(self, txt, align, font, txt_angle):
        item, end = self.screen._write(self._position, txt, align, font, self._pencolor, txt_angle)
        self.items.append(item)
        if self.undobuffer: self.undobuffer.push(("wri", item))
        return end
    def TurtleScreenBaseDOT_write(self, pos, txt, align, font, pencolor, txt_angle):
        x, y = pos ; x = x * self.xscale ; y = y * self.yscale
        anchor = {"left":"sw", "center":"s", "right":"se" }
        item = self.cv.create_text(x-1, -y, text = txt, anchor = anchor[align],
            fill = pencolor, font = font, angle = txt_angle)
        x0, y0, x1, y1 = self.cv.bbox(item)
        self.cv.update()
        return item, x1-1

turtle.RawTurtle.write         = Patch_txt_angle.RawTurtleDOTwrite
turtle.RawTurtle._write        = Patch_txt_angle.RawTurtleDOT_write
turtle.TurtleScreenBase._write = Patch_txt_angle.TurtleScreenBaseDOT_write

# example
#tt = turtle.Turtle()
#tt.write("EXAMPLE", font=("Arial", 12, "bold"), align="right", txt_angle=45)
## the prewious call doesn't affect the following calls.
## infact we can call a write without specifing an angle and it will be not rotated
#tt.forward(100)
#tt.write("EXAMPLE", font=("Arial", 12, "bold"), align="right")

#============================================================================================
#============================== END_OF_CLAUDIO'S_PATCH ======================================
#============================================================================================

class Patch_Vec2D_rotation:
    def rotate(self, angle, center = (0,0)):
        """rotate self counterclockwise by angle relative to an application point that could be
            different from the origin (0,0), because I need the possibility to have an occasional
            relative rotational center and to avoid calculus when zero angle is given.
        """
        if angle == 0:
            return self
        else:
            angle = math.radians(angle)
            c, s = math.cos(angle), math.sin(angle)
            if center == (0,0):
                return Vec2D(self[0]*c-self[1]*s,self[1]*c+self[0]*s)
            else:
                return Vec2D((self[0]-center[0])*c-(self[1]-center[1])*s+center[0],(self[1]-center[1])*c+(self[0]-center[0])*s+center[1])

turtle.Vec2D.rotate = Patch_Vec2D_rotation.rotate
