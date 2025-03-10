import pygame

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

    def destroy(self):
        # Remove the sprite from all groups
        self.kill()


class Food(pygame.sprite.Sprite):
    def __init__(self, color: tuple[int, int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([24, 24])
        self.image.fill(color)
        self.rect = self.image.get_rect()
