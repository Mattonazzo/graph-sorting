import math
from turtle import Vec2D
from core.constants import *
from geometry.numeric import *
from typing import Union

def is_on_segment (point: tuple [float, float], end_point_1: tuple [float,float], end_point_2: tuple[float, float]) -> bool:
    if point != (None,None):
        m, q = line_slope_intercept (end_point_1, end_point_2)
        x, y = point
        a_x, a_y = end_point_1
        b_x, b_y = end_point_2
        check_1 = (m is not None and abs (y - a_y) <= EPSILON)
        if check_1:
            lower_x, upper_x = min (a_x, b_x), max (a_x, b_x)
            return lower_x <= x <= upper_x
        check_2 = (m is None     and abs (x - a_x) <= EPSILON)
        check_3 = (m is not None and abs (m*x + q - y) <= EPSILON)
        if check_2 or check_3:
            lower_y, upper_y = min (a_y, b_y), max (a_y, b_y)
            return lower_y <= y <= upper_y
        else:
            return False
    else:
        return False

def line_ellipse_interception (line: tuple[float, float], ellipse: tuple[Vec2D,Vec2D,float,float]) -> Union [tuple [Vec2D, Vec2D], tuple [None, None]]:
    """I am sure that this function could have been better coded, but I have to move over for now.
        At least it works, I belive..."""
    m_line, q_line = line
    f_1, f_2, double_a, double_b = ellipse
    if f_1 == f_2:
        c_x, c_y = f_1
        radius = double_a / 2
        if m_line is None:
            if abs(q_line - c_x) > radius:
                return None, None
            else:
                radicand = math.pow(radius,2) - math.pow(q_line - c_x, 2)
                var_y = math.sqrt (radicand)
                y_1 = c_y + var_y
                y_2 = c_y - var_y
                x_1 = x_2 = q_line
        else:
            h_1 = 1 + math.pow (m_line, 2)
            h_2 = 2 * (m_line*(q_line - c_y) - c_x)
            h_3 = math.pow(c_x,2) + math.pow(c_y,2) + math.pow(q_line,2) - math.pow(radius,2) - 2*q_line*c_y
            h_2 /= h_1
            h_3 /= h_1
            radicand = math.pow(h_2, 2) - 4 * h_3

            if radicand < 0:
                return None, None
            else:
                x_1 = ( (h_2 * (-1)) + math.sqrt(radicand) ) / 2
                y_1 = m_line * x_1 + q_line
                x_2 = ( (h_2 * (-1)) - math.sqrt(radicand) ) / 2
                y_2 = m_line * x_2 + q_line
    else:
        a = double_a / 2
        b = double_b / 2
        center = (f_1 + f_2) * (1/2)
        c_x, c_y = center
        m_axis, q_axis = line_slope_intercept (f_1, f_2)
        if m_axis is None:
            angle_axis = math.pi / 2
        else:
            angle_axis = math.atan (m_axis)   # radians
        angle = angle_axis *180/math.pi   # degree

        if m_line is None:
            angle_line = math.pi / 2
            p_l = Vec2D(q_line, 0)
        else:
            angle_line = math.atan (m_line)  #radians
            p_l = Vec2D(0, q_line)
        point_line = p_l.rotate (-angle, center)
        angle_rot_line = angle_line - angle_axis  #radians

        if abs(angle_rot_line) == math.pi / 2:  # m_rot_line is None
            if abs(point_line[0] - c_x) > a:
                return None, None
            else:
                radicand = math.pow(a,2) - math.pow(point_line[0] - c_x, 2)
                var_y = b / a * math.sqrt (radicand)
                y_1 = c_y + var_y
                y_2 = c_y - var_y
                x_1 = x_2 = point_line[0]  #q_rot_line
        else:
            m = math.tan(angle_rot_line)          # m_rot_line
            q = point_line[1] - m * point_line[0] # q_rot_line
            a_sqr = math.pow (a, 2)
            b_sqr = math.pow (b, 2)
            m_sqr = math.pow (m, 2)
            q_sqr = math.pow (q, 2)
            c_x_sqr = math.pow (c_x, 2)
            c_y_sqr = math.pow (c_y, 2)
            h_1 = b_sqr + a_sqr * m_sqr
            h_2 = 2 * (a_sqr*m*(q-c_y) - b_sqr*c_x)
            h_3 = b_sqr*c_x_sqr + a_sqr*(q_sqr + c_y_sqr - b_sqr - 2*c_y*q)
            h_2 /= h_1
            h_3 /= h_1
            radicand = math.pow(h_2, 2) - 4 * h_3

            if radicand < 0:
                return None, None
            else:
                x_1 = ( (h_2 * (-1)) + math.sqrt(radicand) ) / 2
                y_1 = m * x_1 + q
                x_2 = ( (h_2 * (-1)) - math.sqrt(radicand) ) / 2
                y_2 = m * x_2 + q
        p_1, p_2 = Vec2D(x_1, y_1), Vec2D(x_2, y_2)
        x_1, y_1 = p_1.rotate (angle, center)
        x_2, y_2 = p_2.rotate (angle, center)
    return Vec2D (truncate(x_1), truncate(y_1)), Vec2D (truncate(x_2), truncate(y_2))

def two_lines_interception (line_1: tuple [float, float], line_2: tuple [float, float]) -> Union [tuple [float, float], tuple [None, None]]:
    m_1, q_1 = line_1
    m_2, q_2 = line_2
    if m_1 == m_2:
        if q_1 == q_2:
            x, y = "All", "points"
        else:
            x, y = None, None
    elif m_1 == None:
        x = q_1
        y = truncate (m_2 * x + q_2)
    elif m_2 == None:
        x = q_2
        y = truncate (m_1 * x + q_1)
    else:
        x = truncate ((q_2 - q_1) / (m_1 - m_2))
        y = truncate (m_1 * x + q_1)
    return x, y

def ellipse_focals_axes (center: tuple [float,float], width: float, height: float, angle: float = 0) -> tuple [Vec2D, Vec2D, float]:
    #the angle is the counterclockwise rotation of axis_1
    axis_1 = width # *SIZE
    axis_2 = height # *SIZE
    if axis_1 == axis_2: # circumference
        f_1 = f_2 = Vec2D (center[0], center[1])
        double_a = double_b = axis_1
    else:
        center = Vec2D (center[0], center[1])
        if max (axis_1, axis_2) == axis_1:
            double_a, double_b = axis_1, axis_2
        else:
            double_a, double_b = axis_2, axis_1
            angle += 90
        c_squared = (math.pow(double_a/2, 2) - math.pow(double_b/2, 2))
        c = truncate(math.sqrt(c_squared)) * SIZE
        f_1 = Vec2D (c, 0)
        f_1 = f_1.rotate(angle)
        f_1 = f_1 + center
        f_1 = Vec2D (truncate(f_1[0]), truncate(f_1[1]))
        f_2 = Vec2D (-c, 0)
        f_2 = f_2.rotate(angle)
        f_2 = f_2 + center
        f_2 = Vec2D (truncate(f_2[0]), truncate(f_2[1]))
    return f_1, f_2, double_a*SIZE, double_b*SIZE

def ellipse_from_squared_label (width: float, height: float) -> tuple[float]:
    """this is based on 2 proprierties of the ellipse:
        - l = math.pow(b,2) / a
        - eccentricity = c/a = math.sqrt(1 - math.pow(b/a, 2))
        the goal is to build an ellipse centered in the origin with focals that intercept
        the label's edges. So we can say that l = height/2 and c = width/2.
        Now, starting by the first proprierty, math.pow(b,2) = l_corner * a -> c/a = math.sqrt(1 - (l/a))
        with a > l_corner and eleveting by 2 each side of the equation leads to math.pow(a,2) - l_corner*a - math.pow(c,2) = 0 ,
        with a delta = math.pow(l,2) + 4*math.pow(c,2) >= math.pow(l,2), so only one solution of the equation is positive.
        """
    width *= SIZE
    height *= SIZE
    l_corner = height/2
    c = width/2
    delta = math.pow(l_corner,2) + 4* math.pow(c,2)
    a = (l_corner + math.sqrt(delta)) /2
    b = math.sqrt(l_corner*a)
    double_a = 2*a
    double_b = 2*b
    return truncate(double_a/SIZE), truncate(double_b/SIZE)

def line_slope_intercept (from_point: tuple[float, float], to_point: tuple[float, float]) -> Union [tuple[float, float], tuple[None, float]]:
    from_x, from_y = from_point
    to_x, to_y = to_point
    if from_x == to_x:
        return None, to_x    # vertical x = q
    else:
        m = truncate ( (to_y - from_y) / (to_x - from_x) )    # slope
        q = truncate ( from_y - (from_x * m) )                # intercept
        return m, q
