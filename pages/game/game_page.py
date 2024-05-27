import random

from core.widget import Widget
import pygame
from core.app_constant import AppConstant
import sys

from service.save_load_manager import SaveLoadManager
from widgets.button import Button
from widgets.game_light import Light

from core.app_colors import AppColors
from widgets.color_block import ColorBlock
import math

from widgets.empty_block import EmptyBlock
from widgets.page import Page

class GamePage(Page):
    def __init__(self,screen,on_open_start_menu=None,on_restart=None):
        super().__init__()
        self.screen = screen
        pygame.display.set_caption(AppConstant.game_title)
        self.save_load_manager = SaveLoadManager(".save", "save_data")
        self.difficulty = self.save_load_manager.load_data(AppConstant.DIFFICULTY)
        self.row = 3
        self.block_count = 12
        self.block_gap = 90
        self.block_start = 150
        self.block_size = 100
        self.block_height = 5
        if self.difficulty is None or self.difficulty == "easy":
            self.cols_count = [4,4,4]
            self.block_height = 6
        elif self.difficulty == "medium":
            self.row = 4
            self.block_count = 16
            self.cols_count = [4,4,4,4]
            self.block_gap = 70
            self.block_start = 100
        elif self.difficulty == "hard":
            self.row = 5
            self.block_count = 20
            self.cols_count = [4,4,4,4,4]
            self.block_gap = 60
            self.block_start = 30

        self.block_pos = [self.block_start+self.block_gap*i+i*self.block_size for i in range(self.row)]
        self.clock = pygame.time.Clock()
        self.selected_block = -1
        self.on_open_start_menu=on_open_start_menu
        self.selected_block_x = 0
        self.selected_block_y = 0
        self.blocks = self.generate_blocks()

        self.block = self.blocks[self.selected_block]
        self.background = pygame.image.load("assets/images/background.jpg")
        self.background= pygame.transform.scale(self.background,(AppConstant.screen_width,AppConstant.screen_height))
        self.light = Light(self.screen)

        self.start_time = pygame.time.get_ticks()
        self.pause_start_time = pygame.time.get_ticks()
        self.pause_end_time = pygame.time.get_ticks()
        self.pause_time = 0
        self.is_pause = False
        self.time = 0
        self.is_mouse_pressed = False
        self.pick_sound = pygame.mixer.Sound("assets/audio/pick.mp3")
        self.drop_sound = pygame.mixer.Sound("assets/audio/drop.mp3")
        self.pause_sound = pygame.mixer.Sound("assets/audio/pause.wav")
        self.win_sound = pygame.mixer.Sound("assets/audio/win.mp3")
        pygame.mixer.Sound("assets/audio/start_game.wav").play()
        self.win_sound_played = False
        self.win =False
        self.on_restart = on_restart

    def get_shorted_block(self,x,y):
        for i in range(len(self.blocks)):
            if self.blocks[i].rect.collidepoint(x, y):
                return i
        return self.selected_block
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.is_mouse_pressed = True
                if not self.is_pause:
                    self.selected_block = self.get_shorted_block(event.pos[0], event.pos[1])
                    self.cols_count = self.get_cols_count()
                    if self.row == 3 and (self.cols_count[0]*self.row-3 == self.selected_block or self.cols_count[1]*self.row-2 == self.selected_block or self.cols_count[2]*self.row-1 == self.selected_block):

                        self.block = self.blocks[self.selected_block]
                        self.blocks[self.selected_block] = EmptyBlock(self.screen,self.block.x,self.block.y,100,50)
                        self.selected_block_x = self.blocks[self.selected_block].x
                        self.selected_block_y = self.blocks[self.selected_block].y
                        if type(self.block) is ColorBlock:
                            self.pick_sound.stop()
                            self.pick_sound.play()
                            self.block.enable_drag()
                        else:
                            self.selected_block=-1
                    if self.row == 4 and (self.cols_count[0] * self.row - 4 == self.selected_block or self.cols_count[1] * self.row - 3 == self.selected_block or self.cols_count[2] * self.row - 2 == self.selected_block or self.cols_count[3] * self.row - 1 == self.selected_block):
                        self.block = self.blocks[self.selected_block]
                        self.blocks[self.selected_block] = EmptyBlock(self.screen, self.block.x, self.block.y, 100, 50)
                        self.selected_block_x = self.blocks[self.selected_block].x
                        self.selected_block_y = self.blocks[self.selected_block].y
                        if type(self.block) is ColorBlock:
                            self.pick_sound.stop()
                            self.pick_sound.play()
                            self.block.enable_drag()
                        else:
                            self.selected_block = -1
                    if self.row == 5 and (self.cols_count[0] * self.row - 5 == self.selected_block or self.cols_count[1] * self.row - 4 == self.selected_block or self.cols_count[2] * self.row - 3 == self.selected_block or self.cols_count[3] * self.row - 2 == self.selected_block or self.cols_count[4] * self.row - 1 == self.selected_block):
                        self.block = self.blocks[self.selected_block]
                        self.blocks[self.selected_block] = EmptyBlock(self.screen, self.block.x, self.block.y, 100, 50)
                        self.selected_block_x = self.blocks[self.selected_block].x
                        self.selected_block_y = self.blocks[self.selected_block].y
                        if type(self.block) is ColorBlock:
                            self.pick_sound.stop()
                            self.pick_sound.play()
                            self.block.enable_drag()
                        else:
                            self.selected_block = -1
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_mouse_pressed = False
                if not self.is_pause:
                    if self.row == 3 and (self.cols_count[0] * self.row - 3 == self.selected_block or self.cols_count[1] * self.row - 2 == self.selected_block or self.cols_count[2] * self.row - 1 == self.selected_block):
                        self.draw_pause()
                        self.drop_sound.play()
                        self.block.disable_drag()
                        self.block_draggable_event()
                        self.selected_block = -1
                    if self.row == 4 and (self.cols_count[0] * self.row - 4 == self.selected_block or self.cols_count[1] * self.row - 3 == self.selected_block or self.cols_count[2] * self.row - 2 == self.selected_block or self.cols_count[3] * self.row - 1 == self.selected_block):
                        self.draw_pause()
                        self.drop_sound.play()
                        self.block.disable_drag()
                        self.block_draggable_event()
                        self.selected_block = -1
                    if self.row == 5 and (self.cols_count[0] * self.row - 5 == self.selected_block or self.cols_count[1] * self.row - 4 == self.selected_block or self.cols_count[2] * self.row - 3 == self.selected_block or self.cols_count[3] * self.row - 2 == self.selected_block or self.cols_count[4] * self.row - 1 == self.selected_block):
                        self.draw_pause()
                        self.drop_sound.play()
                        self.block.disable_drag()
                        self.block_draggable_event()
                        self.selected_block = -1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                if not self.is_pause:
                    self.pause_start_time = pygame.time.get_ticks()
                self.is_pause = not self.is_pause
                self.pause_sound.stop()
                self.pause_sound.play()




    def render(self):
        self.event_handler()
        self.screen.fill((0, 0, 0))
        self.draw_bg()

        self.draw_block()
        if not self.is_pause:
            self.light.render()
        self.draw_time()
        if not self.win:
            self.pause_handler()
        self.win_handler()

        pygame.display.update()
        self.clock.tick(AppConstant.fps)

    def get_cols_count(self):
        cols_count = [0 for i in range(self.row)]
        for i in range(self.block_height):
            if type(self.blocks[0 + i * self.row]) is ColorBlock:
                cols_count[0] += 1
        for i in range(self.block_height):
            if type(self.blocks[1 + i * self.row]) is ColorBlock:
                cols_count[1] += 1
        for i in range(self.block_height):
            if type(self.blocks[2 + i * self.row]) is ColorBlock:
                cols_count[2] += 1
        if self.row >= 4:
            for i in range(self.block_height):
                if type(self.blocks[3 + i * self.row]) is ColorBlock:
                    cols_count[3] += 1
        if self.row == 5:
            for i in range(self.block_height):
                if type(self.blocks[4 + i * self.row]) is ColorBlock:
                    cols_count[4] += 1
        return cols_count

    def draw_block(self):
        for block in self.blocks:
            if type(block) is ColorBlock:
                block.render()
        if self.selected_block >= 0:
            shortest_block = self.get_shortest_block(self.block)
            self.blocks[shortest_block].render()
        if self.selected_block >=0:
            self.block.render()
    def block_draggable_event(self):
        if self.selected_block != -1:
            block = self.block
            if not block.draggable:
                shortest_block_index = self.get_shortest_block(block)
                self.swap_block(shortest_block_index)

    def get_shortest_block(self,block):
        min = math.inf
        index = 0
        result = 0
        for i in range(0,self.row):
            if math.sqrt((block.x - self.block_pos[i])**2) < min:
                min = math.sqrt((block.x - self.block_pos[i])**2)
                index = i
        cols_count =self.get_cols_count()
        if cols_count[index] == self.block_height:
            return self.selected_block
        for i in range(self.block_height):
            if type(self.blocks[index+i*self.row]) is EmptyBlock:
                result = index+i*self.row
                break
        return result


    def swap_block(self,a):
        self.block.move(self.blocks[a].x,self.blocks[a].y)

        self.blocks[a] = self.block
    def swap_block_to_last(self,index):
        tmp = self.blocks[index]
        self.blocks.pop(index)
        self.blocks.append(tmp)
    def draw_bg(self):
        self.screen.blit(self.background,(0,0))
    def generate_blocks(self):
        blocks = []
        blocks_count = [0 for x in range(self.row)]

        i = 0
        for j in blocks_count:
            i += j
        while i < self.block_count:
            random_index = random.randint(0,self.row-1)
            i = 0
            print(blocks_count)
            for j in blocks_count:
                i += j
            if random_index ==0 and blocks_count[0] < 4:
                blocks.append(ColorBlock(self.screen, self.block_pos[i%self.row],AppConstant.bloc_floor-50*math.floor(i/self.row),self.block_size,50,AppColors.blue))
                blocks_count[0] += 1
            if random_index ==1 and blocks_count[1] < 4:
                blocks.append(ColorBlock(self.screen, self.block_pos[i%self.row],AppConstant.bloc_floor-50*math.floor(i/self.row),self.block_size,50,AppColors.red))
                blocks_count[1] += 1
            if random_index ==2 and blocks_count[2] < 4:
                blocks.append(ColorBlock(self.screen, self.block_pos[i%self.row],AppConstant.bloc_floor-50*math.floor(i/self.row),self.block_size,50,AppColors.cyan))
                blocks_count[2] += 1
            if  self.row >= 4 and random_index ==3 and blocks_count[3] < 4:
                blocks.append(ColorBlock(self.screen, self.block_pos[i%self.row],AppConstant.bloc_floor-50*math.floor(i/self.row),self.block_size,50,AppColors.magenta))
                blocks_count[3] += 1
            if self.row == 5 and random_index ==4 and blocks_count[4] < 4:
                blocks.append(ColorBlock(self.screen, self.block_pos[i%self.row],AppConstant.bloc_floor-50*math.floor(i/self.row),self.block_size,50,AppColors.white))
                blocks_count[4] += 1
        for i in range(self.row*2):
            blocks.append(EmptyBlock(self.screen,self.block_pos[i%self.row],AppConstant.bloc_floor-50*math.floor((i+self.block_count)/self.row),self.block_size,50))
        return blocks

    def draw_time(self):
        time = self.get_time()
        message = f"Time  {time}"
        font = pygame.font.SysFont("Sans",20)
        self.screen.blit(font.render(message,True,(255,255,255)),(20,20))
    def get_time(self):
        if not self.is_pause:
            self.time = pygame.time.get_ticks() - self.start_time - self.pause_time
        return f"{math.floor(self.time/60000)}:{math.floor(self.time/1000)%60}"

    def save_time(self):

        difficulty = self.save_load_manager.load_data(AppConstant.DIFFICULTY)
        low = self.save_load_manager.load_data(difficulty + "_score_time")

        if not low:
            self.save_load_manager.save_data(self.get_time(), difficulty + "_score_time")
        time = self.get_time()
        if low:
            if self.convert_time_to_int(low) > self.convert_time_to_int(time):
                self.save_load_manager.save_data(time, difficulty + "_score_time")
    def convert_time_to_int(self,str):
        l_str = str.split(":")
        return int(l_str[0])*60 + int(l_str[1])
    def pause_handler(self):
        if self.is_pause:
            self.pause_end_time = pygame.time.get_ticks()
            self.draw_pause()
        else:
            self.pause_time += self.pause_end_time - self.pause_start_time
            self.pause_start_time = pygame.time.get_ticks()
            self.pause_end_time = self.pause_start_time
        pass
    def draw_pause(self):
        s = pygame.Surface(pygame.display.get_surface().get_size())
        s.set_alpha(230)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        Light(self.screen).render()
        resume_button = Button(self.screen,"Resume",AppConstant.screen_width/2,150,150,100,font_size=36,onClick=self.on_resume,is_mouse_pressed=self.is_mouse_pressed)
        exit_button = Button(self.screen,"Main Menu",AppConstant.screen_width/2,280,200,100,font_size=36,onClick=self.on_open_start_menu,is_mouse_pressed=self.is_mouse_pressed)
        exit_button.render()
        resume_button.render()
    def on_resume(self):
        self.is_pause = False
    def win_handler(self):

        win = True

        color_map = [0 for i in range(self.row)] # red, cyan,blue
        cols_count = [0 for i in range(self.row)]
        for i in range(self.row):
            if self.blocks[i].get_color() == AppColors.red:
                color_map[0] = i
            if self.blocks[i].get_color() == AppColors.cyan:
                color_map[1] = i
            if self.blocks[i].get_color() == AppColors.blue:
                color_map[2] = i
            if self.blocks[i].get_color() == AppColors.magenta:
                color_map[3] = i
            if self.blocks[i].get_color() == AppColors.white:
                color_map[4] = i

        for i in range(4):
            if self.blocks[color_map[0] + self.row*i].get_color() != AppColors.red:
                win = False
                break
            cols_count[color_map[0]] += 1
        for i in range(4):
            if self.blocks[color_map[1] + self.row * i].get_color() != AppColors.cyan:
                win = False
                break
            cols_count[color_map[1]] += 1
        for i in range(4):
            if self.blocks[color_map[2] + self.row * i].get_color() != AppColors.blue:
                win = False
                break
            cols_count[color_map[2]] += 1
        if self.row==4:
            for i in range(4):
                if self.blocks[color_map[3] + self.row * i].get_color() != AppColors.magenta:
                    win = False
                    break
                cols_count[color_map[3]] += 1
        if self.row==5:

            for i in range(4):
                if self.blocks[color_map[4] + self.row * i].get_color() != AppColors.white:
                    win = False
                    break
                cols_count[color_map[4]] += 1
        print(cols_count)
        if win:
            self.win = True
            self.is_pause = True

            self.save_time()
            if not self.win_sound_played:
                self.win_sound.play()
            self.win_sound_played = True
            self.draw_win()

    def draw_win(self):
        s = pygame.Surface(pygame.display.get_surface().get_size())
        s.set_alpha(230)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        s = pygame.Surface(pygame.display.get_surface().get_size())
        score = self.get_time()
        Light(self.screen).render()
        resume_button = Button(self.screen, "New Game", AppConstant.screen_width / 2, 150, 200, 100, font_size=36,
                               onClick=self.on_restart, is_mouse_pressed=self.is_mouse_pressed)
        exit_button = Button(self.screen, "Main Menu", AppConstant.screen_width / 2, 280, 200, 100, font_size=36,
                             onClick=self.on_open_start_menu, is_mouse_pressed=self.is_mouse_pressed)
        exit_button.render()
        resume_button.render()
        score_font= pygame.font.SysFont('Arial',60)
        score_text = score_font.render(score,True,(255,255,255))
        score_dec = pygame.font.SysFont('Arial',30)
        score_dec_text = score_dec.render("Your Time",True,(255,255,255))
        self.screen.blit(score_dec_text, (AppConstant.screen_width / 2 - score_dec_text.get_rect().width / 2, 60))
        self.screen.blit(score_text, (AppConstant.screen_width/2 - score_text.get_rect().width / 2, 100))



