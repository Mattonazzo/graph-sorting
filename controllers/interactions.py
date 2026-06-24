import turtle

from turtle import Vec2D

from ui.button import Button
from ui.area import SquaredArea

from geometry.transforms import *
from core.constants import *

def check_new_position (squaredarea, button, position) -> Vec2D:
    x_c, y_c = position
    if button.get_shape() == "circle" and button.is_regular():
        half_width = button.get_width()*SIZE/2
        lt_x = x_c - half_width
        rt_x = x_c + half_width
        lw_y = y_c - half_width
        up_y = y_c + half_width
    else:
        center = button.get_center()
        edges = button.get_edges()
        to = Vec2D (position[0], position[1])
        dir_vect = to - center
        translate_list (edges, dir_vect)
        lt_x, lw_y = to
        rt_x, up_y = to
        for p in edges:
            lt_x = min(lt_x, p[0])
            rt_x = max(rt_x, p[0])
            lw_y = min(lw_y, p[1])
            up_y = max(up_y, p[1])
    left_x, right_x, lower_y, upper_y = squaredarea.get_corners_coordinates()
    if lt_x < left_x + GAP:
        x_c += (left_x + GAP - truncate(lt_x))
    if rt_x > right_x - GAP:
        x_c += (right_x - GAP - truncate(rt_x))
    if lw_y < lower_y + GAP:
        y_c += (lower_y + GAP - truncate(lw_y))
    if up_y > upper_y - GAP:
        y_c += (upper_y - GAP - truncate(up_y))
    return Vec2D(x_c, y_c)

