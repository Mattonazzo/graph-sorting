from turtle import Turtle, Vec2D

class Label(Turtle):
    _font_style = ("normal", "bold", "italic")
    def __init__ (self, text, color = "black", font = "Arial", size = 8, style = "normal"):
        super().__init__(visible=False)
        self.pencolor(color)
        self.penup()
        if isinstance(text,str):
            self._text = text
        else:
            self._text = ""
        if isinstance(font,str):
            self._font = font
        else:
            raise TypeError ("Font name must be a string format")
        if isinstance(size,float) or isinstance(size,int):
            self._size = size
        else:
            raise TypeError ("Font size must be a number")
        if style in self._font_style:
            self._style = style
        else:
            raise ValueError ("Font style can only be 'normal', 'bold' or 'italic'")

    def hide_label (self) -> None:
        self.clear ()

    def show_label (self, center: Vec2D = None, angle = 0) -> None:
        if center is None:
            center = self.pos()
        self._write_in (center, angle)

    def _write_in (self, center: Vec2D, angle) -> None:
        c_x, c_y = center
        y = c_y  - (self._size * 0.75)
        x = c_x + 1.33
        new_center = Vec2D (x, y)
        new_center = new_center.rotate(angle, center)
        self.goto (new_center)
        self.write (self._text, font = self.get_font_info(), align = "center", txt_angle = angle)

    def get_text (self) -> str:
        return self._text

    def get_font_info (self) -> tuple[str,float,str]:
        return self._font, self._size, self._style

    def set_text (self, text) -> None:
        if isinstance (text,str):
            self._text = text

    def set_font_info (self, font:str = None, size:float = None, style:str = None) -> None:
        if isinstance(font,str):
            self._font = font
        if (isinstance(size,float) or isinstance(size,int)):
            self._size = size
        if style in self._font_style:
            self._style = style

    def set_color (self, color) -> None:
        self.pencolor(color)
