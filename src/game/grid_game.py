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
        self.cell_size = 64  # Define the size of each cell in the grid
        
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

        self.apple_image = AssetCache.get_image(os.path.join(self.path, "Assets", "apple.png"))
        self.apple_image = pygame.transform.scale(self.apple_image, (self.cell_size, self.cell_size))

        # Populate the grid with initial objects
        self.populate_grid()

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onMousePress=self.onMousePress,
            onKeyPress=onKeyPress)

    def populate_grid(self):
        # Define the objects to populate the grid, now including trees and apples

        self.player = Player(self.grid, 5, 5, self.player_image)

        # Mike's note: including the coordinates in the object data is redundant
        # The grid itself already keeps track of that
        # I know this was done for ease of inserting objects for testing
        # But in future (when making levels) there should be a different way of doing this
        objects = [
            #{"type": "enemy", "x": 2, "y": 3,"image":self.enemy_image,"obstruction":True},
            {"type": "tree", "x": 1, "y": 0,"image":self.tree_image,"obstruction":True},
            {"type": "tree", "x": 8, "y": 0,"image":self.tree_image,"obstruction":True},
            {"type": "apple", "x": 3, "y": 9,"image":self.apple_image,"obstruction":True},
            {"type": "apple", "x": 14, "y": 4,"image":self.apple_image,"obstruction":True},
            {"type": "apple", "x": 4, "y": 4,"image":self.apple_image,"obstruction":True},
            # Add more objects as needed
        ]

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])
        
        self.enemyManager.create_enemy(2,3,self.enemy_image,"d6",2)
    
    def render_image_at_coordinates(self,image,x,y):
        return self.screen.blit(image, (x * self.cell_size, y * self.cell_size))

    def render(self, gamestate):
        self.screen.fill((0, 0, 0))
        cell_size = 64  # Define the size of each cell in the grid
        level2_image = AssetCache.get_image(os.path.join(self.path, "Assets", "level2.png"))
        level2_image = pygame.transform.scale(level2_image, self.screen.get_size())
        self.screen.blit(level2_image, (0, 0))
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
        pos = pygame.mouse.get_pos()
        button = pygame.mouse.get_pressed()

        if any(button): 
           pos_x = pos[0]
           pos_y = pos[1]
           pos_player_x = self.player.position[0]
           pos_player_y = self.player.position[1]
           
           if pos_x<320 and pos_x>260 and pos_y<320 and pos_y>260 and pos_player_x >=3 and pos_player_x<=5 and pos_player_y >=3 and pos_player_y<=5 :
               self.grid.remove_at_location(4,4)

           if pos_x<252 and pos_x>199 and pos_y<631 and pos_y>586 and pos_player_x >=2 and pos_player_x<=4 and pos_player_y >=8 and pos_player_y<=10 :
               self.grid.remove_at_location(3,9)

           if pos_x<959 and pos_x>895 and pos_y<320 and pos_y>260 and pos_player_y >=3 and pos_player_y<=5 and pos_player_x >=13 and pos_player_x<=15 :
               self.grid.remove_at_location(14,4)
        
        

def onKeyPress(gamestate, key, mod, unicode, scancode):
    prevLoc = gamestate.scene.player.position
    moved = False

    if (key == pygame.K_TAB):  
        backpack_image = AssetCache.get_image(os.path.join(gamestate.scene.path, "Assets", "backpack.png"))
        backpack_image = pygame.transform.scale(backpack_image, gamestate.scene.screen.get_size())
        gamestate.scene.screen.blit(backpack_image, (0, 0))
        pygame.display.flip()

    if (key == pygame.K_TAB):  
        backpack_image = AssetCache.get_image(os.path.join(gamestate.scene.path, "Assets", "backpack.png"))
        backpack_image = pygame.transform.scale(backpack_image, gamestate.scene.screen.get_size())
        gamestate.scene.screen.blit(backpack_image, (0, 0))
        pygame.display.flip()

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
