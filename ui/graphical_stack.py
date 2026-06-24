from ui.button import Button
from core.constants import SIZE

class GraphicalStack (Button):
    def __init__ (self, label, pos, direction = 'up'):
        super().__init__(label = label, pos = pos, shape = 'squared')
        self.set_label (size = 20, style = 'bold')
        self._direction = direction
        self._items = []

    def push (self, item) -> None:
        if self.isEmpty():
            c_x, c_y = self.get_center()
            w, h = self.get_sizes()
        else:
            p_item = self.peek()
            c_x, c_y = p_item.get_center()
            w, h = self.get_sizes()
        d = self._direction
        if d == 'up':
            x = c_x
            y = c_y + (h*SIZE + 5)
        elif d == 'down':
            x = c_x
            y = c_y - (h*SIZE + 5)
        elif d == 'right':
            x = c_x + (w*SIZE + 5)
            y = c_y
        else: # d == 'left'
            x = c_x - (w*SIZE + 5)
            y = c_y
        b_item = Button (label = str(item), pos = (x, y) )
        b_item.set_label(size = 20, style = 'bold')
        b_item.show_button()
        self._items.append (b_item)

    def pop (self) -> Button:
        if self.isEmpty():
            raise ValueError ("Pop from empty stack")
        p_item = self.peek()
        p_item.hide_button()
        return self._items.pop()

    def peek (self) -> Button:
        if self.isEmpty():
            raise ValueError ("Peeking into an empty stack")
        return self._items[-1]

    def bottom (self) -> Button:
        if self.isEmpty():
            raise ValueError ("Peeking into an empty stack")
        return self._items[0]

    def isEmpty (self) -> bool:
        return len(self._items) == 0

    def size (self) -> int:
        return len (self._items)

    def __str__(self) -> str:
        lst = [str(n) for n in self._items]
        return str(lst)

GStack = GraphicalStack
