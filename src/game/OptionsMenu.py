import pygame
import os
from Buttons import Button

from gamestate import *

ID = "settings"

class SettingsScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        audio_button_y = screen.get_height() // 2 - 50
        video_button_y = screen.get_height() // 2 + 50
        back_button_y = screen.get_height() // 2 + 150

        self.BackButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue")
        
        self.AudioButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, audio_button_y),
                        text_input="Audio", font=self.textFont, base_color="white", hovering_color="blue")
            
        self.VideoButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, video_button_y),
                        text_input="Display", font=self.textFont, base_color="white", hovering_color="blue")

        self.buttons = [self.BackButton, self.AudioButton, self.VideoButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, buttons, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        state.popScene()
    elif (state.scene.AudioButton.checkForInput(pos)):
        print("Audio settings pressed")
    elif (state.scene.VideoButton.checkForInput(pos)):
        print("Video settings pressed")

def render(state: Gamestate):
    # the slowest thing you could possibly do
    background_image = pygame.image.load(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)