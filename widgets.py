import pygame


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
