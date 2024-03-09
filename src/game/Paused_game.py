import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *

<<<<<<< HEAD
import game
global_audio_pack = game.audio_pack
global_audio_control = game.audio_control
global_button_sound_que = game.button_sound_que
global_volume = 0.5

ID = "InPause"

=======

ID = "InPause"


>>>>>>> Video_settings
class PauseScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
<<<<<<< HEAD
        self.textFont = pygame.font.SysFont("Arial", 40)

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


from AudioMenu import AudioScene
=======
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

>>>>>>> Video_settings
from OptionsMenu import SettingsScene
from HowToPlay import InstructionsScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
<<<<<<< HEAD
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        if state.scene.id == "InGame": #this should be what he play ID is
            # In-game, push the settings scene and store the previous scene
            state.pushScene(SettingsScene(state.screen))
            state.scene.SettingsButton.button_sound()
            settings_scene = state.scene
            settings_scene.previous_scene = state.scene
        elif state.scene.id == "InPause":
            state.popScene()


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
=======
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
>>>>>>> Video_settings


def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)