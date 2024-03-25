import pygame
import os
from gamestate import Handler
import AssetCache

from enemy import EnemyManager
from player import Player
from grid import Grid, EMPTY_SPACE  # Adjust this path as needed
# Start game scene

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.id = "game_scene"
        self.cell_size = 32  # Define the size of each cell in the grid
        
        # Calculate the grid size based on the screen size and cell size
        screen_width, screen_height = screen.get_size()
        grid_width = screen_width // self.cell_size
        grid_height = screen_height // self.cell_size
        
        # Initialize the grid with calculated dimensions
        self.grid = Grid(width=grid_width, height=grid_height)
        self.enemyManager = EnemyManager(self.grid)
        
        # Define the path to your assets
        self.path = os.path.dirname(__file__)
        
        # Load and resize images to fit the cell size
        self.player_image = AssetCache.get_image(os.path.join(self.path, "Assets", "player.png"))
        self.player_image = pygame.transform.scale(self.player_image, (self.cell_size, self.cell_size))
        
        self.enemy_image = AssetCache.get_image(os.path.join(self.path, "Assets", "enemy.png"))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.cell_size, self.cell_size))
        
        self.tree_image = AssetCache.get_image(os.path.join(self.path, "Assets", "tree.png"))
        self.tree_image = pygame.transform.scale(self.tree_image, (self.cell_size, self.cell_size))

        self.stone_image = AssetCache.get_image(os.path.join(self.path, "Assets", "stone.png"))
        self.stone_image = pygame.transform.scale(self.stone_image, (self.cell_size, self.cell_size))

        # Populate the grid with initial objects
        self.populate_grid()

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onMousePress=self.onMousePress,
            onKeyPress=onKeyPress)

    def populate_grid(self):
        # Initialize the player
        self.player = Player(self.grid, 5, 5, self.player_image)

        # Create the objects list for trees and apples
        objects = []

        # Create trees along the top and bottom boundaries
        for x in range(self.grid.width):
            objects.append({"type": "tree", "x": x, "y": 0, "image": self.tree_image, "obstruction": True})
            objects.append({"type": "tree", "x": x, "y": self.grid.height - 1, "image": self.tree_image, "obstruction": True})

        # Create trees along the left and right boundaries
        for y in range(1, self.grid.height):  # Avoiding corners
            objects.append({"type": "tree", "x": 0, "y": y, "image": self.tree_image, "obstruction": True})
            objects.append({"type": "tree", "x": self.grid.width - 1, "y": y, "image": self.tree_image, "obstruction": True})

        # Initialize an empty list to hold all the maze objects
        internal_layout = []

        # Define the maze layout as a list of strings for easy visualization and modification
        # "#" represents a stone, " " represents an open path

        maze_design = [
            "                                       ",
            "  #    #                               ",
            "  # #  #  ##########    ############   ",
            "  # #  #  #             #        # #   ",
            "  # #  #  # #######     #  ####### #   ",
            "  # #  #  #       #      # # #         ",
            "    #     #       #    # # # #         ",
            "  ##########      #### # # # #  #####  ",
            "  #        #                        #  ",
            "  # ###### # ### ###      ##### #####  ",
            "  # #    # # #     #      #         #  ",
            "  # #    #   # ### #      #         #  ",
            "  # #    # # #     #      #         #  ",
            "  # # ## # # ### ###      #         #  ",
            "  # #    # #              #         #  ",
            "  # #    # #              ###########  ",
            "  # #    # #                           ",
            "  # ##  ## #                           ",
            "  #        #                           ",
            "  ####  ############# # # # ########## ",
            "                      # # #            ",
            "                                       "
        ]

        # Convert the maze design into objects
        for y, row in enumerate(maze_design):
            for x, col in enumerate(row):
                if col == "#":
                    # Add a stone tile at the corresponding location
                    internal_layout.append({"type": "stone", "x": x, "y": y, "image": self.stone_image, "obstruction": True})

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])

        # Insert each object into the grid
        for obj in internal_layout:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])


        # Enemy positions
        self.enemyManager.create_enemy(22, 3, self.enemy_image, "d6", 2)
        
    def render_image_at_coordinates(self,image,x,y):
        return self.screen.blit(image, (x * self.cell_size, y * self.cell_size))

    def render(self, gamestate):
        self.screen.fill((34, 139, 34))
        cell_size = 32  # Define the size of each cell in the grid
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

def onKeyPress(gamestate, key, mod, unicode, scancode):
    prevLoc = gamestate.scene.player.position
    moved = False

    if (key == pygame.K_a or key == pygame.K_LEFT):
        moved = gamestate.scene.player.moveLeft()
        

    elif (key == pygame.K_s or key == pygame.K_DOWN):
        moved = gamestate.scene.player.moveDown()

    elif (key == pygame.K_w or key == pygame.K_UP):
        moved = gamestate.scene.player.moveUp()

    elif (key == pygame.K_d or key == pygame.K_RIGHT):
        moved = gamestate.scene.player.moveRight()

    if moved:
        gamestate.scene.enemyManager.enemy_step()