import pygame
import os
import AssetCache
from Buttons import Button
from gamestate import Gamestate, Handler


class GameOverScene:
    def __init__(self, screen):
        self.screen = screen
        self.id = "game_over"

        self.background_image = AssetCache.get_image(os.path.join('src/game/background1.jpg'))
        self.background_image = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))

        self.font = pygame.font.SysFont("Arial", 40)
        
        screen_center_x = screen.get_width() // 2
        first_button_y = screen.get_height() // 2 - 100
        button_spacing = 100  # Space between buttons


        # Scale factor for button width
        scale_factor = 1.5

        # Example for PlayButton, apply the same logic to other buttons
        original_button_image = AssetCache.get_image(os.path.join('src/game/Assets/button1.png'))
        # Scale the image to make it wider
        button_width = original_button_image.get_width() * scale_factor
        button_height = original_button_image.get_height()
        scaled_button_image = pygame.transform.scale(original_button_image, (int(button_width), button_height))

        # Now use the scaled image for your buttons
        self.PlayButton = Button(image=scaled_button_image, pos=(screen_center_x, first_button_y),
                                text_input="Play Again", font=self.font, base_color=(255, 255, 255), hovering_color=(100, 255, 100),
                                click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        # Repeat the scaling and creation process for MainMenuButton and QuitButton
        self.MainMenuButton = Button(image=scaled_button_image, pos=(screen_center_x, first_button_y + button_spacing),
                                    text_input="Main Menu", font=self.font, base_color=(255, 255, 255), hovering_color=(100, 100, 255),
                                    click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.QuitButton = Button(image=scaled_button_image, pos=(screen_center_x, first_button_y + 2 * button_spacing),
                                text_input="Quit Game", font=self.font, base_color=(255, 255, 255), hovering_color=(255, 100, 100),
                                click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.buttons = [self.PlayButton, self.MainMenuButton, self.QuitButton]
        
    def render(self, gamestate):
        self.screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.update(self.screen)
        pygame.display.flip()

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=lambda gs, dt: None,  # Assuming no update needed
            onKeyPress=lambda gs, key, mod, unicode, scancode: None,  # Assuming no key press handling
            onMousePress=self.handle_mouse_clicks
        )

    def handle_mouse_clicks(self, gamestate, pos, button, touch):
        for btn in self.buttons:
            if btn.checkForInput(pos):
                btn.button_sound()
                if btn.text_input == "Play Again":
                    pygame.mixer_music.stop()
                    gamestate.switch_to_game()
                elif btn.text_input == "Main Menu":
                    pygame.mixer_music.stop()
                    # Switch to the main menu scene (assuming it's defined somewhere)
                    gamestate.switch_to_menu()
                elif btn.text_input == "Quit Game":
                    pygame.quit()
                    exit()
