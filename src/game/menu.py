import pygame
import os
import AssetCache

from gamestate import *

from Buttons import Button
from grid_game import GameScene

ID = "main_menu"

        
class MenuScene:
    def __init__(self, screen):
        self.id = ID

        self.path = os.path.dirname(__file__) + "/"

        self.textFont = pygame.font.SysFont("Arial", 40)

        #this the current background music    
        pygame.mixer.music.load("src/game/Assets/Music/BabaIsYou.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        # Scale factor for the button width
        button_width_scale = 1.8 
        button_height_scale = 1  
        
        screen_center_x = screen.get_width() // 2
        play_button_y = screen.get_height() // 2 - 200
        exit_button_y = screen.get_height() // 2 + 300
        #putting the settings button in the middle of the play and exit buttons
        settings_button_y = screen.get_height() // 2 
        instruct_button_y = screen.get_height() // 2 + 100
        credit_button_y = screen.get_height() // 2 + 200
        Level_selector_y = screen.get_height() // 2 - 120


        # Load and scale the button image
        original_button_image = AssetCache.get_image(self.path + "Assets/button.png")
        button_image_width = int(original_button_image.get_width() * button_width_scale)
        button_image_height = int(original_button_image.get_height() * button_height_scale)
        scaled_button_image = pygame.transform.scale(original_button_image, (button_image_width, button_image_height))

        # Button positions
        self.PlayButton = Button(image=scaled_button_image, pos=(screen_center_x, screen.get_height() // 2 - 200),
                                 text_input="Play", font=self.textFont, base_color="white", hovering_color="blue",
                                 click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.ExitButton = Button(image=scaled_button_image, pos=(screen_center_x, screen.get_height() // 2 + 300),
                                 text_input="Exit", font=self.textFont, base_color="white", hovering_color="blue",
                                 click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.SettingsButton = Button(image=scaled_button_image, pos=(screen_center_x, screen.get_height() // 2),
                                     text_input="Settings", font=self.textFont, base_color="white", hovering_color="blue",
                                     click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.InstructionsButton = Button(image=scaled_button_image, pos=(screen_center_x, screen.get_height() // 2 + 100),
                                         text_input="Instruction", font=self.textFont, base_color="white", hovering_color="blue",
                                         click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.CreditsButton = Button(image=scaled_button_image, pos=(screen_center_x, screen.get_height() // 2 + 200),
                                    text_input="Credits", font=self.textFont, base_color="white", hovering_color="blue",
                                    click_sound=AssetCache.get_audio(self.path + "Assets/button_click.mp3"))

        self.Level_selector = Button(image=scaled_button_image, pos=(screen_center_x, screen.get_height() // 2 - 120),
                                     text_input="Levels", font=self.textFont, base_color="white", hovering_color="blue",
                                     click_sound=AssetCache.get_audio(self.path + "Assets/button_click.mp3"))

        self.buttons = [self.PlayButton, self.ExitButton, self.SettingsButton, self.InstructionsButton, self.CreditsButton, self.Level_selector]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)
    
    def update_elements(self, width: int, height: int):
        pass 

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene
from credits import CreditsScene
from Level_selector import LevelSelectorScene

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.PlayButton.checkForInput(pos)):
        print("Play button clicked")
        state.scene.PlayButton.button_sound()
        pygame.mixer_music.stop()
        state.pushScene(GameScene(state.screen,"level1.json", state))
    elif (state.scene.ExitButton.checkForInput(pos)):
        state.scene.ExitButton.button_sound()
        state.running = False
    elif (state.scene.SettingsButton.checkForInput(pos)):
        state.scene.SettingsButton.button_sound()
        state.pushScene(SettingsScene(state.screen))
    elif (state.scene.InstructionsButton.checkForInput(pos)):
        state.scene.InstructionsButton.button_sound()
        state.pushScene(InstructionsScene(state.screen))
    elif (state.scene.CreditsButton.checkForInput(pos)):
        state.scene.CreditsButton.button_sound()
        state.pushScene(CreditsScene(state.screen))
    elif (state.scene.Level_selector.checkForInput(pos)):
        state.scene.Level_selector.button_sound()
        state.pushScene(LevelSelectorScene(state.screen))

def render(state: Gamestate):

    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)