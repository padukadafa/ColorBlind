import os
import sys
import pygame
from app import  App
from core.app_constant import AppConstant
from service.save_load_manager import SaveLoadManager


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    pygame.mixer.init()
    pygame.mixer.music.load("assets/audio/apparition.mp3")
    if SaveLoadManager(".save","save_data").load_data(AppConstant.VOLUME_STATUS):
        pygame.mixer.music.play(loops=-1,fade_ms=2000)
    app = App()
    app.loop()
if __name__ == '__main__':
    main()