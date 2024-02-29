import pygame
import os
from Buttons import Button
from Sliders import Slider

from gamestate import *

ID = "Audio_settings"

class AudioScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        slider_one_y = screen.get_height() // 2 - 50
        slider_two_y = screen.get_height() // 2 + 50
        back_button_y = screen.get_height() // 2 + 150

        self.BackButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= pygame.mixer.Sound("src/game/Assets/button_click.mp3"))
        
        self.slider_one = Slider(screen_center_x, slider_one_y, width=200, height=20, min_val=0, max_val=100)
        self.slider_two = Slider(screen_center_x, slider_two_y, width =200, height=20, min_val=0, max_val=100)
        
        self.buttons = [self.BackButton]
        self.sliders = [self.slider_one, self.slider_two]

        self.buttons.extend(self.sliders)

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

    def volume_control(self):
        SFX = self.slider_one.value // 100
        BGM = self.slider_two.value // 100
        pygame.mixer.music.set_volume(BGM)

    def apply_volume_to_buttons(self):
        SFX = self.slider_one.value / 100
        for button in self.buttons:
            if isinstance(button, Button):
                button.click_sound.set_volume(SFX)

    def move_slider_handle(self, pos):
        for slider in self.sliders:
            if slider.container_rect.collidepoint(pos):
                slider.move_handle(pos)
                self.volume_control()

    def update_slider_value(self, val):
        for slider in self.sliders:
            slider.update_value(val)
        self.volume_control()

def mousePress(state: Gamestate, pos, button, touch):
    # Existing button press handling...
    # Add logic to check if the mouse is pressed on a slider
    if button == 1:  # Left mouse button
        for slider in [state.scene.slider_one, state.scene.slider_two]:
            if slider.container_rect.collidepoint(pos):
                slider.is_dragging = True  # You need to add this attribute to your Slider class
                slider.move_handle(pos)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    # Existing mouse move handling...
    # Add logic to move the slider handle if dragging
    for slider in [state.scene.slider_one, state.scene.slider_two]:
        if slider.container_rect.collidepoint(pos):
            slider.move_handle(pos)

    if (state.scene.BackButton.checkForInput(pos)):
        state.scene.BackButton.button_sound()
        state.popScene()

def render(state: Gamestate):
    background_image = pygame.image.load(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for slider in state.scene.sliders:
        slider.draw(state.screen)
    
    for button in state.scene.buttons:
        if isinstance(button, Button):
            button.update(state.screen)