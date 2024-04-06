import pygame
import os
from Buttons import Button
import AssetCache


from gamestate import *

ID = "VideoSettings"

class VideoScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)
        self.Fullscreen = False

        screen_center_x = screen.get_width() // 2
        Option_one_y = screen.get_height() // 2 - 50
        Option_two_y = screen.get_height() // 2 + 50
        back_button_y = screen.get_height() // 2 + 150

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.ResButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, Option_two_y),
                        text_input="Resolution", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.buttons = [self.BackButton, self.ResButton]


    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)
    def update_elements(self, width: int, height: int):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)



def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

from ResMenu import ResolutionScene

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        state.scene.BackButton.button_sound()
        state.popScene()
    elif (state.scene.ResButton.checkForInput(pos)):
        state.scene.ResButton.button_sound()
        state.pushScene(ResolutionScene(state.screen))
    

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)
    
    if hasattr(state.scene, 'draw_ui'):
        state.scene.draw_ui(state.screen)