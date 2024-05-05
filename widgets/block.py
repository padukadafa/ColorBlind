from core.widget import Widget


class Block(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._x=0
        self._y=0
        self._color=(0,0,0)
        self._rect = None
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @property
    def rect(self):
        return self._rect
    def render(self):
        pass
    def distance_from(self, x,y):
        pass
    def get_color(self):
        return self._color
        pass
    @property
    def draggable(self):
        pass

    def disable_drag(self):
        pass
