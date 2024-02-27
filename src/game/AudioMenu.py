import pygame
import os
from Buttons import Button
from Sliders import Slider
import AssetCache

from gamestate import *

ID = "settings"

class AudioScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        slider_one_y = screen.get_height() // 2 - 50
        slider_two_y = screen.get_height() // 2 + 50
        back_button_y = screen.get_height() // 2 + 150

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.slider_one = Slider(pos=(screen_center_x, slider_one_y), width=200, height=200, min_value=0, max_value=100)
        self.slider_two = Slider(pos=(screen_center_x, slider_two_y), width=200, height=200, min_value=0, max_value=100)
        

        self.buttons = [self.BackButton, self.slider_one, self.slider_two]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

    def volume_control(self):
        SFX = self.slider_one.value / 100
        BGM = self.slider_two.value / 100
        for button in self.buttons:
            if isinstance(button, Button):
                button.click_sound.set_volume(SFX)
        pygame.mixer.music.set_volume(BGM)


def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        if isinstance(button, Button):
            button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        state.scene.BackButton.button_sound()
        state.popScene()

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        if isinstance(button, Slider):
            button.update(state.screen)
        else:
            button.update(state.screen)
    state.scene.volume_control()