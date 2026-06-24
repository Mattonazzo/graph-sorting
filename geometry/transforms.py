from turtle import Vec2D

from geometry.numeric import *
from typing import Union

def rotate_list (lst: list [Vec2D], angle: float, center: tuple[float, float] = (0,0)) -> None:
    for p in range (len(lst)):
        lst[p] = lst[p].rotate (angle, center)
        lst[p] = Vec2D ( truncate(lst[p][0]) , truncate(lst[p][1]) )

def translate_list (lst: list [Vec2D], dir_vect: tuple [float, float]) -> None:
    q = Vec2D(truncate(dir_vect[0]), truncate(dir_vect[1]))
    for p in range (len(lst)):
        lst[p] = Vec2D ( truncate(lst[p][0]) , truncate(lst[p][1]) ) + q

def rototranslate_list (lst: list [Vec2D], dir_vect: tuple[float, float] = None, angle: float = None, center: tuple[float, float] = (0,0)) -> None:
    if angle is not None:
        rotate_list (lst, angle, center)
    if dir_vect is not None:
        translate_list (lst, dir_vect)

def vect_transform_list (lst: list [Vec2D], dir_vect: tuple[float, float] = (1,1), center: tuple[float, float] = (0,0), angle: float = 0) -> None:
    """Takes a relative center and a direction value that, based on each vector's component, represents:
        - the percentage of magnification if is positive
        - the percentage of reduction if is negative and higher than -1
        - the reflection on that axis if lower than -1, in particular:
            - if higher than -2 is a percentual reducted reflection
            - if lower than -2 is a percentual magnification reflection
        By default it duplicates every point of an hypothetical figure centered in the origin.
        The angle is given when the figure has been rotated"""
    d_x, d_y = dir_vect
    center = Vec2D (center[0], center[1])
    c_x, c_y = center
    for p in range (len(lst)):
        lst[p] = lst[p] - center
        lst[p] = lst[p].rotate(-angle)
        var_x = lst[p][0] * (d_x + 1)
        var_y = lst[p][1] * (d_y + 1)
        lst[p] = Vec2D (var_x, var_y)
        lst[p] = lst[p].rotate(angle)
        lst[p] = lst[p] + center
        lst[p] = Vec2D ( truncate(lst[p][0]) , truncate(lst[p][1]) )
