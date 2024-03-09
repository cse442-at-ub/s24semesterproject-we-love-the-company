import pygame
import os
import AssetCache
from gamestate import Gamestate, Handler, doNothing
from Buttons import Button
from grid_game import GameScene

from gamestate import *

ID = "main_menu"

class MenuScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.screen = screen
        self.textFont = pygame.font.SysFont("Arial", 40)
        pygame.mixer.music.load("src/game/Assets/Background_music_menu.wav")
        pygame.mixer.music.play(-1)
        #this the current background music   
        
        # Load button assets
        self.button_image = AssetCache.get_image(self.path + "Assets/button.png")
        self.click_sound = AssetCache.get_audio("src/game/Assets/button_click.mp3")
        
        # Initialize buttons without positions
        self.buttons = []
        self.init_buttons()
        
        # Dynamically update button positions
        self.update_button_positions(screen.get_width(), screen.get_height())

    def init_buttons(self):
        # Create buttons with placeholders positions, they will be positioned in update_button_positions
        button_labels = ["Play", "Settings", "How To Play", "Exit"]
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


def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene

def mousePress(state: Gamestate, pos, button, touch):
    # Iterate through each button in the scene's buttons list
    for button in state.scene.buttons:
        if button.checkForInput(pos):
            print(f"{button.text_input} button clicked")  # Generalized button click message
            button.button_sound()

            # Execute button-specific actions
            if button.text_input == "Play":
                state.pushScene(GameScene(state.screen))
            elif button.text_input == "Exit":
                state.running = False
            elif button.text_input == "Settings":
                state.pushScene(SettingsScene(state.screen))  # Ensure SettingsScene is defined
            elif button.text_input == "How To Play":
                state.pushScene(InstructionsScene(state.screen))  # Ensure InstructionsScene is defined
            break  # Exit loop after finding the clicked button

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)

# You will need to adjust mouseMove and mousePress functions if necessary to
# ensure they interact correctly with the dynamically positioned buttons.
