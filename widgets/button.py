import math

import pygame

from core.widget import Widget
from widgets.game_light import Light


class Button(Widget):
    def __init__(self,screen,text,x,y,w,h,font_size=12,onClick=None,show_light=True,is_mouse_pressed = False,disabled = False):
        super().__init__()
        self.screen = screen
        self.onClick = onClick
        self.is_mouse_pressed = is_mouse_pressed
        self.font = pygame.font.SysFont('Arial',font_size)
        self.text = self.font.render(text,True,(255,255,255))
        self.rect = pygame.Rect(x-w/2,y+h/2,w, h)
        self.show_light = show_light
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.hover_sound = pygame.mixer.Sound('assets/audio/tick.mp3')
        self.hover_sound_played = False
        self.disabled = disabled


    def render(self):

        if self.is_mouse_over():
            # if not self.hover_sound_played:
            #     self.hover_sound.stop()
            #     self.hover_sound.play()
            #     # self.hover_sound_played = True
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2, 20)

            if self.is_mouse_pressed and not self.disabled:
                if self.onClick:
                    self.onClick()
            if self.show_light:
                Light(self.screen, radius=220,size=self.rect.size,center=self.rect.topleft,intensity=5).render()
        else:
            self.hover_sound_played=False
            pygame.draw.rect(self.screen, (20, 20, 20), self.rect, 3, 20)
        self.screen.blit(self.text,self.text_rect)


    def is_mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
