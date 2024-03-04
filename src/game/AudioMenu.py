import pygame
import os
from Buttons import Button
from Sliders import Slider


from gamestate import *
import game
global_audio_pack = game.audio_pack
global_audio_control = game.audio_control
global_button_sound_que = game.button_sound_que
global_volume = 0.5


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
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= global_button_sound_que)
        
        self.slider_one = Slider((screen_center_x, slider_one_y), (200, 20), 0, 100,20)
        self.slider_two = Slider((screen_center_x, slider_two_y), (200, 20), 0, 100,20)
        
        self.buttons = [self.BackButton]
        self.sliders = [self.slider_one, self.slider_two]

        self.buttons.extend(self.sliders)
    
    #def move_slider_handle(self,pos):
        #self.slider_one.move_handle(pos)
        #self.update_volume()

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mousePress(state: Gamestate, pos, button, touch):
    for slide in state.scene.sliders:
        if slide.container_rect.collidepoint(pos):
            slide.grabbed = True
            slide.move_handle(pos)
        
        if slide.handle_rect.collidepoint(pos):
            slide.hover()
        
        if slide.grabbed:
            slide.move_handle(pos)
            slide.hover()
        else:
            slide.hovered = False
            slide.grabbed = False

    if (state.scene.BackButton.checkForInput(pos)):
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

# Update volume function (called when needed)
def update_volume():
    pygame.mixer.music.set_volume(global_volume)
    global_button_sound_que.set_volume(global_volume)

    # Inside Slider class, update_volume function
def update_volume(self):
        # Update the global variable with the current value
    global global_volume
    global_volume = self.get_value() / 100