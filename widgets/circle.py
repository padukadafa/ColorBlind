import pygame

from core.widget import Widget
from widgets.game_light import Light


class Circle(Widget):
    def __init__(self, screen,x,y,r):
        self.screen = screen
        self.rect = pygame.Rect(x,y,2*r,2*r)
        self.x = x
        self.y = y
        self.r = r
    def render(self):

        if not self.is_mouse_over():
            pygame.draw.circle(self.screen, (0, 0, 0), self.rect.center, self.r, 2)
        else:
            pygame.draw.circle(self.screen, (255, 255, 255), self.rect.center, self.r, 2)
            Light(self.screen, radius=200, size=self.rect.size, center=self.rect.topleft).render()
    def is_mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
