import pygame
from snake import SnakeEnvironment
from nn_visualizer import VisualNN


class NeuralSnake():
    def __init__(self):
        self.snake_env = SnakeEnvironment()
        self.nn_vis = VisualNN([12,8,8,4])