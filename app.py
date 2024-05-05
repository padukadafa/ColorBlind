from core.widget import Widget
import pygame
import sys
from pages.game.game_page import GamePage
from pages.start_menu.start_menu import StartMenu


class App(Widget):

    def __init__(self):
        super().__init__()
        self.curent_page = StartMenu(onStart=self.on_start_game)
    def render(self):
        self.curent_page.render()
    def loop(self):
        while True:
            self.render()
    def on_start_game(self):
        self.change_page(GamePage(on_open_start_menu=self.on_open_start_menu,on_restart=self.on_start_game))
    def on_open_start_menu(self):
        self.change_page(StartMenu(onStart=self.on_start_game))
    def change_page(self,page):
        print("Change page")
        self.curent_page = page