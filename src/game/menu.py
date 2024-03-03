import pygame
import os

from gamestate import *
import game

from Buttons import Button

from gamestate import *

global_audio_pack = game.audio_pack
global_audio_control = game.audio_control
global_button_sound_que = game.button_sound_que

ID = "main_menu"

class MenuScene:
    def __init__(self, screen):
        self.id = ID

        self.path = os.path.dirname(__file__) + "/"

        self.textFont = pygame.font.SysFont("Arial", 40)

        #this the current background music   
        
        global_audio_pack
        global_audio_control

        screen_center_x = screen.get_width() // 2
        play_button_y = screen.get_height() // 2 - 50
        exit_button_y = screen.get_height() // 2 + 150
        #putting the settings button in the middle of the play and exit buttons
        settings_button_y = screen.get_height() // 2 + 50
        instruct_button_y = screen.get_height() - 50

         # the slowest thing you could possibly do pt2
        self.PlayButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, play_button_y),
                            text_input="Play", font=self.textFont, base_color="white", hovering_color="blue", click_sound = global_button_sound_que)

        self.ExitButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, exit_button_y),
                            text_input="Exit", font=self.textFont, base_color="white", hovering_color="blue", click_sound= global_button_sound_que)
        
        #put a settings button with the button.img. It uses the same fonts and color and hover color
        self.SettingsButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, settings_button_y),
                                text_input="Settings", font=self.textFont, base_color="white", hovering_color="blue", click_sound= global_button_sound_que)

        self.InstructionsButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, instruct_button_y),
                                text_input="How To Play", font=self.textFont, base_color="white", hovering_color="blue", click_sound= global_button_sound_que)

        self.buttons = [self.PlayButton, self.ExitButton, self.SettingsButton, self.InstructionsButton]
        

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.PlayButton.checkForInput(pos)):
        print("Play button clicked")
        state.scene.PlayButton.button_sound()
    elif (state.scene.ExitButton.checkForInput(pos)):
        state.scene.ExitButton.button_sound()
        state.running = False
    elif (state.scene.SettingsButton.checkForInput(pos)):
        state.scene.SettingsButton.button_sound()
        state.pushScene(SettingsScene(state.screen))
    elif (state.scene.InstructionsButton.checkForInput(pos)):
        state.scene.InstructionsButton.button_sound()
        state.pushScene(InstructionsScene(state.screen))

def render(state: Gamestate):

    # the slowest thing you could possibly do
    background_image = pygame.image.load(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)
