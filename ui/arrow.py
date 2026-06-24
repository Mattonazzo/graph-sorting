from turtle import Turtle, Vec2D

from geometry.analytic import *
from geometry.numeric import *
from ui.button import Button

from core.constants import *
from typing import Union

class Arrow(Turtle):
    """A graphical Class only made for mutual supporting to Link Class."""
    _alias_axis = {"y" : "y", "up" : "y", "down" : "y", "x" : "x", "left" : "x", "right" : "x"}

    def __init__ (self, link, corner = 0, color = "black", axis = "y"):
        super().__init__(visible=False)
        self.pencolor(color)
        self.penup()
        if corner > 2:
            raise ValueError ("An Arrow can have 0, 1, or 2 corner \nMaybe one day there will be more, but for now this is what the house can serve")
        self._link = link
        self._corner = corner
        self._axis = self._set_axis (axis)
        self._point_list = self._make_point_list ()
        self._visible = False

    def _set_axis (self, axis) -> Union[str,None]:
        if self._corner == 0:
            return "y"
        elif axis in self._alias_axis:
            return self._alias_axis [axis]
        else:
            raise ValueError ("axis can only be 'x' or 'y' ")

    def _draw_line (self) -> None:
        if self.is_visible () and self._link._weight > EPSILON:
            lst = self.get_points ()
            self.goto (lst[0])
            start, end = self._link.get_extremes ()
            if start != end:
                self.pendown ()
                for p in lst[1:]:
                    self.goto (p)
            else:
                radius = abs(lst[0][0] - lst[1][0])
                self.setheading(90)
                self.forward(start.get_height()*SIZE)
                self.pendown ()
                self.circle(radius, 270)
                self.setheading(0)
            self.penup()

    def _draw_arrowhead (self) -> None:
        heads = self._link.get_orientation ()
        if self.is_visible () and heads !=0 and self._link._weight > EPSILON:
            start_button, end_button = self._link.get_extremes()
            lst = self.get_points ()
            if start_button != end_button:
                start, end = lst[-2],lst[-1]
                m,q = line_slope_intercept (start, end)
                if m is None:
                    if start [1] < end [1]:
                        ang = 90
                    else:
                        ang = -90
                else:
                    ang = math.atan (m) * 180/math.pi
                    if m > 0 and start [1] > end [1]:
                        ang = (-1 * get_sign(ang)) * 180 + ang
                    elif m < 0 and start [1] < end [1]:
                        ang = (-1 * get_sign(ang)) * 180 + ang
                    elif m == 0 and start [0] > end [0]:
                        ang = 180
            else:
                end = lst[-1]
                ang = -30
            self.goto (end)
            self.pendown ()
            self.left (ang + 30)
            self.fillcolor (self.pencolor())
            self.begin_fill ()
            self.backward (ARROWHEAD)
            self.left (60)
            self.forward (ARROWHEAD)
            self.left (60)
            self.backward (ARROWHEAD)
            self.end_fill ()
            self.penup ()
            self.setheading (0)

    def _anchor_point (self, button: Button, ref_point: Vec2D) -> Vec2D:
        line_1 = line_slope_intercept (button.get_center (), ref_point)
        if button.get_shape () == "circle":
            button_ellipse = ellipse_focals_axes ( button.get_center (), button.get_width (), button.get_height (), button.get_angle () )
            anchor_1, anchor_2 = line_ellipse_interception (line_1, button_ellipse)
            if is_on_segment (anchor_1, button.get_center (), ref_point):
                anchor_point = anchor_1
            else:
                anchor_point = anchor_2
        else:
            vertices = button.get_edges ()
            found = False
            line_2 = line_slope_intercept (vertices [-1], vertices [0])
            interception = two_lines_interception (line_1, line_2)
            check_1 = is_on_segment (interception, vertices [-1], vertices [0])
            check_2 = is_on_segment (interception, button.get_center (), ref_point)
            found = check_1 and check_2
            i = 0
            while i < (len (vertices) - 1) and not found:
                line_2 = line_slope_intercept (vertices [i], vertices [i + 1])
                interception = two_lines_interception (line_1, line_2)
                check_1 = is_on_segment (interception, vertices [i], vertices [i + 1])
                check_2 = is_on_segment (interception, button.get_center (), ref_point)
                found = check_1 and check_2
                i += 1
            anchor_point = interception
        return anchor_point

    def _make_point_list (self, corner = None, axis = None) -> list[Vec2D]:
        if self._link._weight > EPSILON:
            start_button, end_button = self._link.get_extremes ()
            start_center = start_button.get_center()
            if start_button != end_button:
                if corner == None:
                    corner = self._corner
                end_center = end_button.get_center ()
                if corner == 0:
                    start_point = self._anchor_point (start_button, end_center)
                    end_point = self._anchor_point (end_button, start_center)
                    return [start_point, end_point]
                else:
                    if axis == None:
                        axis = self._axis
                    if corner == 1:
                        if axis == "y":
                            mid = Vec2D (start_center[0], end_center[1])
                            if mid in start_button: # switch exit axis
                                lst = self._make_point_list (corner = 1, axis = "x")
                            else:
                                if mid in end_button:
                                    lst = self._make_point_list (corner = 2, axis = "y")
                                else:
                                    start_point = self._anchor_point (start_button, mid)
                                    end_point = self._anchor_point (end_button, mid)
                                    return [start_point, mid, end_point]
                        else: # axis == "x"
                            mid = Vec2D (end_center[0], start_center[1])
                            if mid in start_button: # switch exit axis
                                lst = self._make_point_list (corner = 1, axis = "y")
                            else:
                                if mid in end_button:
                                    lst = self._make_point_list (corner = 2, axis = "x")
                                else:
                                    start_point = self._anchor_point (start_button, mid)
                                    end_point = self._anchor_point (end_button, mid)
                                    return [start_point, mid, end_point]
                    else: # corner == 2
                        mid = (start_center + end_center) * (1/2)
                        if axis == "y":
                            if Vec2D (start_center[0], end_center[1]) in start_button: # switch exit axis
                                lst = self._make_point_list (corner = 2, axis = "x")
                            else:
                                mid_1 = Vec2D (start_center [0], mid [1])
                                mid_2 = Vec2D (end_center [0], mid [1])
                                start_point = self._anchor_point (start_button, mid_1)
                                end_point = self._anchor_point (end_button, mid_2)
                                return [start_point, mid_1, mid_2, end_point]
                        else:
                            if Vec2D (end_center[0], start_center[1]) in start_button: # switch exit axis
                                lst = self._make_point_list (corner = 2, axis = "y")
                            else:
                                mid_1 = Vec2D (mid [0], start_center[1])
                                mid_2 = Vec2D (mid [0], end_center [1])
                                start_point = self._anchor_point (start_button, mid_1)
                                end_point = self._anchor_point (end_button, mid_2)
                                return [start_point, mid_1, mid_2, end_point]
            else:
                mid_1 = Vec2D(start_center[0],start_center[1]+start_button.get_height()) # upper
                mid_2 = Vec2D(start_center[0]+start_button.get_width(),start_center[1]) # righter
                start_point = self._anchor_point(start_button, mid_1)
                end_point = self._anchor_point(start_button, mid_2)
                lst = [start_point, end_point]
            return lst
        else:
            return None

    def get_points (self) -> tuple[Vec2D]:
        points = tuple(self._point_list)
        return points

    def is_visible (self) -> None:
        return self._visible

    def show_arrow (self) -> bool:
        self._visible = True
        self._draw_line ()
        self._draw_arrowhead ()

    def hide_arrow (self) -> None:
        self.clear ()
        self._visible = False

    def refresh (self) -> None:
        self.clear ()
        self._point_list = self._make_point_list ()
        self._draw_line ()
        self._draw_arrowhead ()

    def change_form (self, corner = None, axis = None) -> None:
        if corner is not None:
            self._corner = corner
        self._axis = self._set_axis (axis)
        self.refresh ()

    def change_color (self, color) -> None:
        self.hide_arrow ()
        self.pencolor (color)
        self.show_arrow ()
