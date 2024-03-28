import pygame
import os
from gamestate import Gamestate, Handler
import AssetCache
from random import randint, choice

from enemy import EnemyManager
from player import Player
from grid import Grid, EMPTY_SPACE  # Adjust this path as needed
from combat import Combat
# Start game scene

from value import *

import util

ITEM_IMAGE_SCALE = 0.075

class level2Scene:
    def __init__(self, screen):
        self.screen = screen
        self.id = "game_scene"
        self.cell_size = 32  # Define the size of each cell in the grid
        self.combat_manager = Combat()

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
        self.player_image = AssetCache.get_image(os.path.join(self.path, "Assets", "Player_base_transparent.png"))
        self.player_image = pygame.transform.scale(self.player_image, (self.cell_size, self.cell_size))
        
        self.enemy_image = AssetCache.get_image(os.path.join(self.path, "Assets", "enemy_level_2.png"))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.cell_size, self.cell_size))
        
        self.tree_image = AssetCache.get_image(os.path.join(self.path, "Assets", "landslide_level_2.png"))
        self.tree_image = pygame.transform.scale(self.tree_image, (self.cell_size, self.cell_size))

        self.stone_image = AssetCache.get_image(os.path.join(self.path, "Assets", "stalagmite_level_2.png"))
        self.stone_image = pygame.transform.scale(self.stone_image, (self.cell_size, self.cell_size))

        self.player_run_image = AssetCache.get_image(os.path.join(self.path, "Assets", "Player_run.png"))
        self.player_run_image = pygame.transform.scale(self.player_run_image, (self.cell_size, self.cell_size))


        self.player_footstep = AssetCache.get_audio("src/game/Assets/level_2_foot_sound.mp3")
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

        new_maze_design = [
            "########################################",
            "##                          #         ##",
            "## ### ##### ##### ###### ### ### ### ##",
            "##        #     #    #  #     # # #   ##",
            "##       ### # ### #### # # # ### ### ##",
            "##       # # # #      # #   #     #   ##",
            "## ### # # # # ## ### # # # ####### ###",
            "##     #   # #      # # #         #   ##",
            "###### ### # ###### # # # ####### ### ##",
            "##   # #   #      # #     #     # #   ##",
            "## # ### # ###### # ##  ####### # #####",
            "## #         #                  #     ##",
            "## ####### ### ###   ####  ######### ##",
            "##               #   #       #       ##",
            "#### ##### ####### ### ##### # ##### ##",
            "##     #       #     # #       #     ##",
            "## ### ### ### ##### # # # ### #######",
            "## #     # # # #     #   # # #       ##",
            "## ##### # # # # ##### ### # ####### ##",
            "##       #   # #       #               ",
            "########################################"
        ]

        # Convert the maze design into objects
        for y, row in enumerate(new_maze_design):
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

        for i in range(5):
            while not self.enemyManager.create_enemy(
                    randint(0,self.grid.width-1),
                    randint(0,self.grid.height-1),
                    self.enemy_image,
                    choice(self.combat_manager.upgrade_path),
                    randint(1,5)):
                pass
    
    def render_image_at_coordinates(self,image,x,y):
        return self.screen.blit(image, (x * self.cell_size, y * self.cell_size))

    def render(self, gamestate: Gamestate):
        self.screen.fill((0, 0, 0))


        cell_size = 32  # Define the size of each cell in the grid
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

            enemy_list = gamestate.scene.grid.find_object_with_properties({"name":"enemy"})
            player_x,player_y = list(gamestate.scene.grid.find_object_with_properties({"name":"player"}))[0]
            for enemy_x,enemy_y in enemy_list:
                if gamestate.scene.grid.is_adjacent(player_x,player_y,enemy_x,enemy_y,True):
                    # Combat happens here
                    player_die = gamestate.scene.player.hitDie

                    enemy_object = gamestate.scene.grid.get_object(enemy_x,enemy_y)
                    enemy_die = enemy_object["hitDie"]
                    print(f"Combat: {player_die} (player) vs {enemy_die} (enemy)")
                    
                    # Dice roll
                    winner = gamestate.scene.combat_manager.combat_outcome(player_die, enemy_die)
                    print(f"Winner is {winner}")
                    if winner == 'player':
                        # Player wins the fight
                        next_enemy_die = gamestate.scene.combat_manager.downgrade_die(enemy_die)
                        print(f"Enemy die reduced to {next_enemy_die}")
                        if next_enemy_die == 'defeated':
                            # Remove the enemy from the board if they are defeated
                            gamestate.scene.grid.remove_at_location(enemy_x,enemy_y)
                        else:
                            # Otherwise, reduce their die
                            enemy_object["hitDie"] = next_enemy_die
                    elif winner == 'enemy':
                        next_player_die = gamestate.scene.combat_manager.downgrade_die(player_die)
                        print(f"Player die reduced to {next_player_die}")
                        if next_player_die == 'defeated':
                            # Return to main menu when the player is defeated
                            gamestate.popScene()
                            break
                        else:
                            # Otherwise, reduce their die
                            gamestate.scene.player.hitDie = next_player_die

    if (key == pygame.K_TAB):
        gamestate.scene.in_inventory = not gamestate.scene.in_inventory
        gamestate.scene.inventory_sound.play()

    if (key == pygame.K_ESCAPE):
         gamestate.pushScene(PauseScene(gamestate.screen))