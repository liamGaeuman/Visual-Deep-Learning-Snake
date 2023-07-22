import pygame
from game_round import GameRound
from screens import *


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


