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
        pygame.mixer.music.load("src/game/Assets/Background_music_menu.wav")
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play(-1)
        
        screen_center_x = screen.get_width() // 2
        play_button_y = screen.get_height() // 2 - 50
        exit_button_y = screen.get_height() // 2 + 150
        #putting the settings button in the middle of the play and exit buttons
        settings_button_y = screen.get_height() // 2 + 50
        instruct_button_y = screen.get_height() - 50
        credit_button_y = screen.get_height() - 130

        self.PlayButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, play_button_y),
                            text_input="Play", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.ExitButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, exit_button_y),
                            text_input="Exit", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        #put a settings button with the button.img. It uses the same fonts and color and hover color
        self.SettingsButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, settings_button_y),
                                text_input="Settings", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.InstructionsButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, instruct_button_y),
                                text_input="How To Play", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.CreditsButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, credit_button_y),
                                text_input="Credits", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio(self.path + "Assets/button_click.mp3"))


        self.buttons = [self.PlayButton, self.ExitButton, self.SettingsButton, self.InstructionsButton, self.CreditsButton]
        

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

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.PlayButton.checkForInput(pos)):
        print("Play button clicked")
        state.scene.PlayButton.button_sound()
        pygame.mixer_music.stop()
        state.pushScene(GameScene(state.screen))
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

def render(state: Gamestate):

    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)