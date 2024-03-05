import pygame
import os
from gamestate import Handler
import AssetCache

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
        self.player_image = AssetCache.get_image(os.path.join(self.path, "Assets", "player.png"))
        self.player_image = pygame.transform.scale(self.player_image, (self.cell_size, self.cell_size))
        
        self.enemy_image = AssetCache.get_image(os.path.join(self.path, "Assets", "enemy.png"))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.cell_size, self.cell_size))
        
        self.tree_image = AssetCache.get_image(os.path.join(self.path, "Assets", "tree.png"))
        self.tree_image = pygame.transform.scale(self.tree_image, (self.cell_size, self.cell_size))

        self.apple_image = AssetCache.get_image(os.path.join(self.path, "Assets", "apple.png"))
        self.apple_image = pygame.transform.scale(self.apple_image, (self.cell_size, self.cell_size))

        # Populate the grid with initial objects
        self.populate_grid()

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onMousePress=self.onMousePress,)

    def populate_grid(self):
        # Define the objects to populate the grid, now including trees and apples
        objects = [
            {"type": "player", "x": 5, "y": 5,"image":self.player_image},
            {"type": "enemy", "x": 2, "y": 3,"image":self.enemy_image},
            {"type": "tree", "x": 1, "y": 1,"image":self.tree_image},
            {"type": "tree", "x": 8, "y": 1,"image":self.tree_image},
            {"type": "apple", "x": 3, "y": 6,"image":self.apple_image},
            {"type": "apple", "x": 7, "y": 2,"image":self.apple_image},
            {"type": "apple", "x": 4, "y": 4,"image":self.apple_image},
            # Add more objects as needed
        ]

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])
    
    def render_image_at_coordinates(self,image,x,y):
        return self.screen.blit(image, (x * self.cell_size, y * self.cell_size))

    def render(self, gamestate):
        self.screen.fill((0, 0, 0))
        cell_size = 64  # Define the size of each cell in the grid
        images_to_render = self.grid.find_object_with_property_type("image")
        for pair in images_to_render:
            ((x,y),image) = pair
            self.render_image_at_coordinates(image,x,y)

        pygame.display.flip()

    def update(self, gamestate, dt):
        # Add logic to update objects in the grid as needed
        pass

    def onMousePress(self, gamestate, pos, button, touch):
        # Implement interactions based on mouse press
        pass
