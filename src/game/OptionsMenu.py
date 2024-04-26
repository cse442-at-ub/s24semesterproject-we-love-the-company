import pygame
import os
from Buttons import Button
import AssetCache

from gamestate import *

ID = "settings"

class SettingsScene:
    def __init__(self, screen):
        self.id = ID
        self.path = os.path.dirname(__file__) + "/"
        self.textFont = pygame.font.SysFont("Arial", 40)

        screen_center_x = screen.get_width() // 2
        audio_button_y = screen.get_height() // 2 - 100
        video_button_y = screen.get_height() // 2 
        name_button_y = screen.get_height() // 2 + 100
        back_button_y = screen.get_height() // 2 + 200

        self.BackButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                        text_input="Back", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.AudioButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, audio_button_y),
                        text_input="Audio", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
            
        self.VideoButton = Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, video_button_y),
                        text_input="Display", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.NameButton =  Button(image=AssetCache.get_image(self.path + "Assets/button.png"), pos=(screen_center_x, name_button_y),
                        text_input="Name", font=self.textFont, base_color="white", hovering_color="blue", click_sound= AssetCache.get_audio("src/game/Assets/button_click.mp3"))
        
        self.buttons = [self.BackButton, self.AudioButton, self.VideoButton,self.NameButton]

    def initHandlers(self, state: Gamestate):
        state.handlers[ID] = Handler(render, doNothing, doNothing, mouseMove, mousePress)
    
    def update_elements(self, width: int, height: int):
        pass


from AudioMenu import AudioScene
from VideoMenu import VideoScene

def mouseMove(state: Gamestate, pos, rel, buttons, touch):
    for button in state.scene.buttons:
        button.changeColor(pos)

def mousePress(state: Gamestate, pos, button, touch):
    if (state.scene.BackButton.checkForInput(pos)):
        state.scene.BackButton.button_sound()
        state.popScene()
    elif (state.scene.AudioButton.checkForInput(pos)):
        state.scene.AudioButton.button_sound()
        print("Audio settings pressed")
        state.pushScene(AudioScene(state.screen))
    elif (state.scene.VideoButton.checkForInput(pos)):
        state.scene.VideoButton.button_sound()
        print("Video settings pressed")
        state.pushScene(VideoScene(state.screen))
    elif (state.scene.NameButton.checkForInput(pos)):
        state.scene.NameButton.button_sound()
        # Prompt for name input and save it
        new_name = prompt_for_name(state.screen)
        if new_name is not None:
            state.update_player_name(new_name)
            print(new_name)


def render(state: Gamestate):
    background_image = AssetCache.get_image(state.scene.path + 'background.jpg')
    background_image = pygame.transform.scale(background_image, state.screen.get_size())
    state.screen.blit(background_image, (0, 0))

    for button in state.scene.buttons:
        button.update(state.screen)

def prompt_for_name(screen):
    input_box = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # If the window is closed during input
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill((30, 30, 30))  # Clear the screen with a dark grey color
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text