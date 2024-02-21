import pygame
import os

from gamestate import *

from Buttons import Button
from HowToPlay import Instructions

ID = "main_menu"

class MenuScene:
    def __init__(self, screen):
        self.id = ID

        self.path = os.path.dirname(__file__) + "/"

        clock = pygame.time.Clock()

        self.textFont = pygame.font.SysFont("Arial", 40)
        self.paragraphFont = pygame.font.SysFont("Arial", 30)

        #initialize How To Play screen here
        self.HowToPlay = Instructions(screen, clock, self.path, self.textFont, self.paragraphFont)

        screen_center_x = screen.get_width() // 2
        play_button_y = screen.get_height() // 2 - 50
        exit_button_y = screen.get_height() // 2 + 150
        #putting the settings button in the middle of the play and exit buttons
        settings_button_y = screen.get_height() // 2 + 50
        instruct_button_y = screen.get_height() - 50

         # the slowest thing you could possibly do pt2
        self.PlayButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, play_button_y),
                            text_input="Play", font=self.textFont, base_color="white", hovering_color="blue")

        self.ExitButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, exit_button_y),
                            text_input="Exit", font=self.textFont, base_color="white", hovering_color="blue")
        
        #put a settings button with the button.img. It uses the same fonts and color and hover color
        self.SettingsButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, settings_button_y),
                                text_input="Settings", font=self.textFont, base_color="white", hovering_color="blue")

        self.InstructionsButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, instruct_button_y),
                                text_input="How To Play", font=self.textFont, base_color="white", hovering_color="blue")

        self.buttons = [self.PlayButton, self.ExitButton, self.SettingsButton, self.InstructionsButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

from OptionsMenu import SettingsScene

def mousePress(state: Gamestate, pos, buttons, touch):
    if (state.scene.PlayButton.checkForInput(pos)):
        print("Play button clicked")
    elif (state.scene.ExitButton.checkForInput(pos)):
        state.running = False
    elif (state.scene.SettingsButton.checkForInput(pos)):
        state.pushScene(SettingsScene(state.screen))
    elif (state.scene.InstructionsButton.checkForInput(pos)):
        print("How To Play button clicked")
        state.scene.HowToPlay.display_instructions_menu()

def render(state: Gamestate):

    # the slowest thing you could possibly do
    background_image = pygame.image.load(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)
