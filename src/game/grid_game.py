import pygame
import os
from gamestate import Handler
from Paused_game import PauseScene

from grid import Grid, EMPTY_SPACE  # Adjust this path as needed
# Start game scene

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.id = "game_scene"
        self.cell_size = 64  # Define the size of each cell in the grid
        
        # Calculate the grid size based on the screen size and cell size
        screen_width, screen_height = screen.get_size()
        grid_width = screen_width // self.cell_size
        grid_height = screen_height // self.cell_size
        
        # Initialize the grid with calculated dimensions
        self.grid = Grid(width=grid_width, height=grid_height)
        
        # Define the path to your assets
        self.path = os.path.dirname(__file__)
        
        # Load and resize images to fit the cell size
        self.player_image = pygame.image.load(os.path.join(self.path, "Assets", "player.png"))
        self.player_image = pygame.transform.scale(self.player_image, (self.cell_size, self.cell_size))
        
        self.enemy_image = pygame.image.load(os.path.join(self.path, "Assets", "enemy.png"))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.cell_size, self.cell_size))
        
        self.tree_image = pygame.image.load(os.path.join(self.path, "Assets", "tree.png"))
        self.tree_image = pygame.transform.scale(self.tree_image, (self.cell_size, self.cell_size))

        self.apple_image = pygame.image.load(os.path.join(self.path, "Assets", "apple.png"))
        self.apple_image = pygame.transform.scale(self.apple_image, (self.cell_size, self.cell_size))

        # Populate the grid with initial objects
        self.populate_grid()

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onMousePress=self.onMousePress)
    def update_elements(self, width: int, height: int):
        pass
    

    def onKeyPress(self, gamestate, key, mod, unicode, scancode):
        if key == pygame.K_ESCAPE:
            # Push the Pause Menu scene onto the stack
            gamestate.pushScene(PauseScene(gamestate.screen))

    def populate_grid(self):
        # Define the objects to populate the grid, now including trees and apples
        objects = [
            {"type": "player", "x": 5, "y": 5},
            {"type": "enemy", "x": 2, "y": 3},
            {"type": "tree", "x": 1, "y": 1},
            {"type": "tree", "x": 8, "y": 1},
            {"type": "apple", "x": 3, "y": 6},
            {"type": "apple", "x": 7, "y": 2},
            {"type": "apple", "x": 4, "y": 4},
            # Add more objects as needed
        ]

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])

    def render(self, gamestate):
        self.screen.fill((0, 0, 0))
        cell_size = 64  # Define the size of each cell in the grid
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                obj = self.grid.get_object(x, y)
                if obj is not None:
                    # Adjust rendering for new object types
                    if obj["type"] == "player":
                        self.screen.blit(self.player_image, (x * self.cell_size, y * self.cell_size))
                    elif obj["type"] == "enemy":
                        self.screen.blit(self.enemy_image, (x * self.cell_size, y * self.cell_size))
                    elif obj["type"] == "tree":
                        self.screen.blit(self.tree_image, (x * self.cell_size, y * self.cell_size))
                    elif obj["type"] == "apple":
                        self.screen.blit(self.apple_image, (x * self.cell_size, y * self.cell_size))
                else:
                    # Draw grid lines for empty cells
                    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw empty cell borders

        pygame.display.flip()

    def update(self, gamestate, dt):
        # Add logic to update objects in the grid as needed
        pass

    def onMousePress(self, gamestate, pos, button, touch):
        # Implement interactions based on mouse press
        pass
