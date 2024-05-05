import random
import sys

import pygame.display

from core.app_constant import AppConstant
from service.save_load_manager import SaveLoadManager
from widgets.button import Button
from core.widget import Widget
from widgets.circle import Circle
from widgets.game_light import Light


class StartMenu(Widget):
    def __init__(self,onStart=None):
        super().__init__()
        self.onStart = onStart
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((AppConstant.screen_width, AppConstant.screen_height))
        self.is_mouse_pressed = False
        self.circles = self.generate_circle()
    def render(self):
        self.event_handler()
        self.screen.fill((0,0,0))
        self.draw_bg()
        self.draw_menu()
        pygame.display.update()

        self.clock.tick(AppConstant.fps)
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.is_mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_mouse_pressed = False
    def draw_menu(self):
        start_button = Button(self.screen,"Start",self.screen.get_width()/2,250,200,80,font_size=32,onClick=self.onStart,is_mouse_pressed=self.is_mouse_pressed)
        start_button.render()
        self.draw_score(self.screen.get_width()/2)
    def draw_score(self,x):
        save_load_manager = SaveLoadManager(".save","save_data")
        score = "No score"
        if save_load_manager.check_for_file("score_time"):

            score = save_load_manager.load_data("score_time")

        score_font= pygame.font.SysFont('Arial',100)
        score_dec_font = pygame.font.SysFont('Arial',30)
        score_text = score_font.render(f"{score}",True,(255,255,255))
        score_dec_text = score_dec_font.render("Best Time", True, (255, 255, 255))

        self.screen.blit(score_text,(x-score_text.get_rect().width/2,130))
        self.screen.blit(score_dec_text, (x - score_dec_text.get_rect().width / 2, 90))
    def draw_bg(self):
        self.circles = self.generate_circle()
        for circle in self.circles:
            circle.render()
    def generate_circle(self):
        circles = []
        for i in range(random.randint(15, 25)):
            random_pos = (random.randint(0, AppConstant.screen_width-AppConstant.screen_width/4), random.randint(0, AppConstant.screen_height-AppConstant.screen_height/2))
            random_radius = random.randint(8, 10) * 15
            circle = Circle(self.screen, random_pos[0], random_pos[1], random_radius)
            circles.append(circle)
        return circles