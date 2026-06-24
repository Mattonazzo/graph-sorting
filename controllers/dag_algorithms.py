import time

from core.graph import Graph
from core.stack import Stack
from core.constants import SORTING_TIME_SHORT, SORTING_TIME_LONG

from ui.graphical_stack import GraphicalStack, GStack
from ui.graphical_graph import GraphicalGraph
from ui.button import Button

def follow_neighborhood (v: str, g: Graph, lst: list):
    if len(g.neighbors(v)) == 0:
        end = True
    else:
        for n in g.neighbors(v):
            if n in lst:
                end = False
                break
            else:
                lst.append (n)
                end = follow_neighborhood (n, g, lst)
    lst.pop()
    return end

def verify_DAG (g: Graph) -> bool:
    lst = []
    DAG = True
    for v in g.vertices():
        lst.append(v)
        DAG = DAG and follow_neighborhood (v, g, lst)
    return DAG

def topological_sort (g: Graph) -> list:
    color = {}
    order = []
    for v in g.vertices ():
        color [v] = "white"
    for v in g.vertices ():
        if color [v] != "black":
            topological_sort_from (v, g, color, order)
    return order [::-1]

def topological_sort_from (v: str, g: Graph, color: dict, order: list) -> None:
    s = Stack ()
    s.push (v)
    while s.size () > 0:
        v = s.pop ()
        if color [v] == "white":
            s.push (v)
            color [v] = "gray"
            for n in g.neighbors (v):
                if color [n] == "white":
                    s.push (n)
        elif color [v] == "gray":
            order.append (v)
            color [v] = "black"

def graphical_topological_sort (g: GraphicalGraph) -> None:
    s = GStack ('stack'.upper(), (150, 187), direction = 'down')
    s.show_button()
    order = GStack ('list'.upper(), (250, 187), direction = 'down')
    order.show_button()
    vertex = g.get_vertices ()
    for v in vertex:
        vertex[v].set_bgcolor('white')
        vertex[v].set_label (color = 'black')
        vertex[v].refresh()
    for v in vertex:
        if vertex[v].get_bgcolor () != "black":
            graphical_topological_sort_from (vertex[v], g, s, order)
    s.set_label (text = 'order'.upper())
    while not order.isEmpty():
        time.sleep(SORTING_TIME_SHORT)
        s.push (order.pop())
    order.hide_button()

def graphical_topological_sort_from (v: Button, g: GraphicalGraph, s: GraphicalStack, order: GraphicalStack) -> None:
    vertex = g.get_vertices()
    s.push (v)
    while s.size () > 0:
        time.sleep(SORTING_TIME_LONG)
        v_s = str(s.pop ())
        if vertex[v_s].get_bgcolor() == "white":
            time.sleep(SORTING_TIME_LONG)
            s.push (vertex[v_s])
            vertex[v_s].set_bgcolor ("gray")
            vertex[v_s].refresh()
            for n in g.get_neighbors ( vertex[v_s]):
                time.sleep(SORTING_TIME_LONG)
                if n.get_bgcolor() == "white":
                    s.push (n)
        elif vertex[v_s].get_bgcolor() == "gray":
            time.sleep(SORTING_TIME_LONG)
            order.push (vertex[v_s])
            vertex[v_s].set_bgcolor ("black")
            vertex[v_s].set_label (color = "white")
            vertex[v_s].refresh()
