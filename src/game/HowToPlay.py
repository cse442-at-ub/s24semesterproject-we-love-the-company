import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *
import game
global_audio_pack = game.audio_pack
global_audio_control = game.audio_control
global_button_sound_que = game.button_sound_que

# taken from: https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

ID = "how_to_play"

class InstructionsScene:
    def __init__(self, screen):
        self.id = ID
        self.screen = screen  # Store the screen object for later reference
        self.path = os.path.dirname(__file__) + "/"

        self.textFont = pygame.font.SysFont("Arial", 40)
        self.paragraphFont = pygame.font.SysFont("Arial", 30)

        with open(self.path + "how-to-play-text.txt") as instructions_file:
            self.instructions_text = instructions_file.read()

        self.init_ui_elements(screen.get_width(), screen.get_height())

    def init_ui_elements(self, width, height):
        screen_center_x = width // 2
        back_button_y = height - 50

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), 
                    pos=(screen_center_x, back_button_y), text_input="Back", font=self.textFont, 
                    base_color="white", hovering_color="blue", 
                    click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

    def update_elements(self, width: int, height: int):
        # Update the positions of UI elements based on the new screen dimensions
        self.init_ui_elements(width, height)  # Re-initialize UI elements for the new dimensions

        self.BackButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                    text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= global_button_sound_que)


    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    state.scene.BackButton.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        state.scene.BackButton.button_sound()
        state.popScene()

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    screen_center_x = state.screen.get_width() // 2
    # Adjust text start position as needed, for example:
    text_start_pos = (screen_center_x - 400, 50)  # Example starting position, adjust as needed

    blit_text(state.screen, state.scene.instructions_text, text_start_pos, state.scene.paragraphFont)

    state.scene.BackButton.update(state.screen)