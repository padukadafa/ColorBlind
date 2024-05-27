import sys
import random

import pygame

from core.app_constant import AppConstant
from core.widget import Widget
from service.save_load_manager import SaveLoadManager
from widgets.button import Button
from widgets.circle import Circle
from widgets.page import Page

class SettingsPage(Page):
    def __init__(self,screen,on_back=None):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.on_back = on_back
        self.screen = screen
        self.window_status = pygame.display.is_fullscreen()
        self.is_mouse_pressed = False
        self.save_load_manager = SaveLoadManager(".save","save_data")
        self.circles = []
    def render(self):
        self.event_handler()
        self.screen.fill((0, 0, 0))
        self.draw_bg()
        self.draw_settings()
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
    def draw_settings(self):
        sound_status = self.get_sound_status()
        toggle_volume_text ="Disable Music"
        toggle_window_text = "Full Screen"
        if not sound_status:
            toggle_volume_text="Enable Music"
        if self.window_status:
            toggle_window_text="Windowed"
        toggle_volume = Button(self.screen,toggle_volume_text,AppConstant.screen_width/2,100,250,100,is_mouse_pressed=self.is_mouse_pressed,font_size=32,onClick=self.toggle_sound)
        toggle_window = Button(self.screen,toggle_window_text,AppConstant.screen_width/2,220,250,100,is_mouse_pressed=self.is_mouse_pressed,font_size=32,onClick=self.toggle_window)
        back_button = Button(self.screen, "Back", 70, 70, 100, 40, font_size=16, onClick=self.on_back,
                             is_mouse_pressed=self.is_mouse_pressed)
        exit_button = Button(self.screen, "Exit Game", AppConstant.screen_width/2, 340, 250, 100, font_size=32, onClick=self.exit,
                             is_mouse_pressed=self.is_mouse_pressed)
        toggle_window.render()
        back_button.render()
        toggle_volume.render()
        exit_button.render()
    def exit(self):
        self.is_mouse_pressed = False
        pygame.quit()
        sys.exit()
    def toggle_window(self):
        self.is_mouse_pressed = False
        self.window_status = not self.window_status
        pygame.display.toggle_fullscreen()


    def get_sound_status(self):
        sound_status = self.save_load_manager.load_data(AppConstant.VOLUME_STATUS)
        if sound_status == True:
            return True
        return False
    def toggle_sound(self):
        self.is_mouse_pressed = False
        sound_status = self.save_load_manager.load_data(AppConstant.VOLUME_STATUS)
        self.save_load_manager.save_data(not sound_status,AppConstant.VOLUME_STATUS)

        if not sound_status:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()
    def draw_bg(self):
        self.circles = self.generate_circle()
        for circle in self.circles:
            circle.render()
    def generate_circle(self):
        circles = []
        for i in range(random.randint(15, 25)):
            random_pos = (random.randint(0, int(AppConstant.screen_width-AppConstant.screen_width/4)), random.randint(0, int(AppConstant.screen_height-AppConstant.screen_height/2)))
            random_radius = random.randint(8, 10) * 15
            circle = Circle(self.screen, random_pos[0], random_pos[1], random_radius)
            circles.append(circle)
        return circles
