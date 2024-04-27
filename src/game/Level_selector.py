import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *




ID = "level_selector"

class LevelSelectorScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        level1_button_y = screen.get_height() // 2 - 50
        level2_button_y = screen.get_height() // 2 + 50
        back_button_y = screen.get_height() // 2 + 150

        self.Level1Button = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, level1_button_y),
                                   text_input="Level 1", font=self.textFont, base_color="white", hovering_color="blue",
                                   click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.Level2Button = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, level2_button_y),
                                   text_input="Level 2", font=self.textFont, base_color="white", hovering_color="blue",
                                   click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                                   text_input="Back", font=self.textFont, base_color="white", hovering_color="blue",
                                   click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.buttons = [self.Level1Button, self.Level2Button, self.BackButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state:Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

from grid_game import GameScene  
def mousePress(state: Gamestate, pos, button, touch):
    if state.scene.Level1Button.checkForInput(pos):
        state.scene.Level1Button.button_sound()
        state.pushScene(GameScene(state.screen, "level1.json", state))
    elif state.scene.Level2Button.checkForInput(pos):
        state.scene.Level2Button.button_sound()
        state.pushScene(GameScene(state.screen, "level2.json", state))
    elif state.scene.BackButton.checkForInput(pos):
        state.scene.BackButton.button_sound()
        state.popScene()

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)

