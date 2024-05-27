import random
import sys

import pygame.display

from core.app_colors import AppColors
from core.app_constant import AppConstant
from helper import Helper
from service.save_load_manager import SaveLoadManager
from widgets.button import Button
from core.widget import Widget
from widgets.circle import Circle
from widgets.color_block import ColorBlock
from widgets.game_light import Light
from widgets.game_name import GameName
from widgets.page import Page

class StartMenu(Page):
    def __init__(self,screen,onStart=None,onSetting=None):
        super().__init__()
        self.onStart = onStart
        self.onSetting = onSetting
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.is_mouse_pressed = False
        self.is_show_about = False
        self.circles = self.generate_circle()
        self.save_load_manager = SaveLoadManager(".save", "save_data")
        self.difficulty = self.save_load_manager.load_data(AppConstant.DIFFICULTY)
        if self.difficulty is None:
            self.difficulty = "easy"

    def render(self):
        self.event_handler()
        self.screen.fill((0,0,0))
        self.draw_bg()
        self.draw_game_name()
        if self.is_show_about:
            self.show_about()
        else:
            self.draw_menu()
            self.draw_difficult()
        self.draw_score(self.screen.get_width() - 250)
        self.draw_block(600,400)
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
        start_button = Button(self.screen,"Start",150,200,200,70,font_size=32,onClick=self.onStart,is_mouse_pressed=self.is_mouse_pressed,disabled=self.is_show_about)
        shop_button = Button(self.screen, "Shop", 150, 275, 200, 70, font_size=32, onClick=self.on_show_about,
                             is_mouse_pressed=self.is_mouse_pressed)
        setting_button = Button(self.screen, "Settings", 150, 350, 200, 70, font_size=32, is_mouse_pressed=self.is_mouse_pressed,onClick=self.onSetting)
        about_button = Button(self.screen, "About", 150, 425, 200, 70, font_size=32, onClick=self.on_show_about,
                                is_mouse_pressed=self.is_mouse_pressed)


        start_button.render()
        shop_button.render()
        setting_button.render()
        about_button.render()

    def draw_difficult(self):
        if self.difficulty != "easy":
            easy_button = Button(self.screen, "Easy", 350, 230, 150, 50, font_size=24, onClick=self.set_difficulty_easy,
                                 is_mouse_pressed=self.is_mouse_pressed, disabled=self.is_show_about)
        else:
            easy_button = Button(self.screen,"Easy",350,230,150,50,font_size=24,onClick=self.set_difficulty_easy,is_mouse_pressed=self.is_mouse_pressed,disabled=self.is_show_about,background_color=(255,255,255),text_color=(20,20,20))
        if self.difficulty != "medium":
            medium_button = Button(self.screen,"Medium",350,290,150,50,font_size=24,onClick=self.set_difficulty_medium,is_mouse_pressed=self.is_mouse_pressed,disabled=self.is_show_about)
        else:
            medium_button = Button(self.screen,"Medium",350,290,150,50,font_size=24,onClick=self.set_difficulty_medium,is_mouse_pressed=self.is_mouse_pressed,disabled=self.is_show_about,background_color=(255,255,255),text_color=(20,20,20))
        if self.difficulty != "hard":
            hard_button = Button(self.screen,"Hard",350,350,150,50,font_size=24,onClick=self.set_difficulty_hard,is_mouse_pressed=self.is_mouse_pressed,disabled=self.is_show_about)

        else:
            hard_button = Button(self.screen,"Hard",350,350,150,50,font_size=24,onClick=self.set_difficulty_hard,is_mouse_pressed=self.is_mouse_pressed,disabled=self.is_show_about,background_color=(255,255,255),text_color=(20,20,20))

        easy_button.render()
        medium_button.render()
        hard_button.render()
    def draw_score(self,x):
        score = "No score"
        if self.save_load_manager.check_for_file(self.difficulty + "_score_time"):
            score = self.save_load_manager.load_data(self.difficulty + "_score_time")

        score_font= pygame.font.SysFont('Arial',80)
        score_dec_font = pygame.font.SysFont('Arial',30)
        score_text = score_font.render(f"{score}",True,(255,255,255))
        score_dec_text = score_dec_font.render("Best Time", True, (255, 255, 255))

        self.screen.blit(score_text,(x-score_text.get_rect().width/2,70+50))
        self.screen.blit(score_dec_text, (x - score_dec_text.get_rect().width / 2, 70))
    def draw_game_name(self):
        game_name = GameName(self.screen,70,70)
        game_name.render()
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
    def draw_block(self,x,y):
        blocks = []
        for i in range(3):
            if i ==0:
                blocks.append(ColorBlock(self.screen,x,y+50*i,100,50,AppColors.blue))
            if i ==1:
                blocks.append(ColorBlock(self.screen,x,y+50*i,100,50,AppColors.red))
            if i ==2:
                blocks.append(ColorBlock(self.screen,x,y+50*i,100,50,AppColors.cyan))
        for block in blocks:
            block.render()
        Light(self.screen,550,400,use_mouse=False,size=(150,200),center=(550,400)).render()
    def show_about(self):
        back_button = Button(self.screen, "Back", 100, 260, 100, 40, font_size=16, onClick=self.on_deshow_about,
                              is_mouse_pressed=self.is_mouse_pressed)
        back_button.render()
        desc = "Game 'Colour Blind' mencerminkan esensi dan tema utama\n"\
               "yang akan dihadirkan dalam pengalaman bermain game tersebut.\n"\
               "Nama ini secara langsung menggambarkan bahwa pemain akan\n"\
               "menghadapi situasi dimana pengenalan warna menjadi penting,\n"\
               "dan untuk membedakan objek dalam skala warna yang terbatas.\n"\
               "Dengan tema warna yang telah ditentukan oleh sistem game\n"\
               "sehingga menggunakan persepsi warna untuk memecahkan teka-teki.\n"
        Helper.blit_text(self.screen,desc,(40,340),font_size=16)

    def on_show_about(self):
        self.is_show_about = True
    def set_difficulty(self,difficulty):
        self.save_load_manager.save_data(difficulty,AppConstant.DIFFICULTY)
    def set_difficulty_easy(self):
        self.set_difficulty("easy")
        self.difficulty = "easy"

    def set_difficulty_medium(self):
        self.set_difficulty("medium")
        self.difficulty = "medium"

    def set_difficulty_hard(self):
        self.set_difficulty("hard")
        self.difficulty = "hard"

    def on_deshow_about(self):
        self.is_mouse_pressed = False
        self.is_show_about = False