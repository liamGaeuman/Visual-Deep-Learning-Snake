from snake import SnakeEnvironment, Action
import pygame

class SnakeGame: 
    PURPLE = (99, 5, 102)
    DARK_GRAY = (20, 20, 20)
    def __init__(self):
        self.env = SnakeEnvironment()
        x,y = self.env.get_canavs_dim()
        pygame.init()
        self.window = pygame.display.set_mode((x, y+50))
        pygame.display.set_caption('Snake Game')
        self.score = 0
        self.action = self.env.sample_action()
    
    def run(self):
        running = True
        time_delay = 100
        playing = True
        count = 0

        while running:
            
            pygame.time.delay(time_delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if playing:
                running = self._playing()

            score_txt = "Score: " + str(self.score)
            self._draw_text(score_txt, pygame.font.SysFont("ocraii", 35), (255,255,255), 10, 10)    

            pygame.display.update()
            count += 1
            print(count)

    def _baby_menu(self) -> bool:
        pass
            
    def _playing(self) -> bool:

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.action = Action.UP
        elif key[pygame.K_DOWN]:
            self.action = Action.DOWN
        elif key[pygame.K_RIGHT]:
            self.action = Action.RIGHT
        elif key[pygame.K_LEFT]:
            self.action = Action.LEFT

        observation, reward, loss = self.env.step(self.action)

        print(observation)

        self.score += reward

        snake_canvas = self.env.render_frame()
        self.window.fill((0, 0, 0))
        self.window.blit(snake_canvas, (0, 50))
        
        if loss:
            return False
        return True

    def _draw_lines(self, color: tuple[int, int, int]):
        for x in range(0, 525, 25):
            pygame.draw.line(self.window, color, (x, 0), (x, 500), 1)
        for y in range(0, 525, 25):
            pygame.draw.line(self.window, color, (0, y), (500, y), 1) 

    def _draw_text(self, text: str, font, color: tuple[int, int, int], x: int, y: int):
        img = font.render(text, True, color)
        self.window.blit(img, (x, y))

game = SnakeGame()
game.run()
