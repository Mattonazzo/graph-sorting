import math
from turtle import Turtle

from ui.label import Label
from geometry.polygon import Polygon

from geometry.numeric import percent_change, truncate
from geometry.analytic import ellipse_from_squared_label

from core.constants import *
from typing import Union

class Button(Turtle, Polygon): # search Multiple Inheritance and Method Resolution Order (MRO) for more info
    def __init__ (self, label = None, action = None, pos = (0, 0), shape = "squared", size = None, size_h = None, angle = 0, bgcolor = SCREEN_COLOR, pencolor = "black", regular = False):
        Turtle.__init__(self, visible=False)
        self._default_pencolor = pencolor
        self.pencolor(self._default_pencolor)
        self.penup()
        self._visible = False
        self._bgcolor = bgcolor
        self._label = Label (text=label)
        Polygon.__init__(self, shape=shape, pos=pos, angle=angle, regular=regular)
        if self._label.get_text () != "":
            self.adapt_on_label ()
        if size is not None:
            if self.is_regular() or size_h is None:
                self.change_sizes (size, size)
            else:
                self.change_sizes (size, size_h)
        self._action = action
        self._selected = False
        BUTTONS_LIST[self] = self

    def _draw_area (self) -> None:
        if self.is_visible ():
            lst = self.get_edges ()
            self.penup()
            self.fillcolor(self._bgcolor)
            self.goto (lst[0])
            self.pendown()
            self.begin_fill()
            for pnt in lst[::-1]:
                self.goto(pnt)
            self.end_fill()
            self.penup()
            self.goto (self.get_center())

    def hide_button (self) -> None:
        self.clear ()
        self.hide_label ()
        self._visible = False

    def hide_label (self) -> None:
        self._label.hide_label()

    def show_button (self) -> None:
        self._visible = True
        self._draw_area()
        self.show_label ()

    def show_label (self) -> None:
        if self.is_visible ():
            self._label.show_label ( self.get_center(), self.get_angle() )

    def refresh (self) -> None:
        self.clear()
        self.hide_label()
        self._draw_area()
        self.show_label()

    def get_label (self) -> str:
        return self._label.get_text()

    def get_label_info (self) -> tuple[str,float,str]:
        return self._label.get_font_info()

    def do (self, x, y) -> None:
        self._action (x, y)

    def is_visible (self) -> bool:
        return self._visible

    def is_selected (self) -> bool:
        return self._selected

    def set_regularity (self, flag: bool) -> None:
        self.make_it_regular (bool (flag))
        if self.is_regular ():
            self.refresh()

    def _set_sizes (self, width = None, height = None) -> tuple[float,float]:
        w, h = self._adapt_on_label()
        t = self._label.get_text()
        if  width is None or (t != "" and  width < w):
            width = self.get_width()
        if height is None or (t != "" and height < h):
            height = self.get_height()
        if width <= 0 or height <= 0:
            raise ValueError ("Dimensions can't be negative and zero neither")
        return width,height

    def change_sizes (self, width = None, height = None) -> None:
        w, h = self.get_sizes ()
        width, height = self._set_sizes (width, height)
        d_w = percent_change (w, width)
        d_h = percent_change (h, height)
        if d_w != 0 or d_h != 0:
            self.clear ()
            self.hide_label()
            self.resize_percent (d_w, d_h)
            self._draw_area ()
            self.show_label ()

    def _adapt_on_label (self) -> tuple[float,float]:
        text = self._label.get_text()
        w = self.get_width()
        h = self.get_height()
        if text != "":
            font_info = self._label.get_font_info()
            font_size = font_info[1]
            self._label.goto(0,-2000) # to keep the glitch unseen
            start = self._label.pos()
            self._label.write(text, align = "left", font = font_info, move =True)
            stop  = self._label.pos()
            self._label.undo()
            width  = truncate((5 + abs(stop[0]-start[0]))/SIZE)
            height = truncate( (5 + font_size)/SIZE )
            if self.get_shape() != "squared":
                if not self.is_regular():
                    width, height = ellipse_from_squared_label (width, height)
                else:
                    diagonal = math.sqrt(math.pow(width,2) + math.pow(height,2))
                    width = height = truncate(diagonal)
        else:
            width,height = w,h
        return float(width), float(height)

    def adapt_on_label (self) -> None:
        self.change_sizes ( *self._adapt_on_label() )

    def set_label (self, text:str = None, font:str = None, size:float = None, style:str = None, color:str = None) -> None:
        self._label.set_text (text)
        self._label.set_font_info (font, size, style)
        if color is not None:
            self._label.set_color (color)
        self.adapt_on_label ()

    def change_shape (self, shape: Union[str,int]) -> None:
        Polygon.change_shape (self, shape)
        self.refresh()

    def set_action (self, action) -> None:
        self._action = action

    def set_selected (self, flag) -> None:
        self._selected = flag

    def _change_pencolor (self, color = None) -> None:
        if color is None:
            self._t.pencolor (self._default_pencolor)
        else:
            self._t.pencolor(color)

    def set_pencolor (self, color) -> None:
        self._default_pencolor = color
        self._change_pencolor ()

    def set_bgcolor (self, color) -> None:
        self._bgcolor = color

    def get_bgcolor (self) -> str:
        return self._bgcolor

    def move_to (self, pos = None, angle = None, center = None) -> None:
        if pos is None:
            pos = self.get_center()
        if not isinstance (pos,tuple):
            raise TypeError ("Button.move_to() takes one tuple (x,y) as new position")
        self.rototranslate (pos, angle, center)
        self.refresh()

    def touch (self, other:'Button') -> bool:
        if other.is_visible():  # self.is_visible()
            if Polygon.__contains__(self, other.get_center()) or Polygon.__contains__(other, self.get_center()):
                return True
            else:
                inside = False
                i = 0
                lst = self.get_edges()
                while i < len(lst) and not inside:
                    inside = Polygon.__contains__(other, lst[i])
                    i += 1
                if inside:
                    return True
                else:
                    i = 0
                    lst = other.get_edges()
                    while i < len(lst) and not inside:
                        inside = Polygon.__contains__(self, lst[i])
                        i += 1
                    return inside
        return False

    def __str__ (self) -> str:
        return self.get_label()

    def __contains__ (self, point) -> bool:
        if self.is_visible():
            return Polygon.__contains__(self, this_point=point)
