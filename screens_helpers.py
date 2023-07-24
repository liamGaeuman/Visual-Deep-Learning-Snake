from widgets import *
from typing import Callable
from collections import deque


class PickModelScreen:

    def __init__(self):
        pass


class RunModelScreen:

    def __init__(self):
        pass


class TrainingModelScreen:

    def __init__(self):
        self.replay_buffer = deque(maxlen=2000)
        # new instance of an RL session
        # create all the little parts for the NN
        pass

    def get_move(self):
        pass

    def update_state(self):
        pass


class LostGameScreen:
    def __init__(self):
        pass


class HomeScreen:
    WIDTH = 150
    HEIGHT = 50
    PLAY_BUTTON_TEXT = "Play"
    TRAIN_MODEL_TEXT = "Train Model"
    RUN_MODEL_TEXT = "Run Model"
    BG_COLOR = (255, 255, 255)  # white
    TEXT_COLOR = (0, 0, 0)  # black
    HOVER_COLOR = (153, 153, 255)  # random
    CLICK_COLOR = (130, 130, 255)  # random again

    def __init__(self, human_button_function: Callable, train_model_function: Callable, run_model_function: Callable):
        self.medium_font = pygame.font.SysFont("ocraii", 20)
        self.human_play_button = Button((20, 20), self.WIDTH, self.HEIGHT, self.PLAY_BUTTON_TEXT, self.medium_font,
                                        self.BG_COLOR, self.TEXT_COLOR, self.HOVER_COLOR, self.CLICK_COLOR,
                                        human_button_function)
        self.train_model_button = Button((20, 90), self.WIDTH, self.HEIGHT, self.TRAIN_MODEL_TEXT, self.medium_font,
                                         self.BG_COLOR, self.TEXT_COLOR, self.HOVER_COLOR, self.CLICK_COLOR,
                                         train_model_function)
        self.run_model_button = Button((20, 160), self.WIDTH, self.HEIGHT, self.RUN_MODEL_TEXT, self.medium_font,
                                       self.BG_COLOR, self.TEXT_COLOR, self.HOVER_COLOR, self.CLICK_COLOR,
                                       run_model_function)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.human_play_button, self.train_model_button, self.run_model_button)

    def get_sprites(self) -> pygame.sprite.Group:
        return self.all_sprites

    def call_button_updates(self):
        self.human_play_button.update()
        self.train_model_button.update()
        self.run_model_button.update()


