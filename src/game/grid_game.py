import pygame
import os
from gamestate import Gamestate, Handler
import AssetCache
from random import randint, choice
import json
from victory import VictoryScene

from enemy import EnemyManager
from player import Player
from grid import Grid, EMPTY_SPACE  # Adjust this path as needed
from combat import Combat
from game_over import GameOverScene
from itemEffects import ItemEffects
from highscore import Highscores
# Start game scene

from value import *

import util

CELL_SIZE = 32  # Define the size of each cell in the grid
ITEM_IMAGE_SCALE = 0.075

DICE_ROLL_TIME = 0.5
DICE_ROLL_SPEED = 0.05
DICE_STAY_TIME = 1.0

WIN_STRIKE_SCORE = 50
DEFEAT_ENEMY_SCORE = 100

class GameScene:
    def __init__(self, screen, level_filename: str):
        self.screen = screen
        self.id = "game_scene"
        self.combat_manager = Combat()

        self.in_inventory = False
        self.inventory_timer = 1.0

        self.score = 0

        self.in_combat_with = []
        self.cur_combat_enemy = -1
        self.combat_timer = 0.0
        self.player_roll = None
        self.enemy_roll = None
        self.player_rand = 0
        self.enemy_rand = 0
        self.last_rand = -DICE_ROLL_SPEED
        self.selected_item = None

        self.textFont = pygame.font.SysFont("Arial", 35)
        self.subTextFont = pygame.font.SysFont("Arial", 20)
        self.combatFont = pygame.font.SysFont("Arial", CELL_SIZE)

        # Calculate the grid size based on the screen size and cell size
        screen_width, screen_height = screen.get_size()
        grid_width = screen_width // CELL_SIZE
        grid_height = screen_height // CELL_SIZE
        
        # Initialize the grid with calculated dimensions
        self.grid = Grid(width=grid_width, height=grid_height)
        self.enemyManager = EnemyManager(self.grid)
        
        # Define the path to your assets
        self.path = os.path.dirname(__file__)

        # Load and resize images to fit the cell size
        self.player_image = AssetCache.get_image(os.path.join(self.path, "Assets", "Player_base_transparent.png"))
        self.player_image = pygame.transform.scale(self.player_image, (CELL_SIZE, CELL_SIZE))
        
        self.tree_image = AssetCache.get_image(os.path.join(self.path, "Assets", "landslide_level_2.png"))
        self.tree_image = pygame.transform.scale(self.tree_image, (CELL_SIZE, CELL_SIZE))

        self.stone_image = AssetCache.get_image(os.path.join(self.path, "Assets", "stalagmite_level_2.png"))
        self.stone_image = pygame.transform.scale(self.stone_image, (CELL_SIZE, CELL_SIZE))

        self.dice_backdrop = AssetCache.get_image(os.path.join(self.path, "Assets", "dice_icons", "square.png"))
        self.dice_backdrop = pygame.transform.scale(self.dice_backdrop, (CELL_SIZE, CELL_SIZE))

        self.player_run_image = AssetCache.get_image(os.path.join(self.path, "Assets", "Player_run.png"))
        self.player_run_image = pygame.transform.scale(self.player_run_image, (CELL_SIZE, CELL_SIZE))

        self.goal_image = AssetCache.get_image(os.path.join(self.path, "Assets", "RegionMarker.png"))
        self.goal_image = pygame.transform.scale(self.goal_image, (CELL_SIZE, CELL_SIZE))

        self.player_footstep = AssetCache.get_audio("src/game/Assets/footstep_player.wav")
        self.inventory_sound = AssetCache.get_audio("src/game/Assets/inventory.wav")
        self.pickup_sound = AssetCache.get_audio("src/game/Assets/pickup.wav")
        # Populate the grid with initial objects
        self.populate_grid(level_filename)

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onMousePress=self.onMousePress,
            onKeyPress=onKeyPress)

    def populate_grid(self, level_filename: str):
        # Define the objects to populate the grid, now including trees and apples

        # Load level data
        level_file = open(os.path.join(self.path,"Levels",level_filename))
        level_data = json.load(level_file)
        level_file.close()

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
        maze_design = level_data["layout"]

        player_added = False

        # Convert the maze design into objects
        for y, row in enumerate(maze_design):
            for x, col in enumerate(row):
                if col == "#":
                    # Add a stone tile at the corresponding location
                    internal_layout.append({"type": "stone", "x": x, "y": y, "image": self.stone_image, "obstruction": True})
                elif col == "P":
                    if player_added:
                        raise Exception(f"More than 1 player ('P') is in the loaded level '{level_filename}'. The level cannot be loaded.")
                    else:
                        self.player = Player(self.grid, x, y, self.player_image, self.player_run_image)
                        self.player.inventory.add("common")
                        self.player.inventory.add("common")
                        self.player.inventory.add("arrow")
                        player_added = True
                elif col == "G":
                    self.grid.insert(item={
                        "name":"exit",
                        "image":self.goal_image
                    }, x=x, y=y)
                elif col in level_data["enemies"]:
                    die_value = level_data["enemies"][col]["dice"]
                    interval = level_data["enemies"][col]["interval"]
                    enemy_image = AssetCache.get_image(os.path.join(self.path, "Assets", level_data["enemies"][col]["image"]))
                    enemy_image = pygame.transform.scale(enemy_image, (CELL_SIZE, CELL_SIZE))
                    self.enemyManager.create_enemy(x, y, enemy_image, die_value, interval)
                elif col in level_data["items"]:
                    item_image = AssetCache.get_image(os.path.join(self.path, "Assets", level_data["items"][col]["image"]))
                    item_image = pygame.transform.scale(item_image, (CELL_SIZE, CELL_SIZE))
                    self.grid.insert({"type": "item","name": level_data["items"][col]["name"], "obstruction": True, "image": item_image},x,y)
                elif col != ' ':
                    raise Exception(f"Unknown signifier '{col}' in the loaded level '{level_filename}'. The level cannot be loaded.")

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])

        # Insert each object into the grid
        for obj in internal_layout:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])
    
    def render_image_at_coordinates(self,image,x,y):
        return self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

    def render_combat(self, gamestate: Gamestate):
        if (len(self.in_combat_with) > 0 and self.cur_combat_enemy >= 0):
            
            enemy_coords = self.in_combat_with[self.cur_combat_enemy]
            player_x, player_y = list(gamestate.scene.grid.find_object_with_properties({"name": "player"}))[0]

            # draw backdrop above fighters
            self.render_image_at_coordinates(self.dice_backdrop, player_x, player_y - 1)
            self.render_image_at_coordinates(self.dice_backdrop, enemy_coords[0], enemy_coords[1] - 1)

            if (self.combat_timer > DICE_ROLL_TIME):
                # draw final result

                # get color, green for win, red for loss, gray for draw
                player_color = (0, 255, 10) if self.player_roll > self.enemy_roll else (255, 0, 10)
                enemy_color = (0, 255, 10) if self.enemy_roll > self.player_roll else (255, 0, 10)

                if (self.player_roll == self.enemy_roll):
                    player_color = (150, 150, 150)
                    enemy_color = (150, 150, 150)

                # the numbers are drawn "centered" in the box
                width, height = self.combatFont.size(str(self.player_roll))
                player_text = self.combatFont.render(str(self.player_roll), True, player_color)
                self.screen.blit(player_text, (player_x * CELL_SIZE + CELL_SIZE / 2 - width / 2, (player_y - 1) * CELL_SIZE + CELL_SIZE / 2 - height / 2))
            
                width, height = self.combatFont.size(str(self.enemy_roll))
                enemy_text = self.combatFont.render(str(self.enemy_roll), True, enemy_color)
                self.screen.blit(enemy_text, (enemy_coords[0] * CELL_SIZE + CELL_SIZE / 2 - width / 2, (enemy_coords[1] - 1) * CELL_SIZE + CELL_SIZE / 2 - height / 2))

            else:
                # draw dice roll effect

                if (self.combat_timer - self.last_rand >= DICE_ROLL_SPEED):
                    self.last_rand = self.combat_timer

                    player_die = gamestate.scene.player.hitDie
                    enemy_object = gamestate.scene.grid.get_object(enemy_coords[0], enemy_coords[1])
                    enemy_die = enemy_object["hitDie"]

                    self.player_rand = self.combat_manager.roll_die(player_die)
                    self.enemy_rand = self.combat_manager.roll_die(enemy_die)

                width, height = self.combatFont.size(str(self.player_rand))
                player_text = self.combatFont.render(str(self.player_rand), True, (255, 255, 255))
                self.screen.blit(player_text, (player_x * CELL_SIZE + CELL_SIZE / 2 - width / 2, (player_y - 1) * CELL_SIZE + CELL_SIZE / 2 - height / 2))
            
                
                width, height = self.combatFont.size(str(self.enemy_rand))
                enemy_text = self.combatFont.render(str(self.enemy_rand), True, (255, 255, 255))
                self.screen.blit(enemy_text, (enemy_coords[0] * CELL_SIZE + CELL_SIZE / 2 - width / 2, (enemy_coords[1] - 1) * CELL_SIZE + CELL_SIZE / 2 - height / 2))

    def render_backpack(self, gamestate: Gamestate):
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
                #self.player.inventory.items["common"] = 2
                #self.player.inventory.items["arrow"] = 1

                # draw backpack value
                ypos = 0.01 * swidth
                val = value(self.player.inventory, gamestate.items)
                valText = self.textFont.render("Value: " + str(val), True, (255, 255, 255))
                self.screen.blit(valText, (itemPos * swidth, ypos))

                # draw hit die
                hitDieImage = AssetCache.get_image(self.combat_manager.get_icon_path(self.player.hitDie))
                hitDieImage = pygame.transform.scale(hitDieImage, (valText.get_height(), valText.get_height()))
                self.screen.blit(hitDieImage, (itemPos * swidth + valText.get_width() + spacing, ypos + valText.get_height() / 2 - hitDieImage.get_height() / 2))

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

                        color = (255,255,0) if item.identifier == self.selected_item else (255,255,255)

                        # draw title and count
                        self.screen.blit(self.textFont.render(item.name + " (x" + str(count) + ')', True, color), (textX, ypos + spacing))
                        theight = self.textFont.get_height()

                        # draw description
                        self.screen.blit(self.subTextFont.render(item.description, True, color), (textX, ypos + spacing * 2 + theight))

                        # advance to next item
                        y += 1
                    else:
                        print(itemz[0] + " doesn't identify an item")

    def render(self, gamestate: Gamestate):
        self.screen.fill((0, 0, 0))
        
        images_to_render = self.grid.find_object_with_property_type("image")
        for pair in images_to_render:
            ((x,y),image) = pair
            self.render_image_at_coordinates(image,x,y)

        self.render_combat(gamestate)

        self.render_backpack(gamestate)

        pygame.display.flip()

    def update_combat(self, gamestate, dt):
        if (len(self.in_combat_with) > 0):

            self.combat_timer += dt

            # combat with enemy done
            if (self.combat_timer > DICE_STAY_TIME + DICE_ROLL_TIME):

                # kill enemy/player
                if (self.cur_combat_enemy >= 0):
                    enemy_coords = self.in_combat_with[self.cur_combat_enemy]

                    winner = gamestate.scene.combat_manager.outcome(self.player_roll, self.enemy_roll)

                    if winner == 'player': 
                        enemy_object = gamestate.scene.grid.get_object(enemy_coords[0], enemy_coords[1])
                        enemy_die = enemy_object["hitDie"]

                        # Player wins the fight
                        next_enemy_die = gamestate.scene.combat_manager.downgrade_die(enemy_die)
                        print(f"Enemy die reduced to {next_enemy_die}")

                        if next_enemy_die == 'defeated':
                            # Remove the enemy from the board if they are defeated
                            gamestate.scene.grid.remove_at_location(enemy_coords[0], enemy_coords[1])
                            self.score += DEFEAT_ENEMY_SCORE
                        else:
                            # Otherwise, reduce their die
                            enemy_object["hitDie"] = next_enemy_die
                            self.score += WIN_STRIKE_SCORE
                    
                    elif winner == 'enemy':
                        next_player_die = gamestate.scene.combat_manager.downgrade_die(gamestate.scene.player.hitDie)
                        print(f"Player die reduced to {next_player_die}")
                        if next_player_die == 'defeated':
                            highscores = Highscores()  # This should be initialized at the start of the game instead of here if used frequently.
                            highscores.insertScore(gamestate.player_name, self.score)
                            highscores.saveScores()
                            # Return to main menu when the player is defeated
                            game_over_scene = GameOverScene(gamestate.screen)
                            gamestate.pushScene(game_over_scene)
                            return
                        else:
                            # Otherwise, reduce their die
                            gamestate.scene.player.hitDie = next_player_die

                # advance to next player
                self.cur_combat_enemy += 1
                self.combat_timer = 0.0
                self.last_rand = -DICE_ROLL_SPEED
                self.player_roll = None
                self.enemy_roll = None
                    
                # combat with all enemies done
                if (self.cur_combat_enemy >= len(self.in_combat_with)):
                    self.in_combat_with = []
                    return
                    
                # go to next enemy
                # Combat happens here
                player_die = gamestate.scene.player.hitDie

                enemy_coords = self.in_combat_with[self.cur_combat_enemy]
                enemy_object = gamestate.scene.grid.get_object(enemy_coords[0], enemy_coords[1])
                enemy_die = enemy_object["hitDie"]
                print(f"Combat: {player_die} (player) vs {enemy_die} (enemy)")

                # Dice roll
                effects = ItemEffects(gamestate.items, self.player.inventory)
                self.player_roll = int(effects.roll_die(gamestate.scene.combat_manager, player_die))
                self.enemy_roll = gamestate.scene.combat_manager.roll_die(enemy_die)

    def update(self, gamestate, dt):
        # Add logic to update objects in the grid as needed

        # control vfx for backpack fade in/out
        if (self.in_inventory):
            self.inventory_timer = max(self.inventory_timer - dt, 0.0)
        else:
            self.inventory_timer = min(self.inventory_timer + dt, 1.0)

        self.update_combat(gamestate, dt)
    
    def updateWorld(self):
        self.player_footstep.play()
        self.enemyManager.enemy_step()

        self.in_combat_with = []

        enemy_list = self.grid.find_object_with_properties({"name": "enemy"})
        player_x, player_y = list(self.grid.find_object_with_properties({"name": "player"}))[0]
        for enemy_x,enemy_y in enemy_list:
            if self.grid.is_adjacent(player_x, player_y, enemy_x, enemy_y, True):
                self.in_combat_with.append((enemy_x, enemy_y))
                
        if (len(self.in_combat_with) > 0):
            # hacky little way to avoid writing better code
            self.cur_combat_enemy = -1
            self.combat_timer = (DICE_STAY_TIME + DICE_ROLL_TIME) * 2
            self.last_rand = -DICE_ROLL_SPEED

    def onMousePress(self, gamestate, pos, button, touch):
        if (not self.in_inventory):
            # handle item pickups
            x,y = pos
            x = x // CELL_SIZE
            y = y // CELL_SIZE
            player_x, player_y = list(self.grid.find_object_with_properties({"name": "player"}))[0]
            if self.grid.is_inbounds(x,y) and self.grid.is_adjacent(player_x,player_y,x,y):
                obj = self.grid.get_object(x,y)
                if not self.player.inventory.isFull() and obj is not None and obj.get("type",None) == "item": # check that there is an item
                    self.grid.remove_at_location(x,y)
                    self.player.inventory.add(obj["name"])
                    self.pickup_sound.play()
                    self.updateWorld()
                elif not self.player.inventory.isEmpty() and obj is None:
                    # if there's no item, place the selected item (if any)
                    if self.selected_item is None or self.selected_item not in list(self.player.inventory.items.keys()):
                        stuff = list(self.player.inventory.items.keys())
                        if len(stuff) > 0:
                            self.selected_item = stuff[0]
                        else:
                            self.selected_item = None
                    
                    if self.selected_item is not None:
                        item_info = gamestate.items.get(self.selected_item)
                        self.grid.insert({
                            "type":"item",
                            "image":pygame.transform.scale(AssetCache.get_image(item_info.image), (CELL_SIZE, CELL_SIZE)),
                            "name":self.selected_item,
                            "obstruction":True
                        },x,y)
                        self.player.inventory.remove(self.selected_item)
                        self.pickup_sound.play()
                        self.updateWorld()

from Paused_game import PauseScene

def onKeyPress(gamestate, key, mod, unicode, scancode):
    prevLoc = gamestate.scene.player.position
    moved = False

    if (len(gamestate.scene.in_combat_with) != 0):
        # skip combat animations
        add_amount = DICE_STAY_TIME if gamestate.scene.combat_timer >= DICE_ROLL_TIME else DICE_ROLL_TIME - gamestate.scene.combat_timer

        if (key == pygame.K_a or key == pygame.K_LEFT):
            gamestate.scene.combat_timer += add_amount

        elif (key == pygame.K_s or key == pygame.K_DOWN):
            gamestate.scene.combat_timer += add_amount

        elif (key == pygame.K_w or key == pygame.K_UP):
            gamestate.scene.combat_timer += add_amount

        elif (key == pygame.K_d or key == pygame.K_RIGHT):
            gamestate.scene.combat_timer += add_amount

    elif (not gamestate.scene.in_inventory):
        if (key == pygame.K_a or key == pygame.K_LEFT):
            moved = gamestate.scene.player.moveLeft()

        elif (key == pygame.K_s or key == pygame.K_DOWN):
            moved = gamestate.scene.player.moveDown()

        elif (key == pygame.K_w or key == pygame.K_UP):
            moved = gamestate.scene.player.moveUp()

        elif (key == pygame.K_d or key == pygame.K_RIGHT):
            moved = gamestate.scene.player.moveRight()

        if moved == "WIN":
            # player entered the goal tile, level is complete
            score = gamestate.scene.score
            gamestate.popScene()
            gamestate.pushScene(VictoryScene(gamestate.screen,score))
            return
        elif moved:
            gamestate.scene.updateWorld()
    
    else:
        stuff = list(gamestate.scene.player.inventory.items.keys())
        current_index = stuff.index(gamestate.scene.selected_item) if gamestate.scene.selected_item in stuff else -1
        if current_index >= 0:
            if (key == pygame.K_s or key == pygame.K_DOWN):
                current_index += 1
                if current_index >= len(stuff):
                    current_index = 0
            elif (key == pygame.K_w or key == pygame.K_UP):
                current_index -= 1
                if current_index < 0:
                    current_index = len(stuff) - 1
                
            gamestate.scene.selected_item = stuff[current_index]

    if (key == pygame.K_TAB):
        if gamestate.scene.selected_item is None or gamestate.scene.selected_item not in list(gamestate.scene.player.inventory.items.keys()):
            stuff = list(gamestate.scene.player.inventory.items.keys())
            if len(stuff) > 0:
                gamestate.scene.selected_item = stuff[0]
        gamestate.scene.in_inventory = not gamestate.scene.in_inventory
        gamestate.scene.inventory_sound.play()

    if (key == pygame.K_ESCAPE):
         gamestate.pushScene(PauseScene(gamestate.screen))