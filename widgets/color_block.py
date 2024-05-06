import pygame
import math

from core.app_colors import AppColors
from widgets.block import Block
from pygame.locals import *


class ColorBlock(Block):
    def __init__(self,screen, x, y, width, height, color,draggable = False):
        super().__init__()
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.image = pygame.image.load("assets/images/box.png")
        self.image = pygame.transform.scale(self.image, (self._width,self._height))
        self._screen = screen
        self._draggable = draggable
        self._dx = 0
        self._dy = 0
        self._selected = False
    @property
    def rect(self):
        return self._rect
    @property
    def draggable(self):
        return self._draggable
    def mouse_event(self):
        x, y = pygame.mouse.get_pos()
        # if self.distance_from(x,y) > math.sqrt(self._width**2+self._height**2)/2:
        #     self.disable_drag()
        if pygame.mouse.get_pressed()[0] and not self._selected and self._rect.collidepoint(x, y):
            self._dx = self._x - x
            self._dy = self._y - y
            self._selected = True


        if pygame.mouse.get_pressed()[0] and self._draggable  :
            self._x = x - self._width/2
            self._y = y - self._height/2
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)


    def render(self):
        self.mouse_event()
        if self._selected and self._draggable:
            pygame.draw.rect(self._screen,AppColors.white,self._rect.scale_by(1.1,1.1),4)
        pygame.draw.rect(self._screen, self._color,self._rect)
        self._screen.blit(self.image,self._rect,special_flags=BLEND_RGB_MULT)
    def move(self,x,y):
        self._x = x
        self._y = y
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
    def enable_drag(self):
        self._draggable = True
    def disable_drag(self):
        self._draggable = False
    def distance_from(self,x,y):
        return math.sqrt((x-self._rect.centerx)**2+(y-self._rect.centery)**2)