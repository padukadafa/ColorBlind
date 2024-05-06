from core.app_constant import AppConstant
from core.widget import Widget
import pygame
import sys

from helper import Helper
from pages.game.game_page import GamePage
from pages.settings.settings_page import SettingsPage
from pages.start_menu.start_menu import StartMenu




class App(Widget):

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((AppConstant.screen_width, AppConstant.screen_height))
        self.curent_page = StartMenu(self.screen,onStart=self.on_start_game,onSetting=self.on_open_settings)
    def render(self):
        self.curent_page.render()
    def loop(self):
        while True:
            self.render()
    def on_start_game(self):
        self.change_page(GamePage(self.screen,on_open_start_menu=self.on_open_start_menu,on_restart=self.on_start_game))
    def on_open_start_menu(self):
        self.change_page(StartMenu(self.screen,onStart=self.on_start_game,onSetting=self.on_open_settings))
    def on_open_settings(self):
        self.change_page(SettingsPage(self.screen,on_back=self.on_open_start_menu))
    def change_page(self,page):
        self.curent_page = page
