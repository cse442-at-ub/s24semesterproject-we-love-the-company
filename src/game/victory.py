import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *

ID = "victory"

class VictoryScene:
    def __init__(self, screen,score):
        self.score = score

        self.id = ID
        self.path = os.path.dirname(__file__) + "/"

        self.textFont = pygame.font.SysFont("Arial", 40)
        self.paragraphFont = pygame.font.SysFont("Arial", 30)

        with open(self.path + "how-to-play-text.txt") as instructions_file:
            self.instructions_text = instructions_file.read()

        screen_center_x = screen.get_width() // 2
        back_button_y = screen.get_height() - 50

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                    text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    state.scene.BackButton.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        from menu import MenuScene
        state.scene.BackButton.button_sound()
        state.pushScene(MenuScene(state.screen))

def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    big_font = pygame.font.SysFont("Arial", 70)
    victory_text = "You escaped!"
    victory_surface = big_font.render(victory_text,True,(0,0,0))
    victory_rect = victory_surface.get_rect(center=(state.screen.get_width()//2,state.screen.get_height()//3))
    state.screen.blit(victory_surface,victory_rect)

    small_font = pygame.font.SysFont("Arial", 30)
    score_text = "Score: " + str(state.scene.score)
    score_surface = small_font.render(score_text,True,(0,0,0))
    score_rect = score_surface.get_rect(center=(state.screen.get_width()//2,state.screen.get_height()//2))
    state.screen.blit(score_surface,score_rect)

    state.scene.BackButton.update(state.screen)