import random
from snake_sprites import *


def random_grid_num():
    num = random.randint(0, 475 / 25)
    return num * 25 + 1


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