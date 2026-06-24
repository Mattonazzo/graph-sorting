import turtle
from turtle import Vec2D
from typing import Union
from core.constants import *
from ui.button import Button
from ui.area import SquaredArea
from ui.graphical_graph import GraphicalGraph
from controllers.interactions import check_new_position
from controllers.do_nothing import do_nothing

def select_button (x, y) -> Union[Button,Vec2D]:
    point = Vec2D(x,y)
    for button in BUTTONS_LIST:
        #print (f"{point = }, {button.get_center() = }, ", button)
        if point in button and not isinstance(button,SquaredArea):
            return button
    return point

def make_graph_editable (*args) -> None:
    edit_mode()
    for button in BUTTONS_LIST:
        if str(button) == "Edit Graph":
            button.set_label (text = "Stop Edit")
            button.set_action(stop_edit_graph)
            break

def stop_edit_graph (*args) -> None:
    stop_edit_mode()
    for button in BUTTONS_LIST:
        if str(button) == "Stop Edit":
            button.set_label (text = "Edit Graph")
            button.set_action(make_graph_editable)
            break

def _move_node (node, pos) -> bool:
    for button in BUTTONS_LIST:
        if isinstance(button, GraphicalGraph) and button.is_selected():
            vertex = button._graph_vertices
            new_center = check_new_position (button.get_graph_area(), node, pos)
            center = node.get_center()
            node.move_to(new_center)
            wrong_pos = False
            for m in vertex:
                if vertex[m] is not node:
                    wrong_pos = wrong_pos or node.touch(vertex[m])
            if not wrong_pos:
                for link in button._links:
                    if node in link:
                        button._links[link].refresh()
                        button._links[link].show_arrow()
                return True
            else:
                node.move_to(center)
                return False

def move_node (x,y) -> None:
    for button in BUTTONS_LIST:
        if isinstance(button, GraphicalGraph) and button.is_selected():
            s = turtle.Screen()
            vertex = button._graph_vertices
            selected = False
            for v in vertex:
                if vertex[v].is_selected():
                    selected = True
                    node = vertex[v]
                    break
            if not selected:
                node = select_button (x,y)
                if str(node) in vertex: #probably it is meaningless using it
                    node.set_selected(True)
                s.onclick(move_node)
            else:
                pos = select_button (x,y)
                if isinstance (pos, Vec2D):
                    right_point = _move_node(node, pos)
                    if not right_point:
                        s.onclick(move_node)
                    else:
                        vertex[v].set_selected(False)
                        s.onclick(check_action)
                else:
                    s.onclick(move_node)
            break

def edit_mode () -> None:
    for button in BUTTONS_LIST:
        if isinstance(button, GraphicalGraph):
            if not button.is_selected():
                button.hide_button()
            else:
                button.set_action(do_nothing)
                for v in button._graph_vertices:
                    button._graph_vertices[v].set_action(move_node)
        elif str(button) == "Start simulation":
            button.hide_button()

def stop_edit_mode () -> None:
    for button in BUTTONS_LIST:
        if isinstance(button, GraphicalGraph):
            button.show_button()
            if button.is_selected():
                button.set_action(button.new_draw)
                for v in button._graph_vertices:
                    button._graph_vertices[v].set_action(do_nothing)
        elif str(button) == "Start simulation":
            button.show_button()

def check_action (x,y) -> None:
    button = select_button(x,y)
    #print (button)
    #print(x,y)
    if isinstance(button, Button):
        button.do(x,y)

def close_program (x,y) -> None:
    turtle._Screen._destroy(myWin)
