from turtle import Vec2D

from geometry.numeric import *
from geometry.analytic import *
from geometry.transforms import *
from core.constants import *
from typing import Union

class Polygon: #convex
    """every new polygon is built around a tangent circle, to be able to put a label inside"""
    def __init__ (self, shape: Union[str,int], pos: tuple[float,float]=(0,0), size: float=1, size_h: float=1, angle: float=0, regular: bool=True):
        self._regular = bool(regular)
        self._center = Vec2D (pos[0], pos[1])
        self._angle = float(angle)
        self._width = float(size)
        if not self.is_regular () and isinstance(float(size_h),float):
            self._height = float(size_h)
        else:
            self._height = float(size)
        self.change_shape (shape) # defines three variables

    def _nominate_shape (self, shape: Union[str, int]) -> tuple[str, int]:
        if isinstance (shape, str) and shape in POLY_DICT:
                return shape, POLY_DICT [shape]
        elif isinstance (int(shape), int):
            vertices = int(shape)
            found = False
            for name in POLY_DICT:
                if vertices == POLY_DICT[name]:
                    found = True
                    shape = name
            if not found:
                return "generic_poly", vertices
            return shape, vertices
        else:
            raise TypeError (f"{shape} is not a valide name\ninstert at least an integer >= 3")

    def get_shape (self) -> str:
        return self._shape

    def get_number_vertices (self) -> int:
        return self._vertices

    def get_edges (self) -> list[Vec2D]: #return a copy
        poly = self._vertices_list [:]
        return poly

    def get_center (self) -> Vec2D:
        return self._center

    def get_angle (self) -> float:
        return self._angle

    def get_sizes (self) -> tuple[float,float]:
        return self.get_width (), self.get_height ()

    def get_height (self) -> float:
        return self._height

    def get_width (self) -> float:
        return self._width

    def is_regular (self) -> bool:
        return self._regular

    def make_it_regular (self, flag: bool) -> None:
        self._regular = bool (flag)
        if self.is_regular ():
            self._make_it_regular ()

    def _make_it_regular (self) -> None:
        w, h = self.get_sizes ()
        m = max (w,h)
        d_w = (w - m) / m *100
        d_w = truncate (d_w)
        if d_w <= EPSILON:
            d_w = 0
        d_h = (h - m) / m *100
        d_h = truncate (d_h)
        if d_h <= EPSILON:
            d_y = 0
        self.resize_percent (d_w, d_h)

    def _make_vertices_list (self) -> list[Vec2D]:
        shape = self.get_shape()
        n = self.get_number_vertices ()
        angle = 0
        d_angle = 360 / n
        if shape == "circle":
            size = SIZE / 2
        else:
            """the following calculus generates an error = math.pi / n
                in the following rotation (and only for this one time) made for putting
                the figure on a base side and I don't know why.
                I only figured out the consequences by sampling the figures
                from 3 to 20 vertices to reveal the pattern (it was not immediate because
                for 1 and 2 it can't be calculated, because is based on the formula
                cathetus = hypotenuse * sin (opposite_angle) ).
                Probably is the conversion in radians, but I can't be sure
                I only know that it will not appen without this resizing, but
                the consequence is that will be the distance center-vertex to be
                equal to SIZE/2 (as in circle) and not half of a side. Choosing this way
                for the other will influence the resizing made to fit text inside
                the Button and the possibility to use the SquaredArea properly,
                because it can't be possible to put in 2 specific coordinates
                and returning a specific area fitted in that corners"""
            #angle = math.radians(d_angle/2) #for debug checking
            angle = math.pi/n  # = ( (2*math.pi) /n) /2
            sin_a = math.sin(angle) # radians
            cat = SIZE/2
            size = cat/sin_a # so now each side measures 1 SIZE unit
        P = Vec2D(size,0)
        lst = [Vec2D(0,0)] * n
        for i in range(len(lst)):
            lst[i] += P.rotate (angle)
            angle += d_angle
        if shape != "circle":
            _error_ = math.pi / n
            d_angle = d_angle / 2 + 90 + _error_ # degree
            rotate_list (lst, -d_angle)
        return lst

    def _apothem (self) -> float:
        """this function is called just before vertices' list is done, so, in theory,
            the first side is made parallel to the x axes by the contructor (except for circle),
            the apothem (for definition) is perpendicular to each side, and the figure
            is centered in the origin. So..."""
        poly = self.get_edges ()
        c_x = c_y = 0                # I am putting this line just to be better readable
        shape = self.get_shape ()
        if shape == 'circle': # is the only figure that is not rotated by the contructor
            apothem = abs (c_x - poly[0][0])
        else:
            apothem = abs (c_y - poly[0][1])
        ##=============== for debug checking =========================================
        #m_base, q_base = line_slope_intercept (poly[0], poly[1])
        #if m_base == 0:
            #m_apothem = None
            #q_apothem = c_x
        #elif  m_base is None:
            #m_apothem = 0
            #q_apothem = c_y
        #else:
            #m_apothem = -1 / m_base
            #q_apothem = c_y - m_apothem * c_x
        #intersection = two_lines_interception ((m_base,q_base), (m_apothem,q_apothem))
        #apothem = distance ((c_x, c_y), intersection)
        ##=============================================================================
        return apothem

    def _rototranslate (self, dir_vect = None, angle = None, center = (0,0)) -> None:
        rototranslate_list (self._vertices_list, dir_vect, angle, center)

    def rototranslate (self, to: tuple[float,float] = None, angle: float = None, center: tuple[float,float] = None) -> None:
        if to is not None:
            to = Vec2D (to[0], to[1])
            dir_vect = to - self.get_center ()
        else:
            dir_vect = None
        if center is None:
            center = self.get_center()
        self._rototranslate (dir_vect, angle, center)
        if angle is not None:
            self._angle += angle
        if dir_vect is not None:
            self._center = to

    def _vect_transform (self, dir_vect: tuple[float, float], center: tuple[float,float] = None, angle: float = None) -> None:
        if center is None:
            center = self.get_center ()
        if angle is None:
            angle = self.get_angle ()
        if dir_vect != (0,0):
            vect_transform_list (self._vertices_list, dir_vect, center, angle)

    def resize_percent (self, percent: float, percent_h: float = None) -> None:
        if percent < -1:
            raise ValueError ("A figure can't be reduced over 100%")
        size_w = percent
        if percent_h is not None:
            if percent_h < -1:
                raise ValueError ("A figure can't be reduced over 100%")
            size_h = percent_h
            if self.is_regular ():
                size_h = size_w = max (size_h, size_w)
        else:
            size_h = size_w
        size = Vec2D(size_w, size_h)
        self._vect_transform (size)
        self._width  = truncate(self._width  * (1 + size_w))
        self._height = truncate(self._height * (1 + size_h))

    def reflect_on_axis (self, axis: tuple[float,float]) -> None:
        axis_m, axis_q = axis
        c_x, c_y = self.get_center ()
        if axis_m is None:
            axis_angle = math.pi / 2
            perp_m = 0
            perp_q = c_y
        else:
            axis_angle = math.atan (axis_m)
            if axis_m == 0:
                perp_m = None
                perp_q = c_x
            else:
                perp_m = - 1 / axis_m
                perp_q = c_y - perp_m * c_x
        interception = two_lines_interception (axis, (perp_m, perp_q))
        interception = Vec2D (interception[0], interception[1])
        #self._vect_transform ((-2,0), interception, (axis_angle*180/math.pi)-90)     # for debug checking
        c, s = math.cos(2 * axis_angle), math.sin(2 * axis_angle)
        for p in range(len(self._vertices_list)):
            t_p = self._vertices_list[p] - interception
            x, y = t_p
            r_t_p = Vec2D (x*c + y*s, x*s - y*c)
            self._vertices_list[p] = r_t_p + interception
        self._angle = 180 - self._angle
        self._center = 2*interception - self._center

    def reflect_on_point (self, point: tuple[float,float] = None) -> None:
        if point is None:
            point = self.get_center()
        else:
            point = Vec2D (point[0], point[1])
        #self._vect_transform ((-2,-2), point)       # for debug checking
        for p in range (len(self._vertices_list)):
            self._vertices_list[p] = 2*point - self._vertices_list[p]
        self._angle += 180
        self._center = 2*point - self._center

    def change_shape (self, shape: Union[str, int]) -> None:
        self._shape, self._vertices = self._nominate_shape (str(shape))
        self._vertices_list = self._make_vertices_list () # regular polygon
        apothem = self._apothem ()
        width = height = apothem*2 /SIZE
        d_w = percent_change ( width, self._width )
        d_h = percent_change (height, self._height)
        self._vect_transform ( dir_vect=(d_w, d_h), center=(0,0) )
        self._rototranslate (dir_vect = self._center, angle = self._angle)

    def __contains__ (self, this_point: tuple [float, float]) -> bool:
        if isinstance(this_point, Vec2D):
            center = self.get_center ()
            if self.get_shape () == "circle":
                width, height = self.get_sizes ()
                if width == height:
                    d_p_pow_2 = distance_squared (center, this_point)
                    r_pow_2 = math.pow ((width / 2) * SIZE, 2)
                    return d_p_pow_2 - r_pow_2 <= EPSILON
                else:
                    f_1, f_2, double_a, double_b = ellipse_focals_axes (center, width, height, self.get_angle())
                    d_p_1 = distance (f_1, this_point)
                    d_p_2 = distance (f_2, this_point)
                    return (d_p_1 + d_p_2 - double_a) <= EPSILON
            else:
                vertices = self.get_edges()
                inside = False
                line_1 = line_slope_intercept (center, this_point)

                line_2 = line_slope_intercept (vertices [-1], vertices [0])
                interception = two_lines_interception (line_1, line_2)
                if is_on_segment (interception, vertices [-1], vertices [0]):
                    #inside = is_on_segment (this_point, interception, center) # for debug checking
                    lower_x, upper_x = min (center[0], interception[0]), max (center[0], interception[0])
                    lower_y, upper_y = min (center[1], interception[1]), max (center[1], interception[1])
                    check_1 = (lower_x <= this_point[0] <= upper_x)
                    check_2 = (lower_y <= this_point[1] <= upper_y)
                    inside =  check_1 and check_2

                i = 0
                while i < (len (vertices) - 1) and not inside:
                    line_2 = line_slope_intercept (vertices [i], vertices [i + 1])
                    interception = two_lines_interception (line_1, line_2)
                    if is_on_segment (interception, vertices [i], vertices [i + 1]):
                        #inside = is_on_segment (this_point, interception, center) # for debug checking
                        lower_x, upper_x = min (center[0], interception[0]), max (center[0], interception[0])
                        lower_y, upper_y = min (center[1], interception[1]), max (center[1], interception[1])
                        check_1 = (lower_x <= this_point[0] <= upper_x)
                        check_2 = (lower_y <= this_point[1] <= upper_y)
                        inside =  check_1 and check_2
                    i += 1

                return inside
        else:
            raise TypeError ("Only a point (x,y) is accepted")
