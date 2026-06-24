from ui.button import Button
from ui.area import SquaredArea
from ui.graphical_graph import GraphicalGraph

from controllers.interactions import *
from controllers.dag_algorithms import *
from controllers.ui_controllers import *

from core.loader import load_graphs_from_file

from core.constants import *

def DAG_page () -> None:
    graphs_list = load_graphs_from_file("Directed_Acyclic_Graph_examples.txt")
    graph_area = SquaredArea (*GRAPH_AREA)
    graph_area.show_area()
    lt_x, rt_x, lw_y, up_y = graph_area.get_corners_coordinates()
    point = Vec2D(150, 187)
    graph_buttons = {}
    for graph in graphs_list:
        graph_buttons[graph] = GraphicalGraph (graph = graphs_list[graph], area = graph_area, label = graph)
        graph_buttons[graph].set_label (size = 20, style = "bold")
        graph_buttons[graph].move_to (point)
        graph_buttons[graph].set_action(graph_buttons[graph].new_draw)
        graph_buttons[graph].show_button()
        y = point[1] - (graph_buttons[graph].get_height()*SIZE + 5)
        if y < lw_y:
            x = point[0] + (graph_buttons[graph].get_width()*SIZE + 20)
            point = Vec2D (x, 187)
        else:
            point = Vec2D(point[0], y)
    #edit_button
    edit = Button (label = "Edit Graph", pos = (-30, -130))
    edit.set_label (size = 20, style = "bold")
    edit.set_action(make_graph_editable)
    edit.show_button()
    #start_simulation_button
    start = Button (label = "Start simulation", pos = (-220, -130))
    start.set_label (size = 20, style = "bold")
    start.set_action(go_to_DAG_simulation)
    start.show_button()
    #exit_button
    exit = Button (label = 'exit'.upper(), pos = (296, -196))
    exit.set_label (size = 20, style = "bold")
    exit.set_action(close_program)
    exit.show_button()

def DAG_simulation() -> None:
    for button in BUTTONS_LIST:
        if isinstance (button, GraphicalGraph) and button.is_selected():
            button.move_to((-220, -130))
            button.show_button()
            button.set_action(do_nothing)
            g = button
        elif str(button) == "Come Back":
            back = button
    graphical_topological_sort(g)
    #print (topological_sort(g.get_rawgraph())) # for debug checking
    back.show_button()

def go_to_DAG_simulation(*args) -> None:
    #stop_edit_mode()
    selected = False
    for button in BUTTONS_LIST:
        check_1 = str(button) == "Edit Graph"
        check_2 = str(button) == "Start simulation"
        check_3 = isinstance (button, GraphicalGraph)
        if check_1 or check_2 or check_3:
            button.hide_button()
            if check_2:
                button.set_label(text = "Come Back")
                button.set_action(go_to_DAG_page)
                button.move_to((-30, -130))
            if check_3:
                selected = selected or button.is_selected()
                if button.is_selected():
                    g = button
    if not selected:
        go_to_DAG_page (0,0)
    else:
        if verify_DAG (g.get_rawgraph()):
            DAG_simulation()
        else:
            g.goto(-331, -184)
            text = "this is not a directed acyclic graph"
            g.write(text.upper(), font = ('Arial', 20, 'bold'))
            time.sleep (MESSAGE_TIME)
            g.undo()
            go_to_DAG_page (0,0)

def go_to_DAG_page (*args) -> None:
    clear_all()
    DAG_page ()

def clear_all() -> None:
    for button in BUTTONS_LIST:
        if isinstance (button, GraphicalGraph):
            button.hide_graph()
        button.hide_button()
    BUTTONS_LIST.clear()
