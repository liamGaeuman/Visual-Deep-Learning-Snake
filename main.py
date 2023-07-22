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

from game_controller import GameController


def main():
    game_controller = GameController()
    game_controller.run()


if __name__ == '__main__':
    main()
