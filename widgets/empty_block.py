import math

from widgets.block import Block
import pygame

class EmptyBlock(Block):
    def __init__(self,screen,x,y,w,h):
        super().__init__()
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._screen = screen
        self._rect = pygame.Rect(self._x, self._y, self._w, self._h)
    @property
    def draggable(self):
        return False
    def render(self):
        pygame.draw.rect(self._screen,(255,255,255),self._rect,2)
    def distance_from(self,x,y):
        return math.sqrt((x-self._rect.centerx)**2+(y-self._rect.centery)**2)
    def move(self,x,y):
        self._x = x
        self._y = y
        self._rect = pygame.Rect(self._x, self._y, self._w, self._h)
