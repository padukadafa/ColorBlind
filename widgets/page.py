import os
import pyautogui
from core.app_constant import AppConstant
from core.widget import Widget


class Page(Widget):
    def __init__(self):

        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width, screen_height)
        # os.environ['SDL_VIDEO_CENTERED'] = '1'
        super().__init__()