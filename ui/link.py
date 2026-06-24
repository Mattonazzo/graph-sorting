from ui.arrow import Arrow
from ui.button import Button

class Link(Arrow): # an edge
    def __init__ (self, start: 'Button', end: 'Button', oriented = True, weight: float = 1, corner = 0, axis = "y", color = "black"):
        self._start = start
        self._end = end
        if weight < 0:
            raise ValueError ("Weight's link can't be negative")
        self._oriented = bool(oriented)
        self._weight = weight
        Arrow.__init__(self, link = self, corner = corner, color = color, axis = axis)

    def get_extremes (self) -> tuple[Button,Button]:
        return self._start, self._end

    def get_start (self) -> Button:
        return self._start

    def get_end (self) -> Button:
        return self._end

    def get_orientation (self) -> bool:
        return self._oriented

    def get_weight (self) -> float:
        return self._weight

    def set_orientation (self, orientation) -> None:
        self._oriented = bool(orientation)

    def set_weight (self, weight) -> None:
        if weight < 0:
            raise ValueError ("Weight's link can't be negative")
        self._weight = float(weight)

    def __contains__ (self, button) -> bool:
        return button in self.get_extremes()

    def __str__ (self) -> str:
        start, end = self.get_extremes()
        string = f"{str(start)} -> {str(end)}"
        return string
