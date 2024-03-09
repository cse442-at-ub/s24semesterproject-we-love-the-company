import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *


ID = "InPause"


class PauseScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.screen = screen
        self.textFont = pygame.font.SysFont("Arial", 40)
        pygame.mixer.music.load("src/game/Assets/Background_music_menu.wav")
        pygame.mixer.music.play(-1)
        
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
        button_labels = ["Resume", "Settings", "How To Play", "Exit"]
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

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onKeyPress= self.onKeyPress,
            onMousePress=self.onMousePress)

    def onKeyPress(self, state: Gamestate, key, mod, unicode, scancode):
        if key == pygame.K_ESCAPE:
            # Handle ESC key press here
            state.popScene()

from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    for button in state.scene.buttons:
        if button.checkForInput(pos):
            print(f"{button.text_input} button clicked")  # Generalized button click message
            button.button_sound()

            # Execute button-specific actions
            if button.text_input == "Resume":
               # state.pushScene(GameScene(state.screen))
                #self.ResumeButton.button_sound()
                state.popScene()
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