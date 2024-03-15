import pygame
import os
from gamestate import Gamestate, Handler
import AssetCache

from enemy import EnemyManager
from player import Player
from grid import Grid, EMPTY_SPACE  # Adjust this path as needed
# Start game scene

from value import *

import util

ITEM_IMAGE_SCALE = 0.075

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.id = "game_scene"
        self.cell_size = 64  # Define the size of each cell in the grid

        self.in_inventory = False
        self.inventory_timer = 1.0

        self.textFont = pygame.font.SysFont("Arial", 35)
        self.subTextFont = pygame.font.SysFont("Arial", 20)

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

        self.player_footstep = AssetCache.get_audio("src/game/Assets/footstep_player.wav")
        self.inventory_sound = AssetCache.get_audio("src/game/Assets/inventory.wav")
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
            {"type": "tree", "x": 1, "y": 1,"image":self.tree_image,"obstruction":True},
            {"type": "tree", "x": 8, "y": 1,"image":self.tree_image,"obstruction":True},
            {"type": "apple", "x": 3, "y": 6,"image":self.apple_image,"obstruction":True},
            {"type": "apple", "x": 7, "y": 2,"image":self.apple_image,"obstruction":True},
            {"type": "apple", "x": 4, "y": 4,"image":self.apple_image,"obstruction":True},
            # Add more objects as needed
        ]

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])
        
        self.enemyManager.create_enemy(2,3,self.enemy_image,"d6",2)
    
    def render_image_at_coordinates(self,image,x,y):
        return self.screen.blit(image, (x * self.cell_size, y * self.cell_size))

    def render(self, gamestate: Gamestate):
        self.screen.fill((0, 0, 0))
        cell_size = 64  # Define the size of each cell in the grid
        images_to_render = self.grid.find_object_with_property_type("image")
        for pair in images_to_render:
            ((x,y),image) = pair
            self.render_image_at_coordinates(image,x,y)

        if (self.inventory_timer < 1.0): # culling for if inventory open

            # get x position of backpack
            xposR = util.lerp(0.6, 1.0, self.inventory_timer * self.inventory_timer)
            swidth = self.screen.get_width()

            # draw backpack background
            pygame.draw.rect(self.screen, (25, 30, 40), (xposR * swidth, 0, (1.1 - xposR) * swidth, self.screen.get_height()))

            # draw items in backpack
            itemPos = xposR + 0.025
            if (itemPos < 1.0): # culling
                y = 0
                img_size = swidth * ITEM_IMAGE_SCALE
                spacing = img_size * 0.1

                # CHANGE THIS LATER!!!!!
                # for testing purposes
                self.player.inventory.items["common"] = 2
                self.player.inventory.items["arrow"] = 1

                # draw backpack value
                ypos = 0.01 * swidth
                val = value(self.player.inventory, gamestate.items)
                self.screen.blit(self.textFont.render("Value: " + str(val), True, (255, 255, 255)), (itemPos * swidth, ypos))

                # iterate over player inventory
                for itemz in self.player.inventory.items.items():
                    if itemz[0] in gamestate.items.dict:
                        # calculate y positioning
                        ypos = y * (img_size + spacing) + 0.05 * swidth

                        count = itemz[1]
                        item = gamestate.items.get(itemz[0])

                        # scale and get image
                        img = pygame.transform.scale(AssetCache.get_image(item.image), (img_size, img_size))
                        
                        self.screen.blit(img, (itemPos * swidth, ypos, img_size, img_size))

                        # calculate where to put the text
                        textX = itemPos * swidth + img_size + spacing

                        # draw title and count
                        self.screen.blit(self.textFont.render(item.name + " (x" + str(count) + ')', True, (255, 255, 255)), (textX, ypos + spacing))
                        theight = self.textFont.get_height()

                        # draw description
                        self.screen.blit(self.subTextFont.render(item.description, True, (255, 255, 255)), (textX, ypos + spacing * 2 + theight))

                        # advance to next item
                        y += 1
                    else:
                        print(itemz[0] + " doesn't identify an item")

        pygame.display.flip()

    def update(self, gamestate, dt):
        # Add logic to update objects in the grid as needed

        # control vfx for backpack fade in/out
        if (self.in_inventory):
            self.inventory_timer = max(self.inventory_timer - dt, 0.0)
        else:
            self.inventory_timer = min(self.inventory_timer + dt, 1.0)

        pass

    def onMousePress(self, gamestate, pos, button, touch):
        # Implement interactions based on mouse press
        pass

from Paused_game import PauseScene

def onKeyPress(gamestate, key, mod, unicode, scancode):
    prevLoc = gamestate.scene.player.position
    moved = False
    if (not gamestate.scene.in_inventory):
        if (key == pygame.K_a or key == pygame.K_LEFT):
            moved = gamestate.scene.player.moveLeft()


        elif (key == pygame.K_s or key == pygame.K_DOWN):
            moved = gamestate.scene.player.moveDown()

        elif (key == pygame.K_w or key == pygame.K_UP):
            moved = gamestate.scene.player.moveUp()

        elif (key == pygame.K_d or key == pygame.K_RIGHT):
            moved = gamestate.scene.player.moveRight()


        if moved:
            gamestate.scene.player_footstep.play()
            gamestate.scene.enemyManager.enemy_step()
            

    if (key == pygame.K_TAB):
        gamestate.scene.in_inventory = not gamestate.scene.in_inventory
        gamestate.scene.inventory_sound.play()

    if (key == pygame.K_ESCAPE):
         gamestate.pushScene(PauseScene(gamestate.screen))