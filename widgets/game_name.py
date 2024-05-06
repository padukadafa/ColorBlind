import pygame.font

from core.widget import Widget


class GameName(Widget):
    def __init__(self, screen,x,y):
        self.screen = screen
        self.font = pygame.font.Font("assets/font/valorax.otf",52)
        self.x = x
        self.y = y
        super().__init__()
    def render(self):
        self.text_top  = self.font.render("Color", True, (255,255,255))
        self.text_bottom = self.font.render("Blind", True, (255, 255, 255))
        self.screen.blit(self.text_top, (self.x,self.y))
        self.screen.blit(self.text_bottom, (self.x,self.y+40))
