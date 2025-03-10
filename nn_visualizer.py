import pygame
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class VisualNN:
    POS_WEIGHT_CLR = (252, 3, 211)
    NEG_WEIGHT_CLR = (3, 252, 244)
    DEFAULT_NEUR_CLR = (77, 2, 163)
    DEFAULT_NEUR_B_CLR = (200, 200, 200)
    WHITE = (255,255,255)
    DIM = (501, 751)

    def __init__(self, architecture: list, state_dict: dict = None):

        self.architecture = architecture
        self.model = SequentialNetwork(self.architecture)

        self.canvas = pygame.Surface(self.DIM)
        self.all_sprites = pygame.sprite.Group()

        self.activations = [[0]*i for i in self.architecture]  
        self.neuron_sprites = [[Neuron() for _ in range(i)] for i in self.architecture]
        self.all_sprites.add(*[neuron for layer in self.neuron_sprites for neuron in layer])

        if state_dict:
            self.change_state(state_dict) # will call _draw_network
        else:
            self._draw_network()

        self.remaining_animation_steps = 0

    def change_state(self, state_dict: dict):               
        self.model.load_state_dict(state_dict)
        self._draw_network()

    def get_model_state(self):    
        return self.model.state_dict()

    def forward(self, x):  
        x = torch.tensor(x, dtype=torch.float)    
        self.activations = self.model.forward(x)
        self.remaining_animation_steps = len(self.architecture) + 1
        return self.activations[-1] 


    def is_forward_complete(self) -> bool:
        if self.remaining_animation_steps <= 0: # number of neuron columns to pulse
            return True
        return False


    def render_frame(self):
        self._display_activation_step()
        self.all_sprites.draw(self.canvas)
        return self.canvas


    def _display_activation_step(self):

        cur_col_index = -1 * (self.remaining_animation_steps - 1) 

        # revert last layer of neurons
        if cur_col_index == 0:
            for i in range(self.architecture[cur_col_index-1]):
                self.neuron_sprites[-1][i].set_fill_color(self.DEFAULT_NEUR_CLR)
                self.neuron_sprites[-1][i].set_border_color(self.DEFAULT_NEUR_B_CLR)
        else:
            # get max weight value
            max_weight = max(max(abs(x) for x in row) for row in self.activations)
            # update current neuron column of forward pass 
            for i in range(self.architecture[cur_col_index]):
                activation = self.activations[cur_col_index][i]
                self.neuron_sprites[cur_col_index ][i].set_activation_color(activation,self.DEFAULT_NEUR_CLR,self.WHITE, max_val=max_weight)
                self.neuron_sprites[cur_col_index ][i].set_border_color(self.WHITE)

            # revert previous neuorns to original form
            if cur_col_index + len(self.architecture) > 0:
                for i in range(self.architecture[cur_col_index-1]):
                    self.neuron_sprites[cur_col_index-1][i].set_fill_color(self.DEFAULT_NEUR_CLR)
                    self.neuron_sprites[cur_col_index-1][i].set_border_color(self.DEFAULT_NEUR_B_CLR)

        self.remaining_animation_steps -= 1

    def _draw_network(self):

        weight_matrices = [param for name, param in self.model.state_dict().items() if "weight" in name]

        self.canvas.fill((0, 0, 0))

        WIDTH = 120
        HEIGHT = 60
        START_X = 50
        START_Y = 50

        mid_height = max(self.architecture) * HEIGHT / 2

        for i in range(len(self.architecture)):
            x = WIDTH * i + START_X
            y = mid_height - (self.architecture[i] * HEIGHT / 2) + START_Y

            for j in range(self.architecture[i]):
                
                # sub routine to draw lines 
                if i < len(self.architecture)-1:
                    for k in range(self.architecture[i+1]):

                        max_abs_weight = weight_matrices[i].abs().max().item() if weight_matrices[i].numel() > 0 else 1.0
                        weight = weight_matrices[i][k][j].item()
                        fraction = abs(weight) / max_abs_weight if max_abs_weight != 0 else 0
                        min_thickness, max_thickness = 1, 4

                        thickness = int(min_thickness + (max_thickness - min_thickness) * fraction)
                        color = self.POS_WEIGHT_CLR if weight > 0 else self.NEG_WEIGHT_CLR

                        pygame.draw.line(
                            self.canvas, 
                            color,  
                            (x,y), 
                            (x+WIDTH, (mid_height - (self.architecture[i+1] * HEIGHT / 2) + START_Y) + k * HEIGHT),
                            thickness
                        )

                # place a neuron:
                self.neuron_sprites[i][j].set_position(x,y)
                self.neuron_sprites[i][j].set_fill_color(self.DEFAULT_NEUR_CLR)
                self.neuron_sprites[i][j].set_border_color(self.DEFAULT_NEUR_B_CLR)
                y += HEIGHT


class Neuron(pygame.sprite.Sprite):
    def __init__(
        self,
        x=0,
        y=0,
        radius=14,
        fill_color=(0,0,0),   
        border_color=(0,0,0), 
        border_thickness=2
    ):
        super().__init__()
        self.x, self.y = x, y
        self.radius = radius
        
        # Colors
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        
        self.update_image()

    def update_image(self):
        size = self.radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.border_thickness > 0:
            pygame.draw.circle(
                self.image,
                self.border_color,
                (self.radius, self.radius),
                self.radius
            )
            pygame.draw.circle(
                self.image,
                self.fill_color,
                (self.radius, self.radius),
                self.radius - self.border_thickness
            )
        else:
            pygame.draw.circle(
                self.image,
                self.fill_color,
                (self.radius, self.radius),
                self.radius
            )
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_position(self, x, y):
        self.x, self.y = x, y
        self.rect.center = (x, y)

    def set_fill_color(self, color):
        self.fill_color = color
        self.update_image()

    def set_border_color(self, color):
        self.border_color = color
        self.update_image()

    def set_activation_color(self, activation, color_low, color_high, min_val=0.0, max_val=1.0):
        activation = max(min(activation, max_val), min_val)
        fraction = (activation - min_val) / (max_val - min_val) if max_val != min_val else 0

        #linearly interpolate yo!!!!!!!
        r = int(color_low[0] + (color_high[0] - color_low[0]) * fraction)
        g = int(color_low[1] + (color_high[1] - color_low[1]) * fraction)
        b = int(color_low[2] + (color_high[2] - color_low[2]) * fraction)

        self.fill_color = (r, g, b)
        self.update_image()


class SequentialNetwork(nn.Module):
    def __init__(self, architecture):
        super(SequentialNetwork, self).__init__()
        self.layers = nn.ModuleList([
            nn.Linear(in_features, out_features) 
            for in_features, out_features in zip(architecture[:-1], architecture[1:])
        ])
        self.activation = nn.ReLU()  

    def forward(self, x):
        all_activations = []
        all_activations.append(x.view(-1).tolist()) 

        for i, layer in enumerate(self.layers):
            x = layer(x)  
            if i < len(self.layers) - 1:  
                x = self.activation(x)
            all_activations.append(x.view(-1).tolist())  
        
        return all_activations