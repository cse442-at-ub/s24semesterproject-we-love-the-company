Pause
import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *

import game
global_audio_pack = game.audio_pack
global_audio_control = game.audio_control
global_button_sound_que = game.button_sound_que
global_volume = 0.5

ID = "InPause"

class PauseScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)
        self.is_paused = False

        screen_center_x = screen.get_width() // 2
        resume_button_y = screen.get_height() // 2 - 50
        settings_button_y = screen.get_height() // 2 + 50
        Inst_button_y = screen.get_height() // 2 + 100
        back_button_y = screen.get_height() // 2 + 150

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.ResumeButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, resume_button_y),
                        text_input="Audio", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
            
        self.SettingsButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, settings_button_y),
                        text_input="Display", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.InstButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, Inst_button_y),
                        text_input="Display", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.buttons = [self.BackButton, self.ResumeButton, self.SettingsButton, self.InstButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)


from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        if state.scene.id == "game_scene": #this should be what he play ID is
            # In-game, push the settings scene and store the previous scene
            state.is_paused = True
            state.pushScene(SettingsScene(state.screen))
            state.scene.SettingsButton.button_sound()
            settings_scene = state.scene
            settings_scene.previous_scene = state.scene
        
        if state.is_paused:
            if (state.scene.BackButton.checkForInput(pos)):
                state.scene.BackButton.button_sound()
                state.popScene()
            elif (state.scene.ResumeButton.checkForInput(pos)):
                state.scene.ResumeButton.button_sound()
                print("The game has been resumed")
            elif (state.scene.InstButton.checkForInput(pos)):
                state.scene.InstButton.button_sound()
                state.pushScene(InstructionsScene(state.screen))
                print("Instructions to how to play")
            elif (state.scene.SettingsButton.checkForInput(pos)):
                state.scene.SettingsButton.button_sound()
                state.pushScene(SettingsScene(state.screen))
                print("Instructions to how to play")


def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)