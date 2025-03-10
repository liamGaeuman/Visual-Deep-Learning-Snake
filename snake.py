from snake_sprites import *
import random
import math
from enum import Enum

class Action(Enum):
    UP = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3

class SnakeEnvironment:
    LIGHTBLUE = (7, 247, 227)
    GREEN = (0, 102, 0)
    BODY_GREEN = (31, 190, 31)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GRAY = (120, 120, 120)
    DIM = (501, 501)

    def __init__(self) -> None:
        self.canvas = pygame.Surface(self.DIM)
        self._snake = SnakeHead(self.GREEN)
        self._food = Food(self.LIGHTBLUE)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self._food, self._snake)
        self.previous_head_location = (self._snake.rect.x, self._snake.rect.y)
        self.lost = None
        self.score = None
        self.snakeBody = []
        self.reset()

    @staticmethod
    def get_canavs_dim():
        return SnakeEnvironment.DIM


    @staticmethod
    def sample_action() -> Action:
        return random.choice(list(Action))


    def sample_safe_action(self) -> Action:
        observation = self._build_observation()
        available_actions = []

        for i in range(4):
            if observation[i] == 0:
                available_actions.append(Action(i))

        if len(available_actions) > 0:   
            return random.choice(available_actions)
        
        return SnakeEnvironment.sample_action()

    
    def reset(self):
        self.lost = False
        self.score = 0
        for piece in self.snakeBody:
            piece.destroy()
        self.snakeBody = []
        self._food.rect.x = SnakeEnvironment.random_grid_num()
        self._food.rect.y = SnakeEnvironment.random_grid_num()
        self._snake.rect.x = 226
        self._snake.rect.y = 226
        self.previous_head_location = (self._snake.rect.x, self._snake.rect.y)
        self._snake.change_color(self.GREEN)
        return self._build_observation()


    def render_frame(self):
        self.canvas.fill((0, 0, 0))
        self._draw_lines(self.GRAY)
        self.all_sprites.draw(self.canvas)
        return self.canvas


    def step(self, action : int):
        # Move the snake head
        self._move_head(action)
        # Check to see if the snake head is over the food
        reward = self._check_eat()
        if reward == 1:
            self.score += 1
            self.snakeBody.append(SnakeBodyPiece(self.BODY_GREEN))
            self.all_sprites.add(self.snakeBody[self.score - 1]) 
            self._food.rect.x = SnakeEnvironment.random_grid_num()
            self._food.rect.y = SnakeEnvironment.random_grid_num()
        # Check to see if the game has been lost
        self._check_out_of_bounds()
        # Dead Snake :(
        if self.lost:
            self._undo_direction(action)
            self._snake.change_color(self.RED)
        else:
            self._move_body() 
            # Update snakes previous head location
            self.previous_head_location = (self._snake.rect.x, self._snake.rect.y)
        return (self._build_observation() ,reward, self.lost)       


    def get_observation(self):
        return self._build_observation()

    @staticmethod
    def random_grid_num():
        num = random.randint(0, int(475 / 25))
        return num * 25 + 1


    def _draw_lines(self, color: tuple[int, int, int]):
        for x in range(0, 501, 25):
            pygame.draw.line(self.canvas, color, (x, 0), (x, 500), 1)
        for y in range(0, 501, 25):
            pygame.draw.line(self.canvas, color, (0, y), (500, y), 1) 


    def _build_observation(self) -> list:
        observation = []
        # going up?
        # going down?
        # going left?
        # going right?
        # head x coord (0 centered)
        # head y coord (0 centerde)
        # food relative x coord
        # food relative y coord
        # tail relative x coord
        # tail relative y coord
        # snake body center relative x coord
        # snake body center relative y coord
        return observation


    # def _get_body_center_coords(self):
    #     if len(self.snakeBody) >= 1:
    #         center_piece = int(len(self.snakeBody)//2)
    #         return math.sqrt((self._snake.rect.x - self.snakeBody[center_piece].rect.x)**2 
    #             + (self._snake.rect.y - self.snakeBody[center_piece].rect.y)**2)/671.752
    #     return 476/501


    # def _get_tail_coords(self):
    #     if len(self.snakeBody) >= 1:
    #         return math.sqrt((self._snake.rect.x - self.snakeBody[-1].rect.x)**2 
    #             + (self._snake.rect.y - self.snakeBody[-1].rect.y)**2)/671.752
    #     return 476/501


    # def _get_food_coords(self):
    #     return math.sqrt((self._snake.rect.x - self._food.rect.x)**2 + (self._snake.rect.y - self._food.rect.x)**2)/671.752


    # def _get_wall_distance(self):
    #     left = self._snake.rect.x - 1
    #     right = 501 - self._snake.rect.x - 25
    #     up = self._snake.rect.y - 1
    #     down = 501 - self._snake.rect.y - 25
    #     return min(left,right,up,down)/225


    # def _check_food_direction(self, direction : Action) -> int:
    #     if direction == Action.UP:
    #         if self._snake.rect.y < self._food.rect.y:
    #             return 1
    #     elif direction == Action.DOWN:
    #         if self._snake.rect.y > self._food.rect.y:
    #             return 1
    #     elif direction == Action.RIGHT:
    #         if self._snake.rect.x > self._food.rect.x:
    #             return 1
    #     elif direction == Action.LEFT:
    #         if self._snake.rect.x < self._food.rect.x:
    #             return 1
    #     return 0


    # def _check_touch(self, direction : Action) -> int:
    #     if direction == Action.UP:
    #         if (self._snake.rect.y == 1 or self._check_head_snake_body_touch(self._snake.rect.x,self._snake.rect.y - 25)):
    #             return 1
    #     elif direction == Action.DOWN:
    #         if (self._snake.rect.y == 476 or self._check_head_snake_body_touch(self._snake.rect.x,self._snake.rect.y + 25)):
    #             return 1
    #     elif direction == Action.RIGHT:
    #         if (self._snake.rect.x == 476 or self._check_head_snake_body_touch(self._snake.rect.x + 25,self._snake.rect.y)):
    #             return 1
    #     elif direction == Action.LEFT:
    #         if (self._snake.rect.x == 1 or self._check_head_snake_body_touch(self._snake.rect.x - 25,self._snake.rect.y)):
    #             return 1
    #     return 0


    # def _check_head_snake_body_touch(self, x : int ,y : int):
    #     for body_part in self.snakeBody:
    #         if (body_part.rect.x == x and body_part.rect.y == y):
    #             return True
    #     return False


    def _undo_direction(self, direction):
        if direction == Action.UP:
            direction = Action.DOWN
        elif direction == Action.RIGHT:
            direction = Action.LEFT
        elif direction == Action.LEFT:
            direction = Action.RIGHT
        else:
            direction = Action.UP
        self._move_head(direction)


    """Algorithm responsible for moving the snake body following the head"""
    def _move_body(self):
        if self.score >= 1:
            temp_x = self.snakeBody[0].rect.x
            temp_y = self.snakeBody[0].rect.y

            self.snakeBody[0].rect.x = self.previous_head_location[0]
            self.snakeBody[0].rect.y = self.previous_head_location[1]

            if self.score == 1:
                self.snakeBody[0].last_x = self._snake.rect.x
                self.snakeBody[0].last_y = self._snake.rect.y
            else:
                self.snakeBody[0].last_x = temp_x
                self.snakeBody[0].last_y = temp_y

        if self.score > 1:
            for i in range(1, len(self.snakeBody)):
                # check lost
                if ((self.snakeBody[i].rect.y == self._snake.rect.y) and
                        (self.snakeBody[i].rect.x == self._snake.rect.x)):
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


    def _check_out_of_bounds(self):
        if (0 > self._snake.rect.x or 500 < self._snake.rect.x
                or 0 > self._snake.rect.y or 500 < self._snake.rect.y):
            self.lost = True


    def _check_eat(self):
        if ((self._snake.rect.y == self._food.rect.y) and
                (self._snake.rect.x == self._food.rect.x)):
            return 1
        return 0


    def _move_head(self, direction):
        if direction == Action.UP:  
            self._snake.rect.y -= 25
        elif direction == Action.DOWN:  
            self._snake.rect.y += 25
        elif direction == Action.RIGHT:  
            self._snake.rect.x += 25
        elif direction == Action.LEFT:  
            self._snake.rect.x -= 25
        else:
            raise Exception("Invalid direction, must be an int 0-3") 