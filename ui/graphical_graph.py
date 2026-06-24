import random
from turtle import Vec2D
from ui.area import SquaredArea
from ui.button import Button
from ui.link import Link

from core.graph import Graph
from core.constants import BUTTONS_LIST, SCREEN_COLOR

from controllers.interactions import check_new_position
from controllers.do_nothing import do_nothing

class GraphicalGraph (Button):
    def __init__ (self, graph, area, label, oriented = True, corner = 0, axis = "y"):
        Button.__init__(self, label=label)
        self._rawgraph = graph
        self._graph_area = area
        self._graph_vertices = {}
        for key in self._rawgraph.vertices(): #key is a string
            self._graph_vertices[key] = Button (key, shape = 'circle', regular = True)
            self._graph_vertices[key].set_label(size = 20, style = 'bold')
            self._graph_vertices[key].set_action(do_nothing)      #(lambda x, y: None)
        self._links = self._make_links_list (oriented, corner, axis)

    def _make_links_list(self, oriented, corner, axis) -> dict:
        vertex = self._graph_vertices
        lst = {}
        for v in self._rawgraph.vertices():
            for n in self._rawgraph.neighbors(v):
                weight = self._rawgraph.weight(v,n)
                link = Link (vertex[v], vertex[n], oriented, weight, corner, axis)
                lst[link] = link
        return lst

    def get_graph_area (self) -> SquaredArea:
        return self._graph_area

    def get_vertices (self) -> dict:
        return self._graph_vertices

    def get_neighbors (self, vertex) -> list:
        lst = [link.get_end() for link in self._links if vertex is link.get_start()]
        return lst

    def get_rawgraph (self) -> Graph:
        return self._rawgraph

    def show_graph (self) -> None:
        vertex = self._graph_vertices
        for v in vertex:
            vertex[v].show_button()
        for link in self._links:
            self._links[link].show_arrow()

    def hide_graph (self) -> None:
        vertex = self._graph_vertices
        for v in vertex:
            vertex[v].hide_button()
        for link in self._links:
            self._links[link].hide_arrow()

    def new_draw (self, x, y) -> None:
        vertex = self._graph_vertices
        for button in BUTTONS_LIST:
            if isinstance (button,GraphicalGraph):
                button.hide_graph()
                if button is not self:
                    button.set_bgcolor(SCREEN_COLOR)
                    button.refresh()
                    button._selected = False
        self.set_bgcolor ('yellow')
        self.refresh()
        self._selected = True
        x_left, x_right, y_down, y_up = self._graph_area.get_corners_coordinates()
        for v in vertex:
            wrong_pos = True
            while wrong_pos:
                x = random.randrange(int(x_left), int(x_right))
                y = random.randrange(int(y_down), int(y_up))
                position = Vec2D (x,y)
                new_center = check_new_position (self._graph_area, vertex[v], position)
                vertex[v].move_to (new_center)
                wrong_pos = False
                for m in vertex:
                    if vertex[m] is not vertex[v]:
                        wrong_pos = wrong_pos or vertex[v].touch(vertex[m])
            vertex[v].show_button()
        for link in self._links:
            self._links[link].refresh()
            self._links[link].show_arrow()
