import pygame
import os
import AssetCache

from gamestate import *

from Buttons import Button
from grid_game import GameScene

ID = "Pause_menu"

class PauseScene:
    def __init__(self, screen):
        pygame.mixer.music.load("src/game/Assets/Background_music_menu.wav")
        pygame.mixer.music.play(-1)
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"

        self.textFont = pygame.font.SysFont("Arial", 40)

        self.button_image = AssetCache.get_image(self.path + "Assets/button.png")
        self.click_sound = AssetCache.get_audio("src/game/Assets/button_click.mp3")
        self.buttons = []
        self.init_button()

        self.update_button_positions(screen.get_width(), screen.get_height())

    def init_button(self):
        button_labels = ["Resume", "Settings", "Instructions", "Quit game"]
        for label in button_labels:
            self.buttons.append(Button(image=self.button_image, pos=(0, 0),
                                        text_input=label, font=self.textFont,
                                        base_color="white", hovering_color="blue",
                                        click_sound=self.click_sound))
        
    
    def update_button_positions(self, width, height):
        screen_center_x = width // 2
        button_y_start = height // 2 - 50
        button_spacing = 100

        for index, button in enumerate(self.buttons):
            button_y = button_y_start + index * button_spacing
            button.rect.center = (screen_center_x, button_y)
            button.text_rect.center = (screen_center_x, button_y)

    def update_elements(self, width: int, height: int):
        self.update_button_positions(width, height)

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    # Iterate through each button in the scene's buttons list
    for button in state.scene.buttons:
        if button.checkForInput(pos):
            print(f"{button.text_input} button clicked")  # Generalized button click message
            button.button_sound()

            # Execute button-specific actions
            if button.text_input == "Resume":
                pygame.mixer_music.stop()
                state.popScene()
            elif button.text_input == "Settings":
                state.pushScene(SettingsScene(state.screen))
            elif button.text_input == "Instructions":
                state.pushScene(InstructionsScene(state.screen))
            elif button.text_input == "Quit game":
                state.running = False
            break  # Exit loop after finding the clicked button


def onKeyPress(gamestate, key, mod, unicode, scancode):
    if (key == pygame.K_ESCAPE):
         gamestate.popScene()


def render(state: Gamestate):

    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)