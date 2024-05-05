import sys
import pygame
from app import  App

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/audio/apparition.mp3")
    pygame.mixer.music.play(loops=-1,fade_ms=2000)
    app = App()
    app.loop()
if __name__ == '__main__':
    main()