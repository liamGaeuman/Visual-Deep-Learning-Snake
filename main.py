"""
Author: Liam Gaeuman
Start Date: 7/14/2023

Description: This program allows both a user and a deep reinforcement learning algorithm to play the classic snake game.
The program makes use of the Pygame module for the display and PyTorch for the RL. Upon entry of the app, a user can
choose to play a game themselves, pick an existing trained model, or to train a model. The program contains a display
of the Neural Network used when training the model when the train model mode is selected. Both existing models and users
can have their high scores submitted to a scoreboard which will be displayed on the home screen.

python version:
pygame version:
pytorch version:

"""

import pygame
import random
from typing import Callable


def random_grid_num():
    num = random.randint(0, 475 / 25)
    return num * 25 + 1


class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, color: tuple[int, int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([24, 24])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def change_color(self, color: tuple[int, int, int]):
        self.image.fill(color)


class SnakeBodyPiece(pygame.sprite.Sprite):
    def __init__(self, color: tuple[int, int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([24, 24])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.last_x = 0
        self.last_y = 0

    def change_color(self, color: tuple[int, int, int]):
        self.image.fill(color)


class Food(pygame.sprite.Sprite):
    def __init__(self, color: tuple[int, int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([24, 24])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Button(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], width: int, height: int, text: str, font: pygame.font.SysFont,
                 bg_color: tuple[int, int, int], text_color: tuple[int, int, int], hover_color: tuple[int, int, int],
                 click_color: tuple[int, int, int], event_handler):

        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.event_handler = event_handler

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        self.update()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            self.image.fill(self.hover_color)
            if mouse_click[0] == 1:
                self.image.fill(self.click_color)
                if self.event_handler is not None:
                    self.event_handler()
        else:
            self.image.fill(self.bg_color)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(topleft=self.rect.topleft)

        self.image.blit(text_surface, text_rect)


class GameRound:
    LIGHTBLUE = (7, 247, 227)
    GREEN = (0, 102, 0)
    BODY_GREEN = (31, 190, 31)
    RED = (255, 0, 0)

    # PUBLIC:
    def __init__(self):
        self.score = 0
        self.snakeBody = []
        self.food = Food(self.LIGHTBLUE)
        self.food.rect.x = random_grid_num()
        self.food.rect.y = random_grid_num()
        self.snake = SnakeHead(self.GREEN)
        self.snake.rect.x = 226
        self.snake.rect.y = 226
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.food, self.snake)
        self.direction = random.randint(1, 4)
        self.lost = False
        self.previous_head_location = (self.snake.rect.x, self.snake.rect.y)

    def get_sprites(self) -> pygame.sprite.Group:
        return self.all_sprites

    def get_loss_status(self) -> bool:
        return self.lost

    def get_score(self) -> int:
        return self.score

    def set_direction(self, direction: int):
        print(direction)
        print(self.direction)
        print("---")
        # Can't go in opposite direction
        if direction + self.direction == 5 and self.score > 0:
            self.lost = True
        else:
            self.direction = direction

    def update_snake(self):
        # Move the snake head
        self._go_direction()
        # Check to see if the snake head is over the food
        self._check_eat()
        # Check to see if the game has been lost
        self._check_out_of_bounds()
        # Dead Snake
        if self.lost:
            self._undo_direction()
            self.snake.change_color(self.RED)
            return
        # Move the snake body
        self._move_snake_body()
        # Update snakes previous head location
        self.previous_head_location = (self.snake.rect.x, self.snake.rect.y)

    # PRIVATE:
    def _undo_direction(self):
        if self.direction == 1:
            self.direction = 4
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 3:
            self.direction = 2
        else:
            self.direction = 1
        self._go_direction()

    def _go_direction(self):
        if self.direction == 1:  # up
            self.snake.rect.y -= 25
        elif self.direction == 4:  # down
            self.snake.rect.y += 25
        elif self.direction == 2:  # right
            self.snake.rect.x += 25
        elif self.direction == 3:  # left
            self.snake.rect.x -= 25
        else:
            raise Exception("Invalid direction, must be an int 1-4")

    def _check_eat(self):
        if ((self.snake.rect.y == self.food.rect.y) and
                (self.snake.rect.x == self.food.rect.x)):
            # spawn new food
            self.food.rect.x = random_grid_num()
            self.food.rect.y = random_grid_num()
            # increase the score
            self.score += 1
            # extend the body and add to window
            self.snakeBody.append(SnakeBodyPiece(self.BODY_GREEN))
            self.all_sprites.add(self.snakeBody[self.score - 1])

    def _check_out_of_bounds(self):
        if (0 > self.snake.rect.x or 500 < self.snake.rect.x
                or 0 > self.snake.rect.y or 500 < self.snake.rect.y):
            self.lost = True

    def _move_snake_body(self):
        if self.score >= 1:
            temp_x = self.snakeBody[0].rect.x
            temp_y = self.snakeBody[0].rect.y

            self.snakeBody[0].rect.x = self.previous_head_location[0]
            self.snakeBody[0].rect.y = self.previous_head_location[1]

            if self.score == 1:
                self.snakeBody[0].last_x = self.snake.rect.x
                self.snakeBody[0].last_y = self.snake.rect.y
            else:
                self.snakeBody[0].last_x = temp_x
                self.snakeBody[0].last_y = temp_y

        if self.score > 1:
            for i in range(1, len(self.snakeBody)):
                # check for loss
                if ((self.snakeBody[i].rect.y == self.snake.rect.y) and
                        (self.snakeBody[i].rect.x == self.snake.rect.x)):
                    self.lost = True
                    if i + 1 >= len(self.snakeBody):
                        self.snakeBody[i].change_color(self.RED)
                    else:
                        self.snakeBody[i + 1].change_color(self.RED)

                # store current body part's location
                temp_x = self.snakeBody[i].rect.x
                temp_y = self.snakeBody[i].rect.y

                # set current body part to location of prev body part
                self.snakeBody[i].rect.x = self.snakeBody[i - 1].last_x
                self.snakeBody[i].rect.y = self.snakeBody[i - 1].last_y

                # set current body part prev location to old loc (temp)
                self.snakeBody[i].last_x = temp_x
                self.snakeBody[i].last_y = temp_y


class LostGameScreen:

    def __init__(self):
        pass


class HomeScreen:
    WIDTH = 150
    HEIGHT = 50
    PLAY_BUTTON_TEXT = "Human Play"
    TRAIN_MODEL_TEXT = "Meow Play"
    RUN_MODEL_TEXT = "Ruff Play"
    BG_COLOR = (255, 255, 255)  # white
    TEXT_COLOR = (0, 0, 0)  # black
    HOVER_COLOR = (124, 33, 50)  # random
    CLICK_COLOR = (50, 33, 124)  # random again

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


class PickModelScreen:

    def __init__(self):
        pass


class RunModelScreen:

    def __init__(self):
        pass


class TrainingModelScreen:

    def __init__(self):
        # new instance of an RL session
        # create all the little parts for the NN
        pass


class GameController:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PURPLE = (99, 5, 102)
    BLUE = (0, 0, 153)
    GRAY = (120, 120, 120)
    DARK_GRAY = (20, 20, 20)

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Snake Game')
        self.current_game_screen = None
        self.loss_screen = None
        self.pick_model_screen = None
        self.run_model_screen = None
        self.training_model_screen = None
        self.home_screen = None
        self.big_font = pygame.font.SysFont("ocraii", 45)
        self.medium_font = pygame.font.SysFont("ocraii", 35)
        self.small_font = pygame.font.SysFont("ocraii", 15)
        self.screen_dict = {"home screen": False, "game screen": False, "loss screen": False,
                            "train model screen": False, "select model screen": False, "run model screen": False}

    def _leave_home_screen(self, key: str):
        self.screen_dict["home screen"] = False
        self.screen_dict[key] = True

    def run(self):
        self.screen_dict["home screen"] = True
        score = 0
        time_delay = 100
        run = True
        direction = None
        while run:

            pygame.time.delay(time_delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Logic for game session with human player
            if self.screen_dict["game screen"]:
                if self.current_game_screen is None:
                    self.current_game_screen = GameRound()

                key = pygame.key.get_pressed()

                if key[pygame.K_UP]:
                    direction = 1
                elif key[pygame.K_DOWN]:
                    direction = 4
                elif key[pygame.K_RIGHT]:
                    direction = 2
                elif key[pygame.K_LEFT]:
                    direction = 3

                # Change direction
                if direction:
                    self.current_game_screen.set_direction(direction)

                # Update current game state
                self.current_game_screen.update_snake()

                # Redraw game board
                self._redraw_game()

                if self.current_game_screen.get_loss_status():
                    # Exit tasks
                    pygame.time.delay(500)
                    self.screen_dict["game screen"] = False
                    self.screen_dict["loss screen"] = True
                    direction = None
                    score = self.current_game_screen.get_score()
                    self.current_game_screen = None

            # - - - - - - Logic for loss screen - - - - - -
            elif self.screen_dict["loss screen"] and not self.screen_dict["train model screen"]:
                if self.loss_screen is None:
                    self.loss_screen = LostGameScreen()

                self._redraw_loss_screen(score)
                key = pygame.key.get_pressed()

                if key[pygame.K_SPACE]:
                    # Exit tasks
                    self.loss_screen = None
                    score = 0
                    self.screen_dict["loss screen"] = False
                    self.screen_dict["home screen"] = True
                elif key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
                    # Exit tasks
                    self.loss_screen = None
                    score = 0
                    self.screen_dict["loss screen"] = False
                    self.screen_dict["game screen"] = True

            # - - - - - - Logic for home screen - - - - - - -
            elif self.screen_dict["home screen"]:
                if self.home_screen is None:
                    self.home_screen = HomeScreen(lambda: self._leave_home_screen("game screen"),
                                                  lambda: self._leave_home_screen("train model screen"),
                                                  lambda: self._leave_home_screen("select model screen"))

                self.home_screen.call_button_updates()
                self._redraw_home_screen()

                if not self.screen_dict["home screen"]:
                    # Exit tasks
                    self.home_screen = None

            #  - - - - - - Logic for training model - - - - - - -
            elif self.screen_dict["train model screen"]:
                if self.training_model_screen is None:
                    self.training_model_screen = TrainingModelScreen()
                    self.window = pygame.display.set_mode((1000, 500))
                    time_delay = 50

                # Exit tasks
                self.window = pygame.display.set_mode((500, 500))
                self.training_model_screen = None
                time_delay = 100
                self.screen_dict["train model screen"] = False
                self.screen_dict["home screen"] = True

            # - - - - - - Logic for picking existing model - - - - -
            elif self.screen_dict["select model screen"]:
                if self.pick_model_screen is None:
                    self.pick_model_screen = PickModelScreen()
                # self._redraw_model_screen() #DNE yet

                # Exit tasks
                self.pick_model_screen = None
                self.screen_dict["select model screen"] = False
                self.screen_dict["run model screen"] = True

            # - - - - - - Logic for running existing model - - - - -
            elif self.screen_dict["run model screen"]:
                if self.run_model_screen is None:
                    self.run_model_screen = RunModelScreen()

                # Exit tasks
                self.run_model_screen = None
                self.screen_dict["run model screen"] = False
                self.screen_dict["loss screen"] = True

            else:
                raise Exception("No screen to display, check bool screen vars")

        pygame.quit()

    # PRIVATE:
    def _redraw_game(self):
        self.window.fill(self.BLACK)
        # Draw vertical lines
        for x in range(0, 525, 25):
            pygame.draw.line(self.window, self.GRAY, (x, 0), (x, 500), 1)
        # Draw horizontal lines
        for y in range(0, 525, 25):
            pygame.draw.line(self.window, self.GRAY, (0, y), (500, y), 1)
        self.current_game_screen.get_sprites().draw(self.window)
        pygame.display.update()

    def _redraw_home_screen(self):
        self.window.fill(self.PURPLE)
        self.home_screen.get_sprites().draw(self.window)
        pygame.display.update()

    def _redraw_loss_screen(self, score: int):
        self.window.fill(self.BLUE)
        # Draw vertical lines
        for x in range(0, 525, 25):
            pygame.draw.line(self.window, self.DARK_GRAY, (x, 0), (x, 500), 1)
        # Draw horizontal lines
        for y in range(0, 525, 25):
            pygame.draw.line(self.window, self.DARK_GRAY, (0, y), (500, y), 1)
        game_over_str = "Game Over"
        self._draw_text(game_over_str, self.big_font, self.WHITE, 130, 100)
        game_over_str = "Score: " + str(score)
        self._draw_text(game_over_str, self.medium_font, self.WHITE, 160, 170)
        game_over_str = "Press SPACE for Menu or SHIFT to Play Again"
        self._draw_text(game_over_str, self.small_font, self.WHITE, 55, 280)

        # self.loss_screen.get_sprites().draw(self.window)
        pygame.display.update()

    def _draw_text(self, text: str, font, color: tuple[int, int, int], x: int, y: int):
        img = font.render(text, True, color)
        self.window.blit(img, (x, y))


def main():
    game_controller = GameController()
    game_controller.run()


if __name__ == '__main__':
    main()
