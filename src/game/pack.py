import pygame
import os
from Sliders import Slider
import AssetCache
from Buttons import Button
from gamestate import *
ID = "settings"

class BackPackScene:
    def __init__(self, screen, count):
        self.id = ID
        self.screen = screen
        self.count = count
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)
        screen_center_x = screen.get_width() // 2
        back_button_y = screen.get_height() - 680

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/back.png"), pos=(screen_center_x, back_button_y),
                            text_input="Back To Game", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("Assets/button_click.mp3"))
        self.buttons = [self.BackButton]
    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
        pass

def mousePress(state: Gamestate, pos, button, touch):
        
        if (state.scene.BackButton.checkForInput(pos)):
            state.scene.BackButton.button_sound()
            state.popScene()
        pass

def render(state: Gamestate):
    background_image = AssetCache.get_image(os.path.join(os.path.dirname(__file__) + "/", "Assets", "backpack.png"))
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))
    for button in state.scene.buttons:
            button.update(state.screen)
    cell_size = 64
    apple_image = AssetCache.get_image(os.path.join(os.path.dirname(__file__) + "/", "Assets", "apple.png"))
    apple_image = pygame.transform.scale(apple_image, (cell_size, cell_size))
    for i in range(0,state.scene.count):
        state.screen.blit(apple_image, (0, i*64))

    pygame.display.flip()    
