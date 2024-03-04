import pygame
<<<<<<< Updated upstream
import os
from Buttons import Button
from gamestate import *
=======
from gamestate import Handler
from grid import Grid, EMPTY_SPACE
>>>>>>> Stashed changes


class GridScene:
    def __init__(self, screen):
        self.id = "grid"
        self.screen = screen
<<<<<<< Updated upstream
        self.path = os.path.dirname(__file__) + "/"  # Ensure this line is present

        self.screen_width, self.screen_height = screen.get_size()
        
        # Load and scale the background image to fill the screen
        self.background_image = pygame.image.load(self.path + "Assets/grid.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        # Define the grid size
        self.cell_size = 20  # Or whatever size you intended
=======
        self.id = "game_scene"
        screen_width, screen_height = screen.get_size()
        self.cell_size = 64  # size of each cell in the grid
        grid_width, grid_height = screen_width // self.cell_size, screen_height // self.cell_size
        self.grid = Grid(width=grid_width, height=grid_height)

        # Populate the grid with initial objects without using sprites
        self.populate_grid()
>>>>>>> Stashed changes

        self.grid_width = 100  # Number of cells horizontally
        self.grid_height = 100  # Number of cells vertically
        
        # Calculate cell size based on the image size
        self.cell_size_x = self.screen_width // self.grid_width
        self.cell_size_y = self.screen_height // self.grid_height

<<<<<<< Updated upstream
        self.exit_button = Button(image=pygame.image.load(self.path + "Assets/button.png"), 
                          pos=(50, screen.get_height() - 50),
                          text_input="EXIT", 
                          font=pygame.font.SysFont("Arial", 40), 
                          base_color="white", 
                          hovering_color="blue", 
                          click_sound=pygame.mixer.Sound(self.path + "Assets/button_click.mp3"))
=======
    def populate_grid(self):
        # Define the objects to populate the grid
        objects = [
            {"type": "player", "x": 5, "y": 5},
            {"type": "enemy", "x": 2, "y": 3},
            # Add more objects as needed
        ]
>>>>>>> Stashed changes

    def render(self, state):
        # Draw the background image to fill the entire screen
        self.screen.blit(self.background_image, (0, 0))
        
        # Set the color for the grid lines
        grid_color = (0, 255, 0)  # Bright green, for example

<<<<<<< Updated upstream
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
=======
    def render(self, gamestate):
        self.screen.fill((0, 0, 0))
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                obj = self.grid.get_object(x, y)
                if obj is not None:
                    if obj["type"] == "player":
                        color = (0, 255, 0)  # Green for player
                    elif obj["type"] == "enemy":
                        color = (255, 0, 0)  # Red for enemy
                    pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        # Draw white grid lines
        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (self.screen.get_width(), y))

        pygame.display.flip()

    def update(self, gamestate, dt):
        # Update logic goes here
        pass

    def onMousePress(self, gamestate, pos, button, touch):
        # Mouse press logic goes here
        pass
>>>>>>> Stashed changes
