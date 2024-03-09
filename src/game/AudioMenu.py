import pygame
import os
from Buttons import Button
from Sliders import Slider
import AssetCache
from gamestate import *

ID = "Audio_settings"
audio_pack = AssetCache.get_audio("src/game/Assets/button_click.mp3")
sound = pygame.mixer.Sound(audio_pack)

class AudioScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)
        self.screen = screen
        self.init_ui_elements()

    def init_ui_elements(self):
        self.BackButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(0, 0),
                                 text_input="Back", font=self.textFont, base_color="white", hovering_color="blue",
                                 click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.slider_one = Slider((0, 0), (200, 20), 0, 100, 20, Gamestate)
        self.slider_one.set_lable("BGM")
        self.slider_two = Slider((0, 0), (200, 20), 0, 100, 20, Gamestate)
        self.slider_two.set_lable("SFX")

        self.buttons = [self.BackButton]
        self.sliders = [self.slider_one, self.slider_two]

        self.update_elements(self.screen.get_width(), self.screen.get_height())

    def update_elements(self, width: int, height: int):
        screen_center_x = width // 2
        slider_one_y = height // 2 - 50
        slider_two_y = height // 2 + 50
        back_button_y = height // 2 + 150

        # Update BackButton position
        self.BackButton.rect.center = (screen_center_x, back_button_y)
        self.BackButton.text_rect.center = (screen_center_x, back_button_y)

        # Update Slider positions and maintain their current value
        self.slider_one.__init__((screen_center_x, slider_one_y), (200, 20), 0, 100, self.slider_one.get_value(), Gamestate)
        self.slider_two.__init__((screen_center_x, slider_two_y), (200, 20), 0, 100, self.slider_two.get_value(), Gamestate)
       
    def update_volumes(self):
        bgm_volume = self.slider_one.get_value() / 100  # Normalize to 0-1 for pygame
        sfx_volume = self.slider_two.get_value() / 100  # Normalize to 0-1 for pygame

        pygame.mixer.music.set_volume(bgm_volume)
        sound.set_volume(sfx_volume)
        
    
    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mousePress(state: Gamestate, pos, button, touch):
    # Handling sliders
    for slider in state.scene.sliders:
        if slider.container_rect.collidepoint(pos) or slider.handle_rect.collidepoint(pos):
            slider.grabbed = True 
            slider.move_handle(pos) 
            slider.hover() 
            break 

    # Handling back button
    if state.scene.BackButton.checkForInput(pos):
        state.scene.BackButton.button_sound()
        state.popScene()

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for slide in state.scene.sliders:
        # Check both container and handle collision
        if slide.container_rect.collidepoint(pos) or slide.handle_rect.collidepoint(pos):
            slide.hovered = True
            if buttons[0]:  # Check if left mouse button is pressed
                slide.grabbed = True
                slide.move_handle(pos)
        else:
            # Reset grabbed state to False only when left mouse button is not pressed
            if not buttons[0]:
                slide.grabbed = False

    for button in state.scene.buttons:
        if isinstance(button, Button):
            button.changeColor(pos)

def render(state: Gamestate):
    background_image = pygame.image.load(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))
    

    for slider in state.scene.sliders:
        slider.render(state.screen)
        slider.display_value(state.screen)
    
    for button in state.scene.buttons:
        if isinstance(button, Button):
            button.update(state.screen)

