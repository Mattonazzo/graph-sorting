import math
from typing import Union
from core.constants import *

def distance_squared (from_point: tuple [float, float], to_point: tuple [float, float]) -> float:
    p_x, p_y = from_point
    q_x, q_y = to_point
    dist_sqr = math.pow((q_x - p_x), 2) + math.pow((q_y - p_y), 2)
    round_dist_sqr = truncate(dist_sqr)
    return round_dist_sqr

def distance (from_point: tuple [float, float], to_point: tuple [float, float]) -> float:
    dist = math.sqrt(distance_squared (from_point, to_point))
    round_dist = truncate (dist)
    return round_dist

def get_sign (n) -> int:
    if n != 0:
        return n/abs(n)
    return n

def truncate (n, decimals=TRUNC) -> float:
    multiplier = 10**decimals
    sign = get_sign (n)
    tr = int(abs(n) * multiplier + 0.05) / multiplier
    if tr <= EPSILON:
        tr = 0
    return sign * tr

def percent_change (init_val: float, fin_val: float) -> float:
    d_p = (fin_val/init_val -1)
    d_p = truncate (d_p)
    return d_p
