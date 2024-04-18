import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *

ID = "settings"

class ExitScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        audio_button_y = screen.get_height() // 2 - 50
        video_button_y = screen.get_height() // 2 + 50
        back_button_y = screen.get_height() // 2 + 150

        self.YesButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Yes", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("Assets/button_click.mp3"))
        
        self.NoButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, audio_button_y),
                        text_input="No", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("Assets/button_click.mp3"))

        self.buttons = [self.YesButton, self.NoButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)


from AudioMenu import AudioScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.YesButton.checkForInput(pos)):
        state.scene.YesButton.button_sound()
        state.running = False

    elif (state.scene.NoButton.checkForInput(pos)):
        state.scene.NoButton.button_sound()
        state.popScene()

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'exit_background.png')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)   
