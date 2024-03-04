import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *

ID = "InPause"

class SettingsScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        resume_button_y = screen.get_height() // 2 - 50
        settings_button_y = screen.get_height() // 2 + 50
        Inst_button_y = screen.get_height() // 2 + 100
        back_button_y = screen.get_height() // 2 + 150

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.ResumeButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, resume_button_y),
                        text_input="Audio", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
            
        self.SettingsButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, settings_button_y),
                        text_input="Display", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.InstButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, Inst_button_y),
                        text_input="Display", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.buttons = [self.BackButton, self.AudioButton, self.VideoButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)


from AudioMenu import AudioScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        state.scene.BackButton.button_sound()
        state.popScene()
    pass

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)