from ui.button import Button
from turtle import Vec2D

from core.constants import *

class SquaredArea (Button):
    def __init__(self, point_1, point_2):
        self._left_x, self._right_x  = min(point_1[0],point_2[0]), max(point_1[0],point_2[0])
        self._lower_y, self._upper_y = min(point_1[1],point_2[1]), max(point_1[1],point_2[1])
        pos = Vec2D ((self._left_x+self._right_x) /2, (self._lower_y+self._upper_y) /2)
        size = abs (self._right_x - self._left_x) /SIZE
        size_h = abs (self._upper_y - self._lower_y) /SIZE
        super().__init__(pos = pos, size = size, size_h = size_h)

    def get_corners_coordinates (self) ->tuple[float,float,float,float]:
        return self._left_x, self._right_x, self._lower_y, self._upper_y

SquaredArea.hide_area = Button.hide_button
SquaredArea.show_area = Button.show_button
