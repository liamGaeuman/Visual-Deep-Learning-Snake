from nn_visualizer import VisualNN
import pygame
import random

def main():
    x = [12,8,8,4]

    visualizer = VisualNN(x)

    pygame.init()
    window = pygame.display.set_mode((501,751))

    output = None

    while True:

        pygame.time.delay(200)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

        if(visualizer.is_forward_complete()):
            print(output) #use this to take game step
            input = [random.randint(-10,10) for i in range(x[0])]
            output = max(visualizer.forward(input))
            

        window.fill((0, 0, 0))
        window.blit(visualizer.render_frame(), (0, 0))

        pygame.display.update()

main()

