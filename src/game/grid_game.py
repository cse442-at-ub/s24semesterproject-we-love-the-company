import pygame
import os
from Buttons import Button
from gamestate import *


class GridScene:
    def __init__(self, screen):
        self.id = "grid"
        self.screen = screen
        self.path = os.path.dirname(__file__) + "/"  # Ensure this line is present

        self.screen_width, self.screen_height = screen.get_size()
        
        # Load and scale the background image to fill the screen
        self.background_image = pygame.image.load(self.path + "Assets/grid.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        # Define the grid size
        self.cell_size = 20  # Or whatever size you intended

        self.grid_width = 100  # Number of cells horizontally
        self.grid_height = 100  # Number of cells vertically
        
        # Calculate cell size based on the image size
        self.cell_size_x = self.screen_width // self.grid_width
        self.cell_size_y = self.screen_height // self.grid_height

        self.exit_button = Button(image=pygame.image.load(self.path + "Assets/button.png"), 
                          pos=(50, screen.get_height() - 50),
                          text_input="EXIT", 
                          font=pygame.font.SysFont("Arial", 40), 
                          base_color="white", 
                          hovering_color="blue", 
                          click_sound=pygame.mixer.Sound(self.path + "Assets/button_click.mp3"))

    def render(self, state):
        # Draw the background image to fill the entire screen
        self.screen.blit(self.background_image, (0, 0))
        
        # Set the color for the grid lines
        grid_color = (0, 255, 0)  # Bright green, for example

        # Draw the grid on top of the background image
        for y in range(self.grid_height + 1):  # Adjusted to include the border line
            for x in range(self.grid_width + 1):  # Adjusted to include the border line
                # Draw vertical lines
                pygame.draw.line(self.screen, grid_color, (x * self.cell_size_x, 0), (x * self.cell_size_x, self.screen_height))
                # Draw horizontal lines
                pygame.draw.line(self.screen, grid_color, (0, y * self.cell_size_y), (self.screen_width, y * self.cell_size_y))
        
        # Draw the exit button
        self.exit_button.update(self.screen)

    def handle_events(self, state, pos, button, touch):
        if self.exit_button.checkForInput(pos):
            self.exit_button.button_sound()  # Assuming your Button class has this method
            state.popScene()

    def initHandlers(self, state):
        state.handlers[self.id] = Handler(onRender=self.render, onUpdate=doNothing, onMousePress=self.handle_events)